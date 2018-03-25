"""badminton_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include, path, re_path
from . import views

urlpatterns = [
    re_path(r'api_home/?$', views.home),
    re_path(r'api_settings/?$', views.settings),
    re_path(r'api_election/?$', views.elections),
    re_path(r'campaign/?$', views.campaignRouter),
    re_path(r'election/create/?$', views.electionCreateRouter),
    re_path(r'election/?$', views.electionRouter),
    re_path(r'settings/?$', views.settingsRouter),
]

