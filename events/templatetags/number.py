from django import template

register = template.Library()

@register.filter
def colside(value):
    if value % 2:
        # odd numbers on the left
        return "left"
    else:
        # even numbers on the right
        return "right"
