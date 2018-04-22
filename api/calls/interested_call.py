from django.db import connection


def add_interested(user):
    with connection.cursor() as cursor:
        query = """
        INSERT INTO api_interested 
            ("first_name", "last_name", "formerBoardMember", "email")
        VALUES (%s, %s, 0, %s)
        """
        cursor.execute(query, [user.first_name, user.last_name, user.email])