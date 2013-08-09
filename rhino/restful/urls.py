
from django.conf.urls import patterns, url

urlpatterns = patterns('restful.views',
    url(r'^$', 'api_help'),

    url(r'^jquery_client.js$', 'js_client', kwargs={'template_name': 'restful/js/jquery_client.html'}),
    url(r'^jquery_client.min.js$', 'js_client', kwargs={'template_name': 'restful/js/jquery_client.html', 'minify': True}),
    url(r'^angular_client.js$', 'js_client', kwargs={'template_name': 'restful/js/angular_client.html'}),
    url(r'^angular_client.min.js$', 'js_client', kwargs={'template_name': 'restful/js/angular_client.html', 'minify': True}),

    url(r'^APIClient.h$', 'source_file', kwargs={'template_name': 'restful/ios/APIClient_h.html'}),
    url(r'^APIClient.m$', 'source_file', kwargs={'template_name': 'restful/ios/APIClient_m.html'}),
    url(r'^APIClient.zip$', 'ios_client'),

    url(r'^(?P<api_name>\S*)$', 'api'),
)
