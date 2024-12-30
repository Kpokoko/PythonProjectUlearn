from django import template
import re

register = template.Library()

@register.filter(name='wrap_p')
def wrap_p(value):
    if not re.match(r'^<p>.*</p>$', value.strip()):
        value = f'<p>{value}</p>'
    return value
