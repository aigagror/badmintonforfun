from api.calls.match_call import get_top_players, create_match as get_create_match, edit_match as get_edit_match
from api.calls.match_call import find_current_match_by_member, delete_match as get_delete_match, finish_match as get_finish_match
from api.calls.match_call import join_match as get_join_match, leave_match as get_leave_match
from django.contrib.auth.decorators import login_required
from api.routers.router import restrictRouter
from .router import validate_keys, http_response, auth_decorator, get_member_id_from_email, get_match_from_member_id
import json
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from api.cursor_api import dictfetchall, serializeDict, serializeSetOfModels, serializeModel
from django.http import HttpResponse
from api.models import *
from api.utils import MemberClass
from api.routers.router import auth_decorator

@auth_decorator(allowed=MemberClass.MEMBER)
@restrictRouter(allowed=["GET"])
def top_players(request):
    """
    GET -- Gets the top 5 players
        Required Keys: None
    :param request:
    :return:
    """
    return get_top_players()


@restrictRouter(allowed=["POST"])
def edit_match(request):
    """
    POST -- edits the match score, provide the score of the match
        Required Keys: id (match ID), score_A, score_B
    :param request:
    :return:
    """

    dict_post = dict(request.POST.items())
    validate_keys(["score_A", "score_B", "id"], dict_post)
    return get_edit_match(dict_post["id"], dict_post["score_A"], dict_post["score_B"])


@auth_decorator(allowed=MemberClass.MEMBER)
@restrictRouter(allowed=["POST"])
def finish_match(request):
    """
    POST -- ends the match (edits match score, removes court id, adds endDateTime)
            and adds 10 points to the level of all members of the winning team.
        RequiredKeys: scoreA, scoreB
    :param request:
    :return:
    """

    member_id = get_member_id_from_email(request.user.email)

    dict_post = dict(request.POST.items())
    if not validate_keys(["scoreA", "scoreB"], dict_post):
        return http_response(message='missing keys', code=400)
    if 'match_id' in dict_post:
        match_id = int(dict_post['match_id'])
    else:
        match_id = get_match_from_member_id(member_id)
    return get_finish_match(match_id, dict_post["scoreA"], dict_post["scoreB"])


@login_required
@auth_decorator(allowed=MemberClass.MEMBER)
@restrictRouter(allowed=["POST"])
def join_match(request):
    """
        POST -- lets a single player join a match on a particular team's side
            Required Keys: team
    :param request:
    :return:
    """
    member_id = get_member_id_from_email(request.user.email)
    dict_post = dict(request.POST.items())
    validate_keys(["match_id", "team"], dict_post)
    return get_join_match(dict_post["match_id"], member_id, dict_post["team"])


@login_required
@auth_decorator(allowed=MemberClass.MEMBER)
@restrictRouter(allowed=["POST"])
def leave_match(request):
    """
        POST -- lets a player leave a match
            Required Keys: match_id
    :param request:
    :return:
    """
    member_id = get_member_id_from_email(request.user.email)
    dict_post = dict(request.POST.items())
    print(dict_post)
    validate_keys(["match_id"], dict_post)
    return get_leave_match(dict_post["match_id"], member_id)

@login_required
@restrictRouter(allowed=["POST"])
def start_match(request):
    """
    POST -- create a match
        PLEASE PASS IN AS RAW DATA.
        All sorts of things get real angry if you don't
        Required Keys: score_A, score_B, a_players (list), b_players (list)
    :param request:
    :return:
    """

    dict_post = json.loads(request.body.decode('utf8').replace("'", '"'))
    # write something to make sure a_players and b_players are lists
    if not validate_keys(["a_players", "b_players", 'court_id'], dict_post):
        return http_response(message='missing keys', code=400)
    return get_create_match(dict_post["a_players"],
        dict_post["b_players"], dict_post["court_id"])


@login_required
@restrictRouter(allowed=["DELETE"])
def delete_match(request):
    """
    :param request:
    :return:
    """

    # django doesn't have anything that handles delete so...
    dict_delete = json.loads(request.body.decode('utf8').replace("'", '"'))
    if not validate_keys(["id"], dict_delete):
        return http_response(json.dumps({'message': 'Missing parameters'}),
                    content_type='application/json', status=400)
    return get_delete_match(dict_delete["id"])


@auth_decorator(allowed=MemberClass.MEMBER)
@restrictRouter(allowed=["GET"])
def current_match(request):
    """
        GET -- The current match id of the match the member is playing
    :param request:
    :return:
    """

    member_id = get_member_id_from_email(request.user.email)
    return find_current_match_by_member(member_id)


@auth_decorator(allowed=MemberClass.MEMBER)
@restrictRouter(allowed=["GET"])
def get_match(request):
    """
        GET -- Get the current match id of the match a specific member id is playing
            Required keys: id (id of member you want the match of)
    :param request:
    :return:
    """

    # member_id = request.GET.get('id', None)
    # if member_id is None:
    #     return http_response({}, message="Please pass in an id", code=400)
    dict_get = dict(request.GET.items())
    validate_keys("id", dict_get)

    return find_current_match_by_member(dict_get["id"])


@restrictRouter(allowed=["GET"])
def all_matches(request):

    context = {
        'matches': None
    }

    matches = Match.objects.raw("SELECT * FROM api_match")
    matches_dict = []


    for match in matches:

        match_dict = {
            'match': serializeModel(match),
            'team_a': [],
            'team_b': [],
        }

        # team A
        team_a_playedins = PlayedIn.objects.raw("SELECT * FROM api_playedin WHERE match_id = %s AND team = 'A'", [match.id])

        # team B
        team_b_playedins = PlayedIn.objects.raw("SELECT * FROM api_playedin WHERE match_id = %s AND team = 'B'", [match.id])

        for player_a in team_a_playedins:
            players = Member.objects.raw("SELECT * FROM api_member WHERE id = %s", [player_a.id])
            player = players[0]
            player_dict = serializeModel(player)
            match_dict['team_a'].append(player_dict)

        for player_b in team_b_playedins:
            players = Member.objects.raw("SELECT * FROM api_member WHERE id = %s", [player_b.id])
            player = players[0]
            player_dict = serializeModel(player)
            match_dict['team_b'].append(player_dict)


        matches_dict.append(match_dict)

    context['matches'] = matches_dict

    return http_response(context)



@restrictRouter(allowed=["GET"])
def all_matches_from_member(request):
    """
    """
    member_id = request.GET.get('id', None)
    if member_id is None:
        return http_response({}, message="Please pass in a member id", code=400)

    playedins = PlayedIn.objects.raw("SELECT * FROM api_playedin WHERE member_id = %s", [member_id])

    matches = [p.match for p in playedins]
    ret = []
    for match in matches:
        playedins = PlayedIn.objects.raw("SELECT * FROM api_playedin WHERE match_id = %s", [match.id])
        teamA = []
        teamB = []
        for playedin in playedins:
            member = playedin.member
            serealized_member = serializeModel(member)
            if playedin.team == 'A':
                teamA.append(serealized_member)
            else:
                teamB.append(serealized_member)
        dict = {
            'match': serializeModel(match),
            'team_A': teamA,
            'team_B': teamB,
        }

        ret.append(dict)
    return HttpResponse(json.dumps(ret), content_type="application/json")