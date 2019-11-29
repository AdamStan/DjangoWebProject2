from django import template

# THERE ARE TEMPLATES
register = template.Library()

@register.inclusion_tag('drop_down_button.html')
def dropdown_button(name, *arguments):
    return {
        'name': name,
        'arguments': arguments,
        'arg_len': len(arguments)
    }