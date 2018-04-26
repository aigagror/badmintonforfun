import json

from django.db import connection
from django.http import HttpResponse

from api.cursor_api import dictfetchall
from ..models import *
from ..cursor_api import *


def get_all_members():
    all = Member.objects.raw("SELECT * FROM api_member")
    members_list = serializeSetOfModels(all)

    context = {
        'members': members_list
    }

    print("finished getting all members")
    return http_response(context)


def member_profile(member_id):
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

    print("finished getting one particular member at " + str(member_id))
    return HttpResponse(json.dumps(results), status=200, content_type="application/json")