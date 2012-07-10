# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals
import time
import operator

from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from djangorestframework.views import View as JsonView

from lizard_ui.views import UiView
from controlnext import models


class MainView(UiView):
    template_name = 'controlnext/main.html'
    page_title = _('Kraantjesproject')

class PredictionDataView(JsonView):
    _IGNORE_IE_ACCEPT_HEADER = False # Keep this, if you want IE to work

    def get(self, request, *args, **kwargs):
        new_fill = request.GET.get('new_fill', None)
        # NOTE: times should be in UTC
        now = time.time() * 1000
        times = [now + i * 10 * 60 * 60 * 1000 for i in range(6)]
        vals = [5, 50, 60, 20, 50, 60]
        if new_fill is not None:
            vals[0] = int(new_fill)
        minsdiff = [-5, -5, -10, -20, -40, -10]
        maxsdiff = [5, 5, 10, 20, 10, 30]
        mins = map(operator.add, vals, minsdiff)
        maxs = map(operator.add, vals, maxsdiff)
        data = {
            'val': vals,
            'min': mins,
            'max': maxs,
            'abs_min': [20] * len(vals),
            'abs_max': [80] * len(vals)
        }
        for k in data:
            data[k] = zip(times, data[k])
        graph_info = {
            'data': data,
            'xmin': data['val'][0][0],
            'xmax': data['val'][-1][0]
        }
        return {'graph_info': graph_info}
