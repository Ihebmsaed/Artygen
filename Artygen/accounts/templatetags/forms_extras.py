from django import template

register = template.Library()

@register.filter
def attr(field, attrs):
    """
    Set attributes on a field.
    Usage: {{ field|attr:"class:form-control,placeholder:Your Placeholder" }}
    """
    attrs_dict = dict(item.split(":") for item in attrs.split(","))
    for key, value in attrs_dict.items():
        field.field.widget.attrs[key] = value
    return field
