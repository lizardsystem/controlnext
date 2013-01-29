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


admin.site.register(GrowerInfo, GrowerInfoAdmin)
admin.site.register(Basin)
