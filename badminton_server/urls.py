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
from django.urls import include, path
from django.urls import re_path, path, include
from django.contrib.auth import views as auth_views
from api import views as core_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    re_path(r'^login/$', core_views.sign_in, name='login'),
    # TODO
    re_path(r'^logout/$', auth_views.logout, name='logout'),
    re_path(r'^oauth/', include('social_django.urls', namespace='social')),  # <--
    path('flow_redirect/', core_views.done, name="flow_redirect"),
    path('', include('badminton.urls')),
]
