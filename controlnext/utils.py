import datetime
import logging
import pytz

from hashlib import sha1
from functools import wraps

from django.core.cache import cache

logger = logging.getLogger(__name__)


def cache_result(seconds=900, ignore_cache=False, instancemethod=False):
    """
    Cache the result of a function call for the specified number of seconds,
    using Django's caching mechanism.
    Assumes that the function never returns None (as the cache returns None to
    indicate a miss), and that the function's result only depends on its
    parameters. Note that the ordering of parameters is important. e.g.
    myFunction(x=1, y=2), myFunction(y=2, x=1), and myFunction(1, 2) will each
    be cached separately.

    Usage:

    @cache(600)
    def my_expensive_method(parm1, parm2, parm3):
        ....
        return expensive_result
    """
    def do_cache_result(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            cachekeyargs = args[1:] if instancemethod else args
            key = (str(f.__module__) + str(f.__name__) + str(cachekeyargs) +
                   str(kwargs))
            key = sha1(key).hexdigest()
            result = cache.get(key)
            if ignore_cache or result is None:
                result = f(*args, **kwargs)
                cache.set(key, result, seconds)
            return result
        return wrapper
    return do_cache_result


def round_date(date):
    minutes = date.minute - (date.minute % 15)
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
