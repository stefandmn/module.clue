# -*- coding: utf-8 -*-


class ModuleException(Exception):
	def __init__(self, message):
		Exception.__init__(self, message)
		self._message = message

	def getMessage(self):
		return self._message
