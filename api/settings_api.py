from django.db import connection
from .cursor import *


# Members
def edit_privacy(email, new_privacy):
    with connection.cursor() as cursor:
        query = '''
        UPDATE api_member
        SET privacy = '%s'
        WHERE interested_ptr_id=%s;
        '''
        cursor.execute(query, [new_privacy, email])
        results = dictfetchall(cursor)
    return results


def get_privacy(email):
    with connection.cursor() as cursor:
        query = '''
        SELECT private
        FROM api_member
        WHERE interested_ptr_id=%s;
        '''
        cursor.execute(query, [email])
        results = dictfetchall(cursor)
    return results


def edit_bio(email, new_bio):
    with connection.cursor() as cursor:
        query = '''
        UPDATE api_member
        SET bio = '%s'
        WHERE interested_ptr_id=%s;
        '''
        cursor.execute(query, [new_bio, email])
        results = dictfetchall(cursor)
    return results


def get_bio(email):
    with connection.cursor() as cursor:
        query = '''
        SELECT bio
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
        SELECT first_name, last_name, email
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
        SELECT first_name, last_name, email
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
        SELECT first_name, last_name, email, job
        FROM api_interested, api_boardmember
        WHERE email = member_ptr_id;
        '''
        cursor.execute(query)
        results = dictfetchall(cursor)
    return results


def delete(email):
    """
    Deletes the tuple in api_interested with 'email'. This should delete any related tuples in
    api_member and api_boardmember.
    Works for removing Interested's, Member's, or BoardMember's
    :param email: The email of the person we want to remove from the database
    :return:
    """
    with connection.cursor() as cursor:
        query = '''
        DELETE FROM api_interested
        WHERE email=%s;
        '''
        cursor.execute(query, [email])
        results = dictfetchall(cursor)
    return results


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
        cursor.execute(query, [interested.first_name, interested.last_name, interested.formerBoardMember, interested.email])
        results = dictfetchall(cursor)
    return results


def promote_to_member(email, member):
    """
    Promotes an existing Interested to a Member
    :param email: The email of the Interested to be promoted
    :param member: Object that contains level, private, dateJoined, queue, and bio of new member
    :return:
    """
    with connection.cursor() as cursor:
        query = '''
        INSERT INTO api_member (interested_ptr_id, level, private, dateJoined, queue, bio)
        VALUES (%s, %s, %s, %s. %s, %s);
        '''
        cursor.execute(query, [email, member.level, member.private, member.dateJoined, member.queue, member.bio])
        results = dictfetchall(cursor)
    return results


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
        cursor.execute(query, [email, board_member.job])
        results = dictfetchall(cursor)
    return results


def delete_member(email):
    foo = 0


def edit_member(email, attribute, new_value):
    foo = 0


def add_court():
    foo = 0


def remove_court():
    foo = 0


def add_queue():
    foo = 0


def remove_queue():
    foo = 0


def edit_queue():
    foo = 0