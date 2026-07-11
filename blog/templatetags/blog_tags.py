from django import template
from django.utils.safestring import mark_safe
import markdown as md

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
    if not text:
        return ""
    # Configure markdown extensions for a developer-friendly rich blogging experience
    # includes code fences, table support, and auto-links.
    html = md.markdown(text, extensions=['fenced_code', 'tables', 'extra', 'codehilite'])
    return mark_safe(html)
