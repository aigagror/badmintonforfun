from django.db import connection
from api.cursor_api import *
from django.http import HttpResponse
import json

def get_announcements():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM api_announcement ORDER BY date DESC LIMIT 3;")
        results = dictfetchall(cursor)

    return HttpResponse(json.dumps(results), content_type='application/json')

def create_announcement(datetime, title, entry):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO api_announcement(date, title, entry) VALUES(%s, %s, %s)", [serializeDateTime(datetime, )])
        results = dictfetchall(cursor)

    return HttpResponse(json.dumps({"message": "Successfully created an announcement"}), content_type='application/json')
