#coding=utf-8

from restful import register_api, register_processor
from restful import Processor, get_processor, default_processors
from exceptions import APIError

from datetime import datetime
import json


def api(func=None, name=None, **kwargs):
    input_processors = []
    input_processors += default_processors
    for k, v in kwargs.iteritems():
        is_default = False
        for default_processor in default_processors:
            if default_processor.name == k and not v:
                input_processors.remove(default_processor)
                is_default = True
        if not is_default:
            processor = get_processor(k, v)
            if processor:
                input_processors.append(processor)

    output_processors = list(input_processors)
    output_processors.reverse()

    def decorator(api_func):
        api_name = api_func.__name__ if not name else name
        api_info = {
            'name': api_name,
            'module': api_func.__module__,
            'function': api_func,
            'params': api_func.func_code.co_varnames[:api_func.func_code.co_argcount],
            'doc': api_func.__doc__,
            'input_processors': input_processors,
            'output_processors': output_processors,
        }
        register_api(api_name, api_info)
        return api_func

    if func:
        return decorator(func)

    return decorator

def processor(Cls):
    register_processor(Cls)
    return Cls

@processor
class ContextProcessor(Processor):
    name = 'context'
    default = True

    def process_input(self, request, params, api_info, processor_context):

        if 'request' in api_info['params']:
            params['request'] = request
        if 'user' in api_info['params']:
            params['user'] = request.user

        kwargs = request.REQUEST
        for k, v in kwargs.iteritems():
            if k in api_info['params']:
                params[k] = v

@processor
class StatProcessor(Processor):
    name = 'stats'
    default = True

    def process_input(self, request, params, api_info, processor_context):
        from models import CallingRecord
        record = CallingRecord()
        record.session_id = request.session.session_key if request.session.session_key else ''
        record.user_id = request.user.object_id if request.user.is_authenticated() else 0
        record.client_ip = request.META['HTTP_X_REAL_IP'] if request.META.has_key('HTTP_X_REAL_IP') else request.META['REMOTE_ADDR']
        record.api_name = api_info['name']

        vp = dict(params)
        if vp.has_key('request'): vp.pop('request')
        if vp.has_key('user'): vp.pop('user')
        record.input_params = json.dumps(vp)[:200]

        processor_context['begin'] = datetime.now()
        processor_context['record'] = record


    def process_output(self, result, processor_context):
        processor_context['end'] = datetime.now()
        process_time = processor_context['end']-processor_context['begin']
        record = processor_context['record']
        record.status_code = 200
        record.process_time = process_time.total_seconds()*1000
        print record.process_time
        record.response_length = len(result) if result else 0
        record.save()
        return result

    def process_error(self, ex, processor_context):
        processor_context['end'] = datetime.now()
        process_time = processor_context['end']-processor_context['begin']
        record = processor_context['record']
        record.status_code = ex.status
        record.process_time = process_time.total_seconds()*1000
        record.response_length = -1
        record.save()

@processor
class JsonProcessor(Processor):
    name = 'json'
    default = True

    def process_output(self, result, processor_context):
        return json.dumps(result)

@processor
class AuthProcessor(Processor):
    name = 'auth'

    def process_input(self, request, params, api_info, processor_context):
        if self.value and not request.user.is_authenticated():
            raise APIError(403, u'Not authenticated')

    def labels(self):
        if self.value:
            return [u'Need Auth']

@processor
class ConvertProcessor(Processor):
    name = 'convert'

    def process_input(self, request, params, api_info, processor_context):
        if self.value:
            for k, v in self.value.iteritems():
                if params.has_key(k):
                    params[k] = v(params[k])

    def labels(self):
        if self.value:
            labels = []
            for k, v in self.value.iteritems():
                labels.append(u'%s: %s' % (k, v))
            return labels

@processor
class MethodProcessor(Processor):
    name = 'methods'

    def process_input(self, request, params, api_info, processor_context):
        if self.value and request.method not in self.value:
            raise APIError(403, u'Method not allowed')

    def labels(self):
        if self.value:
            labels = []
            for method in self.value:
                labels.append(u'Need %s' % method)
            return labels

@processor
class CommunicationProcessor(Processor):
    name = 'comm'

    def process_input(self, request, params, api_info, processor_context):
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')

        from hashlib import sha1
        pre_validate = [self.value, timestamp, nonce]
        pre_validate.sort()
        validate = sha1(''.join(pre_validate)).hexdigest()
        if signature != validate:
            raise APIError(status=403, data='signature failed')

from lxml import etree
@processor
class WeixinProcessor(Processor):
    name = 'weixin'

    def to_dict(self, node):
        result = {}
        for sub_node in node.getchildren():
            sub_dict = self.to_dict(sub_node)
            result[sub_node.tag] = sub_dict if sub_dict else sub_node.text
        return result

    def build_node(self, parent, obj):
        if isinstance(obj, basestring):
            parent.text = etree.CDATA(obj)
        elif isinstance(obj, int):
            parent.text = '%d' % obj
        elif isinstance(obj, float):
            parent.text = '%.2f' % obj
        elif isinstance(obj, dict):
            for k, v in obj.iteritems():
                node = etree.Element(k)
                parent.append(node)
                self.build_node(node, v)
        elif isinstance(obj, list):
            for v in obj:
                node = etree.Element('item')
                parent.append(node)
                self.build_node(node, v)
        else:
            parent.text = str(obj)

    def process_input(self, request, params, api_info, processor_context):
        xml = etree.XML(request.body)
        params['message'] = self.to_dict(xml)

    def process_output(self, result, processor_context):
        root = etree.Element('xml')
        self.build_node(root, result)
        xml = etree.tostring(root, encoding='utf8')
        return xml