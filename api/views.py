from django.http import HttpResponse
from django.shortcuts import render

import json

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout, login

from social_core.backends.oauth import BaseOAuth1, BaseOAuth2
from social_core.backends.google import GooglePlusAuth
from social_core.backends.utils import load_backends
from social_django.utils import psa, load_strategy
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.template import Context, Template

def sign_in(request):
    url = Template("{% url 'social:begin' backend='google-oauth2' %}")
    return redirect(str(url.render(Context({}))))

@login_required
def done(request):
    return HttpResponse('All set up now')