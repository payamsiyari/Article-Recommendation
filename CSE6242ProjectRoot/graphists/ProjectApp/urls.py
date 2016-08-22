# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from ProjectApp.views import *

urlpatterns = [
    url(r'^$', MainPageView.as_view(), name='main'),
    url(r'search$', searchFunction_graph, name='searched'),
    url(r'searchList$', searchFunction_list, name='searched'),
    url(r'searchCitation$', searchFunction_citation, name='searched'),
    url(r'getCentralNodes$', analyzeFunction_centralNodes, name='searched'),
]