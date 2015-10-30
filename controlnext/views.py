# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals
import datetime
import logging

from django.contrib.auth.models import User
from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
from django.http import Http404
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from lizard_ui.views import LoginView
from lizard_ui.views import LogoutView
from lizard_ui.views import UiView
from rest_framework.response import Response as RestResponse
from rest_framework.views import APIView
import pytz

from controlnext import models
from controlnext.calc_model import CalculationModel
from controlnext.conf import settings
from controlnext.evaporation_table import EvaporationTable
from controlnext.fews_data import FewsJdbcDataSource
from controlnext.models import Constants
from controlnext.models import UserProfile
from controlnext.models import is_valid_crop_type
from controlnext.utils import round_date


logger = logging.getLogger(__name__)


def find_basin(random_url_slug):
    try:
        grower = models.GrowerInfo.objects.get(
            random_url_slug=random_url_slug)
        basin = models.Basin.objects.get(grower=grower)
        return basin
    except MultipleObjectsReturned:
        logger.error("Multiple basins found for one grower ({grower}), "
                     "redirected to first.".format(grower=grower.name))
        return models.Basin.objects.filter(grower=grower)[:1].get()
    except ObjectDoesNotExist:
        raise Http404


class DemandView(APIView):
    """Update demands."""

    def post(self, request, random_url_slug):
        try:
            grower = models.GrowerInfo.objects.get(
                random_url_slug=random_url_slug)
        except ObjectDoesNotExist:
            raise Http404
        data = request.POST
        for key in sorted(data.iterkeys()):
            demands = models.WaterDemand.objects.filter(
                **{'grower': grower, 'weeknumber': key})
            for demand in demands:
                if data.get(key) is None:
                    continue
                if demand.demand != float(data[key]):
                    demand.demand = data[key]
                    demand.save()
        return RestResponse(request.POST)


class BasinView(UiView):
    template_name = 'controlnext/basin_detail.html'
    page_title = _('ControlNEXT')

    def get(self, request, random_url_slug, *args, **kwargs):
        self.basin = find_basin(random_url_slug)
        self.random_url_slug = random_url_slug
        if (self.basin.grower.crop and
                is_valid_crop_type(self.basin.grower.crop)):
            self.crop_type = self.basin.grower.crop
        return super(BasinView, self).get(request, *args, **kwargs)

    def current_demand(self):
        return self.demand_table.get(self.current_week())

    def current_week(self):
        now = datetime.datetime.now()
        return now.isocalendar()[1]

    @property
    def demand_table(self):
        table = EvaporationTable(self.basin, None)
        return table.demands_for_gui()

def float_or_none(val):
    try:
        return float(val)
    except TypeError:
        return None


