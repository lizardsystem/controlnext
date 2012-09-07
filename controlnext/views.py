# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals
import os
import logging
import datetime
import time
import operator
import random

import pytz
from django.conf import settings
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from djangorestframework.views import View as JsonView

from lizard_ui.views import UiView
from controlnext import models
from controlnext.demand_table import DemandTable
from controlnext.calc_model import CalculationModel
from controlnext.fews_data import FewsJdbcDataSource
from controlnext import constants
from controlnext.constants import *

logger = logging.getLogger(__name__)

js_epoch = datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)

def datetime_to_js(dt):
    if dt is not None:
        return (dt - js_epoch).total_seconds() * 1000

def series_to_js(pdseries):
    pdseries = pdseries.fillna(None)
    return [(datetime_to_js(dt), value) for dt, value in pdseries.iterkv()]

class MainView(UiView):
    template_name = 'controlnext/main.html'
    page_title = _('ControlNEXT sturing Delfland')

    def get_context_data(self, *args, **kwargs):
        self.oppervlakte = constants.opp_invloed_regen_m2
        self.max_voorraad = constants.max_berging_m3
        return super(UiView, self).get_context_data(*args, **kwargs)

class DataService(JsonView):
    _IGNORE_IE_ACCEPT_HEADER = False # Keep this, if you want IE to work

    def store_parameters(self, desired_fill, demand_exaggerate, rain_exaggerate, extra=''):
        path = settings.REQUESTED_VALUES_CSV_PATH
        directory = os.path.dirname(path)
        if not os.path.isdir(directory):
            os.makedirs(directory)
        if not os.path.isfile(path):
            # write column headers
            with open(path, 'w') as file:
                file.write('desired_fill;demand_exaggerate;rain_exaggerate;extra\n')
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
            return self.rain(t0, rain_exaggerate)
        elif graph_type == 'prediction':
            self.store_parameters(desired_fill, demand_exaggerate, rain_exaggerate)
            return self.prediction(t0, desired_fill, demand_exaggerate, rain_exaggerate)
        else:
            return self.advanced(t0, desired_fill, demand_exaggerate, rain_exaggerate, graph_type)

    def prediction(self, t0, desired_fill_pct, demand_exaggerate, rain_exaggerate):
        tbl = DemandTable()
        ds = FewsJdbcDataSource()
        model = CalculationModel(tbl, ds)

        future = t0 + fill_predict_future

        prediction = model.predict_fill(t0, future, desired_fill_pct, demand_exaggerate, rain_exaggerate)

        # TODO should use dict comprehension in py > 2.6
        data = dict([(name, series_to_js(scenario['prediction'])) for name, scenario in prediction['scenarios'].items()])
        data['history'] = series_to_js(prediction['history'])
        graph_info = {
            'data': data,
            'x0': datetime_to_js(t0),
            'y_marking_min': min_berging_pct,
            'y_marking_max': max_berging_pct,
            'x_marking_omslagpunt': datetime_to_js(prediction['scenarios']['mean']['omslagpunt']),
            'y_marking_desired_fill': desired_fill_pct,
            'desired_fill': desired_fill_pct,
        }
        result = {
            'graph_info': graph_info,
            'overflow_24h': prediction['scenarios']['mean']['overstort'],
            'demand_24h': tbl.get_total_demand(t0, t0 + datetime.timedelta(hours=24)),
            'current_fill': prediction['current_fill'],
        }
        return result

    def advanced(self, t0, desired_fill_pct, demand_exaggerate, rain_exaggerate, graph_type):
        tbl = DemandTable()
        ds = FewsJdbcDataSource()
        model = CalculationModel(tbl, ds)

        future = t0 + fill_predict_future

        prediction = model.predict_fill(t0, future, desired_fill_pct, demand_exaggerate, rain_exaggerate)

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

    """
    def prediction_old(self, t0, desired_fill, demand_diff):
        # NOTE: times should be in UTC
        dtnow = datetime.datetime.now()
        now = time.time() * 1000
        times = [now + i * 2 * 60 * 60 * 1000 for i in range(72)]
        vals = [5, 50, 60, 20, 50, 60] * 36
        if desired_fill is not None:
            vals[0] = int(desired_fill)
        minsdiff = [-5, -5, -10, -20, -40, -10] * 36
        maxsdiff = [5, 5, 10, 20, 10, 30] * 36
        mins = map(operator.add, vals, minsdiff)
        maxs = map(operator.add, vals, maxsdiff)
        data = {
            'mean': vals,
            'min': mins,
            'max': maxs
        }
        for k in data:
            data[k] = zip(times, data[k])
        data['t0'] = [(data['mean'][0][0], 0), (data['mean'][0][0], 120)]
        # add some history
        data['mean'][0:0] = [(now - (14 * 24 * 60 * 60 * 1000), 40)]
        graph_info = {
            'data': data,
            'x0': datetime_to_js(t0),
            'y_marking_min': min_berging_pct,
            'y_marking_max': max_berging_pct
        }
        overflow = random.randint(0, 4)
        return {
            'graph_info': graph_info,
            'overflow': overflow,
            #'demand24h': demand_table.get_total_demand(dtnow, dtnow + datetime.timedelta(hours=24))
            'demand24h': ''
        }
    """

    def rain(self, t0, rain_exaggerate_pct):
        _from = t0 - constants.fill_history
        to = t0 + constants.fill_predict_future

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
