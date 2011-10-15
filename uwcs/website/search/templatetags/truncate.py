from django import template

register = template.Library()

@register.filter
def truncate(value, arg):
    if len(value) < arg:
        return value
    else:
        return value[:arg] + '...'
