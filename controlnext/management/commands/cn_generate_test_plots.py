from __future__ import print_function
import datetime

from django.conf import settings
from django.core.management.base import BaseCommand

import pytz

from controlnext.calc_model import CalculationModel
from controlnext.demand_table import DemandTable
from controlnext.fews_data import FewsJdbcDataSource
from controlnext.models import GrowerInfo
from controlnext.utils import round_date, mktim


def plot(name, *args):
    if not name:
        name = 'plot'
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(24, 6))
    for df in args:
        fig.add_subplot(df.plot())
    fig.savefig('plot_' + name + '.png')


class Command(BaseCommand):
    """Management command for generating test plots."""
    help = 'Generate controlnext test plots.'

    def mkplot(self, name, t1, t2):
        rains = []
        for which in ['min', 'mean', 'max']:
            rain = self.ds.get_rain(which, t1, t2)
            rains.append(rain)
        plot(name, *rains)

    def handle(self, **options):
        grower = GrowerInfo.objects.get(pk=1)
        basin =  grower.basin_set.all()[0]
        self.ds = FewsJdbcDataSource(basin)
        tbl = DemandTable()
        model = CalculationModel(tbl, self.ds)

        now = datetime.datetime.now(pytz.utc)
        history = now - datetime.timedelta(days=1)
        future = now + datetime.timedelta(days=5)

        now = round_date(now)
        history = round_date(history)
        future = round_date(future)

        self.mkplot('history', history, now)
        self.mkplot('span', history, future)
        self.mkplot('future', now, future)

        now = mktim(2012, 8, 5, 8, 0)  # some rain fell here
        now = round_date(datetime.datetime.now(tz=pytz.utc))
        future = now + settings.CONTROLNEXT_FILL_PREDICT_FUTURE

        ts = model.predict_fill(now, future, 20, 100, 100)

        plot('predict_fill', ts['scenarios']['mean']['prediction'],
             ts['history'])
        # plot('predict_fill_rain', ts['rain'])
        plot('predict_fill_uitstroom',
             ts['scenarios']['mean']['intermediate']['uitstroom'])
        plot('predict_fill_toestroom',
             ts['scenarios']['mean']['intermediate']['toestroom'])
        plot('predict_fill_max_uitstroom',
             ts['intermediate']['max_uitstroom'])
        plot('predict_fill_watervraag', ts['intermediate']['demand'])
