# -*- coding: utf-8 -*-

import sys
from clueshell.utils.Utilities import to_unicode, to_utf8
from clueshell.AbstractContextUI import AbstractContextUI
from .ShellProgressDialog import ShellProgressDialog
from .ShellProgressDialogBG import ShellProgressDialogBG

if hasattr(sys.modules["__main__"], "xbmc"):
	xbmc = sys.modules["__main__"].xbmc
else:
	import xbmc

if hasattr(sys.modules["__main__"], "xbmcgui"):
	xbmcgui = sys.modules["__main__"].xbmcgui
else:
	import xbmcgui


class ShellContextUI(AbstractContextUI):
	def __init__(self, addon, context):
		AbstractContextUI.__init__(self)
		self._addon = addon
		self._context = context
		self._view_mode = None

	def createProgressDialog(self, heading, text=None, background=False):
		if background and self._context.getSystemVersion().getVersion() > (12, 3):
			return ShellProgressDialogBG(heading, text)
		return ShellProgressDialog(heading, text)

	def getSkinId(self):
		return xbmc.getSkinDir()

	def onKeyboardInput(self, title, default='', hidden=False):
		# fallback for Frodo
		if self._context.getSystemVersion().getVersion() <= (12, 3):
			keyboard = xbmc.Keyboard(default, title, hidden)
			keyboard.doModal()
			if keyboard.isConfirmed() and keyboard.getText():
				text = to_unicode(keyboard.getText())
				return True, text
			else:
				return False, u''
		# Starting with Gotham (13.X > ...)
		dialog = xbmcgui.Dialog()
		result = dialog.input(title, to_unicode(default), type=xbmcgui.INPUT_ALPHANUM)
		if result:
			text = to_unicode(result)
			return True, text
		return False, u''

	def onNumericInput(self, title, default=''):
		dialog = xbmcgui.Dialog()
		result = dialog.input(title, str(default), type=xbmcgui.INPUT_NUMERIC)
		if result:
			return True, int(result)
		return False, None

	def onYesNoInput(self, title, text):
		dialog = xbmcgui.Dialog()
		return dialog.yesno(title, text)

	def onOk(self, title, text):
		dialog = xbmcgui.Dialog()
		return dialog.ok(title, text)

	def onRemoveContent(self, content_name):
		text = self._context.localize(30913, "Remove") % content_name
		return self.onYesNoInput(self._context.localize(30911, "Confirm remove"), text)

	def onDeleteContent(self, content_name):
		text = self._context.localize(30912, "Delete") % content_name
		return self.onYesNoInput(self._context.localize(30910, "Confirm delete"), text)

	def onSelect(self, title, items=[]):
		_dict = {}
		_items = []
		i = 0
		for item in items:
			if isinstance(item, tuple):
				_dict[i] = item[1]
				_items.append(item[0])
			else:
				_dict[i] = i
				_items.append(item)
			i += 1
		dialog = xbmcgui.Dialog()
		result = dialog.select(title, _items)
		return _dict.get(result, -1)

	def showNotification(self, message, header='', image_uri='', time_milliseconds=5000):
		_header = header
		if not _header:
			_header = self._context.getName()
		_header = to_utf8(_header)
		_image = image_uri
		if not _image:
			_image = self._context.getIcon()
		_message = to_unicode(message)
		_message = _message.replace(',', ' ')
		_message = to_utf8(_message)
		_message = _message.replace('\n', ' ')
		xbmc.executebuiltin("Notification(%s, %s, %d, %s)" % (_header, _message, time_milliseconds, _image))

	def openSettings(self):
		self._addon.openSettings()

	def refreshContainer(self):
		xbmc.executebuiltin("Container.Refresh")

	def showBusyDialog(self):
		xbmc.executebuiltin("Skin.SetBool(ShowLoading)")
		xbmc.executebuiltin("ActivateWindow(busydialog)")

	def closeBusyDialog(self):
		xbmc.executebuiltin("Skin.Reset(ShowLoading)")
		xbmc.executebuiltin("Dialog.Close(busydialog)")
