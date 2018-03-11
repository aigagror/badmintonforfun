from django.contrib import admin
from django.urls import path
from django.urls import include, path, re_path
from .views import js_server, css_server, template_server, mock_api

urlpatterns = [
	path('js/<path:js_file>', js_server),
	path('css/<path:css_file>', css_server),
	path('mock/<path:data>', mock_api),
	path('<str:template>', template_server),
	re_path(r'', template_server),
]
