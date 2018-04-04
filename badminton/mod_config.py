"""
	This file is to provide configuration parameters to the whole module.
	It is name mod_config to avoid clashing with the existing django settings
	module.

	The module stores paths to all the files to be served. As well as global
	mappings of all the files to resource locators. Eventually, we want these
	to be served from a CDN with a Subresource Integrity checksum to verify
	that we aren't getting http spoofed.

	You have to use path.join so that we can be operating system dependent.
"""

import os
from badminton_server.settings import BASE_DIR, DEBUG

if DEBUG:
	RESOURCE_DIR = 'dist'
else:
	RESOURCE_DIR = 'prod'

ROOT_RESOURCE_PATH = [BASE_DIR, 'badminton', 'templates', RESOURCE_DIR]
JS_PATH = os.path.join(*(ROOT_RESOURCE_PATH + ["js"]))
CSS_PATH = os.path.join(*(ROOT_RESOURCE_PATH + ["css"]))
TEMPLATE_PATH = os.path.join(*(ROOT_RESOURCE_PATH + ["html"]))
STATIC_PATH = os.path.join(*(ROOT_RESOURCE_PATH + ["static"]))
MOCK_PATH = os.path.join(*(ROOT_RESOURCE_PATH + ["mock_data"]))
FRAGMENTS_PATH = os.path.join(TEMPLATE_PATH, 'fragments')


class Resource(object):
	"""
		Simple object to keep track of the resources
	"""

	def __init__(self, url, checksum, anon):
		self._url = url
		self._checksum = checksum
		self._anon = anon


	@property
	def url(self):
		return self._url


	@property
	def checksum(self):
		return self._checksum


	@property
	def anonymous(self):
		return self._anon


if DEBUG:
	GLOBAL_RESOURCES = {
		'react': Resource('https://unpkg.com/react@16.2.0/umd/react.development.js', 
				"sha384-UPapAe7NrpqKvkXZb2NLIqYfbN6v7JdoqAa+aC9PZgLyNtSnT2JR2wZOe6Rimrp9", 
				True),
		'react-dom': Resource('https://unpkg.com/react-dom@16.2.0/umd/react-dom.development.js', 
				"sha384-cOIvn0O161vk0z63S/3qFzS7ofe2V/LJ+4/iFQyQrRuAbSr56ul863bW6b9AoNPZ", 
				True),
		'google-platform': Resource("https://apis.google.com/js/api:client.js", None, True),
	}
else:
	GLOBAL_RESOURCES = {
		'react': Resource('https://unpkg.com/react@16.2.0/umd/react.production.min.js', 
				"sha384-j40ChW3xknV2Dsc9+kP3/6SW2UrR7gYSbx9pmyNU1YTacm/PEj/0bxB9vM8jWFqx", 
				True),
		'react-dom': Resource('https://unpkg.com/react-dom@16.2.0/umd/react-dom.production.min.js', 
				"sha384-P4XM5fEtXj1kXZzsm1EOHZ7HmQIuzyRjjvX4na21R4eRLjmm+oUZua5ALb2PIojw", 
				True),
		'google-platform': Resource("https://apis.google.com/js/api:client.js", None, True),
	}