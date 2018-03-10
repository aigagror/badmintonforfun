import os

rel_path = os.path.dirname(os.path.realpath(__file__))

ROOT_RESOURCE_PATH = [rel_path, 'templates', 'dist']

JS_PATH = os.path.join(*(ROOT_RESOURCE_PATH + ["js"]))
CSS_PATH = os.path.join(*(ROOT_RESOURCE_PATH + ["css"]))
TEMPLATE_PATH = os.path.join(*(ROOT_RESOURCE_PATH + ["html"]))
FRAGMENTS_PATH = os.path.join(TEMPLATE_PATH, 'fragments')

class Resource(object):

	def __init__(self, url, checksum):
		self._url = url
		self._checksum = checksum

	@property
	def url(self):
		return self._url

	@property
	def checksum(self):
		return self._checksum

GLOBAL_RESOURCES = {
	'react': Resource('./js/node/react/umd/react.development.js', None),
	'react-dom': Resource('./js/node/react-dom/umd/react-dom.development.js', None),
	'google-platform': Resource("https://apis.google.com/js/platform.js", ''),
}