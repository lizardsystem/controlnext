# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals
import logging
import datetime

import iso8601
import pytz
import pandas as pd

from lizard_fewsjdbc.models import JdbcSource

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
    def __init__(self, basin, constants=None):
        self.basin = basin
        if constants:
            self.constants = constants
        else:
            self.constants = Constants(basin)

        if self.basin.jdbc_source:
            self.jdbc_source = self.basin.jdbc_source
        elif self.basin.owner.jdbc_source:
            self.jdbc_source = self.basin.owner.jdbc_source
        else:
            try:
                self.jdbc_source = JdbcSource.objects.get(
                    slug=settings.CONTROLNEXT_JDBC_SOURCE_SLUG)
            except JdbcSource.DoesNotExist:
                raise Exception("Jdbc source %s does not exist." %
                                settings.CONTROLNEXT_JDBC_SOURCE_SLUG)

#    @cache_result(settings.CONTROLNEXT_FEWSJDBC_CACHE_SECONDS,
#                  ignore_cache=False, instancemethod=True)
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
        rain /= 4
        # deal with NaN values
        #if np.nan in rain:
        #    raise Exception('Found NaN in results')
        #rain = rain.fillna(0)
        return rain

#    @cache_result(settings.CONTROLNEXT_FEWSJDBC_CACHE_SECONDS,
#                  ignore_cache=False, instancemethod=True)
    def get_fill(self, _from, to, *args, **kwargs):
        validate_date(_from)
        validate_date(to)

        # basin parameters
        fill_filter_id = self.basin.filter_id
        fill_location_id = self.basin.location_id
        fill_parameter_id = self.basin.parameter_id
        level_indicator_height = self.basin.level_indicator_height
        basin_top = self.basin.basin_top
        # max_storage can come from request, therefore from self.constants
        max_storage = self.constants.max_storage

        # waarden zijn in cm onder overstortbuis
        ts = self._get_timeseries_as_pd_series(
            fill_filter_id,
            fill_location_id,
            fill_parameter_id,
            _from, to, 'fill'
        )

        # deal with NaN values
        #if np.NaN in ts:
        #    raise Exception('Found NaN in results')
        #ts = ts.fillna(0)

        # zet om in cm vanaf bodem bak
        ts += level_indicator_height
        # zet om naar fractie totale bak
        ts /= basin_top
        # zet om naar m3
        ts *= max_storage

        return ts

    def get_fill_from_own_meter(self, _from, to, *args, **kwargs):
        """
        Get basin fill values based on grower's own meter parameters.

        :param _from: start date and time
        :param to: end date and time
        :param args: can be for specific caching with cache_result decorator
        :param kwargs: idem as args
        :return: timeseries instance with time (15 minute frequency) and fill
            value (cubic meters) rows ranging from _from to to

        Example query (Van Der Lans):
        "select time, value from extimeseries where filterid='meetpunt' and
         locationid='VP9508:SILO 1' and parameterid='priva.vullingsgraad' and
         time between '2013-01-01 09:00:00' and '2013-01-29 09:00:00'"

        """
        validate_date(_from)
        validate_date(to)

        # basin parameters
        fill_filter_id = self.basin.own_meter_filter_id
        fill_location_id = self.basin.own_meter_location_id
        fill_parameter_id = self.basin.own_meter_parameter_id
        # max_storage could come from request, therefore use self.constants
        max_storage = self.constants.max_storage

        # waarden zijn in cm onder overstortbuis
        ts = self._get_timeseries_as_pd_series(
            fill_filter_id,
            fill_location_id,
            fill_parameter_id,
            _from, to, 'fill'
        )

        # values are percentages (0-100)
        ts /= 100
        # convert to m3
        ts *= max_storage

        # data is in 5 minute intervals, so we need to resample to 15 minutes
        ts = ts.resample('15Min')

        return ts

    def get_discharge_valve_data(self, _from, history_timedelta=None,
                                 *args, **kwargs):
        """
        Get discharge valve data.

        :param _from: start date and time
        :param args: can be for specific caching with cache_result decorator
        :param kwargs: idem as args
        :return: timeseries instance with time (15 minute frequency) and
            discharge (cubic meters) data

        Example query (Van Der Lans):
        "select time, value from extimeseries where filterid='meetpunt' and
         locationid='VP9508:PROG 6' and parameterid='klep.debiet' and time
         between '2013-01-01 09:00:00' and '2013-02-28 09:00:00'"

        """
        if not history_timedelta:
            history_timedelta = settings.CONTROLNEXT_FILL_HISTORY

        validate_date(_from)

        # basin parameters
        filter_id = self.basin.discharge_valve_filter_id
        location_id = self.basin.discharge_valve_location_id
        parameter_id = self.basin.discharge_valve_parameter_id

        # waarden zijn in cm onder overstortbuis
        ts = self._get_timeseries_as_pd_series(
            filter_id,
            location_id,
            parameter_id,
            _from - history_timedelta, _from, 'uitstroom'
        )

        # data is in 5 minute intervals, so we need to resample to 15 minutes
        ts = ts.resample('15Min')
        # values are m3 / hour
        ts /= 4  # correct for 15 min (from m3/hour to m3/15 min)
        ts = -ts  # display values as negatives

        return ts

    def get_greenhouse_valve_data(self, _from, history_timedelta=None,
                                  valve_nr=1, *args, **kwargs):
        """
        Get greenhouse discharge valve data.

        :param _from: start date and time
        :param args: can be for specific caching with cache_result decorator
        :param kwargs: idem as args
        :return: timeseries instance with time (15 minute frequency) and
            discharge (cubic meters) data

        Example query (Van Der Lans):
        "select time, value from extimeseries where filterid='meetpunt'
         and locationid='VP9508:HYDRO PULSM 2' and
         parameterid='priva.kasdebiet' and time between '2013-01-01 09:00:00'
         and '2013-01-31 09:00:00'"

        """
        if not history_timedelta:
            history_timedelta = settings.CONTROLNEXT_FILL_HISTORY

        validate_date(_from)

        # basin parameters
        filter_field = 'greenhouse_valve_%s_filter_id' % valve_nr
        filter_id = getattr(self.basin, filter_field)
        location_field = 'greenhouse_valve_%s_location_id' % valve_nr
        location_id = getattr(self.basin, location_field)
        parameter_field = 'greenhouse_valve_%s_parameter_id' % valve_nr
        parameter_id = getattr(self.basin, parameter_field)

        # waarden zijn in cm onder overstortbuis
        ts = self._get_timeseries_as_pd_series(
            filter_id,
            location_id,
            parameter_id,
            _from - history_timedelta, _from, 'greenhouse_discharge'
        )

        # data is in 5 minute intervals, so we need to resample to 15 minutes
        ts = ts.resample('15Min')
        # values are m3 / hour
        ts /= 4  # correct for 15 min (from m3/hour to m3/15 min)
        ts = -ts  # display values as negatives

        return ts

