from django import template

from guys.views import menu

register = template.Library()


@register.simple_tag()
def get_menu():
    return menu