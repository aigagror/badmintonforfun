from django import template
from ..mod_config import GLOBAL_RESOURCES, FRAGMENTS_PATH
from django.template import Template, Context
import os
from django.utils.safestring import mark_safe

register = template.Library()

script_template = Template('<script src="{{ script_name }}"></script>')
script_checksum_template = Template("<script src='{{ script_name }}', checkusm='{{ checksum }}'"
"crossorigin='anonymous'></script>")

css_template = Template('<link rel="stylesheet" type="text/css" href="{{ stylesheet }}">')

@register.simple_tag(name="resolve_global")
def resolve_global(resource):
    if resource not in GLOBAL_RESOURCES:
        raise Exception("Resource not found")

    res = GLOBAL_RESOURCES[resource]
    if not res.checksum:
        string = script_template.render(Context({'script_name': res.url}))
    else:
        string = script_checksum_template.render(Context({'script_name': res.url, 'checksum': res.checksum}))

    return mark_safe(string)

@register.simple_tag(name="resolve_js_local")
def resolve_js_local(resource):
    string = script_template.render(Context({'script_name': './js/' + resource}))
    return mark_safe(string)

@register.simple_tag(name="resolve_css_local")
def resolve_css_local(resource):
    string = css_template.render(Context({'stylesheet': './css/' + resource}))
    return mark_safe(string)

@register.simple_tag(takes_context=True, name="include_fragment")
def include_fragment(context, resource):
    with open(os.path.join(FRAGMENTS_PATH, resource), "r") as f:
        template = Template(f.read())
        return template.render(context)