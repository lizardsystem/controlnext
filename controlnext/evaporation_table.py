# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals
from __future__ import division
import os
import logging

from django.conf import settings

from controlnext.utils import cache_result, validate_date, mktim

import pytz
import pandas as pd

logger = logging.getLogger(__name__)

EVAPORATION_TABLE_PATH = getattr(settings, 'EVAPORATION_TABLE_PATH', None)
EVAPORATION_TABLE_FILE_PREFIX = 'evaporation_table_'

if not EVAPORATION_TABLE_PATH:
    logger.warn('EVAPORATION_TABLE_PATH is not configured.')
#elif not os.path.isfile(EVAPORATION_TABLE_PATH):
#    logger.warn('Could not find a file at %s.', EVAPORATION_TABLE_PATH)

# semi configurable constants
CSV_COL_DELIMITER = ';'
EVAPORATION_COLUMN_NAME = 'evaporation'
DAY_COLUMN_NAME = 'day_number'


def get_day(date):
    return int(date.strftime('%j'))


class EvaporationTable(object):
    def __init__(self, crop_type):
        self.crop_type = crop_type
        self.data = self._read_csv()

#    @cache_result(3600, ignore_cache=False, instancemethod=True)
    def _read_csv(self):
        '''
        Reads the evaporation csv file and return its contents in a dict
        int(day number) -> int(evaporation_value).
        Evaporation values are in kilogram/acre.
        '''
        # dont use the csv module here, its ancient (no unicode)
        # and less dependencies is generally better
        file_path = os.path.join(
            EVAPORATION_TABLE_PATH, "%s%s.csv" %
            (EVAPORATION_TABLE_FILE_PREFIX, self.crop_type))
        logging.debug('Reading %s', file_path)
        result = {}
        with open(file_path, 'rb') as file:
            cols = file.next().strip().split(CSV_COL_DELIMITER)
            # do some validation, raises value error on missing column
            day_column = cols.index(DAY_COLUMN_NAME)
            evaporation_column = cols.index(EVAPORATION_COLUMN_NAME)
            for line in file:
                row = line.strip().split(CSV_COL_DELIMITER)
                # convert everything to floats
                row = map(float, row)
                result[row[day_column]] = row[evaporation_column]
        return result

    def get_evaporation_for_day(self, day_number):
        '''
        Returns the demand on the given day, in kilogram per acre.
        '''
        # get evaporation value for this day
        result = self.data[day_number]
        return result

    def get_day_evaporation_on(self, date):
        '''
        Returns the week demand on the given date, in kilogram per acre.
        '''
        # determine day number for given date
        day_number = get_day(date)
        if day_number == 0:
            day_number = 1
        elif day_number == 366:
            day_number = 365
        return self.get_evaporation_for_day(day_number)

    def get_demand(self, _from, to):
        validate_date(_from)
        validate_date(to)

        dayly = pd.date_range(_from, to, freq='D', tz=pytz.utc)
        values = [self.get_day_evaporation_on(date) for date in dayly]

        ts = pd.Series(values, dayly, name='evaporation')
        ts = ts.resample('15min')
        ts[0] = values[0]
        # use fillna with ffill instead of ts.interpolate() to keep the data
        # as accurate as possible
        ts.fillna(method='ffill', inplace=True)
        # divide by amount of quarter hours in a day
        ts /= 24 * 4
        return ts[_from:to]

    def get_total_demand(self, _from, to):
        return self.get_demand(_from, to).sum()

    def plot(self):
        '''
        Useful for debugging.
        '''
        import matplotlib.pyplot as plt
        ts = self.get_demand(mktim(2012, 1, 1, 0, 0),
                             mktim(2013, 1, 1, 0, 0))
        fig = plt.figure(figsize=(24, 6))
        axes = ts.plot()
        fig.add_subplot(axes)
        axes.set_ylabel('evaporation (in kg/acre/15min) (crop: %s)' %
                        self.crop_type)
        fig.savefig('evaporation_plot_%s.png' % self.crop_type)
