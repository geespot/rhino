from django.conf.urls import patterns, include, url
from django.shortcuts import render_to_response
from django.conf import settings
import os

def index(request):
    template = 'index_compiled.html' if settings.RELEASE else 'index.html'
    walkdir = lambda path : [{'dir': root[len(path):]+'/', 'files': files } for root, _, files in os.walk(path)]

    return render_to_response(template, {
        'js_files': walkdir('rhino/static/js'),
        'less_files': walkdir('rhino/static/css'),
    })

urlpatterns = patterns('',
    url(r'^api/', include('restful.urls')),
    url(r'^', index),
)