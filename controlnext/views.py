# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals
import os
import logging
import datetime

from django.http import Http404
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist

import pytz
from rest_framework.views import APIView
from rest_framework.response import Response as RestResponse

from lizard_ui.views import UiView
from lizard_map.models import WorkspaceEdit
from lizard_map.views import AppView

from controlnext import models
from controlnext.demand_table import DemandTable
from controlnext.calc_model import CalculationModel
from controlnext.conf import settings
from controlnext.fews_data import FewsJdbcDataSource
from controlnext import constants as legacy_constants
from controlnext.utils import round_date
from controlnext.models import GrowerInfo, Constants, Basin
from controlnext.view_helpers import update_basin_coordinates, \
    update_current_fill

logger = logging.getLogger(__name__)

js_epoch = datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)


def datetime_to_js(dt):
    if dt is not None:
        return (dt - js_epoch).total_seconds() * 1000


def series_to_js(pdseries):
    pdseries = pdseries.fillna(method='pad')
    return [(datetime_to_js(dt), value) for dt, value in pdseries.iterkv()]


class DashboardView(AppView):
    template_name = 'controlnext/dashboard.html'
    page_title = _('ControlNEXT sturing Delfland dashboard')

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardView, self).get_context_data(*args, **kwargs)
        context['basins'] = Basin.objects.filter(on_main_map=True).order_by(
            'owner__id')
        return context

    def dispatch(self, request, *args, **kwargs):
        """Add in the omnipresent workspace item, then proceed as normal."""

        workspace_edit = WorkspaceEdit.get_or_create(
            request.session.session_key, request.user)

        # add default layer with selected basins (see layers.py)
        workspace_edit.add_workspace_item(
            "Basins", "adapter_basin_fill", "{}")

        # check basin coordinates and update current fill
        basins = Basin.objects.all()
        for basin in basins:
            if not basin.location:
                # ^^^ only get coordinates for basins without coordinates
                update_basin_coordinates(basin)
            update_current_fill(basin)  # is cached, no need to update on
            # every request

        return super(DashboardView, self).dispatch(request, *args, **kwargs)


class MainView(UiView):
    template_name = 'controlnext/main.html'
    page_title = _('ControlNEXT sturing Delfland')

    def get_context_data(self, *args, **kwargs):
        self.oppervlakte = legacy_constants.opp_invloed_regen_m2
        self.max_voorraad = legacy_constants.max_berging_m3
        return super(UiView, self).get_context_data(*args, **kwargs)


class GrowerView(UiView):
    template_name = 'controlnext/grower_detail.html'
    page_title = _('ControlNEXT')

    def get_context_data(self, *args, **kwargs):
        self.grower = self.grower_info
        return super(GrowerView, self).get_context_data(*args, **kwargs)

    def get(self, request, grower_id, *args, **kwargs):
        try:
            grower_info = models.GrowerInfo.objects.get(id=grower_id)
        except ObjectDoesNotExist:
            raise Http404
        else:
            self.grower_info = models.Constants(grower_info)
        return super(GrowerView, self).get(request, *args, **kwargs)


