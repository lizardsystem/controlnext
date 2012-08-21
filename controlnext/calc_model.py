# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals
from __future__ import division
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

    def calc_afstroom(self, t0, desired_fill_scalar):
        ts = pd.Series()
        
    def calc_scenario(self, desired_fill_m3, current_fill_m3, demand_m3, rain):
        expected_water = rain * (area_receiving_rain_m2 / 1000)
        # expected_water is now in m^3
        expected_water_summed = expected_water.cumsum()
        
        import pdb; pdb.set_trace()

    def predict_overflow(self, _from, to, desired_fill_pct, demand_diff_pct):
        # do some input validation here, to ensure we are dealing with sane numbers
        if 0 > desired_fill_pct > 100:
            raise ValueError('value should be a percentage between 0 and 100')
        if 0 > demand_diff_pct:
            raise ValueError('value should be a percentage > 0')

        demand_m3 = self.demand_table.get_demand(_from, to)
        current_fill_cm = self.fews_data.get_fill(_from, _from)[0]
        rain_min = self.fews_data.get_rain('min', _from, to)
        rain_mean = self.fews_data.get_rain('mean', _from, to)
        rain_max = self.fews_data.get_rain('max', _from, to)

        # adjust for extra demand
        demand_diff = (demand_diff_pct / 100)
        demand_m3 = demand_m3 * demand_diff

        desired_fill_scalar = desired_fill_pct / 100

        for rain in [rain_min, rain_mean, rain_max]:
            result = self.calc_scenario(-1, -1, demand_m3, rain)

