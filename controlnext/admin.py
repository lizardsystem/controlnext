# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.gis.admin import GeoModelAdmin
from django.utils.translation import ugettext_lazy as _

from controlnext.models import Basin
from controlnext.models import GrowerInfo
from controlnext.models import UserProfile
from controlnext.models import WaterDemand


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
            'fields': ('name', 'image', 'crop', 'crop_surface')
        }),
    )
    inlines = [BasinInline, ]


class BasinAdmin(GeoModelAdmin):
    fieldsets = (
        (None, {
            'classes': ['wide'],
            'fields': (
                'grower', 'name', 'filter_id', 'location_id', 'parameter_id',
                'recirculation',
                # rain parameters
                'rain_filter_id', 'rain_location_id',
                # other basin parameters
                'max_storage', 'current_fill', 'current_fill_updated',
                'rain_flood_surface', 'max_outflow_per_timeunit',
                'reverse_osmosis',
                'osmose_till_date', 'jdbc_source'
            )
        }),
        (_("location"), {
            'classes': ['collapse'],
            'fields': ('location',)
        }),
    )

class UserProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'classes': ['wide'],
            'fields': (
                'grower', 'user'
            )
        }),
    )


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(GrowerInfo, GrowerInfoAdmin)
admin.site.register(Basin, BasinAdmin)
admin.site.register(WaterDemand)
