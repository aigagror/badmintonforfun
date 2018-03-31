from ..models import *
from ..cursor_api import *

def get_all_members():
    all = Member.objects.raw("SELECT * FROM api_member")
    members_list = serializeSetOfModels(all)
    context = {
        'members': members_list
    }

    return http_response(context)