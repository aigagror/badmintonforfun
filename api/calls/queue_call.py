import datetime
import json

from api.cursor_api import *
from api.models import Queue, Party, Member, Court, Match
from api.cursor_api import http_response, dictfetchall, run_connection, serializeDateTime
from operator import itemgetter

"""
    FUNCTIONS: (*) = not sure if works, look at this later
    get_queues() returns an http response
    get_parties_by_playtime(queue_type) returns an http_response
    delete_queue(id) returns an http response
    get_queue_by_id(id) returns a boolean (T/F whether there's a queue with id)
    get_queue_by_type(queue_type) returns a dictionary, or None
    get_queue_type(queue_id) returns a string
    edit_queue(id, type) returns an http response
    create_queue(id) returns an http response
"""


def get_queues():
    """
    Returns a dictionary; "queues" has the queue ID as id, type, and parties in the queue;
            parties have the party ID as id, queue ID as queue, a list of members, and the number of members in
            the party
    :return:
    """
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

            response = get_parties_by_playtime(queue.type)
            content = response.content.decode()
            content = json.loads(content)

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

                response_parties = content['parties']
                curr_party_avg_play_time = 0
                for i in range(len(response_parties)):
                    if response_parties[i]['party_id'] == party.id:
                        curr_party_avg_play_time = round(response_parties[i]['avg_time'], 3)
                        break

                party_dict['average_play_time'] = curr_party_avg_play_time

                queue_dict['parties'].append(party_dict)

            dict['queues'].append(queue_dict)

        print(dict)
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
                                    ORDER BY play_time ASC 
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
                if i["member_id"] in j["member_ids"] and i["member_play_time"] is not None:
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


def get_queue_type(queue_id):
    rawquery = Queue.objects.raw("SELECT * FROM api_queue WHERE id=%s", [str(queue_id)])
    if len(list(rawquery)) == 0:
        return None
    else:
        queue = rawquery[0]
        return str(queue.type)


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


def dequeue_party_to_court_call(queue_type):
    response = get_parties_by_playtime(queue_type)
    my_json = json.loads(response.content.decode())
    parties = my_json['parties']
    if len(parties) == 0:
        return http_response({}, message='No parties on this queue', code=400)
    party_to_dequeue = parties[0]
    party_id = party_to_dequeue['party_id']
    queues = Queue.objects.raw("SELECT * FROM api_queue WHERE type = %s", [queue_type])
    if len(list(queues)) == 0:
        return http_response({}, message='No such queue found', code=400)
    queue = queues[0]
    queue_courts = Court.objects.raw("SELECT * FROM api_court WHERE queue_id = %s", [queue.id])
    if len(list(queue_courts)) == 0:
        return http_response({}, message='No courts available for this queue', code=400)
    found_available_court = False;
    for court in queue_courts:
        if court.match is None:
            # Found an empty court
            found_available_court = True

            # Get the members from the party
            members_query = Member.objects.raw("SELECT * FROM api_member WHERE party_id = %s", [party_id])
            members = []
            for member in members_query:
                member.party = None
                member.save()
                members.append(member)

            # Remove party from queue
            response = run_connection("DELETE FROM api_party WHERE id = %s", party_id)
            if response.status_code != 200:
                # Error
                return response

            # Create match on court
            all_matches = Match.objects.raw("SELECT * FROM api_match")
            largest_id = max([match.id for match in all_matches]) if len(list(all_matches)) > 0 else -1
            id_of_new_match = largest_id + 1

            now = datetime.datetime.now()

            response = run_connection(
                "INSERT INTO api_match(id, startDateTime, scoreA, scoreB) VALUES (%s, %s, 0, 0)",
                id_of_new_match, serializeDateTime(now))
            if response.status_code != 200:
                # Error
                return response

            # Assign teams
            num_members = len(members)
            for i in range(num_members):
                team = "A" if i % 2 == 0 else "B"
                member = members[i]
                response = run_connection("INSERT INTO api_playedin(team, match_id, member_id) VALUES (%s, %s, %s)",
                                          team, id_of_new_match, member.id)
                if response.status_code != 200:
                    # Error
                    return response

            # Add the match to the court
            response = run_connection("UPDATE api_court SET match_id = %s WHERE id = %s", id_of_new_match, court.id)

            break
    if found_available_court:
        return response
    else:
        return http_response(message="No available courts", code=400)


def refresh_all_queues():
    """
    Returns a string of all queues refreshed
    :return:
    """
    queues = Queue.objects.raw("SELECT * FROM api_queue")
    queues_string = ''
    for queue in queues:
        queues_string += '{} '.format(queue.type)
        response = dequeue_party_to_court_call(queue.type)
        while response.status_code == 200:
            response = dequeue_party_to_court_call(queue.type)
    return queues_string