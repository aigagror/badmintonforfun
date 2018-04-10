from django.views.decorators.csrf import csrf_exempt

from api.calls.queue_call import get_parties_by_playtime, create_queue as call_create_queue, get_queues as call_get_queues
from api.routers.router import restrictRouter, validate_keys
from ..cursor_api import *
from ..models import QUEUE_TYPE
from ..models import *
import json

QUEUES = ("CASUAL", "RANKED", "KOTH")


@restrictRouter(allowed=["GET"])
def get_queues(request):
    """
    GET -- Gets the active queues
            Returns a dictionary; "queues" has the queue ID as id, type, and parties in the queue;
            parties have the party ID as id, queue ID as queue, a list of members, and the number of members in
            the party
    :param request:
    :return:
    """
    return call_get_queues()


@restrictRouter(allowed=["GET"])
def next_on_queue(request):
    """
    GET -- The next party on the specified queue to play
        Needs parameter type=one of CASUAL, RANKED, KOTH
        ex: api/queue/party/next/?type=CASUAL
    :param request:
    :return:
    """
    queue_type = request.GET.get('type', None)
    if queue_type is None or queue_type not in QUEUES:
        return http_response({}, message='Please specify a queue type (CASUAL, RANKED, KOTH)', code=400)

    return get_parties_by_playtime(queue_type)


@restrictRouter(allowed=["POST"])
def dequeue_next_party_to_court(request):
    """
    POST -- Dequeues the next party on the specified queue to play
            This function automatically creates a match for the members in the party and assigns
            the match to a court
        Needs parameter type=one of CASUAL, RANKED, KOTH
    :param request:
    :return:
    """
    queue_type = request.POST.get('type', None)
    if queue_type is None or queue_type not in QUEUES:
        return http_response({}, message='Please specify a queue type (CASUAL, RANKED, KOTH)', code=400)

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
        matches = Match.objects.raw("SELECT * FROM api_match WHERE court_id = %s", [court.id])
        if len(list(matches)) == 0:
            # Found an empty court
            found_available_court = True

            # Get the members from the party
            members = Member.objects.raw("SELECT * FROM api_member WHERE party_id = %s", [party_id])

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

            response = run_connection("INSERT INTO api_match(id, startDateTime, court_id, scoreA, scoreB) VALUES (%s, %s, %s, 0, 0)", id_of_new_match, serializeDateTime(now), court.id)
            if response.status_code != 200:
                # Error
                return response

            # Assign teams
            num_members = len(list(members))
            for i in range(num_members):
                team = "A" if i % 2 == 0 else "B"
                member = members[i]
                response = run_connection("INSERT INTO api_playedin(team, match_id, member_id) VALUES (%s, %s, %s)", team, id_of_new_match, member.id)
                if response.status_code != 200:
                    # Error
                    return response

            break
    if found_available_court:
        return response
    else:
        http_response(message="No available courts", code=400)


@restrictRouter(allowed=["POST"])
def create_queue(request):
    """
    POST -- need the queue_type key (CASUAL, RANKED, KOTH)
    :param request:
    :return:
    """

    if request.method == "POST":
        dict_post = dict(request.POST.items())
        validate_keys('queue_type', dict_post)
        return call_create_queue(dict_post["queue_type"])