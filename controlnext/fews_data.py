# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals
import logging
import datetime

import iso8601
import pytz
import pandas as pd

from controlnext.utils import cache_result, validate_date
from controlnext.conf import settings
from controlnext.models import Constants

logger = logging.getLogger(__name__)

RAIN_PARAMETER_IDS = {
    'min': 'P.min',   # Minimum
    'mean': 'P.gem',  # Gemiddeld
    'max': 'P.max'    # Maximum
}
FREQUENCY = datetime.timedelta(minutes=15)


def do_check_frequency(row_data):
    prev_date = None
    for date, value in row_data:
        if prev_date:
            if prev_date + FREQUENCY != date:
                msg = 'Results are non-equidistant for row=({}, {})'.format(
                    date, value)
                raise Exception(msg)
        prev_date = date


class FewsJdbcDataSource(object):
    def __init__(self, grower_info=None):
        self.grower_info = grower_info

    @cache_result(settings.CONTROLNEXT_FEWSJDBC_CACHE_SECONDS,
                  ignore_cache=False, instancemethod=True)
    def get_rain(self, which, _from, to):
        validate_date(_from)
        validate_date(to)

        constants = Constants(self.grower_info)

        rain = self._get_timeseries_as_pd_series(
            constants.rain_filter_id,
            constants.rain_location_id,
            RAIN_PARAMETER_IDS[which],
            _from, to, 'rain_' + which
        )

        # convert to quarterly figures
        rain = rain.resample('15min', fill_method='ffill')
        # 4 quarters in an hour
        rain /= 4
        # deal with NaN values
        #if np.nan in rain:
        #    raise Exception('Found NaN in results')
        #rain = rain.fillna(0)

        return rain

    @cache_result(settings.CONTROLNEXT_FEWSJDBC_CACHE_SECONDS,
                  ignore_cache=False, instancemethod=True)
    def get_fill(self, _from, to):
        validate_date(_from)
        validate_date(to)

        constants = Constants(self.grower_info)

        # waarden zijn in cm onder overstortbuis
        ts = self._get_timeseries_as_pd_series(
            constants.fill_filter_id,
            constants.fill_location_id,
            constants.fill_parameter_id,
            _from, to, 'fill'
        )

        # deal with NaN values
        #if np.NaN in ts:
        #    raise Exception('Found NaN in results')
        #ts = ts.fillna(0)

        # zet om in cm vanaf bodem bak
        ts += constants.hoogte_niveaumeter_cm
        # zet om naar fractie totale bak
        ts /= constants.bovenkant_bak_cm
        # zet om naar m3
        ts *= constants.max_berging_m3

        return ts

    @cache_result(settings.CONTROLNEXT_FEWSJDBC_CACHE_SECONDS,
                  ignore_cache=False, instancemethod=True)
    def get_current_fill(self, _from, history_timedelta=None):
        '''
        returns latest available fill AND its series
        '''
        # optional parameter
        if not history_timedelta:
            history_timedelta = settings.CONTROLNEXT_FILL_HISTORY

        fill_history_m3 = self.get_fill(_from - history_timedelta, _from)

        # take last measured value as 'current' fill
        current_fill_m3 = fill_history_m3[-1]

        return {
            'current_fill_m3': current_fill_m3,
            'fill_history_m3': fill_history_m3
        }

    def _get_timeseries_as_pd_series(
            self, filter_id, location_id, parameter_id, _from, to, name=None,
            check_frequency=False):
        row_data = self._get_timeseries(filter_id, location_id,
                                        parameter_id, _from, to)

        if len(row_data) == 0:
            raise Exception('No data available')

        # check frequency when asked
        if check_frequency:
            do_check_frequency(row_data)

        # store results in a dataframe
        df = pd.DataFrame(row_data)

        # for pandas 0.8.1
        # enforce utc here, because of a bug in pandas 0.8.1
        #dates = pd.tseries.tools.to_datetime(df[0], tz=pytz)
        #import pdb; pdb.set_trace()
        # convert the datetime list to numpy datetime objects
        # build an index of the timeseries and infer its frequency (should be
        # 15min, see above)
        index = pd.DatetimeIndex(df[0], freq='infer', tz=pytz.utc)

        # build a timeseries object so we can compare it with other timeseries
        ts = pd.Series(df[1].values, index=index, name=name)

        return ts

    def _get_timeseries(self, filter_id, location_id, parameter_id, _from, to):
        '''
        Custom implementation of JdbcSource's get_timeseries().
        '''
        if not _from.tzinfo or not to.tzinfo:
            raise ValueError(
                'Please refrain from using naive datetime objects for _from '
                'and to.')

        q = ("select time, value from "
             "extimeseries where filterid='%s' and locationid='%s' "
             "and parameterid='%s' and time between '%s' and '%s'" %
             (filter_id, location_id, parameter_id,
              _from.strftime(settings.CONTROLNEXT_JDBC_DATE_FORMAT),
              to.strftime(settings.CONTROLNEXT_JDBC_DATE_FORMAT)))

        result = self.grower_info.jdbc_source.query(q)

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

    def get_coordinates(self, location_id):
        q = "select x, y from locations where id='%s'" % location_id
        result = self.grower_info.jdbc_source.query(q)
        if not result:
            logger.error("no results for get_coordinates fewsjdbc call "
                         "(location_id: %s)" % location_id)
            return None
        elif len(result) > 1:
            logger.error("too many results for get_coordinates fewsjdbc "
                         "call, only need one (location_id: %s)" %
                         location_id)
        return result[0]
