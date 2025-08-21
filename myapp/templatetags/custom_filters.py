from django import template
import json

register = template.Library()

@register.filter
def get_item(value, key):
    """Handles dictionary lookups and JSON parsing if necessary."""
    if isinstance(value, str):  
        try:
            value = json.loads(value)  # Convert string to dictionary
        except json.JSONDecodeError:
            return None  # Return None if JSON is invalid
    
    if isinstance(value, dict):
        return value.get(str(key), None)  # Ensure key is a string
    
    return None  # If not a dictionary, return None


@register.filter
def subtract(value, arg):
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return value
    

@register.filter
def add(value, arg):
    try:
        return int(value) + int(arg)
    except (ValueError, TypeError):
        return value  


@register.filter
def safe_number(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0



@register.filter(name="join_name")
def join_name(value, arg):
    """
    Safely concatenate two strings with a space in between.
    Example: {{ "LEO"|join_name:"CARLES" }} → "LEO CARLES"
    """
    if value is None:
        value = ""
    if arg is None:
        arg = ""
    return f"{value} {arg}".strip()