from api.routers.router import *
from api.models import *
from django.views.decorators.csrf import ensure_csrf_cookie

_id_key = "id"
_title_key = "title"
_entry_key = "entry"

@restrictRouter(allowed=["GET"])
def get_announcements(request):
    """
    GET - Get the 3 latest announcements
    POST - Edit an announcement
        Required Keys: id
        Optional Keys: datetime, title, entry
    :param request:
    :return:
    """
    announcements = Announcement.objects.raw("SELECT * FROM api_announcement ORDER BY date DESC")
    announcements_list = serializeSetOfModels(announcements)

    context = {
        'announcements': announcements_list
    }
    return http_response(context)

@restrictRouter(allowed=["POST"])
def create_announcement(request):
    """
    POST - Creates an announcement
        Required Keys: title, entry
    :param request:
    :return:
    """
    print(request)
    dict_post = dict(request.POST.items())
    print(dict_post)
    if not validate_keys([_title_key, _entry_key], dict_post):
        return http_response(message='Missing parameters')
    title = dict_post[_title_key]
    entry = dict_post[_entry_key]
    response = run_connection("INSERT INTO api_announcement(date, title, entry) VALUES(%s, %s, %s)", serializeDate(datetime.date.today()), title, entry)
    return response

@restrictRouter(allowed=["POST"])
def edit_announcement(request):
    """
        POST - Creates an announcement
            Required Keys: title, entry, id
        :param request:
        :return:
        """
    dict_post = dict(request.POST.items())
    if not validate_keys([_id_key, _title_key, _entry_key], dict_post):
        return http_response(message='Missing parameters')
    id = dict_post[_id_key]
    title = dict_post[_title_key]
    entry = dict_post[_entry_key]

    response = run_connection("UPDATE api_announcement SET title = %s, entry = %s WHERE id = %s", title, entry, id)
    return response

@restrictRouter(allowed=["POST"])
def delete_announcement(request):
    """
    POST - Deletes an announcement
    :param request:
    :return:
    """
    dict_post = dict(request.POST.items())
    if not validate_keys([_id_key], dict_post):
        return http_response(message='Missing parameters')
    id = dict_post[_id_key]

    response = run_connection("DELETE FROM api_announcement WHERE id = %s", id)
    return response