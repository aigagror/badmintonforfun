from api.calls.queue_call import get_queue_type
from api.models import Court, Match, PlayedIn, TEAMS
from api.cursor_api import http_response

def get_courts_call():
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
    :return:
    """
    ret = {}
    courts_dict = []
    courts = Court.objects.raw("SELECT * FROM api_court")
    for court in list(courts):
        curr_court_dict = {}
        curr_court_dict["court_id"] = court.id
        queue_type = get_queue_type(court.queue_id)
        curr_court_dict["queue_type"] = str(queue_type)

        matches_on_this_court = Match.objects.raw("SELECT * FROM api_match WHERE court_id=%s AND endDateTime IS NULL", [court.id])
        assert(len(list(matches_on_this_court)) <= 1)
        if len(list(matches_on_this_court)) == 0:
            curr_court_dict["match"] = None
        else:
            match = matches_on_this_court[0]
            plays = PlayedIn.objects.filter(match_id=match.id)
            team_a_members = []
            team_b_members = []
            for play in plays:
                if play.team == TEAMS[0][0]:
                    team_a_members.append(str(play.member.first_name + " " + play.member.last_name))
                elif play.team == TEAMS[1][0]:
                    team_b_members.append(str(play.member.first_name + " " + play.member.last_name))
            match_dict = {
                "match_id": match.id,
                "teamA": team_a_members,
                "teamB": team_b_members
            }
            curr_court_dict["match"] = match_dict
        courts_dict.append(curr_court_dict)
    ret["courts"] = courts_dict
    print(ret)

    return http_response(dict=ret)
