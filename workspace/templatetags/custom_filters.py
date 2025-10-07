from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    
    return dictionary.get(key)

@register.filter
def add_class(field, css_class):
    
    return field.as_widget(attrs={"class": css_class})