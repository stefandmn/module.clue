# -*- coding: utf-8 -*-

from modshell.AbstractSettings import AbstractSettings


class ShellSettings(AbstractSettings):
	def __init__(self, addon):
		AbstractSettings.__init__(self)
		self._addon = addon

	def getString(self, setting_id, default_value=None):
		return self._addon.getSetting(setting_id)

	def setString(self, setting_id, value):
		self._addon.setSetting(setting_id, value)
