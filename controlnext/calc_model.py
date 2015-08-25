# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals
from __future__ import division
import logging
import datetime

import pytz
import pandas as pd
import numpy as np

from controlnext.utils import round_date, validate_date

# optionally import matplotlib which can be used to debugging
try:
    import matplotlib.pyplot as plt  # noqa
except ImportError:
    pass

logger = logging.getLogger(__name__)


def fill_m3_to_pct(ts, max_storage):
    ts /= max_storage
    ts *= 100
    return ts


class CalculationModel(object):
    def __init__(self, demand_table, fews_data):
        self.demand_table = demand_table
        self.fews_data = fews_data
        self.basin = fews_data.basin
        # constants is needed for user-overridable rain_flood_surface and
        # max_storage in controlnext_demo
        self.constants = fews_data.constants

    def calc_max_uitstroom(self, _from, periods):
        # tel ook eerste en laatste periode mee
        totale_uitstroom_m3 = (periods *
                               self.basin.max_outflow_per_timeunit)
        values = np.arange(
            0.0, float(totale_uitstroom_m3),
            float(self.basin.max_outflow_per_timeunit))
        dates = pd.date_range(_from, periods=periods, freq='15min',
                              tz=pytz.utc)
        ts = pd.Series(values, dates, name='uitstroom')
        return ts

    def predict_scenario(self, _from, current_fill_m3, demand_m3, rain_mm,
                         dt_aflaat_open=None, dt_aflaat_dicht=None,
                         aflaat_capaciteit=0):
        toestroom_m3 = rain_mm * (self.constants.rain_flood_surface / 1000)
        # Correct for optional reverse osmosis inflow.
        if (self.constants.reverse_osmosis and
                self.constants.reverse_osmosis > 0):
            till_year = self.constants.osmose_till_date.year
            till_month = self.constants.osmose_till_date.month
            till_day = self.constants.osmose_till_date.day
            till_datetime = datetime.datetime(till_year, till_month, till_day,
                                              _from.hour, tzinfo=pytz.utc)
            if till_datetime > _from:
                periods = (till_datetime - _from).total_seconds() / 900
                osmose_indexes = pd.date_range(_from, periods=periods,
                                               freq='15min', tz=pytz.utc)
                toestroom_m3[osmose_indexes[0]:osmose_indexes[-1]] += \
                    self.constants.reverse_osmosis

        vaste_verandering = toestroom_m3 - demand_m3
        if ((dt_aflaat_open is not None) and (dt_aflaat_dicht is not None)):
            aflaat_uitstroom = rain_mm.copy()
            aflaat_uitstroom[pd.Timestamp(dt_aflaat_open):pd.Timestamp(
                dt_aflaat_dicht)] = aflaat_capaciteit
            vaste_verandering = vaste_verandering - aflaat_uitstroom
        result = vaste_verandering.cumsum() + current_fill_m3

        # sommeer waarden boven de max berging
        result_24h = result[:_from + datetime.timedelta(hours=24)]
        overstort_24h = result_24h[result_24h.values > self.constants.
                                   max_storage]
        if len(overstort_24h) > 0:
            overstort_24h = (result[overstort_24h.index].max() -
                             self.constants.max_storage)
        else:
            # geen overstort
            overstort_24h = 0
        # nu ook voor 5 dagen...
        overstort_5d = result[result.values > self.constants.max_storage]
        if len(overstort_5d) > 0:
            overstort_5d = (result[overstort_5d.index].max() -
                            self.constants.max_storage)
        else:
            # geen overstort
            overstort_5d = 0

        # terug naar percentages
        result = fill_m3_to_pct(result, self.constants.max_storage)

        return {
            'prediction': result,
            'overstort_24h': overstort_24h,
            'overstort_5d': overstort_5d,
        }

    def predict_fill(self, _from, to, outflow_open=None,
                     outflow_closed=None, outflow_capacity=0):
        # do some input validation here, to ensure we are dealing with sane
        # numbers
        validate_date(_from)
        validate_date(to)

        rain_mean = self.fews_data.get_rain('mean', _from, to)
        # gebruik de datum van de laatst beschikbaar regenvoorspelling als
        # from en to waarden
        _from = rain_mean.index[0]
        to = rain_mean.index[-1]

        # create a no rain series
        rain_zero = rain_mean.copy()
        rain_zero[...] = 0
        rain_zero.name = 'rain_zero'

        # retrieve fill: just take any data we have,
        # so we can compare measurements with predictions
        current_fill = self.fews_data.get_current_fill(to)
        current_fill_m3 = current_fill['current_fill_m3']

        # bereken watervraag over deze periode
        demand_m3 = self.demand_table.get_demand(_from, to)

        # leidt aantal periodes af uit een vd 'input' tijdreeksen
        periods = len(rain_mean)

        # bereken uitstroom
        max_uitstroom_m3 = self.calc_max_uitstroom(_from, periods)
        if len(max_uitstroom_m3) != len(rain_mean):
            raise Exception('%s != %s' % (len(max_uitstroom_m3),
                                          len(rain_mean)))

        # return ook tussentijdse waarden, vnml. voor debugging
        result = {
            'scenarios': {},
            'history': fill_m3_to_pct(
                current_fill['fill_history_m3'],
                self.constants.max_storage),
            'current_fill': fill_m3_to_pct(
                current_fill_m3, self.constants.max_storage),
            'intermediate': {
                'rain_mean': rain_mean,
                'max_uitstroom': max_uitstroom_m3,
                'demand': demand_m3,
            }
        }

        # bereken de drie scenarios
        calc_scenarios = {
            'no_rain': rain_zero,
            'mean': rain_mean,
        }
        for scenario, rain in calc_scenarios.items():
            result['scenarios'][scenario] = self.predict_scenario(
                _from, current_fill_m3, demand_m3, rain, outflow_open,
                outflow_closed, outflow_capacity)

        return result
