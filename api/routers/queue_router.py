from api.calls.queue_call import get_parties_by_playtime, create_queue as call_create_queue, \
    get_queues as call_get_queues, dequeue_party_to_court_call
from api.routers.router import restrictRouter, validate_keys, auth_decorator
from ..cursor_api import *
from api.utils import MemberClass

QUEUES = ("CASUAL", "RANKED", "KOTH")


@auth_decorator(allowed=MemberClass.MEMBER)
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

    return dequeue_party_to_court_call(queue_type)


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