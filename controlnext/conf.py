# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals
import datetime

# django.conf.settings need to be imported here, because when importing this
# module, you also get the django.conf.settings
from django.conf import settings  # noqa

from appconf import AppConf


class ControlNEXTConf(AppConf):
    """Configurable app settings."""
    JDBC_SOURCE_SLUG = "controlnext"  # used for demo
    JDBC_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    FILL_HISTORY = datetime.timedelta(days=56)
    FILL_PREDICT_FUTURE = datetime.timedelta(days=28)

    class Meta:
        prefix = 'controlnext'
