from django.shortcuts import render
import os 
from django.http import Http404
from django.http import HttpResponse
from .mod_config import JS_PATH, CSS_PATH, TEMPLATE_PATH, MOCK_PATH


def _file_or_error(file_name):
    try:
        with open(file_name, "r") as f:
            return f.read()
    except FileNotFoundError:
        raise Http404("File does not exist")


def js_server(request, js_file):
    file_name = os.path.join(JS_PATH, js_file)
    content = _file_or_error(file_name)
    return HttpResponse(content, content_type="text/js")


def css_server(request, css_file):
    file_name = os.path.join(CSS_PATH, css_file)
    content = _file_or_error(file_name)
    return HttpResponse(content, content_type="text/css")


def template_server(request, template=None):
    if template is None:
        template = "index.html"
    return render(request, template)


def mock_api(request, data):
    file_name = os.path.join(MOCK_PATH, data)
    content = _file_or_error(file_name)
    return HttpResponse(content, content_type="application/json")

