# -*- coding: utf-8 -*-


class AbstractPlayer(object):
	def __init__(self):
		pass

	def play(self, playlist_index=-1):
		raise NotImplementedError()

	def stop(self):
		raise NotImplementedError()

	def pause(self):
		raise NotImplementedError()

	def run(self, url):
		raise NotImplementedError()