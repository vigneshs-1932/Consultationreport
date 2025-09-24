import base64
from django import template

register = template.Library()

@register.filter
def b64encode(value):
    """Encode bytes to base64 string"""
    if value is None:
        return ""
    return base64.b64encode(value).decode("utf-8")
