# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.gis.admin import GeoModelAdmin
from django.utils.translation import ugettext_lazy as _

from controlnext.models import GrowerInfo, Basin


class BasinInline(admin.TabularInline):
    model = Basin
    extra = 1


class GrowerInfoAdmin(GeoModelAdmin):
    """GrowlerInfo admin layout."""
    default_lat = 51.97477
    default_lon = 4.15146
    default_zoom = 10

    fieldsets = (
        (None, {
            'classes': ['wide'],
            'fields': ('name', 'image', 'crop', 'crop_surface', 'jdbc_source')
        }),
        (_("location"), {
            'classes': ['collapse'],
            'fields': ('location',)
        }),
    )
    inlines = [BasinInline, ]


class BasinAdmin(GeoModelAdmin):
    fieldsets = (
        (None, {
            'classes': ['wide'],
            'fields': (
                'owner', 'name', 'filter_id', 'location_id', 'parameter_id',
                'own_meter_filter_id', 'own_meter_location_id',
                'own_meter_parameter_id',
                'recirculation',
                # discharge valve parameters
                'discharge_valve_filter_id',
                'discharge_valve_location_id',
                'discharge_valve_parameter_id',
                # greenhouse valve parameters
                'greenhouse_valve_1_filter_id',
                'greenhouse_valve_1_location_id',
                'greenhouse_valve_1_parameter_id',
                'greenhouse_valve_2_filter_id',
                'greenhouse_valve_2_location_id',
                'greenhouse_valve_2_parameter_id',
                # rain parameters
                'rain_filter_id', 'rain_location_id',
                'predicted_5d_rain_filter_id',
                'predicted_5d_rain_parameter_id',
                'real_5d_rain_filter_id', 'real_5d_rain_parameter_id',
                # other basin parameters
                'max_storage', 'min_storage_pct', 'max_storage_pct',
                'rain_flood_surface', 'max_outflow_per_timeunit', 'basin_top',
                'level_indicator_height', 'reverse_osmosis', 'osmose_till_date', 'jdbc_source',
                'on_main_map'
            )
        }),
        (_("location"), {
            'classes': ['collapse'],
            'fields': ('location',)
        }),
    )


admin.site.register(GrowerInfo, GrowerInfoAdmin)
admin.site.register(Basin, BasinAdmin)
