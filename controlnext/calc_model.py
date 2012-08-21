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

    def predict_overflow(self, _from, to, desired_fill, demand_diff):
        demand = self.demand_table.get_demand(_from, to)
        current_fill = self.fews_data.get_fill(_from, to)
        rain_min = self.fews_data.get_rain('min', _from, to)
        rain_mean = self.fews_data.get_rain('mean', _from, to)
        rain_max = self.fews_data.get_rain('max', _from, to)
        import pdb; pdb.set_trace()
