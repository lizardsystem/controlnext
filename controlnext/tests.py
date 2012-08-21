import datetime
import logging

import pytz
import numpy as np
import pandas as pd

from django.test import TestCase

from controlnext.demand_table import DemandTable
from controlnext.calc_model import CalculationModel
from controlnext.fews_data import FewsJdbcDataSource
from controlnext.constants import *

logger = logging.getLogger(__name__)

def plot(name, *args):
    if not name:
        name = 'plot'
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(24, 6))
    for df in args:
        fig.add_subplot(df.plot())
    fig.savefig('plot_' + name + '.png')

def mktim(*args):
    return datetime.datetime(*args, tzinfo=pytz.utc)

w26_0 = mktim(2012, 6, 25, 0, 0, 0)     # monday, 0:00, week 26 (d = 20000)
w27_0 = mktim(2012, 7, 2, 0, 0, 0)      # monday, 0:00, week 27 (d = 20000)

w28_0 = mktim(2012, 7, 9, 0, 0, 0)      # monday, 0:00, week 28 (d = 19000)
w28_5 = mktim(2012, 7, 12, 11, 59, 59)  # middle of week 28
w28_9 = mktim(2012, 7, 15, 23, 59, 59)  # sunday, 23:59, week 28

w29_0 = mktim(2012, 7, 16, 0, 0, 0)     # sunday, 0:00, week 29 (d = 18000)
w29_5 = mktim(2012, 7, 19, 12, 0, 0)    # middle of week 29
w29_9 = mktim(2012, 7, 22, 23, 59, 59)  # sunday, 23:59, week 29

w30_0 = mktim(2012, 7, 23, 0, 0, 0)     # sunday, 0:00, week 30 (d = 17000)
w30_5 = mktim(2012, 7, 26, 12, 0, 0)    # middle of week 30 (d = 17000)
w30_9 = mktim(2012, 7, 29, 23, 59, 59)  # middle of week 30 (d = 17000)

class DemandTableTest(TestCase):
    def setUp(self):
        tbl = DemandTable()
        tbl.init()
        self.tbl = tbl

    def test_full_week_linear(self):
        res = self.tbl.get_total_demand(w26_0, w27_0)
        expected = self.tbl.get_demand_for_week(26)
        self.assertAlmostEqual(res, expected, delta=200)

    def test_half_week(self):
        res = self.tbl.get_total_demand(w28_0, w28_5)
        expected = self.tbl.get_demand_for_week(28) / 2
        self.assertAlmostEqual(res, expected, delta=500)

    def test_full_week(self):
        res = self.tbl.get_total_demand(w28_0, w29_0)
        expected = self.tbl.get_demand_for_week(28)
        self.assertAlmostEqual(res, expected, delta=500)

    def test_full_week2(self):
        res = self.tbl.get_total_demand(w29_0, w30_0)
        expected = self.tbl.get_demand_for_week(29)
        self.assertAlmostEqual(res, expected, delta=500)

class FewsJdbcDataSourceTest(TestCase):
    fixtures = ['jdbc_source.json']

    def setUp(self):
        self.ds = FewsJdbcDataSource()

    def test_connection(self):
        fews_data = self.ds.get_fill(w30_0, w30_5)
        self.assertGreater(len(fews_data), 10)

class CalculationModelTest(TestCase):
    fixtures = ['jdbc_source.json']

    def setUp(self):
        tbl = DemandTable()
        tbl.init()
        self.tbl = tbl

        ds = FewsJdbcDataSource()
        self.ds = ds

        model = CalculationModel(tbl, ds)
        self.model = model

    def mkplot(self, name, t1, t2):
        rains = []
        for which in ['min', 'mean', 'max']:
            rain = self.ds.get_rain(which, t1, t2)
            rains.append(rain)
        plot(name, *rains)

    def test_make_some_plots(self):
        now = datetime.datetime.now(pytz.utc)
        history = now - datetime.timedelta(days=1)
        future = now + datetime.timedelta(days=5)
        d1 = self.tbl.get_demand(w28_0, w29_5)
        d2 = self.ds.get_fill(w28_0, w29_5)
        d3 = self.ds.get_rain('mean', w28_0, w29_5)
        self.mkplot('history', history, now)
        self.mkplot('span', history, future)
        self.mkplot('future', now, future)

    def test_calc_model(self):
        now = w28_0
        future = now + datetime.timedelta(days=5)
        ts = self.model.predict_overflow(now, future, 80, 100)
        self.assertGreater(len(ts), 10)
