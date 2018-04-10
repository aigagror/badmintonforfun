from django.db import connection
from api.cursor_api import dictfetchall, serializeDict
from django.http import HttpResponse
from enum import Enum

class MemberClass(Enum):
    BOARD_MEMBER = 1
    MEMBER = 2
    INTERESTED = 3
    OUTSIDE = 4

    def isSuperSet(self, other):
        return self.value > other.value

def get_member_class(email):
    with connection.cursor() as cursor:
        query = """
        SELECT COALESCE(
            (SELECT %s FROM api_member 
                JOIN api_boardmember
                    ON api_member.interested_ptr_id = api_boardmember.member_ptr_id 
                JOIN api_interested 
                    ON api_interested.id = api_member.interested_ptr_id 
                WHERE email = %s),
            (SELECT %s FROM api_interested 
                JOIN api_member 
                ON api_interested.id = api_member.interested_ptr_id 
                WHERE email = %s), 
            (SELECT %s FROM api_interested 
                WHERE email = %s), 
            %s) AS member_class;
        """
        params = list(map(str, [MemberClass.BOARD_MEMBER.value, email, 
            MemberClass.MEMBER.value, email,
            MemberClass.INTERESTED.value, email,
            MemberClass.OUTSIDE.value]))
        cursor.execute(query, params)
        results = dictfetchall(cursor)
        return MemberClass(int(results[0]['member_class']))

def id_for_member(email):
    with connection.cursor() as cursor:
        query = """
        SELECT id AS id FROM api_interested
        JOIN api_member ON api_interested.id = api_member.interested_ptr_id 
        WHERE email = %s
        """
        params = [email]
        cursor.execute(query, params)
        results = dictfetchall(cursor)
        return int(results[0]['id'])

def add_interested(user):
    with connection.cursor() as cursor:
        query = """
        INSERT INTO api_interested 
            ("first_name", "last_name", "formerBoardMember", "email")
        VALUES (%s, %s, 0, %s)
        """
        cursor.execute(query, [user.first_name, user.last_name, user.email])