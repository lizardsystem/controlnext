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

from controlnext.utils import cache_result
from controlnext.constants import *
from lizard_fewsjdbc.models import JdbcSource
from lizard_fewsjdbc.models import FewsJdbcQueryError

logger = logging.getLogger(__name__)

# Better not import this in case anyone decides to change it
# from lizard_fewsjdbc.models import JDBC_DATE_FORMAT
JDBC_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

def do_check_frequency(row_data):
    prev_date = None
    for date, value in row_data:
        if prev_date:
            if prev_date + frequency != date:
                raise Exception('Results are non-equidistant for row=({}, {})'.format(date, value))
        prev_date = date

class FewsJdbcDataSource(object):
    def __init__(self):
        try:
            self.jdbc_source = JdbcSource.objects.get(slug=jdbc_source_slug)
        except JdbcSource.DoesNotExist:
            logging.debug('all %s', JdbcSource.objects.all())
            raise Exception("Jdbc source %s doesn't exist." % jdbc_source_slug)

    @cache_result(3600, ignore_cache=False, instancemethod=True)
    def get_rain(self, which, _from, to):
        rain = self._get_timeseries_as_pd_series(
            rain_filter_id,
            rain_location_id,
            rain_parameter_ids[which],
            _from, to,
            name='rain_' + which
        )
        # convert to quarterly figures
        rain = rain.resample('15min', fill_method='ffill')
        # 4 quarters in an hour
        rain /= 4
        return rain

    def get_fill(self, _from, to):
        return self._get_timeseries_as_pd_series(
            fill_filter_id,
            fill_location_id,
            fill_parameter_id,
            _from, to,
            name='fill'
        )

    def _get_timeseries_as_pd_series(self, *args, **kwargs):
        name = kwargs.get('name', None)
        check_frequency = kwargs.get('check_frequency', False)
        row_data = self._get_timeseries(*args)
        if check_frequency:
            do_check_frequency(row_data)
        # store results in a dataframe
        df = pd.DataFrame(row_data)

        # for pandas 0.8.1
        # enforce utc here, because of a bug in pandas 0.8.1
        #dates = pd.tseries.tools.to_datetime(df[0], tz=pytz)

        # convert the datetime list to numpy datetime objects
        # build an index of the timeseries and infer its frequency (should be 15min, see above)
        index = pd.DatetimeIndex(df[0], freq='infer', tz=pytz.utc)

        # build a timeseries object so we can compare it with other timeseries
        ts = pd.Series(df[1].values, index=index, name=name)
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
