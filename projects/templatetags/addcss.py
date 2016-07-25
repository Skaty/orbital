from django import template
from django.forms import fields

register = template.Library()


@register.filter(name='addcss')
def addcss(field, css):
   attributes = {'class': css}
   if isinstance(field.field, fields.DateTimeField):
      attributes['class'] += ' bs-datetime'
   return field.as_widget(attrs=attributes)