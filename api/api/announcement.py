from django.db import connection
from api.cursor_api import *

def get_announcements():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM api_announcement ORDER BY date DESC;")
        results = dictfetchall(cursor)
    # result = Announcement.objects.raw('SELECT * FROM api_announcement ORDER BY date DESC;')
    return results