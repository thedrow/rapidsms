#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

from django.conf.urls.defaults import *
from . import views

urlpatterns = patterns('',
    url(r'^$', views.message_templates, name="message_templates"),
    url(r"^(?P<path>.*)$", views.edit_template))
