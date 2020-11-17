# -*- coding: utf-8 -*-

from .BaseItem import BaseItem


class ImageItem(BaseItem):

	def __init__(self, name, uri, image=u'', fanart=u''):
		BaseItem.__init__(self, name, uri, image, fanart)
		self._title = None

	def setTitle(self, title):
		self._title = str(title)

	def getTitle(self):
		return self._title

