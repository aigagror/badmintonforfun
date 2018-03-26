from api.calls.announcement_call import *
from api.routers.router import restrictRouter
from api.routers.router import validate_keys

_id_key = "id"
_datetime_key = "datetime"
_title_key = "title"
_entry_key = "entry"

@restrictRouter(incomplete=["GET", "POST"])
def announcements(request):
    """
    GET - Get the 3 latest announcements
    POST - Edit an announcement
    :param request:
    :return:
    """
    if request.method == "GET":
        return get_announcements()
    elif request.method == "POST":

        dict_post = dict(request.POST.items())
        validate_keys([_id_key], dict_post)
        return edit_announcement(dict_post[_id_key], dict_post[_title_key], dict_post[_entry_key])



@restrictRouter(incomplete=["POST"])
def create_announcement(request):
    """
    POST - Creates an announcement
    :param request:
    :return:
    """
    dict_post = dict(request.POST.items())
    validate_keys([_datetime_key, _title_key, _entry_key], dict_post)
    create_announcement(dict_post[_datetime_key], dict_post[_title_key], dict_post[_entry_key])