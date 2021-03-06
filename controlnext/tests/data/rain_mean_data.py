import datetime

import pytz


DATA = [
    [datetime.datetime(2013, 1, 24, 10, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 24, 10, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 24, 10, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 24, 11, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 24, 11, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 24, 11, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 24, 11, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 24, 12, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 24, 12, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 24, 12, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 24, 12, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 24, 13, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 24, 13, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 24, 13, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 24, 13, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 24, 14, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 24, 14, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 24, 14, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 24, 14, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 24, 15, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 24, 15, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 24, 15, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 24, 15, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 24, 16, 0, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 24, 16, 15, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 24, 16, 30, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 24, 16, 45, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 24, 17, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 24, 17, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 24, 17, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 24, 17, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 24, 18, 0, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 24, 18, 15, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 24, 18, 30, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 24, 18, 45, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 24, 19, 0, tzinfo=pytz.utc), 0.015],
    [datetime.datetime(2013, 1, 24, 19, 15, tzinfo=pytz.utc), 0.015],
    [datetime.datetime(2013, 1, 24, 19, 30, tzinfo=pytz.utc), 0.015],
    [datetime.datetime(2013, 1, 24, 19, 45, tzinfo=pytz.utc), 0.015],
    [datetime.datetime(2013, 1, 24, 20, 0, tzinfo=pytz.utc), 0.0025],
    [datetime.datetime(2013, 1, 24, 20, 15, tzinfo=pytz.utc), 0.0025],
    [datetime.datetime(2013, 1, 24, 20, 30, tzinfo=pytz.utc), 0.0025],
    [datetime.datetime(2013, 1, 24, 20, 45, tzinfo=pytz.utc), 0.0025],
    [datetime.datetime(2013, 1, 24, 21, 0, tzinfo=pytz.utc), 0.0025],
    [datetime.datetime(2013, 1, 24, 21, 15, tzinfo=pytz.utc), 0.0025],
    [datetime.datetime(2013, 1, 24, 21, 30, tzinfo=pytz.utc), 0.0025],
    [datetime.datetime(2013, 1, 24, 21, 45, tzinfo=pytz.utc), 0.0025],
    [datetime.datetime(2013, 1, 24, 22, 0, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 24, 22, 15, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 24, 22, 30, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 24, 22, 45, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 24, 23, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 24, 23, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 24, 23, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 24, 23, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 0, 0, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 25, 0, 15, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 25, 0, 30, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 25, 0, 45, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 25, 1, 0, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 25, 1, 15, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 25, 1, 30, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 25, 1, 45, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 25, 2, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 2, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 2, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 2, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 3, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 3, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 3, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 3, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 4, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 4, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 4, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 4, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 5, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 5, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 5, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 5, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 6, 0, tzinfo=pytz.utc), 0.0025],
    [datetime.datetime(2013, 1, 25, 6, 15, tzinfo=pytz.utc), 0.0025],
    [datetime.datetime(2013, 1, 25, 6, 30, tzinfo=pytz.utc), 0.0025],
    [datetime.datetime(2013, 1, 25, 6, 45, tzinfo=pytz.utc), 0.0025],
    [datetime.datetime(2013, 1, 25, 7, 0, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 25, 7, 15, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 25, 7, 30, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 25, 7, 45, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 25, 8, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 8, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 8, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 8, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 9, 0, tzinfo=pytz.utc), 0.0025],
    [datetime.datetime(2013, 1, 25, 9, 15, tzinfo=pytz.utc), 0.0025],
    [datetime.datetime(2013, 1, 25, 9, 30, tzinfo=pytz.utc), 0.0025],
    [datetime.datetime(2013, 1, 25, 9, 45, tzinfo=pytz.utc), 0.0025],
    [datetime.datetime(2013, 1, 25, 10, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 10, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 10, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 10, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 11, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 11, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 11, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 11, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 12, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 12, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 12, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 12, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 13, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 13, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 13, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 13, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 14, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 14, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 14, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 14, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 15, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 15, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 15, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 15, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 16, 0, tzinfo=pytz.utc), 0.0025],
    [datetime.datetime(2013, 1, 25, 16, 15, tzinfo=pytz.utc), 0.0025],
    [datetime.datetime(2013, 1, 25, 16, 30, tzinfo=pytz.utc), 0.0025],
    [datetime.datetime(2013, 1, 25, 16, 45, tzinfo=pytz.utc), 0.0025],
    [datetime.datetime(2013, 1, 25, 17, 0, tzinfo=pytz.utc), 0.0025],
    [datetime.datetime(2013, 1, 25, 17, 15, tzinfo=pytz.utc), 0.0025],
    [datetime.datetime(2013, 1, 25, 17, 30, tzinfo=pytz.utc), 0.0025],
    [datetime.datetime(2013, 1, 25, 17, 45, tzinfo=pytz.utc), 0.0025],
    [datetime.datetime(2013, 1, 25, 18, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 18, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 18, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 18, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 19, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 19, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 19, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 19, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 20, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 20, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 20, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 20, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 21, 0, tzinfo=pytz.utc), 0.0025],
    [datetime.datetime(2013, 1, 25, 21, 15, tzinfo=pytz.utc), 0.0025],
    [datetime.datetime(2013, 1, 25, 21, 30, tzinfo=pytz.utc), 0.0025],
    [datetime.datetime(2013, 1, 25, 21, 45, tzinfo=pytz.utc), 0.0025],
    [datetime.datetime(2013, 1, 25, 22, 0, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 25, 22, 15, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 25, 22, 30, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 25, 22, 45, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 25, 23, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 23, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 23, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 25, 23, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 0, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 0, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 0, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 0, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 1, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 1, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 1, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 1, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 2, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 2, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 2, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 2, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 3, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 3, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 3, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 3, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 4, 0, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 26, 4, 15, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 26, 4, 30, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 26, 4, 45, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 26, 5, 0, tzinfo=pytz.utc), 0.0025],
    [datetime.datetime(2013, 1, 26, 5, 15, tzinfo=pytz.utc), 0.0025],
    [datetime.datetime(2013, 1, 26, 5, 30, tzinfo=pytz.utc), 0.0025],
    [datetime.datetime(2013, 1, 26, 5, 45, tzinfo=pytz.utc), 0.0025],
    [datetime.datetime(2013, 1, 26, 6, 0, tzinfo=pytz.utc), 0.0525],
    [datetime.datetime(2013, 1, 26, 6, 15, tzinfo=pytz.utc), 0.0525],
    [datetime.datetime(2013, 1, 26, 6, 30, tzinfo=pytz.utc), 0.0525],
    [datetime.datetime(2013, 1, 26, 6, 45, tzinfo=pytz.utc), 0.0525],
    [datetime.datetime(2013, 1, 26, 7, 0, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 26, 7, 15, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 26, 7, 30, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 26, 7, 45, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 26, 8, 0, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 26, 8, 15, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 26, 8, 30, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 26, 8, 45, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 26, 9, 0, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 26, 9, 15, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 26, 9, 30, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 26, 9, 45, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 26, 10, 0, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 26, 10, 15, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 26, 10, 30, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 26, 10, 45, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 26, 11, 0, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 26, 11, 15, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 26, 11, 30, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 26, 11, 45, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 26, 12, 0, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 26, 12, 15, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 26, 12, 30, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 26, 12, 45, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 26, 13, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 13, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 13, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 13, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 14, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 14, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 14, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 14, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 15, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 15, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 15, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 15, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 16, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 16, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 16, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 16, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 17, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 17, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 17, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 17, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 18, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 18, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 18, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 18, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 19, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 19, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 19, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 19, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 20, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 20, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 20, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 20, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 21, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 21, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 21, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 21, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 22, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 22, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 22, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 22, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 23, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 23, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 23, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 26, 23, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 27, 0, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 27, 0, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 27, 0, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 27, 0, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 27, 1, 0, tzinfo=pytz.utc), 0.195],
    [datetime.datetime(2013, 1, 27, 1, 15, tzinfo=pytz.utc), 0.195],
    [datetime.datetime(2013, 1, 27, 1, 30, tzinfo=pytz.utc), 0.195],
    [datetime.datetime(2013, 1, 27, 1, 45, tzinfo=pytz.utc), 0.195],
    [datetime.datetime(2013, 1, 27, 2, 0, tzinfo=pytz.utc), 0.195],
    [datetime.datetime(2013, 1, 27, 2, 15, tzinfo=pytz.utc), 0.195],
    [datetime.datetime(2013, 1, 27, 2, 30, tzinfo=pytz.utc), 0.195],
    [datetime.datetime(2013, 1, 27, 2, 45, tzinfo=pytz.utc), 0.195],
    [datetime.datetime(2013, 1, 27, 3, 0, tzinfo=pytz.utc), 0.195],
    [datetime.datetime(2013, 1, 27, 3, 15, tzinfo=pytz.utc), 0.195],
    [datetime.datetime(2013, 1, 27, 3, 30, tzinfo=pytz.utc), 0.195],
    [datetime.datetime(2013, 1, 27, 3, 45, tzinfo=pytz.utc), 0.195],
    [datetime.datetime(2013, 1, 27, 4, 0, tzinfo=pytz.utc), 0.195],
    [datetime.datetime(2013, 1, 27, 4, 15, tzinfo=pytz.utc), 0.195],
    [datetime.datetime(2013, 1, 27, 4, 30, tzinfo=pytz.utc), 0.195],
    [datetime.datetime(2013, 1, 27, 4, 45, tzinfo=pytz.utc), 0.195],
    [datetime.datetime(2013, 1, 27, 5, 0, tzinfo=pytz.utc), 0.195],
    [datetime.datetime(2013, 1, 27, 5, 15, tzinfo=pytz.utc), 0.195],
    [datetime.datetime(2013, 1, 27, 5, 30, tzinfo=pytz.utc), 0.195],
    [datetime.datetime(2013, 1, 27, 5, 45, tzinfo=pytz.utc), 0.195],
    [datetime.datetime(2013, 1, 27, 6, 0, tzinfo=pytz.utc), 0.195],
    [datetime.datetime(2013, 1, 27, 6, 15, tzinfo=pytz.utc), 0.195],
    [datetime.datetime(2013, 1, 27, 6, 30, tzinfo=pytz.utc), 0.195],
    [datetime.datetime(2013, 1, 27, 6, 45, tzinfo=pytz.utc), 0.195],
    [datetime.datetime(2013, 1, 27, 7, 0, tzinfo=pytz.utc), 0.055],
    [datetime.datetime(2013, 1, 27, 7, 15, tzinfo=pytz.utc), 0.055],
    [datetime.datetime(2013, 1, 27, 7, 30, tzinfo=pytz.utc), 0.055],
    [datetime.datetime(2013, 1, 27, 7, 45, tzinfo=pytz.utc), 0.055],
    [datetime.datetime(2013, 1, 27, 8, 0, tzinfo=pytz.utc), 0.055],
    [datetime.datetime(2013, 1, 27, 8, 15, tzinfo=pytz.utc), 0.055],
    [datetime.datetime(2013, 1, 27, 8, 30, tzinfo=pytz.utc), 0.055],
    [datetime.datetime(2013, 1, 27, 8, 45, tzinfo=pytz.utc), 0.055],
    [datetime.datetime(2013, 1, 27, 9, 0, tzinfo=pytz.utc), 0.055],
    [datetime.datetime(2013, 1, 27, 9, 15, tzinfo=pytz.utc), 0.055],
    [datetime.datetime(2013, 1, 27, 9, 30, tzinfo=pytz.utc), 0.055],
    [datetime.datetime(2013, 1, 27, 9, 45, tzinfo=pytz.utc), 0.055],
    [datetime.datetime(2013, 1, 27, 10, 0, tzinfo=pytz.utc), 0.055],
    [datetime.datetime(2013, 1, 27, 10, 15, tzinfo=pytz.utc), 0.055],
    [datetime.datetime(2013, 1, 27, 10, 30, tzinfo=pytz.utc), 0.055],
    [datetime.datetime(2013, 1, 27, 10, 45, tzinfo=pytz.utc), 0.055],
    [datetime.datetime(2013, 1, 27, 11, 0, tzinfo=pytz.utc), 0.055],
    [datetime.datetime(2013, 1, 27, 11, 15, tzinfo=pytz.utc), 0.055],
    [datetime.datetime(2013, 1, 27, 11, 30, tzinfo=pytz.utc), 0.055],
    [datetime.datetime(2013, 1, 27, 11, 45, tzinfo=pytz.utc), 0.055],
    [datetime.datetime(2013, 1, 27, 12, 0, tzinfo=pytz.utc), 0.055],
    [datetime.datetime(2013, 1, 27, 12, 15, tzinfo=pytz.utc), 0.055],
    [datetime.datetime(2013, 1, 27, 12, 30, tzinfo=pytz.utc), 0.055],
    [datetime.datetime(2013, 1, 27, 12, 45, tzinfo=pytz.utc), 0.055],
    [datetime.datetime(2013, 1, 27, 13, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 27, 13, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 27, 13, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 27, 13, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 27, 14, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 27, 14, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 27, 14, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 27, 14, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 27, 15, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 27, 15, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 27, 15, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 27, 15, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 27, 16, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 27, 16, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 27, 16, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 27, 16, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 27, 17, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 27, 17, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 27, 17, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 27, 17, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 27, 18, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 27, 18, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 27, 18, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 27, 18, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 27, 19, 0, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 27, 19, 15, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 27, 19, 30, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 27, 19, 45, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 27, 20, 0, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 27, 20, 15, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 27, 20, 30, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 27, 20, 45, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 27, 21, 0, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 27, 21, 15, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 27, 21, 30, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 27, 21, 45, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 27, 22, 0, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 27, 22, 15, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 27, 22, 30, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 27, 22, 45, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 27, 23, 0, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 27, 23, 15, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 27, 23, 30, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 27, 23, 45, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 28, 0, 0, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 28, 0, 15, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 28, 0, 30, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 28, 0, 45, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 28, 1, 0, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 28, 1, 15, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 28, 1, 30, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 28, 1, 45, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 28, 2, 0, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 28, 2, 15, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 28, 2, 30, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 28, 2, 45, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 28, 3, 0, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 28, 3, 15, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 28, 3, 30, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 28, 3, 45, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 28, 4, 0, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 28, 4, 15, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 28, 4, 30, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 28, 4, 45, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 28, 5, 0, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 28, 5, 15, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 28, 5, 30, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 28, 5, 45, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 28, 6, 0, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 28, 6, 15, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 28, 6, 30, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 28, 6, 45, tzinfo=pytz.utc), 0.005],
    [datetime.datetime(2013, 1, 28, 7, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 28, 7, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 28, 7, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 28, 7, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 28, 8, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 28, 8, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 28, 8, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 28, 8, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 28, 9, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 28, 9, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 28, 9, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 28, 9, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 28, 10, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 28, 10, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 28, 10, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 28, 10, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 28, 11, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 28, 11, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 28, 11, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 28, 11, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 28, 12, 0, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 28, 12, 15, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 28, 12, 30, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 28, 12, 45, tzinfo=pytz.utc), 0.0],
    [datetime.datetime(2013, 1, 28, 13, 0, tzinfo=pytz.utc), 0.03],
    [datetime.datetime(2013, 1, 28, 13, 15, tzinfo=pytz.utc), 0.03],
    [datetime.datetime(2013, 1, 28, 13, 30, tzinfo=pytz.utc), 0.03],
    [datetime.datetime(2013, 1, 28, 13, 45, tzinfo=pytz.utc), 0.03],
    [datetime.datetime(2013, 1, 28, 14, 0, tzinfo=pytz.utc), 0.03],
    [datetime.datetime(2013, 1, 28, 14, 15, tzinfo=pytz.utc), 0.03],
    [datetime.datetime(2013, 1, 28, 14, 30, tzinfo=pytz.utc), 0.03],
    [datetime.datetime(2013, 1, 28, 14, 45, tzinfo=pytz.utc), 0.03],
    [datetime.datetime(2013, 1, 28, 15, 0, tzinfo=pytz.utc), 0.03],
    [datetime.datetime(2013, 1, 28, 15, 15, tzinfo=pytz.utc), 0.03],
    [datetime.datetime(2013, 1, 28, 15, 30, tzinfo=pytz.utc), 0.03],
    [datetime.datetime(2013, 1, 28, 15, 45, tzinfo=pytz.utc), 0.03],
    [datetime.datetime(2013, 1, 28, 16, 0, tzinfo=pytz.utc), 0.03],
    [datetime.datetime(2013, 1, 28, 16, 15, tzinfo=pytz.utc), 0.03],
    [datetime.datetime(2013, 1, 28, 16, 30, tzinfo=pytz.utc), 0.03],
    [datetime.datetime(2013, 1, 28, 16, 45, tzinfo=pytz.utc), 0.03],
    [datetime.datetime(2013, 1, 28, 17, 0, tzinfo=pytz.utc), 0.03],
    [datetime.datetime(2013, 1, 28, 17, 15, tzinfo=pytz.utc), 0.03],
    [datetime.datetime(2013, 1, 28, 17, 30, tzinfo=pytz.utc), 0.03],
    [datetime.datetime(2013, 1, 28, 17, 45, tzinfo=pytz.utc), 0.03],
    [datetime.datetime(2013, 1, 28, 18, 0, tzinfo=pytz.utc), 0.03],
    [datetime.datetime(2013, 1, 28, 18, 15, tzinfo=pytz.utc), 0.03],
    [datetime.datetime(2013, 1, 28, 18, 30, tzinfo=pytz.utc), 0.03],
    [datetime.datetime(2013, 1, 28, 18, 45, tzinfo=pytz.utc), 0.03],
    [datetime.datetime(2013, 1, 28, 19, 0, tzinfo=pytz.utc), 0.025],
    [datetime.datetime(2013, 1, 28, 19, 15, tzinfo=pytz.utc), 0.025],
    [datetime.datetime(2013, 1, 28, 19, 30, tzinfo=pytz.utc), 0.025],
    [datetime.datetime(2013, 1, 28, 19, 45, tzinfo=pytz.utc), 0.025],
    [datetime.datetime(2013, 1, 28, 20, 0, tzinfo=pytz.utc), 0.025],
    [datetime.datetime(2013, 1, 28, 20, 15, tzinfo=pytz.utc), 0.025],
    [datetime.datetime(2013, 1, 28, 20, 30, tzinfo=pytz.utc), 0.025],
    [datetime.datetime(2013, 1, 28, 20, 45, tzinfo=pytz.utc), 0.025],
    [datetime.datetime(2013, 1, 28, 21, 0, tzinfo=pytz.utc), 0.025],
    [datetime.datetime(2013, 1, 28, 21, 15, tzinfo=pytz.utc), 0.025],
    [datetime.datetime(2013, 1, 28, 21, 30, tzinfo=pytz.utc), 0.025],
    [datetime.datetime(2013, 1, 28, 21, 45, tzinfo=pytz.utc), 0.025],
    [datetime.datetime(2013, 1, 28, 22, 0, tzinfo=pytz.utc), 0.025],
    [datetime.datetime(2013, 1, 28, 22, 15, tzinfo=pytz.utc), 0.025],
    [datetime.datetime(2013, 1, 28, 22, 30, tzinfo=pytz.utc), 0.025],
    [datetime.datetime(2013, 1, 28, 22, 45, tzinfo=pytz.utc), 0.025],
    [datetime.datetime(2013, 1, 28, 23, 0, tzinfo=pytz.utc), 0.025],
    [datetime.datetime(2013, 1, 28, 23, 15, tzinfo=pytz.utc), 0.025],
    [datetime.datetime(2013, 1, 28, 23, 30, tzinfo=pytz.utc), 0.025],
    [datetime.datetime(2013, 1, 28, 23, 45, tzinfo=pytz.utc), 0.025],
    [datetime.datetime(2013, 1, 29, 0, 0, tzinfo=pytz.utc), 0.025],
    [datetime.datetime(2013, 1, 29, 0, 15, tzinfo=pytz.utc), 0.025],
    [datetime.datetime(2013, 1, 29, 0, 30, tzinfo=pytz.utc), 0.025],
    [datetime.datetime(2013, 1, 29, 0, 45, tzinfo=pytz.utc), 0.025],
    [datetime.datetime(2013, 1, 29, 1, 0, tzinfo=pytz.utc), 0.2825],
    [datetime.datetime(2013, 1, 29, 1, 15, tzinfo=pytz.utc), 0.2825],
    [datetime.datetime(2013, 1, 29, 1, 30, tzinfo=pytz.utc), 0.2825],
    [datetime.datetime(2013, 1, 29, 1, 45, tzinfo=pytz.utc), 0.2825],
    [datetime.datetime(2013, 1, 29, 2, 0, tzinfo=pytz.utc), 0.2825],
    [datetime.datetime(2013, 1, 29, 2, 15, tzinfo=pytz.utc), 0.2825],
    [datetime.datetime(2013, 1, 29, 2, 30, tzinfo=pytz.utc), 0.2825],
    [datetime.datetime(2013, 1, 29, 2, 45, tzinfo=pytz.utc), 0.2825],
    [datetime.datetime(2013, 1, 29, 3, 0, tzinfo=pytz.utc), 0.2825],
    [datetime.datetime(2013, 1, 29, 3, 15, tzinfo=pytz.utc), 0.2825],
    [datetime.datetime(2013, 1, 29, 3, 30, tzinfo=pytz.utc), 0.2825],
    [datetime.datetime(2013, 1, 29, 3, 45, tzinfo=pytz.utc), 0.2825],
    [datetime.datetime(2013, 1, 29, 4, 0, tzinfo=pytz.utc), 0.2825],
    [datetime.datetime(2013, 1, 29, 4, 15, tzinfo=pytz.utc), 0.2825],
    [datetime.datetime(2013, 1, 29, 4, 30, tzinfo=pytz.utc), 0.2825],
    [datetime.datetime(2013, 1, 29, 4, 45, tzinfo=pytz.utc), 0.2825],
    [datetime.datetime(2013, 1, 29, 5, 0, tzinfo=pytz.utc), 0.2825],
    [datetime.datetime(2013, 1, 29, 5, 15, tzinfo=pytz.utc), 0.2825],
    [datetime.datetime(2013, 1, 29, 5, 30, tzinfo=pytz.utc), 0.2825],
    [datetime.datetime(2013, 1, 29, 5, 45, tzinfo=pytz.utc), 0.2825],
    [datetime.datetime(2013, 1, 29, 6, 0, tzinfo=pytz.utc), 0.2825],
    [datetime.datetime(2013, 1, 29, 6, 15, tzinfo=pytz.utc), 0.2825],
    [datetime.datetime(2013, 1, 29, 6, 30, tzinfo=pytz.utc), 0.2825],
    [datetime.datetime(2013, 1, 29, 6, 45, tzinfo=pytz.utc), 0.2825],
    [datetime.datetime(2013, 1, 29, 7, 0, tzinfo=pytz.utc), 0.1425],
    [datetime.datetime(2013, 1, 29, 7, 15, tzinfo=pytz.utc), 0.1425],
    [datetime.datetime(2013, 1, 29, 7, 30, tzinfo=pytz.utc), 0.1425],
    [datetime.datetime(2013, 1, 29, 7, 45, tzinfo=pytz.utc), 0.1425],
    [datetime.datetime(2013, 1, 29, 8, 0, tzinfo=pytz.utc), 0.1425],
    [datetime.datetime(2013, 1, 29, 8, 15, tzinfo=pytz.utc), 0.1425],
    [datetime.datetime(2013, 1, 29, 8, 30, tzinfo=pytz.utc), 0.1425],
    [datetime.datetime(2013, 1, 29, 8, 45, tzinfo=pytz.utc), 0.1425],
    [datetime.datetime(2013, 1, 29, 9, 0, tzinfo=pytz.utc), 0.1425],
    [datetime.datetime(2013, 1, 29, 9, 15, tzinfo=pytz.utc), 0.1425],
]
