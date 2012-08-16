# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals
import os
import logging
import datetime

from django.conf import settings

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

    def init(self):
        '''
        Lazy load and keep the demand table in memory, because it's tiny.
        '''
        if not self.data:
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
