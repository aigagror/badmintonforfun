from django.db import connection, IntegrityError, ProgrammingError
from api.cursor_api import *
import json
from django.http import HttpResponse

from api.routers.router import validate_keys
from ..models import *

def get_status(id):
    """
    Returns "Boardmember", "Member", or "Interested" (or "Not found" if not in db)
    :param id:
    :return:
    """
    if is_board_member(id):
        return "Boardmember"
    elif is_member(id):
        return "Member"
    elif is_interested(id):
        return "Interested"
    else:
        return "Not found"

def is_member(id):
    """
    Returns true if this id is only a member
    :param id:
    :return:
    """
    all = Member.objects.raw("SELECT * FROM api_member")
    foo = list(all)
    members = Member.objects.raw("SELECT * FROM api_member WHERE interested_ptr_id=%s AND interested_ptr_id NOT IN (SELECT member_ptr_id FROM api_boardmember)", [id])
    return len(list(members)) > 0


def is_interested(id):
    """
    Returns true if this id is only interested
    :param id:
    :return:
    """
    all = Interested.objects.raw("SELECT * FROM api_interested")
    foo = list(all)
    interesteds = Interested.objects.raw('SELECT * FROM api_interested WHERE id=%s AND id NOT IN (SELECT interested_ptr_id FROM api_member)', [id])
    return len(list(interesteds)) > 0

def is_board_member(id):
    """
    Returns true if this id is a board member
    :param email:
    :return:
    """
    all = BoardMember.objects.raw("SELECT * FROM api_boardmember")
    foo = list(all)
    boards = BoardMember.objects.raw("SELECT * FROM api_boardmember WHERE member_ptr_id = %s", [id])
    return len(list(boards)) > 0



# Members
def edit_member_info(id, attribute, new_value):
    """
    Edits the specified attribute of a member.
    The attributes available to edit are 'level', 'private', 'dateJoined', 'bio', and possibly 'queue'?
    :param email:
    :param attribute:
    :param new_value:
    :return:
    """
    with connection.cursor() as cursor:
        query = '''
        UPDATE api_member
        SET ''' + attribute + '''=%s
        WHERE interested_ptr_id=%s;
        '''
        try:
            cursor.execute(query, [new_value, id])
        except ProgrammingError:
            return HttpResponse(json.dumps({"message": "The attribute specified does not exist."}),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({"message": "Successfully editted member info."}),
                                content_type="application/json")


def get_member_info(email):
    """
    Retrieves all information on a member.
    The attributes retrieved will be from api_interested and api_member
    Will be used to show the member their current settings.
    :param email:
    :param attribute:
    :return:
    """
    with connection.cursor() as cursor:
        query = '''
        SELECT level, private, dateJoined, bio, party_id, first_name, last_name, formerBoardMember, email
        FROM api_member, api_interested
        WHERE api_interested.email= interested_ptr_id AND interested_ptr_id=%s
        LIMIT 1;
        '''
        cursor.execute(query, [email])
        results = dictfetchall(cursor)
    return results

# Board Members
def edit_boardmember_job(id, new_job):
    """
    Edits the 'job' attribute of a board member.
    :param id:
    :param new_job:
    :return:
    """
    with connection.cursor() as cursor:
        query = '''
        UPDATE api_boardmember
        SET job=%s
        WHERE member_ptr_id=%s;
        '''
        cursor.execute(query, [new_job, id])
        return HttpResponse(json.dumps({"message": "Successfully editted boardmember job."}),
                            content_type="application/json")


def delete_from_interested(id):
    with connection.cursor() as cursor:
        query = '''
        DELETE FROM api_interested
        WHERE id=%s
        '''
        cursor.execute(query, [id])
    return HttpResponse(json.dumps({"message": "Successfully deleted from interested."}),
                        content_type="application/json")



