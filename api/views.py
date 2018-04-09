import json

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout, login
from django.template import Context, Template
from django.contrib.auth import logout as auth_logout

def is_member(request):
    pass

def sign_in(request):
    url = Template("{% url 'social:begin' 'google-oauth2' %}")
    return redirect(str(url.render(Context({}))))

def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('/')

@login_required
def done(request):
    return redirect('/home')