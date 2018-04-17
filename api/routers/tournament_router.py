import json

from django.views.decorators.csrf import csrf_exempt

from api.calls.tournament_call import *
from api.routers.router import restrictRouter, validate_keys, auth_decorator
from api.models import *
from api.cursor_api import *
from api.utils import MemberClass


@auth_decorator(allowed=MemberClass.MEMBER)
@restrictRouter(allowed=["GET"])
def get_tournament(request):
    return get_most_recent_tournament()


@auth_decorator(allowed=MemberClass.BOARD_MEMBER)
@restrictRouter(allowed=["POST"])
def create_tournament_router(request):
    """
    POST function to create a new tournament entry.
    Expect the input dictionary to be
    {
        "num_players": _
        "tournament_type": _ (DOUBLES, SINGLES)
        "elimination_type": _ (SINGLE)
    }
    :param request:
    :return:
    """
    post_dict = dict(request.POST.items())
    if not validate_keys(["num_players", "tournament_type", "elimination_type"], post_dict):
        HttpResponse(json.dumps({'message': 'Missing parameters num_players or tournament_type'}),
                     content_type='application/json', status=400)
    return create_tournament(post_dict)


@auth_decorator(allowed=MemberClass.BOARD_MEMBER)
@restrictRouter(allowed=["POST"])
def finish_tournament_router(request):
    """
        Finish a tournament on this date.
    Expect the dictionary to be
    {
        "tournament_id": _
    }
    :param request:
    :return:
    """
    post_dict = dict(request.POST.items())
    if not validate_keys(["tournament_id"], post_dict):
        http_response(message="Missing parameter tournament_id", code=400)
    return finish_tournament(post_dict)

@auth_decorator(allowed=MemberClass.MEMBER)
@restrictRouter(allowed=["GET"])
def get_bracket_node(request):
    dict_get = dict(request.GET.items())
    validate_keys(['tournament_id', 'level', 'index'], dict_get)

    tournament_id = int(dict_get['tournament_id'])
    level = int(dict_get['level'])
    index = int(dict_get['index'])

    nodes = BracketNode.objects.raw("SELECT * FROM api_bracketnode WHERE tournament_id = %s AND sibling_index = %s AND level = %s", [tournament_id, index, level])
    if len(list(nodes)) > 0:
        node = nodes[0]
        node_dict = serializeModel(node)
        matches_array = []
        # Get the matches associated with this bracket node
        node_matches = Match.objects.raw("SELECT * FROM api_match WHERE bracket_node_id=%s", [node.id])
        if len(list(node_matches)) > 0:
            for node_match in list(node_matches):
                node_match_dict = serializeModel(node_match)
                matches_array.append(node_match_dict)
        node_dict["matches"] = matches_array
        print("BRACKET NODE DICT: " + str(node_dict))
        context = {
            'bracket_node': node_dict
        }
        return http_response(context)
    else:
        return http_response(message='No such bracket node', code=400)


@auth_decorator(allowed=MemberClass.BOARD_MEMBER)
@restrictRouter(allowed=["POST"])
def add_match(request):
    """
    Start a NEW match and associate it with the specified bracket node.
    'team_A' and 'team_B' are both strings of comma-separated member_id's
    Ex: ("2,3")
    :param request:
    :return:
    """
    post_dict = dict(request.POST.items())
    validate_keys(['bracket_node_id', 'team_A', 'team_B'], post_dict)

    bracket_node_id = int(post_dict['bracket_node_id'])
    team_A_str = post_dict['team_A']
    team_A = team_A_str.split(',')
    team_B_str = post_dict['team_B']
    team_B = team_B_str.split(',')


    # Assert bracket node exists
    nodes = BracketNode.objects.raw("SELECT * FROM api_bracketnode WHERE id=%s", [bracket_node_id])
    if len(list(nodes)) <= 0:
        return http_response(message='Invalid bracket_node_id', code=400)

    return add_match_call(bracket_node_id, team_A, team_B)


@auth_decorator(allowed=MemberClass.BOARD_MEMBER)
@restrictRouter(allowed=["POST"])
def register_member_for_tournament_play(request):
    """
    POST -- Given a member_id, mark the member as participating in a tournament.
    :param request:
    :return:
    """
    post_dict = dict(request.POST.items())
    validate_keys(["member_id"], post_dict)
    member_id = post_dict["member_id"]

    # Check if member is already participating in a tournament
    rawquery = Member.objects.raw("SELECT * FROM api_member WHERE interested_ptr_id=%s", [member_id])
    if len(list(rawquery)) > 0:
        member = rawquery[0]
        if member.in_tournament == 1:
            return http_response(message="Member is already in a tournament", code=400)
    else:
        return http_response(message="Specified member does not exist", code=400)

    return run_connection("UPDATE api_member SET in_tournament=1 WHERE interested_ptr_id=%s", member_id)


@auth_decorator(allowed=MemberClass.BOARD_MEMBER)
@restrictRouter(allowed=["POST"])
def unregister_member_from_tournament_play(request):
    """
    POST -- Given a member_id, mark member as not participating in tournament
    :param request:
    :return:
    """
    post_dict = dict(request.POST.items())
    validate_keys(["member_id"], post_dict)
    member_id = post_dict["member_id"]

    # Check if member is even participating in a tournament in the first place
    rawquery = Member.objects.raw("SELECT * FROM api_member WHERE interested_ptr_id=%s", [member_id])
    if len(list(rawquery)) > 0:
        member = rawquery[0]
        if member.in_tournament == 0:
            return http_response(message="Member was not in a tournament to begin with", code=400)
    else:
        return http_response(message="Specified member does not exist", code=400)

    return run_connection("UPDATE api_member SET in_tournament=0 WHERE interested_ptr_id=%s", member_id)
