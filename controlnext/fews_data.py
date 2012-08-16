# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals
import os
import logging
import datetime
import iso8601

from django.conf import settings

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

    def get_current_fill(self, _from, to):
        timeseries = self._get_timeseries(current_fill_filter_id, current_fill_location_id, current_fill_parameter_id, _from, to)
        result = pd.Series(timeseries)
        result = result.asfreq('15Min')
        return result

    def _get_timeseries(self, filter_id, location_id, parameter_id, start_date, end_date):
        '''
        Custom implementation of JdbcSource's get_timeseries().
        '''
        q = ("select time, value from "
             "extimeseries where filterid='%s' and locationid='%s' "
             "and parameterid='%s' and time between '%s' and '%s'" %
             (filter_id, location_id, parameter_id,
              start_date.strftime(JDBC_DATE_FORMAT),
              end_date.strftime(JDBC_DATE_FORMAT)))

        result = self.jdbc_source.query(q)

        #for row in result:
            # Expecting dateTime.iso8601 in a mixed format (basic date +
            # extended time) with time zone indication (Z = UTC),
            # for example: 20110828T00:00:00Z.
            #date_time = row[0]
            #date_time_adjusted = '%s-%s-%s' % (date_time[0:4], date_time[4:6], date_time[6:])
            #row[0] = iso8601.parse_date(date_time_adjusted)

        return result
