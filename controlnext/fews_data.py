# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals
import datetime
import logging

import iso8601
import pandas as pd
import pytz
from lizard_fewsjdbc.models import JdbcSource

from controlnext.conf import settings
from controlnext.models import Constants
from controlnext.utils import validate_date

logger = logging.getLogger(__name__)

RAIN_PARAMETER_IDS = {
    'min': 'P.min',     # Minimum
    'mean': 'P.gem',    # Gemiddeld
    'sum': 'P.voorsp',  # Sum
    'kwadrant': 'advies.kwadrant'
}
FREQUENCY = datetime.timedelta(minutes=15)


class FewsJdbcDataSource(object):
    def __init__(self, basin, constants=None):
        self.basin = basin
        if constants:
            self.constants = constants
        else:
            self.constants = Constants(basin)
        if self.basin.jdbc_source:
            self.jdbc_source = self.basin.jdbc_source
        else:
            try:
                self.jdbc_source = JdbcSource.objects.get(
                    slug=settings.CONTROLNEXT_JDBC_SOURCE_SLUG)
            except JdbcSource.DoesNotExist:
                raise Exception("Jdbc source %s does not exist." %
                                settings.CONTROLNEXT_JDBC_SOURCE_SLUG)

    def get_rain(self, which, _from, to, *args, **kwargs):
        validate_date(_from)
        validate_date(to)

        rain_filter_id = self.basin.rain_filter_id
        rain_location_id = self.basin.rain_location_id

        rain = self._get_timeseries_as_pd_series(
            rain_filter_id,
            rain_location_id,
            RAIN_PARAMETER_IDS[which],
            _from, to, 'rain_' + which
        )

        # convert to quarterly figures
        rain = rain.resample('15min', fill_method='ffill')
        # 4 quarters in an hour
        if which != 'kwadrant':
            rain /= 4
        return rain

    def get_fill(self, _from, to, *args, **kwargs):
        validate_date(_from)
        validate_date(to)

        # basin parameters
        fill_filter_id = self.basin.filter_id
        fill_location_id = self.basin.location_id
        fill_parameter_id = self.basin.parameter_id
        # max_storage can come from request, therefore from self.constants
        max_storage = self.constants.max_storage

        # values are given in percentage as to max_storage
        ts = self._get_timeseries_as_pd_series(
            fill_filter_id,
            fill_location_id,
            fill_parameter_id,
            _from, to, 'fill'
        )
        ts = self.fill_pct_to_m3(ts, max_storage)

        return ts

    def fill_pct_to_m3(self, ts, max_storage):
        # values are percentages (0-100)
        ts /= 100
        # convert to m3
        ts *= max_storage

        # data is in 5 minute intervals, so we need to resample to 15 minutes
        ts = ts.resample('15Min')

        return ts

    def get_current_fill(self, _from, history_timedelta=None, **kwargs):
        '''
        returns latest available fill AND its series
        '''
        # optional parameter
        if not history_timedelta:
            history_timedelta = settings.CONTROLNEXT_FILL_HISTORY

        fill_history_m3 = self.get_fill(
            _from - history_timedelta, _from, **kwargs)

        # take last measured value as 'current' fill
        current_fill_m3 = fill_history_m3[-1]

        return {
            'current_fill_m3': current_fill_m3,
            'fill_history_m3': fill_history_m3
        }

    def _get_timeseries_as_pd_series(
            self, filter_id, location_id, parameter_id, _from, to, name=None):
        row_data = self._get_timeseries(filter_id, location_id,
                                        parameter_id, _from, to)
        if len(row_data) == 0:
            raise Exception('No data available')

        # store results in a dataframe
        df = pd.DataFrame(row_data)

        index = pd.DatetimeIndex(df[0], freq='infer', tz=pytz.utc)

        # build a timeseries object so we can compare it with other timeseries
        ts = pd.Series(df[1].values, index=index, name=name)

        return ts

    def _get_timeseries(self, filter_id, location_id, parameter_id, _from, to):
        """
        Custom implementation of JdbcSource's get_timeseries().

        Example query:
        --------------
          select time, value from extimeseries where
          filterid='waterstand_basins' and locationid='467446797569' and
          parameterid='WNS2820' and time between '2013-01-19 09:15:00' and
          '2013-02-19 09:15:00'

        """
        if not _from.tzinfo or not to.tzinfo:
            raise ValueError(
                'Please refrain from using naive datetime objects for _from '
                'and to.')

        qw = ("select time, value from "
            "extimeseries where filterid='%s' and locationid='%s' "
            "and parameterid='%s' and time between '%s' and '%s'" %
            (filter_id, location_id, parameter_id,
                _from.strftime(settings.CONTROLNEXT_JDBC_DATE_FORMAT),
                to.strftime(settings.CONTROLNEXT_JDBC_DATE_FORMAT)))

        result = self.jdbc_source.query(qw)

        for row in result:
            # Expecting dateTime.iso8601 in a mixed format (basic date +
            # extended time) with time zone indication (Z = UTC),
            # for example: 20110828T00:00:00Z.
            date_time = row[0].value
            date_time_adjusted = '%s-%s-%s' % (date_time[0:4], date_time[4:6],
                                               date_time[6:])
            # Replace the tzinfo object with the pytz one, because the iso8601
            # one seems incomplete
            row[0] = iso8601.parse_date(date_time_adjusted).astimezone(
                pytz.utc)

        return result
