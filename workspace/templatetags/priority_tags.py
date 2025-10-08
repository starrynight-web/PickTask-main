from django import template

register = template.Library()

@register.filter
def priority_color(priority):
    """Returns color class based on task priority"""
    color_map = {
        'urgent': 'red',
        'high': 'red',
        'medium': 'yellow',
        'low': 'green'
    }
    return color_map.get(priority, 'gray')