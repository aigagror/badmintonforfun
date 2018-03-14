"""
    Contains special tags for injecting resources into templates.
    This is useful, so our templates are separated from the resources they represent.

    Another common pattern in this file is that we `mark_safe` fairly often to prevent
    extra levels of escaping. This is alright because we are only compiling our strings
    most of the time. 
"""

from django import template
from ..mod_config import GLOBAL_RESOURCES, FRAGMENTS_PATH
from django.template import Template, Context
import os
from django.utils.safestring import mark_safe

register = template.Library()

# Django templates should be logic-less
# That means that we have a lot of repeated code
# Hopefully they don't change how scripts/css are included :D
script_template = Template('<script src="{{ script_name }}" type="text/javascript"></script>')
script_checksum_template = Template("<script src='{{ script_name }}', checksum='{{ checksum }}'"
"crossorigin='anonymous' type='text/javascript'></script>")
script_anonymous_template = Template("<script src='{{ script_name }}' crossorigin='anonymous' type='text/javascript'></script>")
css_template = Template('<link rel="stylesheet" type="text/css" href="{{ stylesheet }}">')


@register.simple_tag(name="resolve_global")
def resolve_global(resource):
    """
        Resolves a global resource or a library (react, google-auth, etc)
        This has to be configured in badminton.mod_config.GLOBAL_RESOURCES

        If a checksum is given, it is rendered in the script tag along with
        crossorigin anon to let the request go through. If not, then the resource
        has the option of choose anon crossorigin.

        Ideally, we change the class, so we don't have a redundant field.

        :param resource: str Resource of which to fetch the identifier
    """

    if resource not in GLOBAL_RESOURCES:
        raise Exception("Resource not found")

    res = GLOBAL_RESOURCES[resource]
    if not res.checksum:
        if res.anonymous:
            string = script_anonymous_template.render(Context({'script_name': res.url}))
        else:
            string = script_template.render(Context({'script_name': res.url}))
    else:
        string = script_checksum_template.render(Context({'script_name': res.url, 'checksum': res.checksum}))

    return mark_safe(string)

@register.simple_tag(name="resolve_js_local")
def resolve_js_local(resource):
    """
        Resolves a js resource.

        TODO: Put in cache busting based on the last modified time of the file.
        Or if webpack has some nice shortcuts, default to those as the resolver
        (using some kind of globbing for the latest file).
    """

    string = script_template.render(Context({'script_name': './js/' + resource}))
    return mark_safe(string)

@register.simple_tag(name="resolve_css_local")
def resolve_css_local(resource):
    """
        Resolves a css resource.

        TODO: Put in cache busting based on the last modified time of the file.
        Or if webpack has some nice shortcuts, default to those as the resolver
        (using some kind of globbing for the latest file).
    """
    string = css_template.render(Context({'stylesheet': './css/' + resource}))
    return mark_safe(string)

@register.simple_tag(takes_context=True, name="include_fragment")
def include_fragment(context, resource):
    """
        Includes a fragment recursively, rendering it if need be. This is
        one method we need to be careful of injecting, so we don't mark as safe.

        We also need the context recursively in case any of the child templates use
        a variable from a parent template.

        context: The context object
        :param resource: str Template to render
    """

    with open(os.path.join(FRAGMENTS_PATH, resource), "r") as f:
        template = Template(f.read())
        return template.render(context)

@register.simple_tag(name="resolve_api")
def resolve_api(resource):
    """
        Method stub as of now, will probably just be equivalent to resolve or reverse.
        Since these cannot be included in the compiled jsx, we will have to unfortunately
        render them as superglobals in the template. Hopefully there is a library that
        handles this in a clean way. Or we can make a library that creates a global registry
        and we simple request from that when need be.
    """

    resource = "./mock/resource"
    return mark_safe(resource)