# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals
import datetime
import time
import operator
import random

from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from djangorestframework.views import View as JsonView

from lizard_ui.views import UiView
from controlnext import models
from controlnext import demand_table

class MainView(UiView):
    template_name = 'controlnext/main.html'
    page_title = _('Kraantjesproject')

class PredictionDataView(JsonView):
    _IGNORE_IE_ACCEPT_HEADER = False # Keep this, if you want IE to work

    def get(self, request, *args, **kwargs):
        demand_table.test_demand_table()
        new_fill = request.GET.get('new_fill', None)
        # NOTE: times should be in UTC
        dtnow = datetime.datetime.now()
        now = time.time() * 1000
        times = [now + i * 2 * 60 * 60 * 1000 for i in range(72)]
        vals = [5, 50, 60, 20, 50, 60] * 36
        if new_fill is not None:
            vals[0] = int(new_fill)
        minsdiff = [-5, -5, -10, -20, -40, -10] * 36
        maxsdiff = [5, 5, 10, 20, 10, 30] * 36
        mins = map(operator.add, vals, minsdiff)
        maxs = map(operator.add, vals, maxsdiff)
        data = {
            'val': vals,
            'min': mins,
            'max': maxs
        }
        for k in data:
            data[k] = zip(times, data[k])
        data['t0'] = [(data['val'][0][0], 0), (data['val'][0][0], 120)]
        # add some history
        data['val'][0:0] = [(now - (14 * 24 * 60 * 60 * 1000), 40)]
        graph_info = {
            'data': data,
            'xmin': now,
            'xmax': now + (24 * 60 * 60 * 1000),
            'y_marking_min': 20, # fixed value
            'y_marking_max': 100 # fixed value
        }
        overflow = random.randint(0, 4)
        return {
            'graph_info': graph_info,
            'overflow': overflow,
            'demand24h': demand_table.get_total_demand(dtnow, dtnow + datetime.timedelta(hours=24))
        }
