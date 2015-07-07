# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import division
from __future__ import unicode_literals
import datetime
import logging
import os

from django.conf import settings
import pandas as pd
import pytz

from controlnext.utils import cache_result
from controlnext.utils import mktim
from controlnext.utils import validate_date

logger = logging.getLogger(__name__)

DEMAND_TABLE_PATH = getattr(settings, 'DEMAND_TABLE_PATH', None)

if not DEMAND_TABLE_PATH:
    logger.warn('DEMAND_TABLE_PATH is not configured.')
elif not os.path.isfile(DEMAND_TABLE_PATH):
    logger.warn('Could not find a file at %s.', DEMAND_TABLE_PATH)

# semi configurable constants
CSV_COL_DELIMITER = ';'
DEMAND_COLUMN_NAME = 'demand_m3'
WEEK_COLUMN_NAME = 'week_number'


def get_week(date):
    return date.isocalendar()[1]

ONE_WEEK = datetime.timedelta(weeks=1)


class DemandTable(object):
    def __init__(self):
        self.data = self._read_demand_csv()

    @cache_result(3600, ignore_cache=False, instancemethod=True)
    def _read_demand_csv(self):
        '''
        Reads the demand csv file and return its contents in a dict
        int(week number) -> (int(demand_lans), int(demand_waterschap)).
        Demands are in m^3.
        '''
        # dont use the csv module here, its ancient (no unicode)
        # and less dependencies is generally better
        logging.debug('Reading %s', DEMAND_TABLE_PATH)
        result = {}
        with open(DEMAND_TABLE_PATH, 'rb') as file:
            cols = file.next().strip().split(CSV_COL_DELIMITER)
            # do some validation, raises value error on missing column
            week_column = cols.index(WEEK_COLUMN_NAME)
            demand_column = cols.index(DEMAND_COLUMN_NAME)
            for line in file:
                row = line.strip().split(CSV_COL_DELIMITER)
                # convert everything to ints
                row = map(int, row)
                result[row[week_column]] = row[demand_column]
        # table doesn't define anything for week 0 (the days between new year
        # and first sunday)
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
        validate_date(_from)
        validate_date(to)

        # ensure we deal with values for _from which are mid-week
        from_adj = _from - 2 * ONE_WEEK
        to_adj = to + 2 * ONE_WEEK
        # week changes on monday
        weekly = pd.date_range(from_adj, to_adj, freq='W-MON', tz=pytz.utc)
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
        ts = self.get_demand(mktim(2012, 1, 1), mktim(2013, 1, 1))
        fig = plt.figure(figsize=(24, 6))
        axes = ts.plot()
        fig.add_subplot(axes)
        fig.savefig('demand_plot.png')