#    @cache_result(settings.CONTROLNEXT_FEWSJDBC_CACHE_SECONDS,
#                  ignore_cache=False, instancemethod=True)
    def get_current_fill(self, _from, history_timedelta=None, own_meter=False,
                         **kwargs):
        '''
        returns latest available fill AND its series
        '''
        # optional parameter
        if not history_timedelta:
            history_timedelta = settings.CONTROLNEXT_FILL_HISTORY

        if own_meter and self.basin.has_own_meter:
            fill_history_m3 = self.get_fill_from_own_meter(
                _from - history_timedelta, _from, **kwargs)
        else:
            fill_history_m3 = self.get_fill(
                _from - history_timedelta, _from, **kwargs)

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

        result = self.jdbc_source.query(q)

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
        """Retrieve coordinates by location_id.

        JDBC query is expected to return a list with one row of x and y values
        in rd format, something like [[ 74352.0, 440129.0 ]].

        """
        q = "select x, y from locations where id='%s'" % location_id
        result = self.jdbc_source.query(q)
        if not result:
            logger.error("no results for get_coordinates fewsjdbc call "
                         "(location_id: %s)" % location_id)
            return None
        elif len(result) > 1:
            logger.error("too many results for get_coordinates fewsjdbc "
                         "call, only need one (location_id: %s)" %
                         location_id)
        return result[0]
