# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals
import logging

from lizard_map.coordinates import transform_point

from controlnext.fews_data import FewsJdbcDataSource
from controlnext.models import Basin

logger = logging.getLogger(__name__)


def handle_basins_without_point_info():
    """Check if there are basins without location coordinates. If so,
    retrieve and store them.

    """
    basins = Basin.objects.filter(location__isnull=True)
    for basin in basins:
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
