import os
from badminton_server.settings import BASE_DIR

ROOT_RESOURCE_PATH = [BASE_DIR, 'badminton', 'templates', 'dist']

JS_PATH = os.path.join(*(ROOT_RESOURCE_PATH + ["js"]))
CSS_PATH = os.path.join(*(ROOT_RESOURCE_PATH + ["css"]))
TEMPLATE_PATH = os.path.join(*(ROOT_RESOURCE_PATH + ["html"]))
MOCK_PATH = os.path.join(*(ROOT_RESOURCE_PATH + ["mock_data"]))
FRAGMENTS_PATH = os.path.join(TEMPLATE_PATH, 'fragments')

class Resource(object):

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


GLOBAL_RESOURCES = {
	'react': Resource('./js/node/react/umd/react.development.js', None, False),
	'react-dom': Resource('./js/node/react-dom/umd/react-dom.development.js', None, False),
	'google-platform': Resource("https://apis.google.com/js/api:client.js", None, True),
}