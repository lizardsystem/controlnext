# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals
import os
import logging
import datetime

from django.conf import settings

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

if hasattr(settings, 'DEMAND_TABLE_PATH'):
    demand_table_path = settings.DEMAND_TABLE_PATH
else:
    demand_table_path = None

if not demand_table_path:
    logger.warn('DEMAND_TABLE_PATH is not configured.')
elif not os.path.isfile(demand_table_path):
    logger.warn('Could not find a file at %s.', demand_table_path)

# semi configurable constants
delimiter = ';'
required_cols = set(['week_number', 'demand_lans_m3_div_1000', 'demand_waterschap_m3_div_1000'])

# dont use the csv module here, its ancient (no unicode)
# and less dependencies is better
def read_demand_csv():
    '''
    Reads the demand csv file and return its contents in a dict
    int(week number) -> (int(demand_lans), int(demand_waterschap)).
    Demands are in m^3.
    '''
    logging.debug('Reading %s', demand_table_path)
    result = {}
    with open(demand_table_path, 'rb') as file:
        cols = file.next().strip().split(delimiter)
        # do some validation
        if not required_cols.issubset(cols):
            raise Exception('Could not find the necessary columns in the csv.')
        # TODO: column headers are unused, so the CSV isn't very flexible
        for line in file:
            row = line.strip().split(delimiter)
            row = map(int, row)
            # multiply demands by 1000 so we return a sane unit (m^3)
            result[row[0]] = (row[1] * 1000, row[2] * 1000)
    # table doesn't define anything for week 0 (the days between new year and first sunday)
    if not 0 in result:
        # just copy the values from week 1
        result[0] = result[1]
    # table only goes to 52...
    if not 53 in result:
        # just copy the values from week 52
        result[53] = result[52]
    return result

demand_table = None
def get_demand_for_week(week):
    '''
    Returns the demand on the given week, in m^3. 
    '''
    # lazy load and keep the demand table in memory, because it's tiny
    global demand_table
    if not demand_table:
        demand_table = read_demand_csv()
    # get vd lans demand for this week
    result = demand_table[week][0]
    return result

def get_demand_on(date):
    '''
    Returns the demand on the given date, in m^3. 
    '''
    # determine week number for given date
    week = date.isocalendar()[1]
    return get_demand_for_week(week)


def test_demand_table():
    pd_init_table()
    w28  = datetime.datetime(2012, 7, 9, 0, 0, 0)     # monday, 0:00, week 28 (d = 19000)
    w285 = datetime.datetime(2012, 7, 12, 11, 59, 59) # middle of week 28
    w289 = datetime.datetime(2012, 7, 15, 23, 59, 59) # sunday, 23:59, week 28
    w29  = datetime.datetime(2012, 7, 16, 0, 0, 0)    # sunday, 0:00, week 29 (d = 18000)
    w295 = datetime.datetime(2012, 7, 19, 12, 0, 0)   # middle of week 29
    w30  = datetime.datetime(2012, 7, 23, 0, 0, 0)    # sunday, 0:00, week 30 (d = 17000)
    w305 = datetime.datetime(2012, 7, 26, 12, 0, 0)   # middle of week 30 (d = 17000)
    print 'period: expect ~9500'; print pd_get_total_demand(w28, w285)
    print 'period: expect ~19000'; print pd_get_total_demand(w28, w289)

table_year = 2012
ts = None

def pd_init_table():
    global ts
    if ts is None:
        start = datetime.datetime(table_year, 1, 1)
        end = datetime.datetime(table_year + 1, 1, 1)
        weekly = pd.date_range(start, end, freq='W-MON') # week changes on monday
        values = [get_demand_for_week(week) for week in range(1, len(weekly) + 1)] # start at week 1
        ts = pd.Series(values, weekly)
        ts = ts.resample('H', fill_method='pad')
        ts = np.true_divide(ts, 7 * 24) # hours in a week

def pd_plot_table():
    '''
    For debugging
    '''
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(24, 6))
    axes = ts.plot()
    fig.add_subplot(axes)
    fig.savefig('out.png')
    fig.close()

def pd_get_hourly_demand(_from, to):
    # set from and to to year 2012 (leap year Feb. 29 works as well)
    # as we only have a table for one year
    _from = datetime.datetime(table_year, _from.month, _from.day, _from.hour)
    to =    datetime.datetime(table_year, to.month,    to.day,    to.hour)
    return ts[_from:to]

def pd_get_total_demand(_from, to):
    return pd_get_hourly_demand(_from, to).sum()
