from django import template

register = template.Library()


@register.filter
def get_first(list):
    return list[0]