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
from api.routers.router import validate_keys, restrictRouter, auth_decorator
from api.utils import MemberClass, get_member_class, id_for_member
from api.calls.member_call import get_all_members


@restrictRouter(allowed=["GET"])
@auth_decorator(MemberClass.MEMBER)
def get_profile(request):
    """
        input:
        {
            "id": int # Needs to be a valid member
        }
    """
    if 'id' not in request.GET:
        return HttpResponse('Required key id not included', status=400)
    member_id = request.GET['id']
    with connection.cursor() as cursor:
        query = '''
        SELECT bio, first_name, last_name, picture
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
    return HttpResponse(json.dumps(results), status=200, content_type="application/json")


@auth_decorator(MemberClass.MEMBER)
@restrictRouter(allowed=["GET"])
def get_members(request):
    """

    :param request:
    :return:
    """

    return get_all_members()
