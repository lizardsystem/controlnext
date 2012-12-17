import os
import logging

import mapnik
import pyproj

from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D

from lizard_map.coordinates import WGS84, wgs84_to_google, google_to_wgs84
from lizard_map.models import ICON_ORIGINALS
from lizard_map.workspace import WorkspaceItemAdapter
from lizard_map.symbol_manager import SymbolManager

from controlnext.calc_model import fill_m3_to_pct
from controlnext.conf import settings
from controlnext.models import GrowerInfo, Basin

logger = logging.getLogger(__name__)

GENERATED_ICONS = os.path.join(settings.MEDIA_ROOT, 'generated_icons')
SYMBOL_MANAGER = SymbolManager(ICON_ORIGINALS, GENERATED_ICONS)
BASIN_ICON = 'point_3.png'
BASIN_FILL_COLOR_MAP = {
     0: '00CC00',
     5: '00CC00',
    10: '00CC00',
    15: '00CC00',
    20: '00CC00',
    25: '00CC00',
    30: '00CC00',
    35: '00CC00',
    40: '00CC00',
    45: '00CC00',
    50: '00CC00',
    55: '00CC00',
    60: '00CC00',
    65: '00CC00',
    70: '00CC00',
    75: '00CC00',
    80: '00CC00',
    85: 'FF0000',
    90: 'FF0000',
    95: 'FF0000',
    100: 'FF0000'
}


class BasinsAdapter(WorkspaceItemAdapter):

    def __init__(self, *args, **kwargs):
        super(BasinsAdapter, self).__init__(*args, **kwargs)
        self.growers = GrowerInfo.objects.all()

    def layer(self, layer_ids=None, request=None):
        layers = []
        styles = {}

        dbname = 'default'
        database = settings.DATABASES[dbname]

        for grower in self.growers:
            for basin in grower.basin_set.all():
                basin_style = mapnik.Style()
                # check if there is a value for basin
                # else show a question mark icon

                style_name = 'basin style %s' % str(basin)
                styles[style_name] = basin_style

                rule = mapnik.Rule()
                icon = self.icon_filename(basin, grower.max_storage)

                query = """(SELECT location
                    FROM controlnext_basin
                    WHERE id=%d)
                    data""" % (basin.id,)

                datasource = mapnik.PostGIS(
                    host=database['HOST'],
                    port=database['PORT'],
                    user=database['USER'],
                    password=database['PASSWORD'],
                    dbname=database['NAME'],
                    table=query.encode('ascii')
                )

                layer = mapnik.Layer(
                    "Basin %s" % str(basin.name or 'None'), WGS84)
                layer.datasource = datasource
                layer.styles.append(style_name)
                layers.append(layer)

        return layers, styles


    def search(self, x, y, radius=None):
        """
        """
        pt = Point(google_to_wgs84(x, y), 4326)

        # Looking at how radius is derived in lizard_map.js, it's best applied
        # to the y-coordinate to get a reasonable search distance in meters.

        lon1, lat1 = google_to_wgs84(x, y - radius)
        lon2, lat2 = google_to_wgs84(x, y + radius)
        geod = pyproj.Geod(ellps='WGS84')
        forward, backward, distance = geod.inv(lon1, lat1, lon2, lat2)
        distance /= 2.0

        results = []

        # Find all basin owned within the search
        # distance. Order them by distance.
        for basin in Basin.objects.filter(
            location__distance_lte=(pt, D(m=distance))).distance(pt).\
            order_by('distance'):
#        for basin in Basin.objects.all():

            # For each well, we actually find three items:
            # - A picture of the existing regis layers and filters
            # - A table of meta information
            # - If available, historical discharge data in a graph
            #
            # This way, the three types of data show in separate popups,
            # can be added to the collage separately, etc.
            #
            # They also need different names, so they look different
            # in the collage.

            result = {
                'grouping_hint': 'controlnext basin %d' % (self.workspace_item.id),
                'distance': basin.distance,
                'name': unicode(basin),
                'workspace_item': self.workspace_item,
                'identifier': basin.identifier(),
                }
            results.append(result)
            #            result = {
            #                'grouping_hint': 'gmdb well fraction %d' % (
            #                    self.workspace_item.id),
            #                'distance': well.distance,
            #                'name': well.name_fraction(),
            #                'workspace_item': self.workspace_item,
            #                'identifier': well.fraction_identifier(),
            #                }
            #            results.append(result)
#            result = {
#                'grouping_hint': ('gmdb well metadata %d' %
#                                  (self.workspace_item.id)),
#                'distance': well.distance,
#                'name': well.name_metadata(),
#                'workspace_item': self.workspace_item,
#                'identifier': well.metadata_identifier(),
#                }
#            results.append(result)
#            if well.has_discharge_data():
#                result = {
#                    'grouping_hint': ('gmdb well discharge graph %d' %
#                                      (self.workspace_item.id,)),
#                    'distance': well.distance,
#                    'name': well.name_discharge(),
#                    'workspace_item': self.workspace_item,
#                    'identifier': well.discharge_identifier(),
#                    }
#                results.append(result)
#            break

        return results


    def icon_filename(self, basin, max_storage):
        fill_percentage = fill_m3_to_pct(basin.current_fill, max_storage)
        icon_percentage = self.round_percentage_for_icon(fill_percentage)
        color_as_hex = self.color_by_percentage(icon_percentage)
        color_as_float = self.float_color(color_as_hex)
        return SYMBOL_MANAGER.get_symbol_transformed(
            BASIN_ICON, color=color_as_float)


    def color_by_percentage(self, percentage):
        return BASIN_FILL_COLOR_MAP[int(percentage)]


    def float_color(self, color):
        """Return the color as a float 4-tuple as used by
        SymbolManager."""

        if not color:
            return (1.0, 1.0, 1.0, 1.0)

        r, g, b = color[0:2], color[2:4], color[4:6]
        rr, gg, bb = int(r, 16), int(g, 16), int(b, 16)
        return (rr / 255.0, gg / 255.0, bb / 255.0, 1.0)


    def round_percentage_for_icon(self, dividend, divisor=5):
        """Round percentage by divisor. Used for minimizing number of icons.

        Examples (dividend(s) left, return value right, default divisor):
        0,1,2,3,4 ->   0
        5,6,7,8,9 ->  10
        99        ->  95
        100       -> 100

        """
        remainder = dividend % divisor
        return dividend - remainder
