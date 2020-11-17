# -*- coding: utf-8 -*-

import commons


class AbstractSettings(object):
	def __init__(self):
		object.__init__(self)
		pass

	def getString(self, setting_id, default_value=None):
		raise NotImplementedError()

	def setString(self, setting_id, value):
		raise NotImplementedError()

	def openSettings(self):
		raise NotImplementedError()

	def getInt(self, setting_id, default_value, converter=None):
		if not converter:
			converter = lambda x: x
		value = self.getString(setting_id)
		if value is None or value == '':
			return default_value
		try:
			return converter(int(value))
		except Exception as ex:
			commons.error("Failed to get setting '%s' as 'int' (%s)" % setting_id, ex.__str__())
		return default_value

	def setInt(self, setting_id, value):
		self.setString(setting_id, str(value))

	def setBool(self, setting_id, value):
		if value:
			self.setString(setting_id, 'true')
		else:
			self.setString(setting_id, 'false')

	def getBool(self, setting_id, default_value):
		value = self.getString(setting_id)
		if value is None or value == '':
			return default_value
		if value != 'false' and value != 'true':
			return default_value
		return value == 'true'

	def showFanart(self):
		return self.getBool('content.fanart_show', True)

	def getPageSize(self):
		return self.getInt('content.page_size', 20)

	def getSearchSize(self):
		return self.getInt('content.search_size', 5)

	def getCacheSize(self):
		return self.getInt('content.cache_size', 10)
