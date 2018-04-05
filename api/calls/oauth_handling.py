from api.cursor_api import *
from django.db import connection
from django.http import HttpResponse
from ..models import *
import json

def get_tokens(code):
    return None