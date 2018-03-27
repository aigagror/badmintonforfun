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
    with connection.cursor() as cursor:
        try:
            cursor.execute(execute, [arg for arg in args])
        except IntegrityError:
            return HttpResponse(json.dumps({'message': 'IntegrityError!'}),
                                content_type='application/json', status=400)
        except DatabaseError as e:
            print(e)
            return HttpResponse(json.dumps({'message': 'DatabaseError!'}), content_type='application/json',
                                status=400)
        else:
            return HttpResponse(json.dumps({'message': 'OK'}), content_type='application/json')