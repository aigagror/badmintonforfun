import datetime
from django.forms.models import model_to_dict

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

dateFormatString = "%Y-%m-%dT%H:%M:%SZ"

def serializeDatetime(dateObj):
    if not isinstance(dateObj, datetime.date):
        raise ValueError("{} is not a date".format(dateObj))

    return dateObj.strftime(dateFormatString)

def deserializeDateTime(strObj):
    if not isinstance(strObj, str):
        raise ValueError("{} is not a string".format(strObj))

    return datetime.datetime.strptime(strObj, dateFormatString)

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
                json[key] = serializeDatetime(val)

        return json

    return _serializeDict(model_to_dict(model))
