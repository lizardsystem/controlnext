import datetime
import logging

from django.test import TestCase

import json
import mock
from pandas import Series
import pytz

try:
    # new style
    from lizard_fewsjdbc.tests.factories import JdbcSourceFactory
except ImportError:
    # old style
    from lizard_fewsjdbc.tests import JdbcSourceF as JdbcSourceFactory

from controlnext.calc_model import CalculationModel
from controlnext.conf import settings
from controlnext.demand_table import DemandTable
from controlnext.fews_data import FewsJdbcDataSource
from controlnext.utils import round_date, mktim
from controlnext.wur_data import WURXMLService, WURJSONService
from controlnext.tests.factories import GrowerInfoFactory, BasinFactory


logger = logging.getLogger(__name__)


w26_0 = mktim(2012, 6, 25, 0, 0)   # monday, 0:00, week 26 (d = 20000)
w27_0 = mktim(2012, 7, 2, 0, 0)    # monday, 0:00, week 27 (d = 20000)

w28_0 = mktim(2012, 7, 9, 0, 0)    # monday, 0:00, week 28 (d = 19000)
w28_5 = mktim(2012, 7, 12, 12, 0)  # middle of week 28

w29_0 = mktim(2012, 7, 16, 0, 0)   # sunday, 0:00, week 29 (d = 18000)
w29_5 = mktim(2012, 7, 19, 12, 0)  # middle of week 29

w30_0 = mktim(2012, 7, 23, 0, 0)   # sunday, 0:00, week 30 (d = 17000)
w30_5 = mktim(2012, 7, 26, 12, 0)  # middle of week 30 (d = 17000)

# TODO: setup dynamically, otherwise tests will fail after a while
wNOW = mktim(2012, 12, 5, 0, 0)
wNOW_5 = mktim(2012, 12, 8, 12, 0)


MOCK_DATA_IMPORT_ERROR = ("error importing %s; you can generate mock data "
                          "files with management command "
                          "'cn_generate_test_data")


def get_rain_mock_data(self, which, _from, to):
    try:
        module_name = "controlnext.tests.data.rain_%s_data" % which
        data_module = __import__(
            module_name, fromlist=["controlnext.tests.data"])
    except ImportError, info:
        msg = MOCK_DATA_IMPORT_ERROR % module_name
        error_msg = "%s (%s)" % (msg, info)
        logger.error(error_msg)
        raise Exception(error_msg)
    data_dict = dict(data_module.DATA)
    return Series(data_dict)


def get_fill_mock_data(self, _from, to):
    try:
        from controlnext.tests.data.fill_data import DATA
    except ImportError, info:
        module_name = "controlnext.tests.data.fill_data"
        msg = MOCK_DATA_IMPORT_ERROR % module_name
        error_msg = "%s (%s)" % (msg, info)
        logger.error(error_msg)
        raise Exception(error_msg)
    data_dict = dict(DATA)
    return Series(data_dict)


class DemandTableTest(TestCase):
    def setUp(self):
        tbl = DemandTable()
        self.tbl = tbl

    def test_full_week_linear(self):
        res = self.tbl.get_total_demand(w26_0, w27_0)
        expected = self.tbl.get_demand_for_week(26)
        self.assertAlmostEqual(res, expected, delta=200)

    def test_half_week(self):
        res = self.tbl.get_total_demand(w28_0, w28_5)
        expected = self.tbl.get_demand_for_week(28) / 2
        self.assertAlmostEqual(res, expected, delta=500)

    def test_full_week(self):
        res = self.tbl.get_total_demand(w28_0, w29_0)
        expected = self.tbl.get_demand_for_week(28)
        self.assertAlmostEqual(res, expected, delta=500)

    def test_full_week2(self):
        res = self.tbl.get_total_demand(w29_0, w30_0)
        expected = self.tbl.get_demand_for_week(29)
        self.assertAlmostEqual(res, expected, delta=500)


class CalculationModelTest(TestCase):

    def setUp(self):
        tbl = DemandTable()
        self.tbl = tbl

        jdbc_source = JdbcSourceFactory.create(
            connector_string=('jdbc:vjdbc:rmi://p-fews-jd-d3.external-nens.'
                              'local:2001/VJdbc,FewsDataStore'),
            customfilter='',
            filter_tree_root='',
            jdbc_tag_name='controlnext_delfland',
            jdbc_url=('jdbc:vjdbc:rmi://p-fews-jd-d3.external-nens.local:2001'
                      '/VJdbc,FewsDataStore'),
            name='controlnext',
            slug='controlnext',
            usecustomfilter=False,
            timezone_string='UTC'
        )
        self.grower_info = GrowerInfoFactory.create(jdbc_source=jdbc_source)

        basin = BasinFactory.create(owner=self.grower_info,
                                    jdbc_source=jdbc_source)
        ds = FewsJdbcDataSource(basin)
        self.ds = ds
        self.model = CalculationModel(tbl, ds)

    @mock.patch('controlnext.fews_data.FewsJdbcDataSource.get_fill',
                get_fill_mock_data)
    @mock.patch('controlnext.fews_data.FewsJdbcDataSource.get_rain',
                get_rain_mock_data)
    def test_calc_model(self):
        now = mktim(2012, 8, 5, 8, 0)  # some rain fell here
        now = round_date(datetime.datetime.now(tz=pytz.utc))
        future = now + settings.CONTROLNEXT_FILL_PREDICT_FUTURE

        ts = self.model.predict_fill(now, future, 20, 100, 100)

        self.assertGreater(len(ts['scenarios']['mean']['prediction']), 10)


def get_wur_service_mock_data(self):
    try:
        from controlnext.tests.data.wur_response_data import DATA
    except ImportError, info:
        module_name = "controlnext.tests.data.wur_response_data"
        msg = MOCK_DATA_IMPORT_ERROR % module_name
        error_msg = "%s (%s)" % (msg, info)
        logger.error(error_msg)
        raise Exception(error_msg)
    return DATA


def get_wur_json_service_mock_data(self, url):
    try:
        from controlnext.tests.data.wur_response_from_json import DATA
    except ImportError, info:
        module_name = "controlnext.tests.data.wur_response_from_json"
        msg = MOCK_DATA_IMPORT_ERROR % module_name
        error_msg = "%s (%s)" % (msg, info)
        logger.error(error_msg)
        raise Exception(error_msg)
    return DATA


class WURServiceTests(TestCase):

    def setUp(self):
        now = datetime.datetime.now()
        _from = now - datetime.timedelta(days=2)
        to = now
        self.xml_service = WURXMLService(_from, to)

    # TODO: mock suds response with wur_response.xml
    @mock.patch('controlnext.wur_data.WURXMLService.get_data',
                get_wur_service_mock_data)
    def test_get_data(self):
        data = self.xml_service.get_data()
        self.assertEqual(len(data), 48)  # 2 days

    @mock.patch('controlnext.wur_data.WURJSONService.get_data_from_url',
        get_wur_json_service_mock_data)
    def test_json_service(self):
        start_date = datetime.datetime(2013, 1, 1)
        end_date = datetime.datetime(2013, 1, 2)
        json_service = WURJSONService(start_date, end_date)
        data = json_service.get_data()
        self.assertGreater(len(data), 0)
