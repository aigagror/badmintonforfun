from .models import *
from django.db import connection

# def my_custom_sql(self):
#     with connection.cursor() as cursor:
#         cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
#         cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
#         row = cursor.fetchone()
#
#     return row

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def dictfetchone(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()
    return dict(zip(columns, row))


def get_announcements():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM api_announcement ORDER BY date DESC;")
        results = dictfetchall(cursor)
    # result = Announcement.objects.raw('SELECT * FROM api_announcement ORDER BY date DESC;')
    return results


def get_member(email):
    # result = Member.objects.get(email=email)
    with connection.cursor() as cursor:
        cursor.execute('SELECT first_name, last_name FROM api_member, api_interested WHERE interested_ptr_id = email AND email=%s;', [email])
        result = dictfetchone(cursor)
    return result

def get_stats(email):
    member = get_member(email)
    if member is None:
        return None
    total_matches = get_total_matches(email)
    total_wins = get_total_wins(email)

    return {'matches': total_matches, 'wins': total_wins}

def get_total_matches(email):
    member = get_member(email)
    # TODO
    return 0

def get_total_wins(email):
    member = get_member(email)
    # TODO
    return 0