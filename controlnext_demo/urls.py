# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from django.conf import settings
from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from django.contrib import admin
from lizard_ui.urls import debugmode_urlpatterns

from controlnext_demo import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    # url(r'^ui/', include('lizard_ui.urls')),
    # url(r'^map/', include('lizard_map.urls')),
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.DemoMainView.as_view(), name='controlnext-demo'),
    # url(r'^$', views.DashboardView.as_view(), name='controlnext-dashboard'),
#    url(r'^(?P<grower_id>\d+)$', views.GrowerView.as_view(),
#        name='controlnext-grower'),
#    url(r'^data_service/$', views.DataService.as_view(),
#        name='controlnext-data-service'),
#    url(r'^data_service/(?P<grower_id>\d+)/$', views.DataServiceByID.as_view(),
#        name='controlnext-data-service-by-id'),
)

if settings.DEBUG:
    urlpatterns += debugmode_urlpatterns()
