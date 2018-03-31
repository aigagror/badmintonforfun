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
        cursor.execute("INSERT INTO api_announcement(date, title, entry) VALUES(%s, %s, %s)", [serializeDateTime(datetime), title, entry])

    return HttpResponse(json.dumps({"message": "Successfully created an announcement"}), content_type='application/json')

def edit_announcement(id, title=None, entry=None):
    title_query = """
    UPDATE api_announcement SET title = %s WHERE id = %s
    """

    entry_query = """
    UPDATE api_announcement SET entry = %s WHERE id = %s
    """

    ret = HttpResponse(json.dumps({"message": "Didn't edit any announcement"}), content_type='application/json', status=400)
    if title is not None:
        ret = run_connection(title_query, title, id)
    if entry is not None:
        ret = run_connection(entry_query, entry, id)

    return ret