class DataService(APIView):
    _IGNORE_IE_ACCEPT_HEADER = False  # Keep this, if you want IE to work

    def store_parameters(self, desired_fill, demand_exaggerate,
                         rain_exaggerate, extra=''):
        path = settings.REQUESTED_VALUES_CSV_PATH
        directory = os.path.dirname(path)
        if not os.path.isdir(directory):
            os.makedirs(directory)
        if not os.path.isfile(path):
            # write column headers
            with open(path, 'w') as file:
                file.write(
                    'desired_fill;demand_exaggerate;rain_exaggerate;extra\n')
        # write parameter values
        parameters = [desired_fill, demand_exaggerate, rain_exaggerate, extra]
        parameters = map(str, parameters)
        with open(path, 'a') as file:
            file.write(';'.join(parameters) + '\n')

    def get(self, request):
        graph_type = request.GET.get('graph_type', None)
        hours_diff = request.GET.get('hours_diff', None)

        desired_fill = request.GET.get('desired_fill')
        demand_exaggerate = request.GET.get('demand_exaggerate')
        rain_exaggerate = request.GET.get('rain_exaggerate')
        desired_fill = int(desired_fill)
        demand_exaggerate = int(demand_exaggerate)
        rain_exaggerate = int(rain_exaggerate)

        # note: t0 is Math.floor() 'ed to a full quarter
        t0 = round_date(datetime.datetime.now(pytz.utc))
        if hours_diff:
            t0 += datetime.timedelta(hours=int(hours_diff))

        if graph_type == 'rain':
            response_dict = self.rain(t0, rain_exaggerate)
        elif graph_type == 'prediction':
            self.store_parameters(desired_fill, demand_exaggerate,
                                  rain_exaggerate)
            response_dict = self.prediction(t0, desired_fill,
                                            demand_exaggerate, rain_exaggerate)
        else:
            response_dict = self.advanced(t0, desired_fill, demand_exaggerate,
                                          rain_exaggerate, graph_type)
        return RestResponse(response_dict)

    def prediction(self, t0, desired_fill_pct, demand_exaggerate,
                   rain_exaggerate):
        tbl = DemandTable()
        ds = FewsJdbcDataSource()
        model = CalculationModel(tbl, ds)

        future = t0 + settings.CONTROLNEXT_FILL_PREDICT_FUTURE

        prediction = model.predict_fill(t0, future, desired_fill_pct,
                                        demand_exaggerate, rain_exaggerate)

        # TODO should use dict comprehension in py > 2.6
        data = dict([(name, series_to_js(scenario['prediction']))
                     for name, scenario in prediction['scenarios'].items()])
        data['history'] = series_to_js(prediction['history'])
        graph_info = {
            'data': data,
            'x0': datetime_to_js(t0),
            'y_marking_min': legacy_constants.min_berging_pct,
            'y_marking_max': legacy_constants.max_berging_pct,
            'x_marking_omslagpunt': datetime_to_js(
                prediction['scenarios']['mean']['omslagpunt']),
            'y_marking_desired_fill': desired_fill_pct,
            'desired_fill': desired_fill_pct,
        }
        result = {
            'graph_info': graph_info,
            'overflow_24h': prediction['scenarios']['mean']['overstort_24h'],
            'overflow_5d': prediction['scenarios']['mean']['overstort_5d'],
            'demand_week': tbl.get_week_demand_on(t0),
            'demand_24h': tbl.get_total_demand(
                t0, t0 + datetime.timedelta(hours=24)),
            'current_fill': prediction['current_fill'],
        }
        return result

    def advanced(self, t0, desired_fill_pct, demand_exaggerate,
                 rain_exaggerate, graph_type):
        tbl = DemandTable()
        ds = FewsJdbcDataSource()
        model = CalculationModel(tbl, ds)

        future = t0 + settings.CONTROLNEXT_FILL_PREDICT_FUTURE

        prediction = model.predict_fill(t0, future, desired_fill_pct,
                                        demand_exaggerate, rain_exaggerate)

        data = []
        unit = ''
        if graph_type == 'demand':
            data = prediction['intermediate']['demand']
            unit = 'm3'
        elif graph_type == 'max_uitstroom':
            data = prediction['intermediate']['max_uitstroom']
            unit = 'm3'
        elif graph_type == 'toestroom':
            data = prediction['scenarios']['mean']['intermediate']['toestroom']
            unit = 'm3'
        elif graph_type == 'uitstroom':
            data = prediction['scenarios']['mean']['intermediate']['uitstroom']
            unit = 'm3'

        result = {
            'graph_info': {
                'data': series_to_js(data),
                'x0': datetime_to_js(t0),
                'unit': unit,
            }
        }
        return result

    def rain(self, t0, rain_exaggerate_pct):
        _from = t0 - settings.CONTROLNEXT_FILL_HISTORY
        to = t0 + settings.CONTROLNEXT_FILL_PREDICT_FUTURE

        ds = FewsJdbcDataSource()
        min = ds.get_rain('min', t0, to)
        mean = ds.get_rain('mean', _from, to)
        max = ds.get_rain('max', t0, to)

        if rain_exaggerate_pct != 100:
            rain_exaggerate = rain_exaggerate_pct / 100
            min *= rain_exaggerate
            mean *= rain_exaggerate
            max *= rain_exaggerate

        #import pdb; pdb.set_trace()
        rain_graph_info = {
            'data': {
                'min': series_to_js(min),
                'mean': series_to_js(mean),
                'max': series_to_js(max)
            },
            'x0': datetime_to_js(t0)
        }
        return {
            't0': t0,
            'rain_graph_info': rain_graph_info,
        }


