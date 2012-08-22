# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals
import logging
import datetime
import time
import operator
import random

import pytz
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from djangorestframework.views import View as JsonView

from lizard_ui.views import UiView
from controlnext import models
from controlnext.demand_table import DemandTable
from controlnext.calc_model import CalculationModel
from controlnext.fews_data import FewsJdbcDataSource
from controlnext.constants import *

logger = logging.getLogger(__name__)

js_epoch = datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)

def datetime_to_js(dt):
    return (dt - js_epoch).total_seconds() * 1000

def series_to_js(pdseries):
    pdseries = pdseries.fillna(None)
    return [(datetime_to_js(dt), value) for dt, value in pdseries.iterkv()]

class MainView(UiView):
    template_name = 'controlnext/main.html'
    page_title = _('Kraantjesproject')

class DataService(JsonView):
    _IGNORE_IE_ACCEPT_HEADER = False # Keep this, if you want IE to work

    def get(self, request, data_type=None):
        hours_diff = request.GET.get('hours_diff', None)

        # note: t0 is Math.floor() 'ed to a full quarter
        t0 = round_date(datetime.datetime.now(pytz.utc))
        if hours_diff:
            t0 += datetime.timedelta(hours=int(hours_diff))

        if data_type == 'rain':
            return self.rain(t0)
        elif data_type == 'prediction':
            desired_fill = request.GET.get('desired_fill')
            demand_diff = request.GET.get('demand_diff')
            desired_fill = int(desired_fill)
            demand_diff = int(demand_diff)
            return self.prediction(t0, desired_fill, demand_diff)

    def prediction(self, t0, desired_fill, demand_diff):
        tbl = DemandTable()
        ds = FewsJdbcDataSource()
        model = CalculationModel(tbl, ds)
        future = t0 + fill_predict_future
        prediction = model.predict_fill(t0, future, desired_fill, demand_diff, fill_history)
        # TODO should use dict comprehension in py > 2.6
        data = dict([(name, series_to_js(scenario['prediction'])) for name, scenario in prediction['scenarios'].items()])
        graph_info = {
            'data': data,
            'x0': datetime_to_js(t0),
            'y_marking_min': min_berging_pct,
            'y_marking_max': max_berging_pct
        }
        result = {
            'graph_info': graph_info,
            'overflow': '',
            #'demand24h': demand_table.get_total_demand(dtnow, dtnow + datetime.timedelta(hours=24))
            'demand24h': ''
        }
        return result

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

    def rain(self, t0):
        tmin = t0 - datetime.timedelta(days=2)
        tmax = t0 + datetime.timedelta(days=5)

        ds = FewsJdbcDataSource()
        min = ds.get_rain('min', tmin, tmax)
        mean = ds.get_rain('mean', tmin, tmax)
        max = ds.get_rain('max', tmin, tmax)
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