def delete_from_member(id):
    with connection.cursor() as cursor:
        query = '''
        DELETE FROM api_member
        WHERE interested_ptr_id=%s
        '''
        cursor.execute(query, [id])
    return HttpResponse(json.dumps({"message": "Successfully deleted from member."}),
                        content_type="application/json")



def delete_from_boardmember(id):
    with connection.cursor() as cursor:
        query = '''
        DELETE FROM api_boardmember
        WHERE member_ptr_id=%s
        '''
        cursor.execute(query, [id])
    return HttpResponse(json.dumps({"message": "Successfully deleted from boardmember."}),
                        content_type="application/json")


def get_interested():
    """
    Returns the names and emails of the interested exclusively
    :return:
    """
    # with connection.cursor() as cursor:
    #     query = '''
    #     SELECT *
    #     FROM api_interested
    #     WHERE email NOT IN (
    #         SELECT interested_ptr_id
    #         FROM api_member
    #     )
    #     '''
    #     cursor.execute(query)
    #     results = dictfetchall(cursor)
    # return results
    return Interested.objects.raw("SELECT * FROM api_interested WHERE id NOT IN (SELECT interested_ptr_id FROM api_member)")


def get_members():
    """
    Returns the names and emails of the members, exclusively (not board members)
    :return:
    """
    # with connection.cursor() as cursor:
    #     query = '''
    #     SELECT *
    #     FROM api_interested, api_member
    #     WHERE api_interested.email = interested_ptr_id;
    #     '''
    #     cursor.execute(query)
    #     results = dictfetchall(cursor)
    # return results
    return (Member.objects.raw("SELECT * FROM api_member WHERE interested_ptr_id NOT IN (SELECT member_ptr_id FROM api_boardmember)"))

def get_board_members():
    """
    Returns information on the board members, exclusively
    :return:
    """
    return BoardMember.objects.raw("SELECT * FROM api_boardmember")

def remove_member(member_id):
    """
    Deletes the tuple in api_interested with 'email'. This should delete any related tuples in
    api_member and api_boardmember.
    Works for removing Interested's, Member's, or BoardMember's
    :param member_id: The id of the person we want to remove from the database
    :return:
    """
    with connection.cursor() as cursor:
        query = '''
                DELETE FROM api_boardmember
                WHERE member_ptr_id=%s;
                '''
        cursor.execute(query, [member_id])

        query = '''
                DELETE FROM api_member
                WHERE interested_ptr_id=%s;
                '''
        cursor.execute(query, [member_id])

        query = '''
                DELETE FROM api_interested
                WHERE id=%s;
                '''
        cursor.execute(query, [member_id])

    return HttpResponse(json.dumps({"message": "Successfully deleted member."}),
                        content_type="application/json")


def add_interested(interested):
    """
    Creates a new entry and puts it in api_interested
    :param interested: Object that contains first_name, last_name, formerBoardMember, and email of a joining interested
    :return:
    """

    query = '''
                INSERT INTO api_interested (first_name, last_name, formerBoardMember, email)
                VALUES (%s, %s, %s, %s);
                '''
    return run_connection(query, interested.first_name, interested.last_name, interested.formerBoardMember, interested.email)


def promote_to_member(id):
    """
    Promotes an existing Interested to a Member
    :param id: The email of the Interested to be promoted
    :return:
    """
    today = datetime.date.today()
    query = '''
            INSERT INTO api_member (interested_ptr_id, dateJoined, level, private, bio)
            VALUES (%s, %s, 0, 0, '');
            '''
    s_today = serializeDate(today)
    return run_connection(query, id, s_today)

def promote_to_board_member(id, job):
    """
    Promotes an existing Member to a BoardMember
    :param id: The email of the Member to be promoted
    :param board_member: Object that contains job of a new board member
    :return:
    
    """
    query = '''
            INSERT INTO api_boardmember (member_ptr_id, job)
            VALUES (%s, %s);
            '''
    return run_connection(query, id, job)

