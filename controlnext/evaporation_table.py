# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import division
from __future__ import unicode_literals
import datetime
import logging

from django.conf import settings
import pandas as pd
import pytz

from controlnext import models
from controlnext.utils import mktim
from controlnext.utils import validate_date

logger = logging.getLogger(__name__)

EVAPORATION_TABLE_PATH = getattr(settings, 'EVAPORATION_TABLE_PATH', None)
EVAPORATION_TABLE_FILE_PREFIX = 'evaporation_table_'

if not EVAPORATION_TABLE_PATH:
    logger.warn('EVAPORATION_TABLE_PATH is not configured.')

# semi configurable constants
CSV_COL_DELIMITER = ';'
EVAPORATION_COLUMN_NAME = 'evaporation'
DAY_COLUMN_NAME = 'day_number'
WEEK_COLUMN_NAME = 'week_number'
ACRE_IN_M2 = 10000  # one acre is 10000 square meters
ONE_DAY = datetime.timedelta(days=1)
TWO_WEEKS = datetime.timedelta(days=14)


def get_day(date):
    return int(date.strftime('%j'))


class EvaporationTable(object):
    def __init__(self, basin, crop_surface):
        self.crop_type = basin.grower.crop
        self.crop_surface = crop_surface
        self.grower = basin.grower
        self.data = self._retrieve_demand()
        self.basin = basin

    def _retrieve_demand(self):
        demands = models.WaterDemand.objects.filter(grower=self.grower)
        demand_dict = {}
        for demand in demands:
            demand_dict[demand.daynumber] = demand.demand
        return demand_dict

    def demands_for_gui(self):
        demands = models.WaterDemand.objects.filter(grower=self.grower)
        demand_dict = {}
        for demand in demands:
            demand_dict[demand.weeknumber] = demand.demand
        return demand_dict

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

    def get_demand_raw(self, _from, to):
        """Use for demand chart."""
        validate_date(_from)
        validate_date(to)
        from_adj = _from
        to_adj = to
        dayly = pd.date_range(from_adj, to_adj, freq='D', tz=pytz.utc)
        values = [self.get_day_evaporation_on(date) for date in dayly]

        ts = pd.Series(values, dayly, name='evaporation')

        # use fillna with ffill instead of ts.interpolate() to keep the data
        # as accurate as possible
        ts.fillna(method='ffill', inplace=True)
        # divide by amount of quarter hours in a day

        return ts[from_adj:to_adj]

    def get_demand(self, _from, to):
        """Use for prediction chart. Convert demand from m2 to m3."""
        validate_date(_from)
        validate_date(to)

        # ensure we deal with broader range to avoid resample edge problems
        from_adj = _from
        to_adj = to
        dayly = pd.date_range(from_adj, to_adj, freq='D', tz=pytz.utc)
        values = [self.get_day_evaporation_on(date) for date in dayly]

        ts = pd.Series(values, dayly, name='evaporation')
        ts = ts.resample('15min')

        # use fillna with ffill instead of ts.interpolate() to keep the data
        # as accurate as possible
        ts.fillna(method='ffill', inplace=True)
        # divide by amount of quarter hours in a day
        ts /= 24 * 4
        ts *= float(0.001)
        ts *= self.crop_surface
        ts *= self.basin.recirculation
        result = ts[from_adj:to_adj]
        return result
