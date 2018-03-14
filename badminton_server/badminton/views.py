from django.shortcuts import render
import os 
from django.http import Http404
from django.http import HttpResponse
from .mod_config import JS_PATH, CSS_PATH, TEMPLATE_PATH, MOCK_PATH, STATIC_PATH
import os.path


def _file_or_error(file_name, ret_type=str):
    if ret_type == str:
        read_type = "r"
    else:
        read_type = "rb"
    try:
        with open(file_name, read_type) as f:
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

def static_server(request, static_file):
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


def template_server(request, template=None):
    if template is None:
        template = "index.html"
    if not template.endswith('.html'):
        template += '.html'
    context = dict()
    if request.GET:
        context = dict(request.GET)
    for key, value in context.items():
        if isinstance(value, list) and len(value) == 1:
            context[key] = value[0]
    print(context)
    return render(request, template, context=context)


def mock_api(request, data):
    file_name = os.path.join(MOCK_PATH, data)
    content = _file_or_error(file_name)
    return HttpResponse(content, content_type="application/json")

