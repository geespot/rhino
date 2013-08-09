#coding=utf-8

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse

from restful import get_api, api_table, docs
from restful.decorators import api
from restful.exceptions import APIError

@api
def help():
    """Get API info table, grouped by modules"""
    return docs.items()

def api_help(request):
    api_root = reverse(api, kwargs={'api_name': ''})
    return render_to_response('restful/doc/help.html', {'api_root': api_root}, RequestContext(request))

def js_client(request, template_name, minify=False):
    import slimit
    api_root = reverse(api, kwargs={'api_name': ''})
    js = render_to_string(template_name, {'root': api_root, 'api_table': api_table})
    if minify: js = slimit.minify(js)
    response = HttpResponse(js)
    response['content-type'] = 'application/javascript'
    return response

def source_file(request, template_name):
    api_root = request.get_host() + reverse(api, kwargs={'api_name': ''})
    source = render_to_string(template_name, {'root': api_root, 'api_table': api_table})
    response = HttpResponse(source)
    response['content-type'] = 'text/plain'
    return response

def ios_client(request):
    import glob, zipfile, os
    from django.conf import settings
    root = os.path.join(settings.STATIC_ROOT, 'restful/RestfulIOSClient')

    output_name = os.tempnam()
    output = zipfile.ZipFile(output_name, 'w')
    directories = ['RestfulIOSClient', 'RestfulIOSClient/en.lproj', 'RestfulIOSClient.xcodeproj']

    for directory in directories:
        p = os.path.join(root, directory)
        for name in glob.glob('%s/*' % p):
            filename = os.path.basename(name)
            output.write(name, os.path.join(directory, filename))

    api_root = request.get_host() + reverse(api, kwargs={'api_name': ''})
    api_files = [
        ('restful/ios/APIClient_h.html', 'RestfulIOSClient/APIClient.h'),
        ('restful/ios/APIClient_m.html', 'RestfulIOSClient/APIClient.m'),
    ]
    for api_template, api_file in api_files:
        name = os.tempnam()
        f = file(name, 'w')
        source = render_to_string(api_template, {'root': api_root, 'api_table': api_table})
        f.write(source)
        f.close()
        output.write(name, api_file)
    output.close()

    f = file(output_name, 'r')
    response = HttpResponse(f.read(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=APIClient.zip'
    f.close()
    os.remove(output_name)

    return response


@csrf_exempt
def api(request, api_name):
    # remove the trailing slash
    if api_name.endswith('/'): api_name = api_name[:-1]
    api_info = get_api(api_name)
    params = {}
    processor_context = {}

    try:
        for processor in api_info['input_processors']:
            processor.process_input(request, params, api_info, processor_context)

        result = api_info['function'](**params)

        for processor in api_info['output_processors']:
            result = processor.process_output(result, processor_context)

        response = HttpResponse(result, status=200)
        response['Content-Length'] = len(result) if result else 0
        return response

    except APIError as ex:
        for processor in api_info['output_processors']:
            processor.process_error(ex, processor_context)
        return HttpResponse(ex.data, status=ex.status)

    except Exception as ex:
        import traceback
        traceback.print_exc()
        return HttpResponse(ex, status=500)
