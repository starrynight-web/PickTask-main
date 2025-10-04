from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Returns the value for the given key in the dictionary.
    Usage in template: {{ my_dict|get_item:key_variable }}
    """
    return dictionary.get(key, [])