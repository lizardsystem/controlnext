import datetime
import logging

import pytz
import numpy as np
import pandas as pd

from django.test import TestCase

from controlnext.demand_table import DemandTable
from controlnext.calc_model import CalculationModel
from controlnext.fews_data import FewsJdbcDataSource

logger = logging.getLogger(__name__)

def plot(*args):
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(24, 6))
    for df in args:
        fig.add_subplot(df.plot())
    fig.savefig('plot.png')

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

class CalculationModelTest(TestCase):
    def setUp(self):
        tbl = DemandTable()
        tbl.init()
        self.tbl = tbl

        model = CalculationModel(tbl, None)
        model.init()
        self.model = model

    def test_full_week_linear(self):
        res = self.model.get_total_demand(w26_0, w27_0)
        res_tbl = self.tbl.get_demand_for_week(26)
        self.assertAlmostEqual(res, res_tbl, delta=200)

    def test_half_week(self):
        res = self.model.get_total_demand(w28_0, w28_5)
        self.assertAlmostEqual(res, 9500.0, delta=500)

    def test_full_week(self):
        res = self.model.get_total_demand(w28_0, w29_0)
        res_tbl = self.tbl.get_demand_for_week(28)
        self.assertAlmostEqual(res, res_tbl, delta=500)

    def test_full_week2(self):
        res = self.model.get_total_demand(w29_0, w30_0)
        res_tbl = self.tbl.get_demand_for_week(29)
        self.assertAlmostEqual(res, res_tbl, delta=500)

class FewsDataTest(TestCase):
    fixtures = ['jdbc_source.json']

    def setUp(self):
        self.ds = FewsJdbcDataSource()

    def test_connection(self):
        fews_data = self.ds.get_current_fill(w30_0, w30_5)
        self.assertGreater(len(fews_data), 10)

class CalcTest(TestCase):
    fixtures = ['jdbc_source.json']

    def setUp(self):
        tbl = DemandTable()
        tbl.init()
        self.tbl = tbl

        ds = FewsJdbcDataSource()
        self.ds = ds

        model = CalculationModel(tbl, ds)
        self.model = model

    def test_calculation(self):
        d1 = self.tbl.get_demand(w28_0, w29_5)
        d2 = self.ds.get_current_fill(w28_0, w29_5)
        # build dataframe index based on intersection of d1 and d1 indices
        d3 = pd.DataFrame(data={d1.name: d1, d2.name: d2})
        plot(d1, d2)
        import pdb; pdb.set_trace()
        #d3 = d1.cov(d2)
