import re

from django import template
from django.urls import reverse, NoReverseMatch


register = template.Library()


@register.simple_tag(takes_context=True)
def active(context, pattern_or_urlname, slug):
    try:
        if slug == '':
            pattern = reverse(pattern_or_urlname)
        else:
            pattern = '^' + reverse(pattern_or_urlname, slug)
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context['request'].path
    if re.search(pattern, path):
        return 'active'
    return ''