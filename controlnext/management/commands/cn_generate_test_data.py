from __future__ import print_function
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError

import pytz

from controlnext.fews_data import FewsJdbcDataSource
from controlnext.models import GrowerInfo

DATA_MODULE_START_TEXT = """import datetime

import pytz


DATA = [
"""
DATA_MODULE_END_TEXT = "]\n"

def convert_timeseries_to_python(ts):
    tuples = zip(ts.index.to_pydatetime(), ts)
    return tuples

def format_datetime(dt):
    """Format datetime to be printable as a working datetime string."""
    dt = "%r" % dt
    return dt.replace('<UTC>', 'pytz.utc')


class Command(BaseCommand):
    """Management command for generating test data for mocking
    get_rain and get_fill."""
    help = 'Generate test data.'

    def handle(self, **options):
        grower = GrowerInfo.objects.get(pk=1)
        ds = FewsJdbcDataSource(grower)

        _from = datetime(2013, 1, 24, 9, 30, tzinfo=pytz.utc)
        to = datetime(2013, 1, 29, 9, 30, tzinfo=pytz.utc)

        # get_rain data
        for rain_type in ('min', 'mean', 'max'):  # rain types
            results = ds.get_rain(rain_type, _from, to)
            data = convert_timeseries_to_python(results)
            if data:
                f = open('rain_%s_data.py' % rain_type, 'w')
                f.write(DATA_MODULE_START_TEXT)
                for dt, value in data:
                    f.write("    [%s, %s],\n" % (format_datetime(dt), value))
                f.write(DATA_MODULE_END_TEXT)
                f.close()

        # get_fill data
        _from = datetime(2012, 12, 29, 9, 30, tzinfo=pytz.utc)
        to = datetime(2013, 1, 29, 9, 30, tzinfo=pytz.utc)

        results = ds.get_fill(_from, to)
        data = convert_timeseries_to_python(results)
        if data:
            f = open('fill_data.py', 'w')
            f.write(DATA_MODULE_START_TEXT)
            for dt, value in data:
                f.write("    [%s, %s],\n" % (format_datetime(dt), value))
            f.write(DATA_MODULE_END_TEXT)
            f.close()

