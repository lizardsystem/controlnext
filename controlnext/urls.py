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
    url(r'^ui/', include('lizard_ui.urls')),
    # url(r'^map/', include('lizard_map.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',
        views.MainView.as_view(),
        name='controlnext-main'
    ),
    url(r'^data_service/(?P<data_type>[-a-zA-Z0-9_]+)/$',
        views.DataService.as_view(),
        name='controlnext-data-service'
    ),
    # TEMP
    url(r'^fewsjdbc/', include('lizard_fewsjdbc.urls')),
)

if settings.DEBUG:
    urlpatterns += debugmode_urlpatterns()
