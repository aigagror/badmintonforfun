from django.views.decorators.csrf import csrf_exempt

from api.routers.router import restrictRouter, validate_keys
from api.cursor_api import http_response, run_connection
from api.calls.party_call import create_party as call_create_party

@csrf_exempt
@restrictRouter(allowed=["POST"])
def create_party(request):
    """
    POST -- Creates a party
        Required Keys: queue_id, member_ids
            NOTE: member_ids is a comma separated list of ids to add to the party
    :param request:
    :return:
    """

    post_dict = dict(request.POST.items())
    if not validate_keys(['queue_id', 'member_ids'], post_dict):
        return http_response({}, message="Keys not found", code=400)

    queue_id = int(post_dict['queue_id'])
    member_ids = post_dict['member_ids']
    member_ids = [int(i) for i in member_ids.split(',')]

    response = call_create_party(queue_id, member_ids)
    return response


@restrictRouter(allowed=["POST"])
def edit_party(request):
    """
    POST -- Edits a party
        Required Keys: id
        Optional Keys: type, add, remove
            NOTE: `add` and `remove` are lists of
                member id's to add or remove from the party respectively

    DELETE -- Deletes a party
        Required Keys: id
    :param request:
    :return:
    """
    foo = 0