# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals
import datetime
from decimal import Decimal
import logging

import pytz

from django.db.backends.util import format_number

from lizard_map.coordinates import transform_point

from controlnext.fews_data import FewsJdbcDataSource
from controlnext.utils import round_date

logger = logging.getLogger(__name__)


def update_basin_coordinates(basin):
    """Get and store coordinates for basin by its location id.

    PM: better put this kind of code in a manager?
    """
    if basin.location_id:
        location_id = basin.location_id
    else:
        # TODO: move location_id to basin
        location_id = basin.owner.fill_location_id
    if location_id:
        logger.debug("about to retrieve coordinates for location "
                     "with id = %s" % location_id)
        ds = FewsJdbcDataSource(basin.owner)
        coordinates = ds.get_coordinates(location_id)
        point = transform_point(coordinates[0], coordinates[1], 'rd',
                                'wgs84')
        basin.location = point
        basin.save()
    else:
        logger.error('basin %s does not have a required location id' %
                     basin.id)


def update_current_fill(basin):
    """Update basin's current_fill field. Only update if changed."""
    ds = FewsJdbcDataSource(basin.owner)
    now = datetime.datetime.now(tz=pytz.utc)
    to = round_date(now)
    history_timedelta = datetime.timedelta(days=1)
    unique_cache_key = "%s:%s" % (unicode(basin), basin.id)
    current_fill = ds.get_current_fill(to, history_timedelta,
                                       cache_key=unique_cache_key)
    current_fill_m3 = current_fill['current_fill_m3']
    # need to format to Decimal with same decimal places as basin.current_fill
    current_formatted = Decimal(format_number(current_fill_m3, 10, 2))
    if not basin.current_fill == current_formatted:
        basin.current_fill = current_fill_m3
        basin.current_fill_updated = now
        basin.save()
        return current_formatted
