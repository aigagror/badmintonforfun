from api.calls import match_call
from api.calls.queue_call import get_queue_type, refresh_all_queues
from api.models import Court, Match, PlayedIn, TEAMS
from api.cursor_api import *

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
    _hard_refresh()  # Get rid of bad matches

    ret = {}
    courts_dict = []
    courts = Court.objects.raw("SELECT * FROM api_court")
    for court in list(courts):
        curr_court_dict = {}
        curr_court_dict["court_id"] = court.id
        queue_type = get_queue_type(court.queue_id)
        curr_court_dict["queue_type"] = queue_type

        match_on_this_court = court.match
        if match_on_this_court is None:
            curr_court_dict["match"] = None
        else:
            match = match_on_this_court
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

    refresh_all_queues()

    return http_response(dict=ret)


def _hard_refresh():
    """
    Makes sure there are no empty matches (no members are in it) and no unfinished matches
    that are not on the court.
    :return:
    """

    # Get rid of matches that nobody is playing in
    query1 = """
    SELECT * FROM api_match WHERE id NOT IN (SELECT match_id FROM api_playedin)
    """
    empty_matches = Match.objects.raw(query1)
    for empty_match in list(empty_matches):
        match_call.delete_match(empty_match.id)

    # Get rid of unfinished matches that aren't on the court
    query2 = """
    SELECT * FROM api_match WHERE endDateTime IS NULL AND api_match.id NOT IN 
    (SELECT match_id FROM api_court WHERE match_id NOT NULL)
    """

    bad_unfinished_matches = Match.objects.raw(query2)
    for bad_unfinished_match in list(bad_unfinished_matches):
        match_call.delete_match(bad_unfinished_match.id)
