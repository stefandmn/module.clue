# -*- coding: utf-8 -*-

__all__ = ['createPath', 'createUriPath', 'stripHtmlFromText', 'findBestFit', 'to_utf8', 'to_unicode']

import re
import urllib


def to_utf8(text):
	result = text
	if isinstance(text, unicode):
		result = text.encode('utf-8')
	return result

def to_unicode(text):
	result = text
	if isinstance(text, str):
		result = text.decode('utf-8')
	return result

def findBestFit(data, compare_method=None):
	result = None
	last_fit = -1
	if isinstance(data, dict):
		for key in data.keys():
			item = data[key]
			fit = abs(compare_method(item))
			if last_fit == -1 or fit < last_fit:
				last_fit = fit
				result = item
	elif isinstance(data, list):
		for item in data:
			fit = abs(compare_method(item))
			if last_fit == -1 or fit < last_fit:
				last_fit = fit
				result = item
	return result

def createPath(*args):
	comps = []
	for arg in args:
		if isinstance(arg, list):
			return createPath(*arg)
		comps.append(unicode(arg.strip('/').replace('\\', '/').replace('//', '/')))
	uri_path = '/'.join(comps)
	if uri_path:
		return u'/%s/' % uri_path
	return '/'

def createUriPath(*args):
	comps = []
	for arg in args:
		if isinstance(arg, list):
			return createUriPath(*arg)
		comps.append(arg.strip('/').replace('\\', '/').replace('//', '/').encode('utf-8'))
	uri_path = '/'.join(comps)
	if uri_path:
		return urllib.quote('/%s/' % uri_path)
	return '/'

def stripHtmlFromText(text):
	"""
	Removes html tags
	:param text: html text
	:return:
	"""
	return re.sub('<[^<]+?>', '', text)