class DataServiceByID(APIView):
    _IGNORE_IE_ACCEPT_HEADER = False  # Keep this, if you want IE to work

    def store_parameters(self, desired_fill, demand_exaggerate,
                         rain_exaggerate, extra=''):
        path = settings.REQUESTED_VALUES_CSV_PATH
        directory = os.path.dirname(path)
        if not os.path.isdir(directory):
            os.makedirs(directory)
        if not os.path.isfile(path):
            # write column headers
            with open(path, 'w') as file:
                file.write(
                    'desired_fill;demand_exaggerate;rain_exaggerate;extra\n')
            # write parameter values
        parameters = [desired_fill, demand_exaggerate, rain_exaggerate, extra]
        parameters = map(str, parameters)
        with open(path, 'a') as file:
            file.write(';'.join(parameters) + '\n')

    def get(self, request, grower_id, *args, **kwargs):
        try:
            grower_info = GrowerInfo.objects.get(id=grower_id)
            self.grower_info = grower_info
            self.constants = Constants(self.grower_info)
        except ObjectDoesNotExist:
            raise Http404

        graph_type = request.GET.get('graph_type', None)
        hours_diff = request.GET.get('hours_diff', None)

        desired_fill = request.GET.get('desired_fill')
        demand_exaggerate = request.GET.get('demand_exaggerate')
        rain_exaggerate = request.GET.get('rain_exaggerate')
        desired_fill = int(desired_fill)
        demand_exaggerate = int(demand_exaggerate)
        rain_exaggerate = int(rain_exaggerate)

        # note: t0 is Math.floor() 'ed to a full quarter
        t0 = round_date(datetime.datetime.now(pytz.utc))
        if hours_diff:
            t0 += datetime.timedelta(hours=int(hours_diff))

        if graph_type == 'rain':
            response_dict = self.rain(t0, rain_exaggerate)
        elif graph_type == 'prediction':
            self.store_parameters(desired_fill, demand_exaggerate,
                                  rain_exaggerate)
            response_dict = self.prediction(t0, desired_fill,
                                            demand_exaggerate, rain_exaggerate)
        else:
            response_dict = self.advanced(t0, desired_fill, demand_exaggerate,
                                          rain_exaggerate, graph_type)
        return RestResponse(response_dict)

    def prediction(self, t0, desired_fill_pct, demand_exaggerate,
                   rain_exaggerate):
        tbl = DemandTable()
        ds = FewsJdbcDataSource(self.grower_info)
        model = CalculationModel(tbl, ds)

        future = t0 + settings.CONTROLNEXT_FILL_PREDICT_FUTURE

        prediction = model.predict_fill(t0, future, desired_fill_pct,
                                        demand_exaggerate, rain_exaggerate)

        # TODO should use dict comprehension in py > 2.6
        data = dict([(name, series_to_js(scenario['prediction']))
                     for name, scenario in prediction['scenarios'].items()])
        data['history'] = series_to_js(prediction['history'])
        graph_info = {
            'data': data,
            'x0': datetime_to_js(t0),
            'y_marking_min': self.constants.min_berging_pct,
            'y_marking_max': self.constants.max_berging_pct,
            'x_marking_omslagpunt': datetime_to_js(
                prediction['scenarios']['mean']['omslagpunt']),
            'y_marking_desired_fill': desired_fill_pct,
            'desired_fill': desired_fill_pct,
        }
        result = {
            'graph_info': graph_info,
            'overflow_24h': prediction['scenarios']['mean']['overstort_24h'],
            'overflow_5d': prediction['scenarios']['mean']['overstort_5d'],
            'demand_week': tbl.get_week_demand_on(t0),
            'demand_24h': tbl.get_total_demand(
                t0, t0 + datetime.timedelta(hours=24)),
            'current_fill': prediction['current_fill'],
        }
        return result

    def advanced(self, t0, desired_fill_pct, demand_exaggerate,
                 rain_exaggerate, graph_type):
        tbl = DemandTable()
        ds = FewsJdbcDataSource(self.grower_info)
        model = CalculationModel(tbl, ds)

        future = t0 + settings.CONTROLNEXT_FILL_PREDICT_FUTURE

        prediction = model.predict_fill(
            t0, future, desired_fill_pct, demand_exaggerate, rain_exaggerate)

        data = []
        unit = ''
        if graph_type == 'demand':
            data = prediction['intermediate']['demand']
            unit = 'm3'
        elif graph_type == 'max_uitstroom':
            data = prediction['intermediate']['max_uitstroom']
            unit = 'm3'
        elif graph_type == 'toestroom':
            data = prediction['scenarios']['mean']['intermediate']['toestroom']
            unit = 'm3'
        elif graph_type == 'uitstroom':
            data = prediction['scenarios']['mean']['intermediate']['uitstroom']
            unit = 'm3'

        result = {
            'graph_info': {
                'data': series_to_js(data),
                'x0': datetime_to_js(t0),
                'unit': unit,
            }
        }
        return result

    def rain(self, t0, rain_exaggerate_pct):
        _from = t0 - settings.CONTROLNEXT_FILL_HISTORY
        to = t0 + settings.CONTROLNEXT_FILL_PREDICT_FUTURE

        ds = FewsJdbcDataSource(self.grower_info)
        min = ds.get_rain('min', t0, to)
        mean = ds.get_rain('mean', _from, to)
        max = ds.get_rain('max', t0, to)

        if rain_exaggerate_pct != 100:
            rain_exaggerate = rain_exaggerate_pct / 100
            min *= rain_exaggerate
            mean *= rain_exaggerate
            max *= rain_exaggerate

        #import pdb; pdb.set_trace()
        rain_graph_info = {
            'data': {
                'min': series_to_js(min),
                'mean': series_to_js(mean),
                'max': series_to_js(max)
            },
            'x0': datetime_to_js(t0)
        }
        return {
            't0': t0,
            'rain_graph_info': rain_graph_info,
        }
