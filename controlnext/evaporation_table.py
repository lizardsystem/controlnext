# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals
from __future__ import division
import os
import datetime
import logging

from django.conf import settings

#from controlnext.utils import cache_result, validate_date, mktim

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
WEEK_COLUMN_NAME = 'week_number'
ACRE_IN_M2 = 10000  # one acre is 10000 square meters
ONE_DAY = datetime.timedelta(days=1)


def get_day(date):
    return int(date.strftime('%j'))


def rewrite_demand_csv(data, crop):
    
    file_path = os.path.join(
        EVAPORATION_TABLE_PATH, "%s%s.csv" %(
            EVAPORATION_TABLE_FILE_PREFIX, crop))
    logging.debug('Writing to %s', file_path)
    with open(file_path, 'wb') as file:
        file.write(str(DAY_COLUMN_NAME) + CSV_COL_DELIMITER)
        file.write(str(EVAPORATION_COLUMN_NAME) + CSV_COL_DELIMITER)
        file.write(str(WEEK_COLUMN_NAME) + '\n')
        year_days = 365
        day = 1
        for key in sorted(data.iterkeys()):
            for week_day in range(1, 8):
                if day > year_days:
                    break
                file.write(str(day) + CSV_COL_DELIMITER)
                file.write(str(data[key]) + CSV_COL_DELIMITER)
                file.write(str(key) + '\n')
                day = day + 1
                
        
class EvaporationTable(object):
    def __init__(self, crop_type, crop_surface):
        self.crop_type = crop_type
        self.crop_surface = crop_surface
        self.data = self._read_csv()

#    @cache_result(3600, ignore_cache=False, instancemethod=True)
    def _read_csv(self):
        '''
        Reads the evaporation csv file and return its contents in a dict
        int(day number) -> int(evaporation_value).
        Evaporation values are in m3 / acre.
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
                result[row[day_column]] = row[evaporation_column] + 10
        return result

    def read_csv_for_gui(self):
        '''
        Reads the evaporation csv file and return its contents in a dict
        int(week number) -> int(evaporation_value).
        Evaporation values are in m3 / acre.
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
            week_column = cols.index(WEEK_COLUMN_NAME)
            evaporation_column = cols.index(EVAPORATION_COLUMN_NAME)
            for line in file:
                row = line.strip().split(CSV_COL_DELIMITER)
                # convert everything to floats
                #row = map(float, row)
                result[int(row[week_column])] = row[evaporation_column] + 10
        return result

    def get_evaporation_for_day(self, day_number):
        '''
        Returns the demand on the given day, in m3 per acre.
        '''
        # get evaporation value for this day
        result = self.data[day_number]
        return result

    def get_day_evaporation_on(self, date):
        '''
        Returns the week demand on the given date, in m3 per acre.
        '''
        # determine day number for given date
        day_number = get_day(date)
        if day_number == 0:
            day_number = 1
        elif day_number == 366:
            day_number = 365
        return self.get_evaporation_for_day(day_number)

    def get_week_demand_on(self, start_date):
        # needed for calc model
        end_date = start_date + datetime.timedelta(days=7)
        return self.get_total_demand(start_date, end_date)

    def get_demand(self, _from, to):
        validate_date(_from)
        validate_date(to)

        # ensure we deal with broader range to avoid resample edge problems
        from_adj = _from - ONE_DAY
        to_adj = to + ONE_DAY
        dayly = pd.date_range(from_adj, to_adj, freq='D', tz=pytz.utc)
        values = [self.get_day_evaporation_on(date) for date in dayly]

        ts = pd.Series(values, dayly, name='evaporation')
        ts = ts.resample('15min')
        ts[0] = values[0]
        # use fillna with ffill instead of ts.interpolate() to keep the data
        # as accurate as possible
        ts.fillna(method='ffill', inplace=True)
        # divide by amount of quarter hours in a day
        ts /= 24 * 4
        # correct for crop surface
        surface_correction_factor = self.crop_surface / ACRE_IN_M2
        ts *= surface_correction_factor
        result = ts[_from:to]
        return result

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
        axes.set_ylabel('evaporation (in m3/acre/15min) (crop: %s)' %
                        self.crop_type)
        fig.savefig('evaporation_plot_%s.png' % self.crop_type)
