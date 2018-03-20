"""
	Sub URL router for the frontend module
"""

from django.contrib import admin
from django.urls import path
from django.urls import include, path, re_path
# There is no way to do relative named imports.
# We are going to have to settle for this
from .views import *


# Set up the error handlers for client side
handler404 = handle_404
handler500 = handle_500
handler403 = handle_403
handler400 = handle_400

# Set the patterns in most-least
urlpatterns = [
	# We would like to keep paths to access node_modules
	# This should be changed back to str for security
	path('js/<path:js_file>', js_server),
	path('css/<path:css_file>', css_server),
	path('mock/<path:data>', mock_api),
	path('assets/<path:static_file>', static_server),

	# All templates are in the first level directory
	path('<str:template>', template_server),
	# Additional rule for the special index.html
	re_path(r'', template_server, name='index'),
]