def schedule_date_exists(date):
    """
    Returns True if there is already a tuple in api_schedule with 'date'
    :param date:
    :return:
    """
    with connection.cursor() as cursor:
        query = '''
        SELECT *
        FROM api_schedule
        WHERE date=%s;
        '''
        cursor.execute(query, [date])
        data = cursor.fetchall()

        if len(data) == 0:
            return False
        else:
            return True


def add_to_schedule(date, number_of_courts):
    """
    Allow board members to insert the number of available courts on the specified date.
    :param date:
    :param number_of_courts: If this is 4, only courts 1-4 will be available
    :return:
    """
    with connection.cursor() as cursor:
        query = '''
                INSERT INTO api_schedule (date, number_of_courts)
                VALUES (%s, %s)
                '''
        cursor.execute(query, [date, number_of_courts])
    return HttpResponse(json.dumps({"status": "up", "message": "Successfully added to schedule."}),
                        content_type="application/json")


def edit_schedule(date, number_of_courts):
    """
    Edit existing entry in api_schedule.
    :param date:
    :param number_of_courts:
    :return:
    """
    with connection.cursor() as cursor:
        query = '''
                UPDATE api_schedule
                SET number_of_courts=%s
                WHERE date=%s
                '''
        cursor.execute(query, [number_of_courts, date])
    return HttpResponse(json.dumps({"status": "up", "message": "Successfully editted schedule."}),
                        content_type="application/json")


def delete_from_schedule(date):
    """
    Delete existing entry in api_schedule.
    :param date:
    :return:
    """
    with connection.cursor() as cursor:
        query = '''
                DELETE FROM api_schedule
                WHERE date=%s;
                '''
        cursor.execute(query, [date])
    return HttpResponse(json.dumps({"status": "up", "message": "Successfully deleted schedule."}),
                        content_type="application/json")


def get_schedule():
    """
    Returns all the tuples in api_schedule in descending order
    :return:
    """
    # with connection.cursor() as cursor:
    #     query = '''
    #     SELECT *
    #     FROM api_schedule
    #     ORDER BY date DESC;
    #     '''
    #     cursor.execute(query)
    #     results = dictfetchall(cursor)
    # return results
    return Schedule.objects.raw("SELECT * FROM api_schedule ORDER BY date DESC")

def get_available_courts(date):
    """
    Returns the courts available on 'date'
    :param date:
    :return:
    """
    with connection.cursor() as cursor:
        query = '''
        SELECT *
        FROM api_court
        WHERE id <=
            (SELECT number_of_courts
            FROM api_schedule
            WHERE date=%s);
        '''
        cursor.execute(query, [date])
        results = dictfetchall(cursor)
    return results


def get_all_courts():
    """
    Returns all courts
    :return:
    """
    # with connection.cursor() as cursor:
    #     query = '''
    #         SELECT *
    #         FROM api_court;
    #         '''
    #     cursor.execute(query)
    #     results = dictfetchall(cursor)
    # return results
    return Court.objects.raw("SELECT * FROM api_court")


def get_court(court_id):
    with connection.cursor() as cursor:
        query = '''
        SELECT *
        FROM api_court
        WHERE id=%s
        LIMIT 1
        '''
        cursor.execute(query, [court_id])
        results = dictfetchall(cursor)
    return results

def court_id_exists(court_id):
    with connection.cursor() as cursor:
        query = '''
        SELECT *
        FROM api_court
        WHERE id=%s;
        '''
        cursor.execute(query, [court_id])
        data = cursor.fetchall()

        if len(data) == 0:
            return False
        else:
            return True


def add_court(court_id, queue_id):
    with connection.cursor() as cursor:
        query = '''
        INSERT INTO api_court (id, queue_id)
        VALUES (%s, %s)
        '''
        try:
            cursor.execute(query, [court_id, queue_id])
        except IntegrityError:
            return HttpResponse(json.dumps({"message": "This court already exists or the queue specified does not exist."}),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({"message": "Successfully added court."}),
                                content_type="application/json")


