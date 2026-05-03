import markdown
import nh3
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def render_markdown(text):
    html = markdown.markdown(text)
    return mark_safe(nh3.clean(html))
