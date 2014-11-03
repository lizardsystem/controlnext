# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals
import os
import logging
import datetime

from django.http import Http404
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response as RestResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from django.views.decorators.csrf import csrf_protect, csrf_exempt

import pytz

from lizard_ui.views import UiView
from lizard_map.models import WorkspaceEdit
from lizard_map.views import AppView

from controlnext import models
from controlnext.demand_table import DemandTable
from controlnext.calc_model import CalculationModel
from controlnext.conf import settings
from controlnext.evaporation_table import EvaporationTable
from controlnext.fews_data import FewsJdbcDataSource
from controlnext.utils import round_date
from controlnext.models import Constants, Basin,\
    is_valid_crop_type
from controlnext.view_helpers import update_basin_coordinates, \
    update_current_fill

logger = logging.getLogger(__name__)

js_epoch = datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)


def datetime_to_js(dt):
    if dt is not None:
        return (dt - js_epoch).total_seconds() * 1000


def series_to_js(pdseries):
    # bfill because sometimes first element is a NaN
    pdseries = pdseries.fillna(method='bfill')
    return [(datetime_to_js(dt), value) for dt, value in pdseries.iterkv()]
 

class DemandView(APIView):
    """Update demands."""
    def post(self, request, basin_id, format=None):
        try:
            basin = models.Basin.objects.get(id=basin_id)
        except ObjectDoesNotExist:
            raise Http404
        data = request.POST
        for key in sorted(data.iterkeys()):
            demands = models.WaterDemand.objects.filter(**{'owner':basin.owner, 'weeknumber':key})
            for demand in demands:
                if data.get(key) is None:
                    continue
                if demand.demand != float(data[key]):
                    demand.demand = data[key]
                    demand.save()
        return RestResponse(request.POST)


class DashboardView(AppView):
    template_name = 'controlnext/dashboard.html'
    page_title = _('ControlNEXT Delfland dashboard')

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

        # check basin coordinates and update current fill when the basin is
        # shown on the main map
        basins = Basin.objects.filter(on_main_map=True)
        for basin in basins:
            if not basin.location:
                # ^^^ only get coordinates for basins without coordinates
                update_basin_coordinates(basin)
            update_current_fill(basin)  # is cached, no need to update on
            # every request

        return super(DashboardView, self).dispatch(request, *args, **kwargs)


class BasinView(UiView):
    template_name = 'controlnext/basin_detail.html'
    page_title = _('ControlNEXT')

    def get(self, request, basin_id, *args, **kwargs):
        try:
            self.basin = models.Basin.objects.get(id=basin_id)
        except ObjectDoesNotExist:
            raise Http404
        else:
            if (self.basin.owner.crop and
                    is_valid_crop_type(self.basin.owner.crop)):
                self.crop_type = self.basin.owner.crop
        return super(BasinView, self).get(request, *args, **kwargs)

    def current_demand(self):
        return self.demand_table().get(self.current_week())

    def current_week(self):
        now = datetime.datetime.now()
        return now.isocalendar()[1]

    def demand_table(self):        
        table = EvaporationTable(self.basin, None)
        return table.demands_for_gui()


