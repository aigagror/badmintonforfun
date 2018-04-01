import datetime
import json

from django.db import connection, IntegrityError, DatabaseError
from django.forms.models import model_to_dict
from django.http import HttpResponse


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def dictfetchone(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()
    if row == None:
        return {}
    return dict(zip(columns, row))

dateTimeFormatString = "%Y-%m-%d %H:%M:%S"
dateFormatString = "%Y-%m-%d"

def serializeDate(dateObj):
    if not isinstance(dateObj, datetime.date):
        raise ValueError("{} is not a date".format(dateObj))
    return dateObj.strftime(dateFormatString)

def deserializeDate(strObj):
    if not isinstance(strObj, str):
        raise ValueError("{} is not a string".format(strObj))

    return datetime.datetime.strptime(strObj, dateFormatString).date()

# NOTE: There is an important distinction between date and datetime

def serializeDateTime(dateTimeObj):
    if not isinstance(dateTimeObj, datetime.datetime):
        raise ValueError("{} is not a date time".format(dateTimeObj))

    return dateTimeObj.strftime(dateTimeFormatString)

def deserializeDateTime(strObj):
    if not isinstance(strObj, str):
        raise ValueError("{} is not a string".format(strObj))

    return datetime.datetime.strptime(strObj, dateTimeFormatString)

def serializeModel(model):

    def _serializeDict(json):
        if isinstance(json, list):
            for i in json:
                _serializeDict(json[i])
            return

        for key, val in json.items():
            if isinstance(val, dict):
                _serializeDict(val)
            elif isinstance(val, datetime.date):
                json[key] = serializeDate(val)

        return json

    return _serializeDict(model_to_dict(model))


def serializeSetOfModels(models):
    ret = []
    for model in models:
        s = serializeModel(model)
        ret.append(s)

    return ret


def run_connection(execute, *args):
    """
    This function should only be used for insertion, deletion or updating
    :param execute:
    :param args:
    :return:
    """
    with connection.cursor() as cursor:
        try:
            cursor.execute(execute, [arg for arg in args])
        except IntegrityError:
            raise
            return http_response({}, message='Integrity Error!', code=400, status="down")
        except DatabaseError as e:
            print(e)
            return http_response({}, message='Database Error!', code=400, status="down")
        else:
            return http_response({})


def http_response(dict, message=None, status=None, code=200):
    """
    Helper function for all of those annoying HttpResponses with the json dumps and content_type.
    Makes sure that 'message' and 'status' are keys in this dictionary
    :param dict:
    :param message:
    :param status:
    :param code:
    :return:
    """
    if 'message' not in dict:
        dict['message'] = message if message is not None else "OK"
    if 'status' not in dict:
        dict['status'] = status if status is not None else "up"

    return HttpResponse(json.dumps(dict), content_type='application/json', status=code)