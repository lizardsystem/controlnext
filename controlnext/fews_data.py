# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals
import os
import logging
import datetime

from django.conf import settings

import iso8601
import pytz
import pandas as pd
import numpy as np

from lizard_fewsjdbc.models import JdbcSource
from lizard_fewsjdbc.models import FewsJdbcQueryError

logger = logging.getLogger(__name__)

# Better not import this in case anyone decides to change it
# from lizard_fewsjdbc.models import JDBC_DATE_FORMAT
JDBC_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

jdbc_source_slug = 'controlnext'

rain_filter_id = 'neerslag_combo'    # Neerslag gecombimeerd
rain_location_id = 'OPP1'            # Oranjebinnenpolder Oost
rain_parameter_ids = {
    'min': 'P.min',   # Minimum
    'mean': 'P.gem',  # Gemiddeld
    'max': 'P.max'    # Maximum
}

current_fill_filter_id = 'waterstand_basins' # Waterstanden
current_fill_location_id = '467446797569'    # Van der Lans-west, niveau1
current_fill_parameter_id = 'WNS2820'        # Waterdiepte (cm)

class FewsJdbcDataSource(object):
    def __init__(self):
        try:
            self.jdbc_source = JdbcSource.objects.get(slug=jdbc_source_slug)
        except JdbcSource.DoesNotExist:
            logging.debug('all %s', JdbcSource.objects.all())
            raise Exception("Jdbc source %s doesn't exist." % jdbc_source_slug)

    def get_rain(self, which, _from, to):
        timeseries = self._get_timeseries(rain_filter_id, rain_location_id, rain_parameter_ids[which], _from, to)
        return timeseries

    def get_current_fill(self, _from, to, check_frequency=False):
        row_data = self._get_timeseries(current_fill_filter_id, current_fill_location_id, current_fill_parameter_id, _from, to)
        if check_frequency:
            d15min = datetime.timedelta(minutes=15)
            prev_date = None
            for date, value in row_data:
                if prev_date:
                    if prev_date + d15min != date:
                        raise Exception('Results are non-equidistant for row=({}, {})'.format(date, value))
                prev_date = date
        # store results in a pandas dataframe (fast numpy like datastructure)
        df = pd.DataFrame(row_data)
        # convert the datetime list to numpy datetime objects
        # enforce utc here, because of a bug in pandas 0.8.1
        dates = pd.tseries.tools.to_datetime(df[0], utc='True')
        # build an index of the timeseries and infer its frequency (should be 15min, see above)
        index = pd.DatetimeIndex(dates, freq='infer', tz='UTC')
        # build a timeseries object so we can compare it with other timeseries
        ts = pd.Series(df[1], index=index, name='current_fill')
        return ts

    def _get_timeseries(self, filter_id, location_id, parameter_id, start_date, end_date):
        '''
        Custom implementation of JdbcSource's get_timeseries().
        '''
        if not start_date.tzinfo or not end_date.tzinfo:
            raise ValueError('Please refrain from using naive datetime objects for start_date and end_date.')

        q = ("select time, value from "
             "extimeseries where filterid='%s' and locationid='%s' "
             "and parameterid='%s' and time between '%s' and '%s'" %
             (filter_id, location_id, parameter_id,
              start_date.strftime(JDBC_DATE_FORMAT),
              end_date.strftime(JDBC_DATE_FORMAT)))

        result = self.jdbc_source.query(q)

        for row in result:
            # Expecting dateTime.iso8601 in a mixed format (basic date +
            # extended time) with time zone indication (Z = UTC),
            # for example: 20110828T00:00:00Z.
            date_time = row[0].value
            date_time_adjusted = '%s-%s-%s' % (date_time[0:4], date_time[4:6], date_time[6:])
            # Replace the tzinfo object with the pytz one, because the iso8601 one seems incomplete
            row[0] = iso8601.parse_date(date_time_adjusted).astimezone(pytz.utc)

        return result
