# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals
import os
import logging
import datetime

from django.conf import settings

import pytz
import pandas as pd
import numpy as np

from controlnext.constants import *

logger = logging.getLogger(__name__)

demand_table_path = getattr(settings, 'DEMAND_TABLE_PATH', None)

if not demand_table_path:
    logger.warn('DEMAND_TABLE_PATH is not configured.')
elif not os.path.isfile(demand_table_path):
    logger.warn('Could not find a file at %s.', demand_table_path)

# semi configurable constants
csv_col_delimiter = ';'
demand_column_name = 'demand_m3'
week_column_name = 'week_number'

def get_week(dt):
    return dt.isocalendar()[1]

one_week = datetime.timedelta(weeks=1)

class DemandTable(object):
    def __init__(self):
        self.data = self._read_demand_csv()

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
            cols = file.next().strip().split(csv_col_delimiter)
            # do some validation, raises value error on missing column
            week_column = cols.index(week_column_name)
            demand_column = cols.index(demand_column_name)
            for line in file:
                row = line.strip().split(csv_col_delimiter)
                # convert everything to ints
                row = map(int, row)
                result[row[week_column]] = row[demand_column]
        # table doesn't define anything for week 0 (the days between new year and first sunday)
        if not 0 in result:
            # just copy the values from week 1
            result[0] = result[1]
        # table only goes to 52, but a week 53 exists for some years
        if not 53 in result:
            # just copy the values from week 52
            result[53] = result[52]
        return result

    def get_demand_for_week(self, week):
        '''
        Returns the demand on the given week, in m^3. 
        '''
        # get demand for this week
        result = self.data[week]
        return result

    def get_week_demand_on(self, date):
        '''
        Returns the week demand on the given date, in m^3. 
        '''
        # determine week number for given date
        week = get_week(date)
        return self.get_demand_for_week(week)

    def get_demand(self, _from, to):
        _from = round_date(_from)
        to = round_date(to)

        # ensure we interpolate between two values at least
        to_adj = to + one_week
        weekly = pd.date_range(_from, to_adj, freq='W-MON', tz=pytz.utc) # week changes on monday
        values = [self.get_week_demand_on(date) for date in weekly]

        ts = pd.Series(values, weekly, name='demand')
        ts = ts.resample('15min')
        ts = ts.interpolate()
        # divide by amount of quarter hours in a week
        ts /= 7 * 24 * 4
        return ts[_from:to]

    def get_total_demand(self, _from, to):
        return self.get_demand(_from, to).sum()

    def plot(self):
        '''
        Useful for debugging.
        '''
        import matplotlib.pyplot as plt
        ts = self.get_demand(datetime.datetime(2011, 1, 1), datetime.datetime(2012, 1, 1))
        fig = plt.figure(figsize=(24, 6))
        axes = ts.plot()
        fig.add_subplot(axes)
        fig.savefig('demand_plot.png')
