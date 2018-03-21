from django.db import connection, IntegrityError
from .cursor import *
import json

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
        cursor.execute(query, [new_value, email])


def get_member_attr(email, attribute):
    """
    Retrieves the specified attribute of a member.
    The attributes available to retrieve are 'level', 'private', 'dateJoined', 'bio', and possibly 'queue'?.
    Will be used to show the member their current settings.
    :param email:
    :param attribute:
    :return:
    """
    with connection.cursor() as cursor:
        query = '''
        SELECT ''' + attribute + '''
        FROM api_member
        WHERE interested_ptr_id=%s;
        '''
        cursor.execute(query, [email])
        results = dictfetchall(cursor)
    return results


# Board Members
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
            cursor.execute(query, [interested.first_name, interested.last_name, interested.formerBoardMember, interested.email])
        except IntegrityError:
            return json.dumps({'code': 400, 'message': 'This person is already in the club.'})
        else:
            return json.dumps({'code': 200, 'message': 'OK'})


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
            return json.dumps({'code': 400, 'message': 'This person is already a member.'})
        else:
            return json.dumps({'code': 200, 'message': 'OK'})


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
            return json.dumps({'code': 400, 'message': 'This person is already a board member.'})
        else:
            return json.dumps({'code': 200, 'message': 'OK'})


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
        WHERE id=%s;
        '''
        cursor.execute(query, [court_id])
        results = dictfetchall(cursor)
    return results


def add_court(court):
    with connection.cursor() as cursor:
        query = '''
        INSERT INTO api_court (id, number, queue_id)
        VALUES (%s, %s, %s)
        '''
        try:
            cursor.execute(query, [court.id, court.number, court.queue])
        except IntegrityError:
            return json.dumps({'code': 400, 'message': 'This court already exists.'})
        else:
            return json.dumps({'code': 200, 'message': 'OK'})


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
            return json.dumps({'code': 400, 'message': 'This queue type does not exist.'})
        else:
            return json.dumps({'code': 200, 'message': 'OK'})


def add_queue(queue):
    with connection.cursor() as cursor:
        query = '''
        INSERT INTO api_queue (type)
        VALUES (%s)
        '''
        try:
            cursor.execute(query, [queue.type])
        except IntegrityError:
            return json.dumps({'code': 400, 'message': 'This queue type already exists.'})
        else:
            return json.dumps({'code': 200, 'message': 'OK'})


