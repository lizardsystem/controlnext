# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.gis.admin import GeoModelAdmin
from django.utils.translation import ugettext_lazy as _

from controlnext.models import GrowerInfo


class GrowerInfoAdmin(GeoModelAdmin):
    """GrowlerInfo admin layout."""
    default_lat = 51.97477
    default_lon = 4.15146
    default_zoom = 10

    fieldsets = (
        (None, {
            'classes': ['wide'],
            'fields': ('name', 'crop', 'rain_location_id', 'rain_filter_id',
            'fill_location_id', 'fill_filter_id', 'fill_parameter_id')
        }),
        (_('basin parameters'), {
            'classes': ['wide'],
            'fields': ('min_storage_pct', 'max_storage_pct', 'max_storage',
            'rain_flood_surface', 'max_outflow_per_timeunit', 'basin_top',
            'level_indicator_height')
        }),
        (_("location"), {
            'classes': ['collapse'],
            'fields': ('location',)
        }),
    )

admin.site.register(GrowerInfo, GrowerInfoAdmin)
