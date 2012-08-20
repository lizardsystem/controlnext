# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals
import os
import logging
import datetime

from django.conf import settings

import pytz
import pandas as pd
import numpy as np

from controlnext.constants import *

# optionally import matplotlib which can be used to debugging
try:
    import matplotlib.pyplot as plt
except ImportError:
    pass

logger = logging.getLogger(__name__)

class CalculationModel(object):
    def __init__(self, demand_table, fews_data):
        self.demand_table = demand_table
        self.fews_data = fews_data
