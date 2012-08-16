# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals
import os
import logging
import datetime

from django.conf import settings

import pandas as pd
import numpy as np
# optionally import matplotlib which can be used to debugging
try:
    import matplotlib.pyplot as plt
except ImportError:
    pass

from controlnext.demand_table import DemandTable

logger = logging.getLogger(__name__)

class CalculationModel(object):
    def __init__(self, demand_table):
        self.demand_table = demand_table
        self.year = self.demand_table.year
        self.ts = None

    def init(self):
        '''
        Initialize the timeseries object used for calculation.
        '''
        start = datetime.datetime(self.year, 1, 1)
        end = datetime.datetime(self.year + 1, 1, 1)
        weekly = pd.date_range(start, end, freq='W-MON', tz='UTC') # week changes on monday
        values = [self.demand_table.get_demand_for_week(week) for week in range(1, len(weekly) + 1)] # start at week 1

        ts = pd.Series(values, weekly)
        #ts = ts.resample('H', fill_method='pad')
        ts = ts.resample('15min')
        ts = ts.interpolate()
        ts = np.true_divide(ts, 7 * 24 * 4) # quarter hours in a week
        self.ts = ts

    def plot(self):
        '''
        Useful for debugging.
        '''
        fig = plt.figure(figsize=(24, 6))
        axes = self.ts.plot()
        fig.add_subplot(axes)
        fig.savefig('out.png')

    def get_demand(self, _from, to):
        # set from and to to year 2012 (leap year, so Feb. 29 works as well)
        # as we only have a table for one year
        _from = datetime.datetime(self.year, _from.month, _from.day, _from.hour)
        to = datetime.datetime(self.year, to.month, to.day, to.hour)
        return self.ts[_from:to]

    def get_total_demand(self, _from, to):
        return self.get_demand(_from, to).sum()
