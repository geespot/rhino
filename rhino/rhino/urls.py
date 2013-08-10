from django.conf.urls import patterns, include, url
from django.shortcuts import render_to_response

urlpatterns = patterns('',
    url(r'^api/', include('restful.urls')),
    url(r'^', lambda req: render_to_response('index.html')),
)
