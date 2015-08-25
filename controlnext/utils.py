import datetime
import logging

import pytz

logger = logging.getLogger(__name__)


def round_date(date, divisor=15):
    minutes = date.minute - (date.minute % divisor)
    return date.replace(minute=minutes, second=0, microsecond=0)


def validate_date(date):
    if date.tzinfo != pytz.utc:
        raise ValueError(
            'can not deal with non-UTC (or timezone-naive) datetime objects')
    if date.second or date.microsecond or date.minute % 15 != 0:
        raise ValueError('please round dates to full quarter hours')


def mktim(year, month, day, hour, minute_quarter):
    if minute_quarter % 15 != 0:
        raise ValueError('not rounded to a quarter hour')
    return datetime.datetime(year, month, day, hour, minute_quarter,
                             tzinfo=pytz.utc)
