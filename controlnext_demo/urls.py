# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from django.conf import settings
from django.conf.urls import patterns, url
from django.contrib import admin
from lizard_ui.urls import debugmode_urlpatterns

from controlnext_demo import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', views.DemoMainView.as_view(), name='controlnext-demo'),
)

if settings.DEBUG:
    urlpatterns += debugmode_urlpatterns()
