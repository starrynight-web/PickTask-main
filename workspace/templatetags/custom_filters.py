from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Template filter to get dictionary item by key
    Usage: {{ my_dict|get_item:key }}
    """
    return dictionary.get(key)

@register.filter
def add_class(field, css_class):
    """
    Add CSS class to form field
    Usage: {{ field|add_class:"form-input" }}
    """
    return field.as_widget(attrs={"class": css_class})