def edit_court_queue(court_id, new_queue_id):
    """
    Used to edit the queue_id of the court with id=court_id.
    :param court_id: 
    :param new_queue_id:
    :return: 
    """
    with connection.cursor() as cursor:
        query = '''
        UPDATE api_court
        SET queue_id=%s
        WHERE id=%s;
        '''
        try:
            cursor.execute(query, [new_queue_id, court_id])
        except IntegrityError:
            return HttpResponse(json.dumps({"message": "The specified queue id does not exist."}),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({"message": "Successfully updated the queue_id for the specified court."}),
                                content_type="application/json")


def delete_court(court_id):
    with connection.cursor() as cursor:
        query = '''
        DELETE FROM api_court
        WHERE id=%s
        '''
        cursor.execute(query, [court_id])
    return HttpResponse(json.dumps({"message": "Successfully deleted the specified court."}),
                        content_type="application/json")

def get_all_queues():
    # with connection.cursor() as cursor:
    #     query = '''
    #     SELECT *
    #     FROM api_queue
    #     '''
    #     cursor.execute(query)
    #     results = dictfetchall(cursor)
    # return results
    return Queue.objects.raw("SELECT * FROM api_queue")


def add_queue(queue_type):
    with connection.cursor() as cursor:
        query = '''
        INSERT INTO api_queue (type)
        VALUES (%s)
        '''
        try:
            cursor.execute(query, [queue_type])
        except IntegrityError:
            return HttpResponse(json.dumps({"message": "This queue type already exists."}),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({"message": "Successfully added queue."}),
                                content_type="application/json")


def delete_queue(queue_type):
    with connection.cursor() as cursor:
        query = '''
        DELETE FROM api_queue
        WHERE type=%s
        '''
        cursor.execute(query, [queue_type])
    return HttpResponse(json.dumps({"message": "Successfully deleted queue."}),
                        content_type="application/json")


# The functions below are used to package information for the frontend to use

def member_config(member_id):
    """
    GET function to see settings information for members
    :param member_id:
    :return:
    """

    members = Member.objects.raw("SELECT * FROM api_member WHERE interested_ptr_id = %s", [member_id])
    if len(list(members)) == 0:
        return HttpResponse(json.dumps({"message": "This person is not a member."}), content_type="application/json")

    member = members[0]
    # data = serializeModel(member)
    data = [
        {
            "type": "bool",
            "name": 'private',
            "display_name": "Show ranking",
            "value": member.private
        },
        {
            "type": "long_text",
            "name": 'bio',
            "display_name": "Member Bio",
            "value": member.bio
        }
    ]
    return HttpResponse(json.dumps(data), content_type="application/json")


def member_config_edit(member_id, dict_post):
    """
    Updates attribute values for a member
    Ex: update 'private' to True and 'bio' to 'Hi'
            dict_post = {'private' = True, 'bio' = 'Hi'}
    :param member_id: member
    :param dict_post: Dictionary containing the new values for the keys we want updated.
    :return:
    """
    for k, v in dict_post.items():
        edit_member_info(member_id, k, v)
    return HttpResponse(json.dumps({"message": "Successfully editted member settings."}),
                        content_type="application/json")


def boardmembers_config():
    """
    GET function to see list of board members
    :return:
    """
    # Get list of all boardmembers
    boardmembers = get_board_members()
    ret_list = []
    for boardmember in boardmembers:
        boardmember_dict = {
            'member_id': boardmember.id,
            'first_name': boardmember.first_name,
            'last_name': boardmember.last_name,
            'email': boardmember.email,
            'job': boardmember.job
        }
        ret_list.append(boardmember_dict)
    context = {'boardmembers': ret_list}

    return HttpResponse(json.dumps(context, indent=4, sort_keys=True), content_type="application/json")

