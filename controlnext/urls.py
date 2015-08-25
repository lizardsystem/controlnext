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
    url(r'^$', views.ControlnextLoginView.as_view(), name='controlnext-login'),
    url(r'^login_error/$', views.ControlnextLoginErrorView.as_view(), name='controlnext-login-error'),
    url(r'^$', views.ControlnextLogoutView.as_view(), name='controlnext-logout'),
    url(r'^(?P<random_url_slug>\w+)/$', views.BasinView.as_view(),
        name='controlnext-basin'),
    url(r'^data_service/(?P<random_url_slug>\w+)/$',
        views.DataService.as_view(),
        name='controlnext-data-service'),
    url(r'^data_service/(?P<random_url_slug>\w+)/demand/$',
        views.DemandView.as_view(),
        name='controlnext-data-demand'),
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
