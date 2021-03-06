# -*- coding: utf-8 -*-


class AbstractSystemVersion(object):

	def __init__(self, version, releasename, appname):
		if not isinstance(version, tuple):
			self._version = (0, 0, 0, 0)
		else:
			self._version = version
		if not releasename or not isinstance(releasename, str):
			self._releasename = 'UNKNOWN'
		else:
			self._releasename = releasename
		if not appname or not isinstance(appname, str):
			self._appname = 'UNKNOWN'
		else:
			self._appname = appname
		pass

	def __str__(self):
		return str(self).encode('utf-8')

	def __unicode__(self):
		obj_str = "%s (%s-%s)" % (self._releasename, self._appname, '.'.join(map(str, self._version)))
		return obj_str

	def getReleaseName(self):
		return self._releasename

	def getVersion(self):
		return self._version

	def getAppName(self):
		return self._appname
