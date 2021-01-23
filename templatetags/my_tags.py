from django import template
from django.utils.safestring import mark_safe
register = template.Library()

@register.filter
def my_filter(v1,v2):
    return v1+v2

@register.simple_tag
def my_html_tag(v1):
    temp_html = "<p>%s</p>" %(v1)
    return mark_safe(temp_html)
