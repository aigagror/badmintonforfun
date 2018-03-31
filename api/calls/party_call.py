from api.calls.queue_call import get_next_on_queue, get_queues as call_get_queues
from api.routers.router import restrictRouter, validate_keys, run_connection
from api.models import Party

def create_party(queue_id, member_ids):

    parties_with_max_id = Party.objects.raw("SELECT * FROM api_party WHERE id = (SELECT MAX(id) FROM api_party)")
    if len(list(parties_with_max_id)) == 0:
        new_id = 0
    else:
        party_with_max_id = parties_with_max_id[0]
        new_id = parties_with_max_id.id + 1

    response = run_connection("INSERT INTO api_party(id, queue_id) VALUES (%s, %s)", new_id, queue_id)
    if response.status_code != 200:
        return response
    for member_id in member_ids:
        response = run_connection("UPDATE api_member SET party_id = %s WHERE interested_ptr_id = %s", new_id, member_id)
        if response.status_code != 200:
            return response

    return response