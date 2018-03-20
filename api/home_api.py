from .models import *
from django.db import connection
from .cursor import *

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
        SELECT match.scoreA as scoreA, match.scoreB as scoreB, match.teamA_id as teamA, match.teamB_id as teamB
        FROM api_match AS match, api_team AS team, api_finishedmatch AS finishedmatch 
        WHERE (match.teamA_id = team.id OR match.teamB_id = team.id) AND (team.member1_id = %s OR team.member2_id = %s) 
              AND match.id = finishedmatch.match_ptr_id
        '''
        cursor.execute(query, [email, email])
        results = dictfetchall(cursor)

        for r in results:
            teamA = r['teamA']
            teamB = r['teamB']

            r['teamA'] = {}
            r['teamB'] = {}
            p1Query = '''
                    SELECT p1.first_name, p1.last_name
                    FROM api_team, api_interested AS p1
                    WHERE api_team.id = %s AND api_team.member1_id = p1.email
                    LIMIT 1
                    '''
            p2Query = '''
                    SELECT p2.first_name, p2.last_name
                    FROM api_team, api_interested AS p2
                    WHERE api_team.id = %s AND api_team.member2_id = p2.email
                    LIMIT 1
                    '''
            cursor.execute(p1Query, [teamA])
            a1 = dictfetchone(cursor)
            r['teamA']['p1'] = a1

            cursor.execute(p2Query, [teamA])
            a2 = dictfetchone(cursor)
            r['teamA']['p2'] = a2

            cursor.execute(p1Query, [teamB])
            b1 = dictfetchone(cursor)
            r['teamB']['p1'] = b1

            cursor.execute(p2Query, [teamB])
            b2 = dictfetchone(cursor)
            r['teamB']['p2'] = b2


    return results

def get_total_matches(email):
    results = get_matches(email)
    return len(results)

def get_won_matches(email):
    with connection.cursor() as cursor:
        query = '''
        SELECT match.scoreA as scoreA, match.scoreB as scoreB, match.teamA_id as teamA, match.teamB_id as teamB
        FROM api_match AS match, api_team AS team, api_finishedmatch AS finishedmatch 
        WHERE ((match.teamA_id = team.id AND match.scoreA > match.scoreB) OR (match.teamB_id = team.id AND match.scoreB > match.scoreA)) 
              AND (team.member1_id = %s OR team.member2_id = %s) 
              AND match.id = finishedmatch.match_ptr_id
        '''
        cursor.execute(query, [email, email])
        results = dictfetchall(cursor)

    return results

def get_total_wins(email):
    results = get_won_matches(email)
    return len(results)