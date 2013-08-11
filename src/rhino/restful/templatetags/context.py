
from django.template import Library
register = Library()

@register.filter
def context(value):
    params = list(value)
    if 'user' in params: params.remove('user')
    if 'request' in params: params.remove('request')
    return params