def boardmembers_config_edit(dict_post):
    """
    POST function to edit jobs of boardmembers
    :param dict_post:
    :return:
    """
    boardmembers = dict_post['boardmembers']
    for boardmember in boardmembers:
        member_id = boardmember['member_id']
        new_job = boardmember['job']
        print(new_job)
        edit_boardmember_job(member_id, new_job)
    return HttpResponse(json.dumps({"message": "Successfully updated boardmember jobs."}),
                        content_type="application/json")

def get_all_club_members():
    """
    GET function to get info on all the people in the club
    :return:
    """
    interested = get_interested()
    ret_list = []
    for interested_member in interested:
        interested_dict = {
            'member_id': interested_member.id,
            'first_name': interested_member.first_name,
            'last_name': interested_member.last_name,
            'email': interested_member.email,
            'status': "Interested"
        }
        ret_list.append(interested_dict)

    members = get_members()
    for member in members:
        member_dict = {
            'member_id': member.id,
            'first_name': member.first_name,
            'last_name': member.last_name,
            'email': member.email,
            'status': "Member"
        }
        ret_list.append(member_dict)

    boardmembers = get_board_members()
    for boardmember in boardmembers:
        boardmember_dict = {
            'member_id': boardmember.id,
            'first_name': boardmember.first_name,
            'last_name': boardmember.last_name,
            'email': boardmember.email,
            'status': "Boardmember"
        }
        ret_list.append(boardmember_dict)

    context = {'members': ret_list}

    return HttpResponse(json.dumps(context, indent=4, sort_keys=True), content_type="application/json")


def update_all_club_members_status(dict_post):
    """
    POST request for boardmembers. Alter the statuses of members.
    Assumes a list of members and a drop-down for each one with the choices (Interested, Member, Boardmember).
    :param dict_post:
    :return:
    """
    members = dict_post['members']
    for member in members:
        member_id = member['member_id']
        new_status = member['status']
        curr_status = get_status(member_id)

        if new_status == "Boardmember":
            if curr_status == "Member":
                promote_to_board_member(member_id, "OFFICER")
            elif curr_status == "Interested":
                promote_to_member(member_id)
                promote_to_board_member(member_id, "OFFICER")
        elif new_status == "Member":
            if curr_status == "Boardmember":
                delete_from_boardmember(member_id)
            elif curr_status == "Interested":
                promote_to_member(member_id)
        elif new_status == "Interested":
            if curr_status == "Boardmember":
                delete_from_boardmember(member_id)
                delete_from_member(member_id)
            elif curr_status == "Member":
                delete_from_member(member_id)

    return HttpResponse(json.dumps({"message": "Successfully updated club member statuses."}),
                        content_type="application/json")

def delete_multiple_club_members(dict_delete):
    """
    DELETE request for boardmembers to remove club members. The provided dictionary
    should ONLY have the information for the club members that will be deleted
    :param dict_delete:
    :return:
    """
    print(dict_delete)
    members = dict_delete['members']
    for member in members:
        member_id = member['member_id']
        remove_member(member_id)
    return HttpResponse(json.dumps({"message": "Successfully removed club members."}),
                        content_type="application/json")

def schedule_to_dict():
    """
    Returns the schedule as a dictionary of the form
    {
        'schedule': [
            {
                'date': _,
                'number_of_courts': _
            },
            ...
        ]
    }
    :return:
    """
    schedule = get_schedule()
    num_entries = len(list(schedule))
    if num_entries == 0:
        return HttpResponse(json.dumps({"message": "There is nothing in the schedule."}),
                            content_type="application/json")
    ret_list = []
    for i in range(num_entries):
        entry = serializeModel(schedule[i])
        entry_dict = {
            'date': entry['date'],
            'number_of_courts': entry['number_of_courts']
        }
        ret_list.append(entry_dict)

    context = {'schedule': ret_list}

    return HttpResponse(json.dumps(context, indent=4, sort_keys=True), content_type="application/json")


