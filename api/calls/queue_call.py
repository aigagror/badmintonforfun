from api.cursor_api import *
from api.models import Queue, Party, Member
from api.cursor_api import http_response, dictfetchall
from operator import itemgetter


def get_queues():
    dict = {}
    dict['queues'] = []
    queues = Queue.objects.raw("SELECT * FROM api_queue");
    if len(list(queues)) >= 1:
        for queue in queues:
            queue_dict = {
                "type": queue.type,
                "id": queue.id,
                "parties": []
            }
            parties = Party.objects.raw("SELECT * FROM api_party WHERE queue_id = %s", [queue.id])
            for party in parties:
                party_dict = serializeModel(party)

                members = Member.objects.raw("SELECT * FROM api_member WHERE party_id = %s", [party.id])
                members_dict = [{
                    "first_name": member.first_name,
                    "last_name": member.last_name,
                    "id": member.id
                } for member in members]
                party_dict['members'] = members_dict
                party_dict['num_members'] = len(members_dict)

                queue_dict['parties'].append(party_dict)

            dict['queues'].append(queue_dict)

        return http_response(dict)
    else:
        return http_response({}, message="There are no queues.", code=200)


def get_parties_by_playtime(queue_type):
    """
    Returns the (party_id, member ids, average party playtime) in order of minimum party playtime
    Note: this is probably the Least Effective Way^TM and Least Efficient Way^TM but I can't for the life of me get it
    to work solely in the SQL so if someone can wrap their head around this logic lol
    :param queue_type:
    :return:
    """
    with connection.cursor() as cursor:
        query_members_on_queue = "SELECT DISTINCT api_member.interested_ptr_id AS member_id, api_member.party_id\
                FROM api_party, api_member, api_queue \
                WHERE api_party.id=api_member.party_id AND api_queue.type=%s AND api_party.queue_id=api_queue.id"

        cursor.execute(query_members_on_queue, [queue_type])
        party_members = dictfetchall(cursor)

        query_members_playtime = '''SELECT party_members.member_id, SUM(play_time) AS member_play_time FROM
                                    (SELECT api_playedin.member_id, api_match.id AS match_id,
                                    (julianday(api_match.endDateTime)-julianday(api_match.startDateTime))*8640.0
                                    AS play_time
                                    FROM api_match, api_playedin
                                    WHERE api_playedin.member_id IN
                                    (SELECT DISTINCT api_member.interested_ptr_id AS member_id
                                    FROM api_party, api_member, api_queue
                                    WHERE api_party.id=api_member.party_id AND api_queue.type=%s
                                    AND api_party.queue_id=api_queue.id) AND api_match.id=api_playedin.match_id
                                    GROUP BY api_playedin.member_id, api_match.id) AS party_members
                                    GROUP BY party_members.member_id
                                     '''

        cursor.execute(query_members_playtime, [queue_type])
        members_with_playtime = dictfetchall(cursor)

        save_parties = []
        parties = []
        for i in party_members:
            if i["party_id"] not in save_parties:
                party_dict = {}
                save_parties.append(i["party_id"])
                party_dict["party_id"] = i["party_id"]
                party_list = []
                for k in party_members:
                    if k["party_id"] == party_dict["party_id"]:
                        party_list.append(k["member_id"])
                party_dict["member_ids"] = party_list
                party_dict["avg_time"] = 0
                parties.append(party_dict)

        for i in members_with_playtime:
            for j in parties:
                if i["member_id"] in j["member_ids"]:
                    j["avg_time"] += i["member_play_time"]

        for i in parties:
            i["avg_time"] /= len(i["member_ids"])

        parties = sorted(parties, key=itemgetter('avg_time'))
        serialized_queue = get_queue_by_type(queue_type)
        return http_response({"id": serialized_queue["id"], "type": serialized_queue["type"],
                              "parties": parties}, message='OK')


def delete_queue(id):
    """
        Deletes the queue with id
    :param id:
    :return:
    """

    return run_connection("DELETE FROM api_queue WHERE id=%s", id)


def get_queue_by_id(id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM api_queue WHERE id=%s", [id])
        result = dictfetchone(cursor)
        print(result)
        if result:
            return True
        else:
            return False


def get_queue_by_type(queue_type):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM api_queue WHERE type=%s", [queue_type])
        result = dictfetchone(cursor)
        if result:
            return result
        else:
            return None


def edit_queue(id, type):
    """
        Modifies queue with id to a different type
    :param id:
    :param type:
    :return:
    """
    if get_queue_by_id(id):
        return run_connection("UPDATE api_queue SET type=%s WHERE id=%s", type, id)
    else:
        return http_response({}, message='No queue exists with this id!', code=400)


def create_queue(type):
    """
    :param type:
    :return:
    """

    return run_connection("INSERT INTO api_queue (type) VALUES (%s)", type)