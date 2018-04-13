import json

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout, login
from django.template import Context, Template
from django.contrib.auth import logout as auth_logout
from api.calls.interested_call import add_interested
from api.utils import MemberClass, get_member_class
from api.routers.router import auth_decorator, restrictRouter, validate_keys
from django.db import connection
from api.cursor_api import dictfetchall

def sign_in(request):
    url = Template("{% url 'social:begin' 'google-oauth2' %}")
    return redirect(str(url.render(Context({}))))

def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('/')

@login_required
def done(request):
    email = request.user.email
    member_class = get_member_class(email)
    print(member_class)
    if member_class == MemberClass.OUTSIDE:
        add_interested(request.user)
        auth_logout(request)
        return redirect('/registered')
    elif member_class == MemberClass.INTERESTED:
        auth_logout(request)
        return redirect('/registered')
    return redirect('/home')

@auth_decorator(allowed=MemberClass.OUTSIDE)
def test(request):
    return HttpResponse("Hello!")

interested_mail_key = "interested"
board_mail_key = "board"
member_mail_key = "current"

def emails_for_key(key):
    if key == board_mail_key:
        with connection.cursor() as cursor:
            query = """
            SELECT api_interested.email AS email FROM api_interested 
                JOIN api_boardmember 
                    ON api_interested.id = api_boardmember.member_ptr_id
            """
            cursor.execute(query)
            results = dictfetchall(cursor)
    elif key == member_mail_key:
        with connection.cursor() as cursor:
            query = """
            SELECT api_interested.email AS email FROM api_interested 
                JOIN api_member 
                    ON api_interested.id = api_member.interested_ptr_id
            """
            cursor.execute(query)
            results = dictfetchall(cursor)
    else:
        with connection.cursor() as cursor:
            query = """
            SELECT api_interested.email AS email FROM api_interested 
                WHERE api_interested.id NOT IN (SELECT id FROM api_member);
            """
            cursor.execute(query)
            results = dictfetchall(cursor)
    print(results)
    emails = list(map(lambda x: x['email'], results))
    return emails


@auth_decorator(allowed=MemberClass.BOARD_MEMBER)
@restrictRouter(allowed=["GET", "POST"])
def mail(request):
    if request.method == "GET":
        mailing_lists = [
            {
                "name": "Interested Members",
                "key": interested_mail_key
            },
            {
                "name": "Current Member",
                "key": member_mail_key
            },
            {
                "name": "Board Member",
                "key": board_mail_key
            }
        ]
        return HttpResponse(json.dumps(mailing_lists), content_type="application/json")
    elif request.method == "POST":
        """
            Expecting
            {
                "mailing_list": str
                "title": str
                "body": str
            }
        """
        list_mail_key = "mailing_list"
        title_mail_key = "title"
        body_mail_key = "body"
        keys = [list_mail_key, title_mail_key, body_mail_key]

        if not validate_keys(keys, request.POST):
            return HttpResponse("Missing key, one of %s".format(','.join(keys)), status=400)

        print(emails_for_key(request.POST[list_mail_key]))

        raise NotImplementedError("Hello")
