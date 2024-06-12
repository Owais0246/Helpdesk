"""
Django template filter for retrieving a value from a dictionary.

This module defines a custom template filter called 'get_item' that can be used in Django templates
to retrieve a value from a dictionary given a key.

Usage:
In a Django template, load the template library containing this filter and use it as follows:
    {% load <your_template_library_name> %}
    {{ your_dictionary|get_item:your_key }}

Parameters:
    dictionary (dict): The dictionary from which to retrieve the value.
    key: The key of the item to retrieve from the dictionary.

Returns:
    The value corresponding to the given key in the dictionary. 
    If the key is not found, returns None.

"""

from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    """
    Retrieve a value from a dictionary.

    Args:
        dictionary (dict): The dictionary from which to retrieve the value.
        key: The key of the item to retrieve from the dictionary.

    Returns:
        The value corresponding to the given key in the dictionary. 
        If the key is not found, returns None.

    """
    return dictionary.get(key)
