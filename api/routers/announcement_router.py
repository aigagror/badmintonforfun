from api.calls.announcement_call import get_announcements
from api.routers.router import restrictRouter
from api.routers.router import validate_keys


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
        validate_keys(["id"], dict_post)


@restrictRouter(incomplete=["POST"])
def create_announcement(request):
    """
    POST - Creates an announcement
    :param request:
    :return:
    """
    foo = 0