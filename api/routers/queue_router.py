from api.calls.queue_call import get_next_on_queue, create_queue as call_create_queue, get_queues as call_get_queues
from api.routers.router import restrictRouter, validate_keys
from ..cursor_api import http_response
from ..models import QUEUE_TYPE

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

    if request.method == "GET":
        queue_type = request.GET.get('type', None)
        if queue_type is None or queue_type not in QUEUES:
            return http_response({}, message='Please specify a queue type (CASUAL, RANKED, KOTH)', code=400)

        return get_next_on_queue(queue_type)


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