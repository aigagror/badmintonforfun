"""
    Contains the views from the 6.

    Serves the js, css, html, and error pages
"""

from django.shortcuts import render
import os 
from django.http import Http404
from django.http import HttpResponse
from .mod_config import JS_PATH, CSS_PATH, TEMPLATE_PATH, MOCK_PATH, STATIC_PATH
import os.path
from badminton_server.settings import DEBUG
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from api.utils import MemberClass, get_member_class, id_for_member


def _file_or_error(file_name, ret_type=str):
    """
        Either loads the absolute path as either
        a str or a sequence of bytes.

        If the file is not found, it raises a 404.
    """

    if ret_type == str:
        read_type = "r"
    elif ret_type == bytes:
        read_type = "rb"
    else:
        raise TypeError("ret_type can onlt be str or bytes")
    try:
        with open(file_name, read_type, encoding="utf8") as f:
            return f.read()

    except FileNotFoundError:
        raise Http404("File does not exist")

def js_server(request, js_file):
    """
        Serves files from the js folder. Sets the content
        type to text/js as well.

        :param request: HttpRequest Standard django request object
        :param data: str JS to serve
    """
    file_name = os.path.join(JS_PATH, js_file)
    content = _file_or_error(file_name)

    return HttpResponse(content, content_type="text/js")


def css_server(request, css_file):
    """
        Serves files from the css folder. Sets the content
        type to text/css as well.

        :param request: HttpRequest Standard django request object
        :param data: str CSS to serve
    """

    file_name = os.path.join(CSS_PATH, css_file)
    content = _file_or_error(file_name)
    return HttpResponse(content, content_type="text/css")

def static_server(request, static_file):
    """
        Serves all static files. These are all images,
        audio, video etc... It tries to make an intelligent
        guess about the ending resource and what application type
        to set using the extension on the file but may 
        fail for the more exotic ones.

        We can't use the standard django loader because our
        directory structure is so weird, so we roll our own.

        :param request: HttpRequest Standard django request object
        :param data: str resource to serve
    """

    file_name = os.path.join(STATIC_PATH, static_file)
    content = _file_or_error(file_name, ret_type=bytes)
    mappings = {
        '.png': 'image/png',
        '.jpg': 'image/jpg',
        '.jpeg': 'image/jpeg',
    }
    file_type = os.path.splitext(static_file)[-1]
    print(file_type)
    if file_type in mappings:
        content_type = mappings[file_type]
    else:
        content_type = None

    return HttpResponse(content, content_type=content_type)

public_templates = ['index.html', 'interested.html', 'registered.html']

def _get_template_name(template):
    if template is None:
        template = "index.html"

    # Don't need the .html
    if not template.endswith('.html'):
        template += '.html'
    return template

@ensure_csrf_cookie
def _bypass_template_server(request, template, ensure_cookie=True):
    """
        This function takes the template string and renders
        and serves the template that has the same name.

        The function does forward any request.GET parameters.
        request.POST params are not considered because ideally
        we want all front end applications to be reversible,
        meaning that users' back function works. i.e. we shouldn't
        be rendering sensitive data but letting the api validate it
        asynchronously.

        :param request: HttpRequest Standard django request object
        :param data: str Template to render
    """

    # Forward all query params to the template
    # Flatten lists because django gives you query params
    # in lists regardless
    context = dict()
    if request.GET:
        context = dict(request.GET)
    for key, value in context.items():
        if isinstance(value, list) and len(value) == 1:
            context[key] = value[0]
    response = render(request, template, context=context)
    if ensure_cookie:
        email = request.user.email
        response.set_cookie('member_id', str(id_for_member(email)))
        is_board = "true" if get_member_class(email) == MemberClass.BOARD_MEMBER else "false"
        response.set_cookie('is_board_member', is_board)
    return response

@login_required
def _login_template_server(request, template):
    return _bypass_template_server(request, template)

def template_server(request, template=None):
    template = _get_template_name(template)
    if template in public_templates:
        return _bypass_template_server(request, template, ensure_cookie=False)
    else:
        return _login_template_server(request, template)

def mock_api(request, data):
    """
        Module to mock the api. This will be removed when the actual API
        is up and running. All api is simply reading in the dist/mock/
        folder and outputting it as application/json format. If the file
        is not valid json, it immediately becomes text and errors out.
        This is useful for validating the mock data.

        :param request: HttpRequest Standard django request object
        :param data: str Resource to grab from the mock directory
    """

    file_name = os.path.join(MOCK_PATH, data)
    content = _file_or_error(file_name)
    return HttpResponse(content, content_type="application/json")


# Rerouting all the normal requests to our special directory structure
# TODO: have the servers send different responses based on the user agent
# i.e. if it is a web browser send the html but for axios just sent the header

def handle_404(request, exception, template_name='404.html'):
    return template_server(template_name)

def handle_500(request, exception, template_name='500.html'):
    return template_server(template_name)

def handle_403(request, exception, template_name='403.html'):
    return template_server(template_name)

def handle_400(request, exception, template_name='400.html'):
    return template_server(template_name)