class DataService(APIView):
    JS_EPOCH = datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)

    def datetime_to_js(self, dt):
        if dt is not None:
            return (dt - self.JS_EPOCH).total_seconds() * 1000

    def series_to_js(self, pdseries):
        # bfill because sometimes first element is a NaN
        pdseries = pdseries.fillna(method='bfill')
        return [(self.datetime_to_js(dt), float_or_none(value))
                for dt, value in pdseries.iterkv()]

    def get(self, request, random_url_slug, *args, **kwargs):
        self.basin = find_basin(random_url_slug)
        self.constants = Constants(self.basin)
        graph_type = request.GET.get('graph_type', None)
        hours_diff = request.GET.get('hours_diff', None)  # debug param

        # overridable variables for demo purposes
        rain_flood_surface = request.GET.get('rain_flood_surface', None)

        # debug params
        if not rain_flood_surface:
            rain_flood_surface = request.GET.get('basin_surface', None)
        basin_storage = request.GET.get('basin_storage', None)
        reverse_osmosis = request.GET.get('reverse_osmosis', None)

        if rain_flood_surface:
            try:
                # basic validation, if not integer, default value is used
                # other validations can be put here, like upper bounds
                self.constants.rain_flood_surface = int(rain_flood_surface)
            except ValueError:
                logger.error("invalid value for rain_flood_surface: %s" %
                             rain_flood_surface)
        if basin_storage:
            try:
                # basic validation, if not integer, default value is used
                # other validations can be put here, like upper bounds
                self.constants.max_storage = int(basin_storage)
            except ValueError:
                logger.error("invalid value for basin_storage: %s" %
                             basin_storage)

        if reverse_osmosis:
            try:
                # basic validation, if not integer, default value is used
                # other validations can be put here, like upper bounds
                self.constants.reverse_osmosis = float(reverse_osmosis)
            except ValueError:
                logger.error("invalid value for reverse_osmosis: %s" %
                             reverse_osmosis)
        osmose_till_date = request.GET.get('osmose_date_till', None)
        if osmose_till_date is not None:
            date_format = "%d-%m-%Y"
            self.constants.osmose_till_date = datetime.datetime.strptime(
                osmose_till_date, date_format).date()

        # note: t0 is Math.floor() 'ed to a full quarter
        t0 = round_date(datetime.datetime.now(pytz.utc))
        if hours_diff:
            t0 += datetime.timedelta(hours=int(hours_diff))

        if graph_type == 'rain':
            response_dict = self.rain(t0)
        elif graph_type == 'prediction' or graph_type == 'meter_comparison':
            outflow_open = request.GET.get('outflowOpen', None)
            outflow_closed = request.GET.get('outflowClosed', None)
            outflow_capacity = request.GET.get('outflowCapacity', 0)
            if outflow_open is not None:
                outflow_open = datetime.datetime.fromtimestamp(
                    int(outflow_open) / 1000, pytz.utc)
            if outflow_closed is not None:
                outflow_closed = datetime.datetime.fromtimestamp(
                    int(outflow_closed) / 1000, pytz.utc)
            response_dict = self.prediction(
                t0, outflow_open, outflow_closed, outflow_capacity)
        else:
            table = EvaporationTable(self.basin,
                                     self.constants.rain_flood_surface)
            future = t0 + settings.CONTROLNEXT_FILL_PREDICT_FUTURE
            history = t0 - settings.CONTROLNEXT_FILL_HISTORY
            data = table.get_demand_raw(history, future)
            result = {
                'graph_info': {
                    'data': self.series_to_js(data),
                }
            }
            response_dict = result

        return RestResponse(response_dict)

    def get_demand_table(self):
        # first try to get surface from request
        table = EvaporationTable(self.basin, self.constants.rain_flood_surface)
        return table

    def prediction(self, t0, outflow_open, outflow_closed, outflow_capacity):
        tbl = EvaporationTable(self.basin, self.constants.rain_flood_surface)
        ds = FewsJdbcDataSource(self.basin, self.constants)
        model = CalculationModel(tbl, ds)
        future = t0 + settings.CONTROLNEXT_FILL_PREDICT_FUTURE
        print('future', future)

        prediction = model.predict_fill(t0, future, outflow_open,
                                        outflow_closed, outflow_capacity)
        data = {name: self.series_to_js(scenario['prediction'])
                for name, scenario in prediction['scenarios'].items()}
        data['history'] = self.series_to_js(prediction['history'])
        graph_info = {
            'data': data,
        }
        result = {
            'graph_info': graph_info,
            'overflow_24h': prediction['scenarios']['mean']['overstort_24h'],
            'overflow_5d': prediction['scenarios']['mean']['overstort_5d'],
        }
        return result

    def rain(self, t0):
        _from = t0 - settings.CONTROLNEXT_FILL_HISTORY
        to = t0 + settings.CONTROLNEXT_FILL_PREDICT_FUTURE

        ds = FewsJdbcDataSource(self.basin, self.constants)
        mean = ds.get_rain('mean', _from, to)
        sum_ = ds.get_rain('sum', t0, to)
        kwadrant = ds.get_rain('kwadrant', t0, to)

        rain_graph_info = {
            'data': {
                'mean': self.series_to_js(mean),
                'sum': self.series_to_js(sum_),
                'kwadrant': self.series_to_js(kwadrant)
            },
            'x0': self.datetime_to_js(t0)
        }
        return {
            't0': t0,
            'rain_graph_info': rain_graph_info,
        }


class ControlnextLoginView(LoginView):
    default_redirect = "/controlnext/"
    template_name = 'controlnext/controlnextlogin.html'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            login(self.request, form.get_user())
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            username = form.cleaned_data['username']
            user = User.objects.get(username=username)
            try:
                grower_url_slug = UserProfile.objects.get(user=user).grower\
                    .random_url_slug
                next_url = "/controlnext/" + grower_url_slug
            except ObjectDoesNotExist:
                next_url = "/controlnext/login_error"
            return HttpResponseRedirect(next_url)
        return self.form_invalid(form)


class ControlnextLoginErrorView(ControlnextLoginView):
    template_name = 'controlnext/loginerror.html'


class ControlnextLogoutView(LogoutView):
    template_name = 'controlnext/controlnextlogout.html'
    default_redirect = "/controlnext/"