# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals
from datetime import datetime
import json
import logging
import random
import string

from django.contrib.gis.db import models as geomodels
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

SRID_WGS84 = 4326
SRID = SRID_WGS84

logger = logging.getLogger(__name__)


def random_slug(length=20):
    # generate a string, which is not already existing in the earlier Promotion instances
    while True:
        slug = ''.join(random.choice(string.ascii_lowercase + string.digits)
                       for _ in range(length))
        try:
            GrowerInfo.objects.get(random_url_slug=slug)
        except:
            return slug


class GrowerInfo(models.Model):
    """Model for holding grower info."""
    # crop type constants
    TOMAAT = 'tomaat'
    CHRYSANT = 'chrysant'
    CROP_CHOICES = (
        (TOMAAT, _("tomaat")),
        (CHRYSANT, _("chrysant")),
    )
    # general info
    name = models.CharField(max_length=100, blank=True, null=True,
                            verbose_name=_("name of the grower"))
    random_url_slug = models.CharField(max_length=20, unique=True,
                                       default=random_slug)
    crop = models.CharField(max_length=100, blank=True, null=True,
                            verbose_name=_("type of crop"),
                            choices=CROP_CHOICES)
    crop_surface = models.IntegerField(
        blank=True, null=True, verbose_name=_("crop surface area (m2)"))
    image = models.ImageField(verbose_name=_("image"), blank=True, null=True,
                              upload_to='grower_images')

    class Meta:
        ordering = ('name',)
        verbose_name = _("grower info")
        verbose_name_plural = _("grower info")

    def __unicode__(self):
        return self.name


def is_valid_crop_type(crop_type):
    """Check whether crop type is valid.

    N.B.: each crop type should also have a <crop_type>.jpg in the static/
        directory!

    """
    crop_types = zip(*GrowerInfo.CROP_CHOICES)[0]
    if crop_type.lower() in crop_types:
        return True
    return False


class Basin(geomodels.Model):
    """Basin specific model.
    """
    grower = models.ForeignKey('GrowerInfo', verbose_name=_("grower"))
    name = models.CharField(max_length=100, blank=True, null=True,
                            verbose_name=_("name of the basin"),
                            help_text=_("must be unique for grower"))
    location = geomodels.PointField(blank=True, null=True, srid=SRID,
                                    verbose_name=_("location"))

    # water level meter params
    filter_id = models.CharField(
        max_length=100, blank=True, null=True,
        help_text=_("e.g. waterstand_basins"), verbose_name = _("filter id"))
    location_id = models.CharField(
        max_length=100, blank=True, null=True, verbose_name=_("location id"))
    parameter_id = models.CharField(max_length=100, blank=True,
                                    null=True)

    recirculation = models.FloatField(default=float(0.0),
                                      help_text=(
                                          "Water recirculation coefficient " +
                                          "from 0.0 to 1.0."),
                                      verbose_name=_("recirculation")
                                      )
    # rain info
    # rain_filter_id = 'neerslag_combo' # Neerslag gecombimeerd
    rain_filter_id = models.CharField(max_length=100, blank=True, null=True,
                                      help_text=_("e.g. neerslag_combo"),
                                      verbose_name=_("rain filter id"))
    # rain_location_id = 'OPP1'  # Oranjebinnenpolder Oost
    rain_location_id = models.CharField(
        max_length=100, blank=True, null=True,
        help_text=_("e.g. OPP1 (i.e. Oranjebinnenpolder Oost)"),
        verbose_name=_("rain location id"))
    # basin parameters
    max_storage = models.IntegerField(
        blank=True, null=True,
        verbose_name=_("maximum storage capacity (m3)"))
    rain_flood_surface = models.IntegerField(
        blank=True, null=True,
        verbose_name=_("rain flood surface (m2)"))
    # max_uitstroom_per_tijdstap_m3 = 4.5 # in m^3
    max_outflow_per_timeunit = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True,
        verbose_name=_("maximum outflow per time unit (m3)"))
    # reverse_osmosis field
    reverse_osmosis = models.IntegerField(
        blank=True, null=True,
        verbose_name=_("reverse osmosis capacity (m3/h)"))
    osmose_till_date = models.DateField(blank=True, null=True,
                                        default=datetime.now,
                                        verbose_name=_(
                                            "reverse osmosis date till")
                                        )
    # current fill data
    # in m^3
    current_fill = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True,
        verbose_name=_("current fill (m3)"))
    current_fill_updated = models.DateTimeField(blank=True, null=True,
                                                verbose_name=_(
                                                    "current fill updated"))
    jdbc_source = models.ForeignKey('lizard_fewsjdbc.JdbcSource', blank=True,
                                    null=True, verbose_name=_("jdbc source"))

    objects = geomodels.GeoManager()

    def get_absolute_url(self):
        return reverse('controlnext-basin', args=[str(self.id)])

    class Meta:
        ordering = ('name',)
        verbose_name = _("basin")
        verbose_name_plural = _("basins")

    def __unicode__(self):
        identifier = self.name if self.name else self.id
        return "%s (%s)" % (self.grower.name, identifier)


class WaterDemand(models.Model):

    daynumber = models.IntegerField(verbose_name=_("day number"))
    weeknumber = models.IntegerField(verbose_name=_("week number"))
    demand = models.FloatField(verbose_name=_("demand"))
    grower = models.ForeignKey(GrowerInfo, verbose_name=_("grower"))

    def __unicode__(self):
        return "Demand for {}.".format(self.grower.name)


class Constants(object):
    """
    Utility class for accessing basin specific constants. Also used to store
    user-defined request parameters for controlnext_demo app. For now,
    user-defined parameters are rain_flood_surface and max_storage.

    """
    def __init__(self, instance=None):
        self.instance = instance

    def __getattr__(self, item):
        if self.instance:
            if isinstance(self.instance, Basin):
                # custom mapping when instance is a basin
                if item.startswith('fill_'):
                    item = item[5:]
            return getattr(self.instance, item)
        raise Exception("should never reach this point")


class UserProfile(models.Model):
    user = models.ForeignKey(User, verbose_name=_("user"))
    grower = models.ManyToManyField(GrowerInfo, verbose_name=_("grower"))

    def __unicode__(self):
        identifier = self.user if self.user else self.id
        return "{} ({})".format(identifier, ', '.join([str(x) for x in
                                                      self.grower.all()]))

    class Meta:
        ordering = ("user",)
        verbose_name = _("user profile")
        verbose_name_plural = _("user profile")
