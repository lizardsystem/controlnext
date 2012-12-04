# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
# from django.utils.translation import ugettext_lazy as _

from controlnext import constants

""" ### from constants.py ###
#    jdbc_source_slug = 'controlnext'  # settings candidate (TODO)

    rain_filter_id = 'neerslag_combo'    # Neerslag gecombimeerd
    rain_location_id = 'OPP1'            # Oranjebinnenpolder Oost
#    rain_parameter_ids = {  # settings candidate
#        'min': 'P.min',   # Minimum
#        'mean': 'P.gem',  # Gemiddeld
#        'max': 'P.max'    # Maximum
#    }

    fill_filter_id = 'waterstand_basins' # Waterstanden
    fill_location_id = '467446797569'    # Van der Lans-west, niveau1
    fill_parameter_id = 'WNS2820'        # Waterdiepte (cm)

#    frequency = datetime.timedelta(minutes=15)  # settings candidate (TODO)

    min_berging_pct = 20
    max_berging_pct = 100
    max_berging_m3 = 15527 # in m^3
    opp_invloed_regen_m2 = 94000 # in m^2
    max_uitstroom_per_tijdstap_m3 = 4.5 # in m^3
    bovenkant_bak_cm = 265 # in cm
    hoogte_niveaumeter_cm = 265 # in cm

#    fill_history = datetime.timedelta(days=31)  # settings candidate (TODO)
#    fill_predict_future = datetime.timedelta(days=5)  # settings candidate (TODO)

#    fewsjdbc_cache_seconds = 15 * 60  # settings candidate (TODO)
"""

class AgriculturistInfo(models.Model):
    """Model for holding agriculturist info."""
    # general info
    name = models.CharField(max_length=100, blank=True, null=True)
    crop = models.CharField(max_length=100, blank=True, null=True)  # TODO: consider making this a separate model

    # fill info
    # fill_filter_id = 'waterstand_basins' # Waterstanden
    fill_filter_id = models.CharField(max_length=100, blank=True, null=True)
    # fill_location_id = '467446797569' # Van der Lans-west, niveau1
    fill_location_id = models.CharField(max_length=100, blank=True, null=True)
    # fill_parameter_id = 'WNS2820' # Waterdiepte (cm)
    fill_parameter_id = models.CharField(max_length=100, blank=True, null=True)

    # rain info
    # rain_filter_id = 'neerslag_combo' # Neerslag gecombimeerd
    rain_filter_id = models.CharField(max_length=100, blank=True, null=True)
    # rain_location_id = 'OPP1'  # Oranjebinnenpolder Oost
    rain_location_id = models.CharField(max_length=100, blank=True, null=True)

    # basin info (translated legacy constants from constants.py)
    max_storage = models.IntegerField(blank=True, null=True)   # orig: max_berging_m3 = 15527 # in m^3
    min_storage_pct = models.IntegerField(blank=True, null=True)  # orig: min_berging_pct = 20
    max_storage_pct = models.IntegerField(blank=True, null=True)  # orig: max_berging_pct = 100
    rain_flood_surface = models.IntegerField(blank=True, null=True)  # orig: opp_invloed_regen_m2 = 94000 # in m^2
    # max_uitstroom_per_tijdstap_m3 = 4.5 # in m^3
    max_outflow_per_timeunit = models.IntegerField(blank=True, null=True)
    basin_top = models.IntegerField(blank=True, null=True)  # orig: bovenkant_bak_cm = 265 # in cm
    level_indicator_height = models.IntegerField(blank=True, null=True)  # orig: hoogte_niveaumeter_cm = 265 # in cm

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class Constants(object):
    """Utility class for accessing agriculturist specific constants with consideration of legacy defaults.

    """
    LEGACY_ATTRS = {
        # legacy map
        'max_berging_m3': 'max_storage',
        'min_berging_pct': 'min_storage_pct',
        'max_berging_pct': 'max_storage_pct',
        'opp_invloed_regen_m2': 'rain_flood_surface',
        'max_uitstroom_per_tijdstap_m3': 'max_outflow_per_timeunit',
        'bovenkant_bak_cm': 'basin_top',
        'hoogte_niveaumeter_cm': 'level_indicator_height',
    }

    def __init__(self, id):
        try:
            self.info = AgriculturistInfo.objects.get(id=id)
        except ObjectDoesNotExist:
            self.info = None

    def __getattr__(self, item):
        if self.info:
            try:
                if item in LEGACY_ATTRS:
                    return getattr(self.info, LEGACY_ATTRS[item])
                else:
                    return getattr(self.info, item)
            except AttributeError:
                pass
        return getattr(constants, item)
