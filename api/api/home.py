from api.models import *
from django.db import connection
from api.cursor import *

# def my_custom_sql(self):
#     with connection.cursor() as cursor:
#         cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
#         cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
#         row = cursor.fetchone()
#
#     return row


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
    if len(member) == 0:
        return {}
    total_matches = get_total_matches(email)
    total_wins = get_total_wins(email)

    return {'matches': total_matches, 'wins': total_wins}

def get_matches(email):
    with connection.cursor() as cursor:
        query = '''
        SELECT * 
        FROM api_playedin, api_match
        WHERE api_playedin.member_id = %s AND api_playedin.match_id = api_match.id
        '''
        cursor.execute(query, [email])
        results = dictfetchall(cursor)
    return results

def get_total_matches(email):
    results = get_matches(email)
    return len(results)

def get_won_matches(email):
    with connection.cursor() as cursor:
        query = '''
                SELECT * 
                FROM api_playedin, api_match
                WHERE api_playedin.member_id = %s AND api_playedin.match_id = api_match.id AND 
                ((api_match.scoreA > api_match.scoreB AND api_playedin.team = 'A') OR (api_match.scoreA > api_match.scoreB AND api_playedin.team = 'A')) 
                '''
        cursor.execute(query, [email])
        results = dictfetchall(cursor)

    return results

def get_total_wins(email):
    results = get_won_matches(email)
    return len(results)

def get_schedule():
    with connection.cursor() as cursor:
        query = '''
        SELECT *
        FROM api_schedule
        '''
        cursor.execute(query)
        results = dictfetchall(cursor)
    return results
