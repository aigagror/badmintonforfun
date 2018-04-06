from api.cursor_api import *
from django.db import connection
from django.http import HttpResponse
from ..models import *
import oauth2


def logged_in(code):
    tokens = get_tokens(code)

    return True


def get_tokens(code):
    return None