from django import template

register = template.Library()

@register.filter
def colside(value):
    if value % 2:
        return "right"
    else:
        # even numbers on the left
        return "left"

@register.filter
def tableno(value):
    return value / 2 + 1
