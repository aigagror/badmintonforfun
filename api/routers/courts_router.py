from api.utils import MemberClass
from api.calls.courts_call import *
from api.routers.router import *


@auth_decorator(allowed=MemberClass.MEMBER)
@restrictRouter(allowed=["GET"])
def get_courts(request):
    """
    GET -- Gets the info on all the courts. If the "match" attribute is None, then that court is open.
    {
        "courts": [
            {
                "court_id": _,
                "queue_type": _,
                "match": { <- (Can be None)
                    "match_id": _,
                    "teamA": [], <- (Names of members)
                    "teamB": []
                }
            },
            ...
        ]
    }
    :param request:
    :return:
    """
    return get_courts_call()