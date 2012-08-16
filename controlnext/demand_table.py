# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals
import os
import logging
import datetime

from django.conf import settings

import pytz
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

demand_table_path = getattr(settings, 'DEMAND_TABLE_PATH', None)

if not demand_table_path:
    logger.warn('DEMAND_TABLE_PATH is not configured.')
elif not os.path.isfile(demand_table_path):
    logger.warn('Could not find a file at %s.', demand_table_path)

# semi configurable constants
col_delimiter = ';'
required_cols = set(['week_number', 'demand_lans_m3_div_1000', 'demand_waterschap_m3_div_1000'])

class DemandTable(object):
    year = 2012

    def __init__(self):
        self.data = None
        self.ts = None

    def init(self):
        '''
        Lazy load and keep the demand table in memory, because it's tiny.
        '''
        if not self.data:
            self.data = self._read_demand_csv()
            self.ts = self._generate_series()

    def _read_demand_csv(self):
        '''
        Reads the demand csv file and return its contents in a dict
        int(week number) -> (int(demand_lans), int(demand_waterschap)).
        Demands are in m^3.
        '''
        # dont use the csv module here, its ancient (no unicode)
        # and less dependencies is generally better
        logging.debug('Reading %s', demand_table_path)
        result = {}
        with open(demand_table_path, 'rb') as file:
            cols = file.next().strip().split(col_delimiter)
            # do some validation
            if not required_cols.issubset(cols):
                raise Exception('Could not find the necessary columns in the csv.')
            # TODO: column headers are unused, so the CSV isn't very flexible
            for line in file:
                row = line.strip().split(col_delimiter)
                row = map(int, row)
                # multiply demands by 1000 so we return a sane unit (m^3)
                result[row[0]] = (row[1] * 1000, row[2] * 1000)
        # table doesn't define anything for week 0 (the days between new year and first sunday)
        if not 0 in result:
            # just copy the values from week 1
            result[0] = result[1]
        # table only goes to 52, but a week 53 exists for some years
        if not 53 in result:
            # just copy the values from week 52
            result[53] = result[52]
        return result

    def _generate_series(self):
        '''
        Generate a pandas Series object used for calculation.
        '''
        start = datetime.datetime(self.year, 1, 1, tzinfo=pytz.utc)
        end = datetime.datetime(self.year + 1, 1, 1, tzinfo=pytz.utc)
        weekly = pd.date_range(start, end, freq='W-MON', tz='UTC') # week changes on monday
        values = [self.get_demand_for_week(week) for week in range(1, len(weekly) + 1)] # start at week 1

        ts = pd.Series(values, weekly, name='demand')
        #ts = ts.resample('H', fill_method='pad')
        ts = ts.resample('15min')
        ts = ts.interpolate()
        ts = np.true_divide(ts, 7 * 24 * 4) # quarter hours in a week
        return ts

    def get_demand_for_week(self, week):
        '''
        Returns the demand on the given week, in m^3. 
        '''
        # get demand for this week
        result = self.data[week][0]
        return result

    def get_week_demand_on(self, date):
        '''
        Returns the week demand on the given date, in m^3. 
        '''
        # determine week number for given date
        week = date.isocalendar()[1]
        return self.get_demand_for_week(week)

    def get_demand(self, _from, to):
        # set from and to to year 2012 (leap year, so Feb. 29 works as well)
        # as we only have a table for one year
        _from = _from.replace(year=self.year)
        to = to.replace(year=self.year)
        return self.ts[_from:to]

    def get_total_demand(self, _from, to):
        return self.get_demand(_from, to).sum()

    def plot(self):
        '''
        Useful for debugging.
        '''
        import matplotlib.pyplot as plt
        fig = plt.figure(figsize=(24, 6))
        axes = self.ts.plot()
        fig.add_subplot(axes)
        fig.savefig('{}_plot.png'.format(__name__))
