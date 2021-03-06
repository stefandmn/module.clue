# -*- coding: utf-8 -*-

import sys
from clueshell.AbstractPlaylist import AbstractPlaylist
from clueshell.utils import MediaItems

if hasattr(sys.modules["__main__"], "xbmc"):
	xbmc = sys.modules["__main__"].xbmc
else:
	import xbmc


class ShellPlaylist(AbstractPlaylist):
	def __init__(self, playlist_type, context):
		AbstractPlaylist.__init__(self)
		self._context = context
		self._playlist = None
		if playlist_type == 'video':
			self._playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		elif playlist_type == 'audio':
			self._playlist = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)

	def clear(self):
		self._playlist.clear()

	def add(self, base_item):
		item = MediaItems.to_item(self._context, base_item)
		if item:
			self._playlist.add(base_item.getUri(), listitem=item)

	def shuffle(self):
		self._playlist.shuffle()

	def unshuffle(self):
		self._playlist.unshuffle()
