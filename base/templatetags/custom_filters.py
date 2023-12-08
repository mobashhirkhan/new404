# custom_filters.py
from django import template

register = template.Library()


@register.filter(name='remove_api')
def remove_api(value):
    """
    Custom template filter to remove the 'api/' prefix from a URL.
    """
    return value.replace('api/', '', 1)
