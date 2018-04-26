from .router import http_response
from api.routers.router import validate_keys, restrictRouter, auth_decorator
from api.utils import MemberClass, id_for_member
from api.calls.member_call import get_all_members, member_profile


@restrictRouter(allowed=["GET"])
@auth_decorator(MemberClass.BOARD_MEMBER)
def view_member_profile(request):
    """
        input:
        {
            "id": int # Needs to be a valid member
        }
    """
    dict_get = dict(request.GET.items())
    if not validate_keys(['id'] in dict_get):
        return http_response(message='Missing id', code=400)

    member_id = int(dict_get['id'])
    return member_profile(member_id)



@restrictRouter(allowed=["GET"])
@auth_decorator(MemberClass.MEMBER)
def get_profile(request):

    member_id = request.GET.get('id', None)
    return member_profile(member_id)


@auth_decorator(MemberClass.MEMBER)
@restrictRouter(allowed=["GET"])
def get_members(request):
    """

    :param request:
    :return:
    """

    return get_all_members()
