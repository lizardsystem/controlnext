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
     0: '00FFAA',
     5: '00FF88',
    10: '00FF66',
    15: '00FF44',
    20: '00FF22',
    25: '00FF00',
    30: '22FF00',
    35: '44FF00',
    40: '66FF00',
    45: '88FF00',
    50: 'AAFF00',
    55: 'CCFF00',
    60: 'EEFF00',
    65: 'FFEE00',
    70: 'FFCC00',
    75: 'FFAA00',
    80: 'FF8800',
    85: 'FF6600',
    90: 'FF4400',
    95: 'FF2200',
    100: 'FF0000'
}  # rounded percentage based colors derived with http://www.colorpicker.com/


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

                style_name = 'basin style %s' % str(basin)
                styles[style_name] = basin_style

                rule = mapnik.Rule()
                icon = self.icon_filename(basin, grower.max_storage)

                symbol = mapnik.PointSymbolizer(
                    os.path.join(GENERATED_ICONS, icon),
                    "png", 16, 16)

                symbol.allow_overlap = True
                rule.symbols.append(symbol)
                basin_style.rules.append(rule)

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
        pt = Point(google_to_wgs84(x, y), 4326)
        # Looking at how radius is derived in lizard_map.js, it's best applied
        # to the y-coordinate to get a reasonable search distance in meters.
        lon1, lat1 = google_to_wgs84(x, y - radius)
        lon2, lat2 = google_to_wgs84(x, y + radius)
        geod = pyproj.Geod(ellps='WGS84')
        forward, backward, distance = geod.inv(lon1, lat1, lon2, lat2)
        # distance /= 2.0
        distance = 1000000.0  # hack for previous statement, because
        # otherwise no basins are returned; TODO: figure this out
        results = []
        # Find all basins within the search distance. Order them by distance.
        for basin in Basin.objects.filter(
            location__distance_lte=(pt, D(m=distance))).\
            distance(pt).order_by('distance'):

            fill_percentage = fill_m3_to_pct(basin.current_fill,
                basin.owner.max_storage)
            result = {
                'grouping_hint': 'controlnext basin %d' % (
                    self.workspace_item.id),
                'distance': basin.distance,
                'name': "%s (%d%% vol)" % (unicode(basin), fill_percentage),
                'workspace_item': self.workspace_item,
                'identifier': basin.identifier(),
            }
            results.append(result)
        return results


    def icon_filename(self, basin, max_storage):
        """Icon file based on basin fill percentage."""
        fill_percentage = fill_m3_to_pct(basin.current_fill, max_storage)
        icon_percentage = self.round_percentage_for_icon(fill_percentage)
        color_as_hex = self.color_by_percentage(icon_percentage)
        color_as_float = self.float_color(color_as_hex)
        symbol = SYMBOL_MANAGER.get_symbol_transformed(
            BASIN_ICON, color=color_as_float)
        return symbol


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


    def round_percentage_for_icon(self, percentage, divisor=5):
        """Round percentage by divisor. Used for minimizing number of icons.

        Examples (dividend(s) left, return value right, default divisor):
        0,1,2,3,4 ->   0
        5,6,7,8,9 ->  10
        99        ->  95
        100       -> 100

        """
        if percentage > 100:
            return 100
        if percentage < 0:
            return 0
        remainder = percentage % divisor
        return percentage - remainder
