import bleach
from django import template
from django.conf import settings
from django.forms import fields

register = template.Library()


@register.filter()
def bleach_sanitize(value):
    return bleach.clean(value, tags=settings.BLEACH_ALLOWED_TAGS, attributes=settings.BLEACH_ALLOWED_ATTRIBUTES)