def addto_edit_schedule(dict_post):
    """
    POST request for boardmembers to add to or edit entries in the schedule.
    :param dict_post:
    :return:
    """
    schedule = dict_post['schedule']
    today = datetime.date.today()
    for entry in schedule:
        date = entry.get('date', today)
        number_of_courts = entry.get('number_of_courts', 0)

        if schedule_date_exists(date):
            edit_schedule(date, number_of_courts)
        else:
            add_to_schedule(date, number_of_courts)

    return HttpResponse(json.dumps({"message": "Successfully updated schedule."}),
                        content_type="application/json")

def delete_multiple_from_schedule(dict_delete):
    """
    DELETE request for boardmembers to delete entries from schedule. The dictionary should ONLY
    contain information for the entries that they want to be deleted.
    :param dict_delete:
    :return:
    """
    schedule = dict_delete['schedule']
    for entry in schedule:
        date = entry.get('date', '')
        # If the provided date doesn't exist, ignore and continue
        if schedule_date_exists(date):
            delete_from_schedule(date)

    return HttpResponse(json.dumps({"message": "Successfully deleted entries from schedule."}),
                        content_type="application/json")

def get_all_courts_formmated():
    """
    GET request to get all the courts
    :return:
    """
    courts = get_all_courts()
    if not courts:
        return HttpResponse(json.dumps({"message": "There are no courts stored in the database."}),
                            content_type="application/json")
    ret_list = []
    for c in courts:
        court_dict = {
            'court_id': c.id,
            'queue_id': c.queue_id
        }
        ret_list.append(court_dict)
    context = {'courts': ret_list}
    return HttpResponse(json.dumps(context, indent=4, sort_keys=True), content_type="application/json")

def addto_edit_courts_formatted(dict_post):
    """
    POST method
    :param dict_post:
    :return:
    """
    courts = dict_post['courts']
    for c in courts:
        if validate_keys(['court_id', 'queue_id'], c):
            court_id = c['court_id']
            queue_id = c['queue_id']
            if court_id_exists(court_id):
                edit_court_queue(court_id, queue_id)
            else:
                add_court(court_id, queue_id)
    return HttpResponse(json.dumps({"message": "Successfully updated courts."}),
                        content_type="application/json")


def delete_courts_formatted(dict_delete):
    """
    DELETE
    :param dict_delete:
    :return:
    """
    courts = dict_delete['courts']
    for c in courts:
        if validate_keys(['court_id'], c):
            court_id = c['court_id']
            delete_court(court_id)
    return HttpResponse(json.dumps({"message": "Successfully deleted specified courts."}),
                        content_type="application/json")


def get_all_queues_formatted():
    """
    GET method
    :return:
    """
    queues = get_all_queues()
    if not queues:
        return HttpResponse(json.dumps({"message": "There are no queues."}),
                            content_type="application/json")
    ret_list = []
    for q in queues:
        queue_dict = {
            'queue_id': q.id,
            'queue_type': q.type
        }
        ret_list.append(queue_dict)
    context = {'queues': ret_list}

    return HttpResponse(json.dumps(context, indent=4, sort_keys=True), content_type="application/json")

def add_queues_formatted(dict_post):
    """
    POST
    :return:
    """
    queues = dict_post['queues']
    for q in queues:
        if validate_keys(['queue_type'], q):
            queue_type = q['queue_type']
            add_queue(queue_type)
    return HttpResponse(json.dumps({"message": "Successfully added queue type."}),
                        content_type="application/json")

def delete_queues_formatted(dict_delete):
    """
    DELETE
    :param dict_delete:
    :return:
    """
    queues = dict_delete['queues']
    for q in queues:
        if validate_keys(['queue_id', 'queue_type'], q):
            queue_type = q['queue_type']
            delete_queue(queue_type)
    return HttpResponse(json.dumps({"message": "Successfully deleted queue type."}),
                        content_type="application/json")