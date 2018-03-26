from api.calls.announcement_call import get_announcements
from api.routers.router import restrictRouter


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


@restrictRouter(incomplete=["POST"])
def create_announcement(request):
    """
    POST - Creates an announcement
    :param request:
    :return:
    """
    foo = 0