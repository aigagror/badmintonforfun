from django.db import connection, IntegrityError, ProgrammingError
from api.cursor import *
import json
from django.http import HttpResponse

def get_next_on_queue(queue_type):
    """
    Returns the (party_id, party leader, average party playtime) with the minimum average party playtime
    that is currently on the specified queue
    :param queue_type:
    :return:
    """
    with connection.cursor() as cursor:
        query = '''
        SELECT party.id AS party_id, party.leader_id, AVG (play_time) AS average_party_play_time_seconds
        FROM api_party AS party, api_member AS m1 JOIN 
        (SELECT pin.member_id, SUM((julianday(fm.endDate)-julianday(m2.startDate))*86400.0) AS play_time 
        FROM api_match AS m2 JOIN api_finishedmatch fm JOIN api_playedin AS pin 
        WHERE m2.id=fm.match_ptr_id AND m2.id=pin.match_id AND  date(m2.startDate) > date(julianday()) 
        GROUP BY pin.member_id) 
        WHERE party.id=m1.party_id AND m1.interested_ptr_id=member_id AND party.queue_id = %s 
        GROUP BY party.id ORDER BY play_time ASC LIMIT 1;
        '''
        cursor.execute(query, [queue_type])
        results = dictfetchall(cursor)
    return results
