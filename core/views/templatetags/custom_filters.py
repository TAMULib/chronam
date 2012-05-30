from django import template
from django.template.defaultfilters import stringfilter

from rfc3339 import rfc3339

from chronam.utils import url
from chronam.core.utils import label



register = template.Library()

@register.filter(name='rfc3339')
def rfc3339_filter(d):
    return rfc3339(d)

@register.filter(name='pack_url')
def pack_url(value, default='-'):
    return url.pack_url_path(value, default)

@register.filter(name='label')
def _label(value):
    return label(value)

