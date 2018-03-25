from django.db import connection, IntegrityError, ProgrammingError
from .cursor import *
import json
from django.http import HttpResponse


def is_board_member(email):
    """
    Returns if the member with 'email' is a board member or not
    :param email:
    :return:
    """
    with connection.cursor() as cursor:
        query = '''
        SELECT member_ptr_id
        FROM api_boardmember
        WHERE member_ptr_id=%s;
        '''
        cursor.execute(query, [email])
        data = cursor.fetchall()

        if len(data) == 0:
            return False
        else:
            return True


# Members
def edit_member_info(email, attribute, new_value):
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
            cursor.execute(query, [new_value, email])
        except ProgrammingError:
            return HttpResponse(json.dumps({"status": "down", "message": "The attribute specified does not exist."}),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status": "up", "message": "Successfully editted member info."}),
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
def edit_boardmember_info(email, new_value):
    """
    Edits the 'job' attribute of a board member.
    :param email:
    :param new_value:
    :return:
    """
    with connection.cursor() as cursor:
        query = '''
        UPDATE api_member
        SET job=%s
        WHERE member_ptr_id=%s;
        '''
        cursor.execute(query, [new_value, email])
        return HttpResponse(json.dumps({"status": "up", "message": "Successfully editted member info."}),
                            content_type="application/json")


def get_interested():
    """
    Returns the names and emails of the interested exclusively
    :return:
    """
    with connection.cursor() as cursor:
        query = '''
        SELECT *
        FROM api_interested
        WHERE email NOT IN (
            SELECT interested_ptr_id
            FROM api_member
        )
        '''
        cursor.execute(query)
        results = dictfetchall(cursor)
    return results


def get_members():
    """
    Returns the names and emails of the members (includes board members)
    :return:
    """
    with connection.cursor() as cursor:
        query = '''
        SELECT *
        FROM api_interested, api_member
        WHERE api_interested.email = interested_ptr_id;
        '''
        cursor.execute(query)
        results = dictfetchall(cursor)
    return results

def get_board_members():
    """
    Returns the names, emails, and jobs of the board members, exclusively
    :return:
    """
    with connection.cursor() as cursor:
        query = '''
        SELECT *
        FROM api_interested, api_boardmember
        WHERE email = member_ptr_id;
        '''
        cursor.execute(query)
        results = dictfetchall(cursor)
    return results

def remove_member(email):
    """
    Deletes the tuple in api_interested with 'email'. This should delete any related tuples in
    api_member and api_boardmember.
    Works for removing Interested's, Member's, or BoardMember's
    :param email: The email of the person we want to remove from the database
    :return:
    """
    with connection.cursor() as cursor:
        query = '''
                DELETE FROM api_boardmember
                WHERE member_ptr_id=%s;
                '''
        cursor.execute(query, [email])

        query = '''
                DELETE FROM api_member
                WHERE interested_ptr_id=%s;
                '''
        cursor.execute(query, [email])

        query = '''
                DELETE FROM api_interested
                WHERE email=%s;
                '''
        cursor.execute(query, [email])

    return HttpResponse(json.dumps({"status": "up", "message": "Successfully deleted member."}),
                        content_type="application/json")


def add_interested(interested):
    """
    Creates a new entry and puts it in api_interested
    :param interested: Object that contains first_name, last_name, formerBoardMember, and email of a joining interested
    :return:
    """
    with connection.cursor() as cursor:
        query = '''
        INSERT INTO api_interested (first_name, last_name, formerBoardMember, email)
        VALUES (%s, %s, %s, %s);
        '''
        try:
            cursor.execute(query, [interested.first_name, interested.last_name, interested.formerBoardMember,
                                   interested.email])
        except IntegrityError:
            return HttpResponse(json.dumps({"status": "down", "message": "This person is already in the club."}),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status": "up", "message": "Successfully added an interested."}),
                                content_type="application/json")


def promote_to_member(email, member):
    """
    Promotes an existing Interested to a Member
    :param email: The email of the Interested to be promoted
    :param member: Object that contains level, private, dateJoined, queue, and bio of new member
    :return:
    """
    with connection.cursor() as cursor:
        query = '''
        INSERT INTO api_member (interested_ptr_id, level, private, dateJoined, bio)
        VALUES (%s, %s, %s, %s, %s);
        '''
        try:
            arr = [email, member.level, member.private, member.dateJoined, member.bio]
            cursor.execute(query, arr)
        except IntegrityError:
            return HttpResponse(json.dumps({"status": "down", "message": "This person is already a member."}),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status": "up", "message": "Successfully promoted to member."}),
                                content_type="application/json")


def promote_to_board_member(email, board_member):
    """
    Promotes an existing Member to a BoardMember
    :param email: The email of the Member to be promoted
    :param board_member: Object that contains job of a new board member
    :return:
    """
    with connection.cursor() as cursor:
        query = '''
        INSERT INTO api_boardmember (member_ptr_id, job)
        VALUES (%s, %s);
        '''
        try:
            cursor.execute(query, [email, board_member.job])
        except IntegrityError:
            return HttpResponse(json.dumps({"status": "down", "message": "This person is already a board member."}),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status": "up", "message": "Successfully promoted to board member."}),
                                content_type="application/json")


def schedule_date_exists(date):
    """
    Returns True if there is already a tuple in api_schedule with 'date'
    :param date:
    :return:
    """
    with connection.cursor() as cursor:
        query = '''
        SELECT *
        FROM api_boardmember
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
    with connection.cursor() as cursor:
        query = '''
        SELECT * 
        FROM api_schedule
        ORDER BY date DESC;
        '''
        cursor.execute(query)
        results = dictfetchall(cursor)
    return results


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
    with connection.cursor() as cursor:
        query = '''
            SELECT *
            FROM api_court;
            '''
        cursor.execute(query)
        results = dictfetchall(cursor)
    return results

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


def add_court(court):
    with connection.cursor() as cursor:
        query = '''
        INSERT INTO api_court (id, number, queue_id)
        VALUES (%s, %s, %s)
        '''
        try:
            cursor.execute(query, [court.id, court.number, court.queue])
        except IntegrityError:
            return HttpResponse(json.dumps({"status": "down", "message": "This court already exists."}),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status": "up", "message": "Successfully added court."}),
                                content_type="application/json")


def edit_court_info(court_id, attribute, new_value):
    """
    Used to edit any attribute of the court with id=court_id. The attributes
    available to edit are 'id', 'number', and 'queue_id'.
    :param court_id: 
    :param attribute: 
    :param new_value: 
    :return: 
    """
    with connection.cursor() as cursor:
        query = '''
        UPDATE api_court
        SET ''' + attribute + '''=%s
        WHERE id=%s;
        '''
        try:
            cursor.execute(query, [new_value, court_id])
        except IntegrityError:
            return HttpResponse(json.dumps({"status": "down", "message": "This queue type does not exist."}),
                                content_type="application/json")
        except ProgrammingError:
            return HttpResponse(json.dumps({"status": "down", "message": "The specified attribute does not exist."}),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status": "up", "message": "Successfully editted court info."}),
                                content_type="application/json")


def get_all_queues():
    with connection.cursor() as cursor:
        query = '''
        SELECT *
        FROM api_queue
        '''
        cursor.execute(query)
        results = dictfetchall(cursor)
    return results

def add_queue(queue):
    with connection.cursor() as cursor:
        query = '''
        INSERT INTO api_queue (type)
        VALUES (%s)
        '''
        try:
            cursor.execute(query, [queue.type])
        except IntegrityError:
            return HttpResponse(json.dumps({"status": "down", "message": "This queue type already exists."}),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status": "up", "message": "Successfully added queue."}),
                                content_type="application/json")


def member_config(email):
    """
    GET function to see settings information for members
    :param email:
    :return:
    """
    context = {}
    # email = 'ezhuang2@illinois.edu'
    # Get this member's info
    my_info = get_member_info(email)
    if not my_info:
        return HttpResponse(
            json.dumps({"status": "down", "message": "This person is not a member."}, indent=4, sort_keys=True),
            content_type="application/json")

    # Convert 'dateJoined' attribute to be JSON serializable
    # datetime.datetime.utcnow().strftime(“ % Y - % m - % dT % H: % M: % SZ”)
    my_info[0].__setitem__('dateJoined', my_info[0].__getitem__('dateJoined').strftime('%Y-%m-%dT%H:%M:%SZ'))
    # my_info.dateJoined = my_info.dateJoined.strftime('%Y-%m-%dT%H:%M:%SZ')

    context['my_info'] = my_info
    return HttpResponse(json.dumps(context, indent=4, sort_keys=True), content_type="application/json")


def member_config_edit(email, dict_post):
    """
    Updates attribute values for a member
    Ex: update 'private' to True and 'bio' to 'Hi'
            dict_post = {'private' = True, 'bio' = 'Hi'}
    :param email: member
    :param dict_post: Dictionary containing the new values for the keys we want updated. If an attribute is not
                        being updated, it won't be in the dictionary
    :return:
    """
    for k, v in dict_post.items():
        edit_member_info(email, k, v)
    return HttpResponse(json.dumps({"status": "up", "message": "Successfully editted member info."}),
                        content_type="application/json")


def board_member_config():
    """
    GET function to see settings information exclusive to board members
    :return:
    """
    # Get list of everybody (interested, members, boardmembers)
    board_members = get_board_members()
    members = get_members()
    for m in members:
        m.__setitem__('dateJoined', m.get('dateJoined').strftime('%Y-%m-%dT%H:%M:%SZ'))
        # m.dateJoined = m.dateJoined.strftime('%Y-%m-%dT%H:%M:%SZ')
    interested = get_interested()

    # Get schedule
    schedule = get_schedule()
    for s in schedule:
        s.__setitem__('date', s.get('date').strftime('%Y-%m-%dT%H:%M:%SZ'))
        # s.date = s.date.strftime('%Y-%m-%dT%H:%M:%SZ')
    all_courts = get_all_courts()
    all_queues = get_all_queues()

    context = {
        'board_members': board_members,
        'members': members,
        'interested': interested,
        'schedule': schedule,
        'all_courts': all_courts,
        'all_queues': all_queues
    }

    return HttpResponse(json.dumps(context, indent=4, sort_keys=True), content_type="application/json")