class DataService(APIView):
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

    def get(self, request, basin_id, *args, **kwargs):
        try:
            self.basin = Basin.objects.get(id=basin_id)
            # still needed for request params rain_flood_surface and
            # basin_storage/max_storage
            self.constants = Constants(self.basin)
        except ObjectDoesNotExist:
            raise Http404

        graph_type = request.GET.get('graph_type', None)
        hours_diff = request.GET.get('hours_diff', None)  # debug param

        # overridable variables for demo purposes
        rain_flood_surface = request.GET.get('rain_flood_surface', None)

        # debug params
        if not rain_flood_surface:
            rain_flood_surface = request.GET.get('basin_surface', None)
        basin_storage = request.GET.get('basin_storage', None)
        reverse_osmosis = request.GET.get('reverse_osmosis', None)

        if rain_flood_surface:
            try:
                # basic validation, if not integer, default value is used
                # other validations can be put here, like upper bounds
                self.constants.rain_flood_surface = int(rain_flood_surface)
            except ValueError:
                logger.error("invalid value for rain_flood_surface: %s" %
                             rain_flood_surface)
        if basin_storage:
            try:
                # basic validation, if not integer, default value is used
                # other validations can be put here, like upper bounds
                self.constants.max_storage = int(basin_storage)
            except ValueError:
                logger.error("invalid value for basin_storage: %s" %
                             basin_storage)

        if reverse_osmosis:
            try:
                # basic validation, if not integer, default value is used
                # other validations can be put here, like upper bounds
                self.constants.reverse_osmosis = float(reverse_osmosis)
            except ValueError:
                logger.error("invalid value for reverse_osmosis: %s" %
                             reverse_osmosis)

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
        elif graph_type == 'prediction' or graph_type == 'meter_comparison':
            self.store_parameters(desired_fill, demand_exaggerate,
                                  rain_exaggerate)
            outflow_open = request.GET.get('outflowOpen', None)
            outflow_closed = request.GET.get('outflowClosed', None)
            outflow_capacity = request.GET.get('outflowCapacity', 0)
            if outflow_open is not None:
                outflow_open = datetime.datetime.fromtimestamp(int(outflow_open)/1000, pytz.utc)
            if outflow_closed is not None:
                outflow_closed = datetime.datetime.fromtimestamp(int(outflow_closed)/1000, pytz.utc)
            response_dict = self.prediction(
                t0, desired_fill, demand_exaggerate, rain_exaggerate,
                graph_type, outflow_open, outflow_closed, outflow_capacity)
        else:
            table = EvaporationTable(self.basin, self.constants.rain_flood_surface)
            future = t0 + settings.CONTROLNEXT_FILL_PREDICT_FUTURE
            history = t0 - settings.CONTROLNEXT_FILL_HISTORY
            data = table.get_demand(history, future)
            result = {
                'graph_info': {
                    'data': series_to_js(data),
                    'x0': datetime_to_js(t0),
                    'unit': 'mmmm',
                    'type': graph_type
                }
            }
            response_dict = result
        return RestResponse(response_dict)

    def get_demand_table(self):
        # first try to get crop and surface from request
        crop = self.request.GET.get('crop')  # None if none given
        table = EvaporationTable(self.basin, self.constants.rain_flood_surface)
        return table

    def prediction(self, t0, desired_fill_pct, demand_exaggerate,
                   rain_exaggerate, graph_type, outflow_open,
                   outflow_closed, outflow_capacity):
        
        tbl = EvaporationTable(self.basin, self.constants.rain_flood_surface)
        ds = FewsJdbcDataSource(self.basin, self.constants)
        model = CalculationModel(tbl, ds)
        future = t0 + settings.CONTROLNEXT_FILL_PREDICT_FUTURE

        prediction = model.predict_fill(t0, future, desired_fill_pct,
                                        demand_exaggerate, rain_exaggerate,
                                        outflow_open, outflow_closed,
                                        outflow_capacity)

        if desired_fill_pct == 0:  # first load version
            desired_fill_pct = prediction['current_fill']

        # TODO should use dict comprehension in py > 2.6
        data = dict([(name, series_to_js(scenario['prediction']))
                     for name, scenario in prediction['scenarios'].items()])
        data['history'] = series_to_js(prediction['history'])
        if self.basin.has_own_meter:
            data['history_own_meter'] = series_to_js(
                prediction['history_own_meter'])

        graph_info = {
            'type': graph_type,
            'data': data,
            'x0': datetime_to_js(t0),
            'y_marking_min': self.constants.min_storage_pct,
            'y_marking_max': self.constants.max_storage_pct,
            'x_marking_omslagpunt': datetime_to_js(
                prediction['scenarios']['mean']['omslagpunt']),
            'y_marking_desired_fill': desired_fill_pct,
            'desired_fill': desired_fill_pct,
            'rain_flood_surface': self.constants.rain_flood_surface,
            'basin_storage': self.constants.max_storage,
            'reverse_osmosis': self.constants.reverse_osmosis,
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
        if self.basin.has_own_meter:
            result['current_fill_own_meter'] = (
                prediction['current_fill_own_meter'])
        return result

    def advanced(self, t0, desired_fill_pct, demand_exaggerate,
                 rain_exaggerate, graph_type):
        tbl = self.get_demand_table()
        ds = FewsJdbcDataSource(self.basin, self.constants)
        model = CalculationModel(tbl, ds)
        import pdb; pdb.set_trace()
        future = t0 + settings.CONTROLNEXT_FILL_PREDICT_FUTURE

        prediction = model.predict_fill(
            t0, future, desired_fill_pct, demand_exaggerate, rain_exaggerate)

        data = []
        data_2 = []  # optional secondary dataset
        unit = ''
        historic_data = []
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
            if self.basin.has_discharge_valve:
                historic_data = ds.get_discharge_valve_data(t0)
        elif graph_type == 'greenhouse_discharge':
            unit = 'm3'
            data_method = ds.get_greenhouse_valve_data
            if self.basin.has_greenhouse_valve_1:
                data = data_method(t0, valve_nr=1)
            if self.basin.has_greenhouse_valve_2:
                dataset = data_method(t0, valve_nr=2)
                if len(data):
                    data_2 = dataset
                else:
                    data = dataset
        elif graph_type == '5day_rain':
            data = ds.get_5day_rain_data(t0, predicted=True)
            unit = 'mm'
            historic_data = ds.get_5day_rain_data(t0)

        result = {
            'graph_info': {
                'data': series_to_js(data),
                'x0': datetime_to_js(t0),
                'unit': unit,
                'type': graph_type
            }
        }
        # need to use len for testing truth value, because it is a pandas
        # Series instance (numpy array)
        if len(historic_data):
            result['graph_info'].update(
                {'history': series_to_js(historic_data)})
        # if secondary dataset exists, add it to the result
        if len(data_2):  # need to use len for truth checking (numpy array)
            result['graph_info'].update(
                {'data_2': series_to_js(data_2)})

        return result

    def rain(self, t0, rain_exaggerate_pct):
        _from = t0 - settings.CONTROLNEXT_FILL_HISTORY
        to = t0 + settings.CONTROLNEXT_FILL_PREDICT_FUTURE

        ds = FewsJdbcDataSource(self.basin, self.constants)
        #min = ds.get_rain('min', t0, to)
        mean = ds.get_rain('mean', _from, to)
        #max = ds.get_rain('max', t0, to)
        sum = ds.get_rain('sum', t0, to)
        kwadrant = ds.get_rain('kwadrant', t0, to)

        if rain_exaggerate_pct != 100:
            rain_exaggerate = rain_exaggerate_pct / 100
            #min *= rain_exaggerate
            mean *= rain_exaggerate
            #max *= rain_exaggerate
            sum *= rain_exaggerate
            kwadrant *= rain_exaggerate
        
        rain_graph_info = {
            'data': {
                #'min': series_to_js(min),
                'mean': series_to_js(mean),
                #'max': series_to_js(max),
                'sum': series_to_js(sum),
                'kwadrant': series_to_js(kwadrant)
            },
            'x0': datetime_to_js(t0)
        }
        return {
            't0': t0,
            'rain_graph_info': rain_graph_info,
        }
