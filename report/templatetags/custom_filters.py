from django import template

register = template.Library()

@register.filter(name='hours_minutes')
def hours_minutes(value):
    if value is None:
        return ""
    hours = int(value)
    minutes = int((value - hours) * 60)
    return f"{hours}h {minutes}m"
