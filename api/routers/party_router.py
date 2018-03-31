from django.views.decorators.csrf import csrf_exempt

from api.routers.router import restrictRouter, validate_keys
from api.cursor_api import http_response, run_connection
from api.calls.party_call import create_party as call_create_party, delete_party, edit_party as call_edit_party

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

@csrf_exempt
@restrictRouter(allowed=["POST"])
def edit_party(request):
    """
    POST -- Edits or deletes a party
        Required Keys: id, delete
        Optional Keys: queue_id, add_members, remove_members
            NOTE: `add_members` and `remove_members` are comma separated lists of
                member id's to add or remove from the party respectively

    :param request:
    :return:
    """

    post_dict = dict(request.POST.items())
    if not validate_keys(['id', 'delete'], post_dict):
        return http_response({}, message="Keys not found", code=400)

    party_id = int(post_dict['id'])
    delete = int(post_dict['delete'])
    if delete == 1:
        return delete_party(party_id)
    else:
        queue_id = int(post_dict.get('queue_id', None))
        add_members = post_dict.get('add_members', None)
        remove_members = post_dict.get('remove_members', None)

        add_members = [int(i) for i in add_members.split(',')] if add_members is not None else None
        remove_members = [int(i) for i in remove_members.split(',')] if remove_members is not None else None

        return call_edit_party(party_id=party_id, queue_id=queue_id, add_members=add_members, remove_members=remove_members)

