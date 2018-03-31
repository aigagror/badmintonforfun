from django.http import HttpResponse

from api.calls.election_call import get_votes_from_member, cast_vote, get_all_votes
from api.cursor_api import deserializeDate
from api.routers.router import restrictRouter


@restrictRouter(allowed=["GET", "POST"])
def vote(request):
    """
    GET -- Gets votes of given member
        Required Keys: id
    POST -- Casts/updates a vote for the current election
        Required Keys: voter, campaign
    :param request:
    :param job:
    :return:
    """

    if request.method == "GET":
        dict_get = dict(request.GET.items())
        idKey = "id"
        if idKey not in dict_get:
            return HttpResponse("Missing required param {}".format(idKey), status=400)
        id = dict_get[idKey]
        return get_votes_from_member(id)
    elif request.method == "POST":
        dict_post = dict(request.POST.items())
        voterKey = "voter"
        campaignKey = "campaign"
        keys = [voterKey, campaignKey]
        for key in keys:
            if key not in dict_post:
                return HttpResponse("Missing required param {}".format(key), status=400)

        voter_id = dict_post[voterKey]
        campaign_id = int(dict_post[campaignKey])
        return cast_vote(voter_id, campaign_id)


@restrictRouter(allowed=["GET"])
def all_votes(request):
    """
    GET - Gets all votes of the current campaign
        Required Keys: None
    :param request:
    :return:
    """
    return get_all_votes()