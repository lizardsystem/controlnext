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

def cross(series, cross=0, direction='cross'):
    """
    Given a Series returns all the index values where the data values equal
    the 'cross' value.

    Direction can be 'rising' (for rising edge), 'falling' (for only falling
    edge), or 'cross' for both edges.
    """
    # Find if values are above or bellow yvalue crossing:
    above = series.values > cross
    below = np.logical_not(above)
    left_shifted_above = above[1:]
    left_shifted_below = below[1:]
    # Find indexes on left side of crossing point
    if direction == 'rising':
        idxs = (left_shifted_above & below[0:-1]).nonzero()[0]
    elif direction == 'falling':
        idxs = (left_shifted_below & above[0:-1]).nonzero()[0]
    else:
        rising = left_shifted_above & below[0:-1]
        falling = left_shifted_below & above[0:-1]
        idxs = (rising | falling).nonzero()[0]

    # Return crossings, if any
    result = series.index[idxs]
    return result

def m3_to_pct(ts):
    ts /= max_berging_m3
    ts *= 100
    return ts

class CalculationModel(object):
    def __init__(self, demand_table, fews_data):
        self.demand_table = demand_table
        self.fews_data = fews_data

    def calc_max_uitstroom(self, _from, periods):
        # tel ook eerste en laatste periode mee
        periods += 2
        totale_uitstroom_m3 = periods * max_uitstroom_per_tijdstap_m3
        values = np.arange(0.0, totale_uitstroom_m3, max_uitstroom_per_tijdstap_m3)
        dates = pd.date_range(_from, periods=periods, freq='15min', tz=pytz.utc)
        ts = pd.Series(values, dates, name='uitstroom')
        return ts

    def calc_scenario(self, current_fill_m3, desired_fill_m3, demand_m3, rain, max_uitstroom_m3):
        # expected_water is in m^3 after this
        toestroom = rain * (opp_invloed_regen_m2 / 1000)
        vaste_verandering = (toestroom.cumsum() - demand_m3.cumsum()) + current_fill_m3
        vast_met_max_uitstroom = vaste_verandering - max_uitstroom_m3

        # zoek eerste waarde waar de gewenste vulling bereikt wordt
        omslagpunt = None
        cross_desired = cross(vast_met_max_uitstroom, desired_fill_m3)
        if len(cross_desired) > 0:
            # gewenste vulling wordt bereikt
            omslagpunt = cross_desired[0]
            uitstroom_m3 = max_uitstroom_m3.copy()
            uitstroom_m3[omslagpunt:] = uitstroom_m3[omslagpunt]
        else:
            uitstroom_m3 = max_uitstroom_m3
        result = vaste_verandering - uitstroom_m3

        # terug naar percentages
        result = m3_to_pct(result)

        return {
            'prediction': result,
            'uitstroom': uitstroom_m3,
            'toestroom': toestroom.cumsum(),
            'omslagpunt': omslagpunt,
        }

    def predict_fill(self, _from, to, desired_fill_pct, demand_diff_pct, history_timedelta=None):
        # do some input validation here, to ensure we are dealing with sane numbers
        if 0 > desired_fill_pct > 100:
            raise ValueError('value should be a percentage between 0 and 100')
        if 0 > demand_diff_pct:
            raise ValueError('value should be a percentage > 0')

        # optional parameter
        if not history_timedelta:
            history_timedelta = fill_history

        # haal vulgraad op
        fill = self.fews_data.get_fill(_from - history_timedelta, _from)

        # take last measured value as current fill
        current_fill_m3 = fill[-1]

        # bepaal gewenste vulgraad
        desired_fill_m3 = max_berging_m3 * (desired_fill_pct / 100)

        rain_mean = self.fews_data.get_rain('mean', _from, to)
        if to < round_date(datetime.datetime.now(tz=pytz.utc)):
            # HACK: indien data uit het verleden wordt opgevraagd, zit er geen min en max meer in FEWS
            rain_min = rain_max = rain_mean
        else:
            rain_min = self.fews_data.get_rain('min', _from, to)
            rain_max = self.fews_data.get_rain('max', _from, to)
        # HACK: gebruik de datum van de laatst beschikbaar regenvoorspelling als to
        _from = rain_mean.index[0] 
        to = rain_mean.index[-1]

        # bereken watervraag over deze periode
        demand_m3 = self.demand_table.get_demand(_from, to)

        # pas reguliere watervraag aan met de opgegeven factor
        demand_diff = (demand_diff_pct / 100)
        demand_m3 = demand_m3 * demand_diff

        # leidt aantal periodes af uit een vd 'input' tijdreeksen
        periods = len(rain_mean)

        # bereken uitstroom
        max_uitstroom_m3 = self.calc_max_uitstroom(_from, periods)

        # return ook tussentijdse waarden, vnml. voor debugging
        result = {
            'scenarios': {},
            'history': m3_to_pct(fill),
            'rain': rain_mean,
            'max_uitstroom': max_uitstroom_m3,
            'demand': demand_m3.cumsum(),
        }

        # bereken de drie scenarios
        calc_scenarios = {
            'min': rain_min,
            'mean': rain_mean,
            'max': rain_max,
        }

        for scenario, rain in calc_scenarios.items():
            result['scenarios'][scenario] = self.calc_scenario(current_fill_m3, desired_fill_m3, demand_m3, rain, max_uitstroom_m3)

        #import pdb; pdb.set_trace()

        return result
