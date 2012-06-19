# -*- coding: utf-8 -*-

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from urlwrapper.utils import Parser

register = template.Library()


@stringfilter
def wrap_urls(value):
    parser = Parser(20);
    p_result = parser.parse(value)
    return mark_safe(p_result.html)

register.filter(wrap_urls)
