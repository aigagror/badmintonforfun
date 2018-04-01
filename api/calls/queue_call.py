from api.cursor_api import *
from api.models import Queue, Party, Member
from api.cursor_api import http_response


def get_queues():
    dict = {}
    dict['queues'] = []
    queues = Queue.objects.raw("SELECT * FROM api_queue")
    if len(list(queues)) >= 1:
        for queue in queues:
            queue_dict = serializeModel(queue)
            queue_dict['parties'] = []
            parties = Party.objects.raw("SELECT * FROM api_party WHERE queue_id = %s", [queue.id])
            for party in parties:
                party_dict = serializeModel(party)

                members = Member.objects.raw("SELECT * FROM api_member WHERE party_id = %s", [party.id])
                members_dict = serializeSetOfModels(members)
                party_dict['members'] = members_dict
                party_dict['number of members'] = len(members_dict)

                queue_dict['parties'].append(party_dict)

            dict['queues'].append(queue_dict)

        return http_response(dict)
    else:
        return http_response({}, message="There are no queues.", code=200)

from api.cursor_api import dictfetchall


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


def delete_queue(id):
    """
        Deletes the queue with id
    :param id:
    :return:
    """

    return run_connection("DELETE FROM api_queue WHERE id=%s", id)


def get_queue(id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM api_queue WHERE id=%s", [id])
        result = dictfetchone(cursor)
        print(result)
        if result:
            return True
        else:
            return False


def edit_queue(id, type):
    """
        Modifies queue with id to a different type
    :param id:
    :param type:
    :return:
    """
    if get_queue(id):
        return run_connection("UPDATE api_queue SET type=%s WHERE id=%s", type, id)
    else:
        return http_response({}, message='No queue exists with this id!', code=400)


def create_queue(type):
    """
    :param type:
    :return:
    """

    return run_connection("INSERT INTO api_queue (type) VALUES (%s)", type)