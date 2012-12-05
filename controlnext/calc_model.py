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

from controlnext.models import Constants
from controlnext.utils import round_date, validate_date

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
    # Find if values are above or below yvalue crossing:
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

def fill_m3_to_pct(ts, max_storage):
    ts /= max_storage
    ts *= 100
    return ts

class CalculationModel(object):
    def __init__(self, demand_table, fews_data):
        self.demand_table = demand_table
        self.fews_data = fews_data
        self.constants = Constants(self.fews_data.grower_info)

    def calc_max_uitstroom(self, _from, periods):
        # tel ook eerste en laatste periode mee
        totale_uitstroom_m3 = periods * self.constants.max_uitstroom_per_tijdstap_m3
        values = np.arange(0.0, float(totale_uitstroom_m3),
            float(self.constants.max_uitstroom_per_tijdstap_m3))
        dates = pd.date_range(_from, periods=periods, freq='15min', tz=pytz.utc)
        ts = pd.Series(values, dates, name='uitstroom')
        return ts

    def predict_scenario(self, _from, current_fill_m3, desired_fill_m3, demand_m3, rain_mm, max_uitstroom_m3):
        toestroom_m3 = rain_mm * (self.constants.opp_invloed_regen_m2 / 1000)
        vaste_verandering = toestroom_m3 - demand_m3 # + current_fill_m3
        vaste_verandering_summed = vaste_verandering.cumsum()

        variabele_verandering = np.zeros(len(vaste_verandering))
        totale_verandering = vaste_verandering + variabele_verandering
        result = totale_verandering.cumsum() + current_fill_m3
        for i in xrange(len(vaste_verandering) - 1):
            if result[i + 1] > desired_fill_m3:
                # volgende tijdstap wordt gewenste vulgraad overschreden, dus
                # zet de uitstroom aan
                variabele_verandering[i] = -self.constants.max_uitstroom_per_tijdstap_m3
                # bereken de nieuwe situatie
                totale_verandering = vaste_verandering + variabele_verandering
                result = totale_verandering.cumsum() + current_fill_m3

        uitstroom_m3 = pd.Series(
            variabele_verandering,
            index=result.index,
            name='uitstroom'
        )
        omslagpunten = cross(result, desired_fill_m3)
        omslagpunt = omslagpunten[0] if len(omslagpunten) > 0 else None

        # sommeer waarden boven de max berging
        result_24h = result[:_from + datetime.timedelta(hours=24)]
        overstort_24h = result_24h[result_24h.values > self.constants.max_berging_m3]
        if len(overstort_24h) > 0:
            overstort_24h = result[overstort_24h.index].max() - self.constants.max_berging_m3
        else:
            # geen overstort
            overstort_24h = 0
        # nu ook voor 5 dagen...
        overstort_5d = result[result.values > self.constants.max_berging_m3]
        if len(overstort_5d) > 0:
            overstort_5d = result[overstort_5d.index].max() - self.constants.max_berging_m3
        else:
            # geen overstort
            overstort_5d = 0

        # terug naar percentages
        result = fill_m3_to_pct(result, self.constants.max_berging_m3)

        return {
            'prediction': result,
            'omslagpunt': omslagpunt,
            'overstort_24h': overstort_24h,
            'overstort_5d': overstort_5d,
            'intermediate': {
                'uitstroom': uitstroom_m3,
                'toestroom': toestroom_m3.cumsum(),
            },
        }

    def predict_fill(self, _from, to, desired_fill_pct, demand_exaggerate_pct, rain_exaggerate_pct):
        # do some input validation here, to ensure we are dealing with sane numbers
        validate_date(_from)
        validate_date(to)
        if 0 > desired_fill_pct > 100:
            raise ValueError('value should be a percentage between 0 and 100')
        if 0 > demand_exaggerate_pct:
            raise ValueError('value should be a percentage > 0')
        if 0 > rain_exaggerate_pct:
            raise ValueError('value should be a percentage > 0')

        # determine desired fill in m^3
        desired_fill_m3 = self.constants.max_berging_m3 * (desired_fill_pct / 100)

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
        if rain_exaggerate_pct != 100:
            rain_exaggerate = rain_exaggerate_pct / 100
            rain_min *= rain_exaggerate
            rain_mean *= rain_exaggerate
            rain_max *= rain_exaggerate

        # retrieve fill: just take any data we have,
        # so we can compare measurements with predictions
        current_fill = self.fews_data.get_current_fill(to)
        current_fill_m3 = current_fill['current_fill_m3']

        # bereken watervraag over deze periode
        demand_m3 = self.demand_table.get_demand(_from, to)

        # pas reguliere watervraag aan met de opgegeven factor
        if demand_exaggerate_pct != 100:
            demand_exaggerate = demand_exaggerate_pct / 100
            demand_m3 *= demand_exaggerate
            #demand_m3 = demand_m3.cumsum()

        # leidt aantal periodes af uit een vd 'input' tijdreeksen
        periods = len(rain_mean)

        # bereken uitstroom
        max_uitstroom_m3 = self.calc_max_uitstroom(_from, periods)
        if len(max_uitstroom_m3) != len(rain_mean):
            raise Exception('%s != %s' % (len(max_uitstroom_m3), len(rain_mean)))

        # return ook tussentijdse waarden, vnml. voor debugging
        result = {
            'scenarios': {},
            'history': fill_m3_to_pct(current_fill['fill_history_m3'],
                self.constants.max_berging_m3),
            'current_fill': fill_m3_to_pct(current_fill_m3,
                self.constants.max_berging_m3),
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
            result['scenarios'][scenario] = self.predict_scenario(_from, current_fill_m3, desired_fill_m3, demand_m3, rain, max_uitstroom_m3)

        #import pdb; pdb.set_trace()

        return result
