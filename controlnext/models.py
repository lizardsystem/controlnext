# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals
import logging

from django.db import models
from django.contrib.gis.db import models as geomodels
from django.utils.translation import ugettext_lazy as _

from controlnext import constants as legacy_constants

SRID_WGS84 = 4326
SRID = SRID_WGS84

logger = logging.getLogger(__name__)


class GrowerInfo(models.Model):
    """Model for holding grower info."""
    # general info
    name = models.CharField(max_length=100, blank=True, null=True,
                            verbose_name=_("name of the grower"))
    # TODO: consider making crop a separate model
    crop = models.CharField(max_length=100, blank=True, null=True,
                            verbose_name=_("type of crop"))
    location = geomodels.PointField(blank=True, null=True, srid=SRID)
    # fill info
    # fill_filter_id = 'waterstand_basins' # Waterstanden
    fill_filter_id = models.CharField(
        max_length=100, blank=True, null=True,
        help_text=_("e.g. waterstand_basins"))
    # fill_location_id = '467446797569' # Van der Lans-west, niveau1
    fill_location_id = models.CharField(max_length=100, blank=True, null=True)
    # fill_parameter_id = 'WNS2820' # Waterdiepte (cm)
    fill_parameter_id = models.CharField(max_length=100, blank=True,
                                         null=True)
    # rain info
    # rain_filter_id = 'neerslag_combo' # Neerslag gecombimeerd
    rain_filter_id = models.CharField(max_length=100, blank=True, null=True,
                                      help_text=_("e.g. neerslag_combo"))
    # rain_location_id = 'OPP1'  # Oranjebinnenpolder Oost
    rain_location_id = models.CharField(
        max_length=100, blank=True, null=True,
        help_text=_("e.g. OPP1 (i.e. Oranjebinnenpolder Oost)"))
    # basin info (translated legacy constants from constants.py)
    # orig: max_berging_m3 = 15527 # in m^3
    max_storage = models.IntegerField(
        blank=True, null=True,
        verbose_name=_("maximum storage capacity (m3)"))
    # orig: min_berging_pct = 20
    min_storage_pct = models.IntegerField(
        blank=True, null=True,
        verbose_name=_("minimum storage capacity (%)"))
    # orig: max_berging_pct = 100
    max_storage_pct = models.IntegerField(
        blank=True, null=True,
        verbose_name=_("maximum storage capacity (%)"))
    # orig: opp_invloed_regen_m2 = 94000 # in m^2
    rain_flood_surface = models.IntegerField(
        blank=True, null=True,
        verbose_name=_("rain flood surface (m2)"))
    # max_uitstroom_per_tijdstap_m3 = 4.5 # in m^3
    max_outflow_per_timeunit = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True,
        verbose_name=_("maximum outflow per time unit (m3)"))
    # orig: bovenkant_bak_cm = 265 # in cm
    basin_top = models.IntegerField(
        blank=True, null=True, verbose_name=_("top of basin (cm)"))
    # orig: hoogte_niveaumeter_cm = 265 # in cm
    level_indicator_height = models.IntegerField(
        blank=True, null=True,
        verbose_name=_("height of level indicator (cm)"))

    jdbc_source = models.ForeignKey('lizard_fewsjdbc.JdbcSource', blank=True,
                                    null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _("grower info")
        verbose_name_plural = _("grower info")

    def __unicode__(self):
        return self.name


class Basin(geomodels.Model):
    """Basin specific model.

    TODO: remove basin specific fields from GrowerInfo
    """
    owner = models.ForeignKey(GrowerInfo)
    name = models.CharField(max_length=100, blank=True, null=True,
        verbose_name=_("name of the basin"), help_text=_("must be unique for"
        "grower"))
    location = geomodels.PointField(blank=True, null=True, srid=SRID)
    filter_id = models.CharField(
        max_length=100, blank=True, null=True,
        help_text=_("e.g. waterstand_basins"))
    location_id = models.CharField(
        max_length=100, blank=True, null=True,
        help_text=_("e.g. OPP1 (i.e. Oranjebinnenpolder Oost)"))
    parameter_id = models.CharField(max_length=100, blank=True,
        null=True)
    # rain info
    # rain_filter_id = 'neerslag_combo' # Neerslag gecombimeerd
    rain_filter_id = models.CharField(max_length=100, blank=True, null=True,
        help_text=_("e.g. neerslag_combo"))
    # rain_location_id = 'OPP1'  # Oranjebinnenpolder Oost
    rain_location_id = models.CharField(
        max_length=100, blank=True, null=True,
        help_text=_("e.g. OPP1 (i.e. Oranjebinnenpolder Oost)"))

    # basin parameters
    max_storage = models.IntegerField(
        blank=True, null=True,
        verbose_name=_("maximum storage capacity (m3)"))
    # orig: min_berging_pct = 20
    min_storage_pct = models.IntegerField(
        blank=True, null=True,
        verbose_name=_("minimum storage capacity (%)"))
    # orig: max_berging_pct = 100
    max_storage_pct = models.IntegerField(
        blank=True, null=True,
        verbose_name=_("maximum storage capacity (%)"))
    # orig: opp_invloed_regen_m2 = 94000 # in m^2
    rain_flood_surface = models.IntegerField(
        blank=True, null=True,
        verbose_name=_("rain flood surface (m2)"))
    # max_uitstroom_per_tijdstap_m3 = 4.5 # in m^3
    max_outflow_per_timeunit = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True,
        verbose_name=_("maximum outflow per time unit (m3)"))
    # orig: bovenkant_bak_cm = 265 # in cm
    basin_top = models.IntegerField(
        blank=True, null=True, verbose_name=_("top of basin (cm)"))
    # orig: hoogte_niveaumeter_cm = 265 # in cm
    level_indicator_height = models.IntegerField(
        blank=True, null=True,
        verbose_name=_("height of level indicator (cm)"))
    # current fill data
    # in m^3
    current_fill = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True,
        verbose_name=_("current fill (m3)"))
    current_fill_updated = models.DateTimeField(blank=True, null=True)

    jdbc_source = models.ForeignKey('lizard_fewsjdbc.JdbcSource', blank=True,
        null=True)

    # if true, icon is shown on main dashboard map
    on_main_map = models.BooleanField(default=False)

    objects = geomodels.GeoManager()

    def google_coordinates(self):
        return transform_point(self.location.x, self.location.y,
                               from_proj='wgs84', to_proj='google')

    class Meta:
        ordering = ('name',)
        verbose_name = _("basin")
        verbose_name_plural = _("basins")

    def __unicode__(self):
        identifier = self.name if self.name else self.id
        return "%s (%s)" % (self.owner.name, identifier)

    def identifier(self):
        return {
            'basin': self.pk,
            'type': 'basin',
        }

    def metadata_identifier(self):
        return {
            'basin': self.pk,
            'type': 'metadata',
        }

    def metadata_identifier_json(self):
        return json.dumps(self.metadata_identifier())

    def name_metadata(self):
        return "%s - metadata" % unicode(self)


class Constants(object):
    """Utility class for accessing grower specific constants taken legacy
    defaults into consideration.

    """
    LEGACY_ATTRS = {
        # legacy key mapper
        'max_berging_m3': 'max_storage',
        'min_berging_pct': 'min_storage_pct',
        'max_berging_pct': 'max_storage_pct',
        'opp_invloed_regen_m2': 'rain_flood_surface',
        'max_uitstroom_per_tijdstap_m3': 'max_outflow_per_timeunit',
        'bovenkant_bak_cm': 'basin_top',
        'hoogte_niveaumeter_cm': 'level_indicator_height',
    }

    def __init__(self, grower_info):
        self.info = grower_info

    def __getattr__(self, item):
        if self.info:
            try:
                if item in self.LEGACY_ATTRS:
                    return getattr(self.info, self.LEGACY_ATTRS[item])
                else:
                    return getattr(self.info, item)
            except AttributeError:
                pass
        return getattr(legacy_constants, item)
