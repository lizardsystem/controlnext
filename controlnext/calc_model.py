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

def fill_m3_to_pct(ts):
    ts /= max_berging_m3
    ts *= 100
    return ts

class CalculationModel(object):
    def __init__(self, demand_table, fews_data):
        self.demand_table = demand_table
        self.fews_data = fews_data

    def calc_max_uitstroom(self, _from, periods):
        # tel ook eerste en laatste periode mee
        totale_uitstroom_m3 = periods * max_uitstroom_per_tijdstap_m3
        values = np.arange(0.0, totale_uitstroom_m3, max_uitstroom_per_tijdstap_m3)
        dates = pd.date_range(_from, periods=periods, freq='15min', tz=pytz.utc)
        ts = pd.Series(values, dates, name='uitstroom')
        return ts

    def predict_scenario(self, current_fill_m3, desired_fill_m3, demand_m3, rain_mm, max_uitstroom_m3):
        toestroom_m3 = (rain_mm * (opp_invloed_regen_m2 / 1000)).cumsum()
        vaste_verandering = (toestroom_m3 - demand_m3) + current_fill_m3
        vast_met_max_uitstroom = vaste_verandering - max_uitstroom_m3

        # zoek eerste waarde waar de gewenste vulling bereikt wordt
        omslagpunt = None
        cross_desired = cross(vast_met_max_uitstroom, desired_fill_m3)
        if len(cross_desired) > 0:
            # gewenste vulling wordt bereikt
            omslagpunt = cross_desired[0]
            uitstroom_m3 = max_uitstroom_m3.copy()
            # uitstroom 'kraan' kan dicht als het omslagpunt bereikt is
            uitstroom_m3[omslagpunt:] = uitstroom_m3[omslagpunt]
        else:
            uitstroom_m3 = max_uitstroom_m3
        result = vaste_verandering - uitstroom_m3

        # sommer waarden boven de max berging
        overstort = result[result.values > max_berging_m3]
        overstort = overstort[:overstort.index[0] + datetime.timedelta(hours=24)] - max_berging_m3
        import pdb; pdb.set_trace()

        result += current_fill_m3
        # terug naar percentages
        result = fill_m3_to_pct(result)

        return {
            'prediction': result,
            'omslagpunt': omslagpunt,
            'overstort': overstort,
            'intermediate': {
                'uitstroom': uitstroom_m3,
                'toestroom': toestroom_m3,
            },
        }

    def predict_fill(self, _from, to, desired_fill_pct, demand_diff_pct, rain_exaggerate_factor=None):
        # do some input validation here, to ensure we are dealing with sane numbers
        validate_date(_from)
        validate_date(to)
        if 0 > desired_fill_pct > 100:
            raise ValueError('value should be a percentage between 0 and 100')
        if 0 > demand_diff_pct:
            raise ValueError('value should be a percentage > 0')

        # determine desired fill in m^3
        desired_fill_m3 = max_berging_m3 * (desired_fill_pct / 100)

        rain_mean = self.fews_data.get_rain('mean', _from, to)
        if to < round_date(datetime.datetime.now(tz=pytz.utc)):
            # HACK: indien data uit het verleden wordt opgevraagd, zit er geen min en max meer in FEWS
            rain_min = rain_max = rain_mean
        else:
            rain_min = self.fews_data.get_rain('min', _from, to)
            rain_max = self.fews_data.get_rain('max', _from, to)

        # gebruik de datum van de laatst beschikbaar regenvoorspelling als from en to waarden
        _from = rain_mean.index[0] 
        to = rain_mean.index[-1]

        # optionele overdrijf factor voor regen
        if rain_exaggerate_factor is not None:
            rain_min *= rain_exaggerate_factor
            rain_mean *= rain_exaggerate_factor
            rain_max *= rain_exaggerate_factor

        # retrieve fill
        current_fill = self.fews_data.get_current_fill(_from)
        current_fill_m3 = current_fill['current_fill_m3']

        # bereken watervraag over deze periode
        demand_m3 = self.demand_table.get_demand(_from, to)

        # pas reguliere watervraag aan met de opgegeven factor
        demand_diff = (demand_diff_pct / 100)
        demand_m3 = demand_m3 * demand_diff
        demand_m3 = demand_m3.cumsum()

        # leidt aantal periodes af uit een vd 'input' tijdreeksen
        periods = len(rain_mean)

        # bereken uitstroom
        max_uitstroom_m3 = self.calc_max_uitstroom(_from, periods)
        if len(max_uitstroom_m3) != len(rain_mean):
            raise Exception('%s != %s' % (len(max_uitstroom_m3), len(rain_mean)))

        # return ook tussentijdse waarden, vnml. voor debugging
        result = {
            'scenarios': {},
            'history': fill_m3_to_pct(current_fill['fill_history_m3']),
            'current_fill': fill_m3_to_pct(current_fill_m3),
            'intermediate': {
                'rain_mean': rain_mean,
                'max_uitstroom': max_uitstroom_m3,
                'demand': demand_m3,
            }
        }

        # bereken de drie scenarios
        calc_scenarios = {
            'min': rain_min,
            'mean': rain_mean,
            'max': rain_max,
        }

        for scenario, rain in calc_scenarios.items():
            result['scenarios'][scenario] = self.predict_scenario(current_fill_m3, desired_fill_m3, demand_m3, rain, max_uitstroom_m3)

        #import pdb; pdb.set_trace()

        return result
