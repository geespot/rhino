
api_table = {}
processor_table = {}
default_processors = []

docs = {}

class Processor(object):
    default = False

    def __init__(self, value):
        self.value = value

    def process_input(self, request, params, api_info, processor_context):
        return params

    def process_output(self, result, processor_context):
        return result

    def process_error(self, ex, processor_context):
        return

    def labels(self):
        return []

def get_api(api_name):
    return api_table[api_name]

def get_processor(name, value):
    if not processor_table.has_key(name):
        return None

    return processor_table[name](value)

def register_api(api_name, api_info):
    api_table[api_name] = api_info

    module = api_info['module']
    api_list = docs[module]['api_list'] if docs.has_key(module) else []

    labels = []
    for processor in api_info['input_processors']:
        labels += processor.labels()

    api_list.append({
        'name': api_name,
        'params': api_info['params'],
        'doc': api_info['doc'],
        'labels': labels,
    })
    docs[module] = {
        'id': module.replace('.', '_'),
        'url': '#',
        'api_list': api_list,
    }

def register_processor(processor_Cls):
    processor_table[processor_Cls.name] = processor_Cls
    if processor_Cls.default:
        default_processors.append(processor_Cls(True))
