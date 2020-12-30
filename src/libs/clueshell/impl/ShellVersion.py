# -*- coding: utf-8 -*-

import sys
import json
from clueshell.AbstractSystemVersion import AbstractSystemVersion

if hasattr(sys.modules["__main__"], "xbmc"):
	xbmc = sys.modules["__main__"].xbmc
else:
	import xbmc


class ShellVersion(AbstractSystemVersion):

	def __init__(self, version, releasename, appname):
		super(ShellVersion, self).__init__(version, releasename, appname)
		try:
			json_query = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Application.GetProperties", "params": {"properties": ["version", "name"]}, "id": 1 }')
			json_query = json.loads(json_query)
			result = json_query['result']['version']
			self._version = (result.getPropertyControlValue('major', 1), result.getPropertyControlValue('minor', 0))
			self._appname = json_query['result']['name']
		except:
			self._version = (1, 0)
			self._appname = 'Unknown'
		self._releasename = 'Unknown'
		if self._version >= (12, 0):
			self._releasename = 'Frodo'
		if self._version >= (13, 0):
			self._releasename = 'Gotham'
		if self._version >= (14, 0):
			self._releasename = 'Helix'
		if self._version >= (15, 0):
			self._releasename = 'Isengard'
		if self._version >= (16, 0):
			self._releasename = 'Jarvis'
		if self._version >= (17, 0):
			self._releasename = 'Krypton'
		if self._version >= (18, 0):
			self._releasename = 'Leia'
		if self._version >= (19, 0):
			self._releasename = 'Matrix'
