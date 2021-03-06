# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from django.conf import settings
from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.contrib import admin
from lizard_ui.urls import debugmode_urlpatterns

from controlnext import views


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^redirect/$', views.RedirectAfterLoginView.as_view(),
        name='controlnext-redirect'),
    url(r'^selectbasin/$', views.SelectBasinView.as_view(),
        name='controlnext-selectbasin'),
    url(r'^403Error/$', views.Http403View.as_view(),
        name='controlnext-403error'),
    url(r'^(?P<random_url_slug>\w+)/$', views.BasinView.as_view(),
        name='controlnext-basin'),
    url(r'^data_service/(?P<random_url_slug>\w+)/$',
        views.DataService.as_view(),
        name='controlnext-data-service'),
    url(r'^data_service/(?P<random_url_slug>\w+)/demand/$',
        views.DemandView.as_view(),
        name='controlnext-data-demand'),
    url(r'^$', views.RedirectAfterLoginView.as_view(),
        name='controlnext-redirect'),
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
