# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from django.conf import settings
from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from django.contrib import admin
from lizard_ui.urls import debugmode_urlpatterns

from controlnext import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', views.DashboardView.as_view(), name='controlnext-dashboard'),
    #url(r'^(?P<basin_id>\d+)/$', views.BasinView.as_view(),
    #    name='controlnext-basin'),
    url(r'^(?P<basin_id>\d+)/$', views.BasinView.as_view(),
        name='controlnext-basin'),
    url(r'^data_service/(?P<basin_id>\d+)/$',
        views.DataService.as_view(),
        name='controlnext-data-service'),
    url(r'^data_service/(?P<basin_id>\d+)/demand/$',
        views.DemandView.as_view(),
        name='controlnext-data-demand'),
    url(r'^data_service/(?P<basin_id>\d+)/save/$',
        views.BasinDataView.as_view(),
        name='controlnext_save_basin_data')
)

if getattr(settings, 'LIZARD_CONTROLNEXT_STANDALONE', False):
    admin.autodiscover()
    urlpatterns += patterns(
        '',
        (r'^ui/', include('lizard_ui.urls')),
        (r'^map/', include('lizard_map.urls')),
        (r'^admin/', include(admin.site.urls)),
    )
    urlpatterns += debugmode_urlpatterns()
