from api.calls.match_call import get_top_players, create_match as get_create_match, edit_match as get_edit_match
from api.calls.match_call import find_current_match_by_member, delete_match as get_delete_match, finish_match as get_finish_match
from api.routers.router import restrictRouter
from .router import validate_keys, http_response
import json
from django.views.decorators.csrf import csrf_exempt
from django.db import connection, IntegrityError, ProgrammingError
from api.cursor_api import dictfetchall
import json
from django.http import HttpResponse
from api.routers.router import validate_keys, restrictRouter


@restrictRouter(allowed=["GET"])
def get_profile(request):
    """
        input:
        {
            "id": int # Needs to be a valid member
        }
    """
    params = request.GET
    id_key = 'id'
    if not id_key in params:
        return HttpResponse('Required param {} type integer not given'.format(id_key), status=400)
    member_id = params[id_key]
    with connection.cursor() as cursor:
        query = '''
        SELECT bio, first_name, last_name
        FROM api_member
        JOIN api_interested ON api_member.interested_ptr_id = api_interested.id
        WHERE id=%s
        LIMIT 1;
        '''
        cursor.execute(query, [member_id])
        res = dictfetchall(cursor)
        if len(res) == 0:
            return HttpResponse('Member id {} not found'.format(member_id), status=400)
        results = res[0]
    print(results)
    return HttpResponse(json.dumps(results), status=200, content_type="application/json")

@restrictRouter(allowed=["GET"])
def get_profile(request):
    """
        input:
        {
            "id": int # Needs to be a valid member
        }
    """
    params = request.GET
    id_key = 'id'
    if not id_key in params:
        return HttpResponse('Required param {} type integer not given'.format(id_key), status=400)
    member_id = params[id_key]
    with connection.cursor() as cursor:
        query = '''
        SELECT bio, first_name, last_name
        FROM api_member
        JOIN api_interested ON api_member.interested_ptr_id = api_interested.id
        WHERE id=%s
        LIMIT 1;
        '''
        cursor.execute(query, [member_id])
        res = dictfetchall(cursor)
        if len(res) == 0:
            return HttpResponse('Member id {} not found'.format(member_id), status=400)
        results = res[0]
    print(results)
    return HttpResponse(json.dumps(results), status=200, content_type="application/json")