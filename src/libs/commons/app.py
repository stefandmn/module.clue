# -*- coding: utf-8 -*-

from env import *
import urllib2
import sys

if hasattr(sys.modules["__main__"], "xbmc"):
	xbmc = sys.modules["__main__"].xbmc
else:
	import xbmc
if hasattr(sys.modules["__main__"], "xbmcgui"):
	xbmcgui = sys.modules["__main__"].xbmcgui
else:
	import xbmcgui
if hasattr(sys.modules["__main__"], "xbmcaddon"):
	xbmcaddon = sys.modules["__main__"].xbmcaddon
else:
	import xbmcaddon

if hasattr(sys.modules["__main__"], "opener"):
	urllib2.install_opener(sys.modules["__main__"].opener)


def Addon():
	return xbmcaddon.Addon()


def AddonId():
	return Addon().getAddonInfo('id')


def AddonName():
	return Addon().getAddonInfo('name')


def AddonIcon():
	return Addon().getAddonInfo('icon')


def AddonPath():
	return Addon().getAddonInfo('path')


def AddonVersion():
	return Addon().getAddonInfo('version')


def AddonProfile():
	return Addon().getAddonInfo('profile')


def log(txt, code="", level=0):
	if isinstance(txt, str):
		txt = txt.decode("utf-8")
	if not code:
		msgid = "%s" % AddonId()
	else:
		msgid = "%s [%s]" % (AddonId(), code)
	try:
		message = u"%s: %s" % (msgid, txt)
		xbmc.log(message.encode("utf-8"), level)
	except:
		message = u"%s: %s" % (msgid, repr(txt))
		xbmc.log(message.encode("utf-8"), level)


def trace(txt, code=""):
	if any2bool(setting('debug')):
		log(txt, code, xbmc.LOGDEBUG)


def debug(txt, code=""):
	log(txt, code, xbmc.LOGDEBUG)


def info(txt, code=""):
	log(txt, code, xbmc.LOGINFO)


def notice(txt, code=""):
	log(txt, code, xbmc.LOGNOTICE)


def warn(txt, code=""):
	log(txt, code, xbmc.LOGWARNING)


def error(txt, code=""):
	log(txt, code, xbmc.LOGERROR)


def translate(id):
	string = Addon().getLocalizedString(id).encode('utf-8', 'ignore')
	return string


def setting(id):
	_value = Addon().getSetting(id)
	if _value is not None and _value.lower() == "true":
		return True
	elif _value is not None and _value.lower() == "false":
		return False
	elif _value is not None and _value.isdigit():
		return int(_value)
	elif _value is not None and not _value.isdigit() and _value.replace('.', '', 1).isdigit():
		return float(_value)
	elif _value is not None and _value.lower() == "null":
		return None
	else:
		return _value


def getSetting(id):
	return Addon().getSetting(id)


def setSetting(id, value):
	if value is None:
		value = ''
	Addon().setSetting(id, value)


def PasswordDialog():
	pwd = ""
	keyboard = xbmc.Keyboard("", AddonName() + "," + translate(32016), True)
	keyboard.doModal()
	if (keyboard.isConfirmed()):
		pwd = keyboard.getText()
	return pwd


def NotificationMsg(line, time=15000, icon=AddonIcon()):
	try:
		if isinstance(line, int):
			msg = translate(line)
		else:
			code = int(line)
			msg = translate(code)
	except:
		if not isinstance(line, int):
			msg = line
		else:
			msg = ""
	xbmc.executebuiltin("Notification(%s, %s, %d, %s)" % (AddonName(), msg, time, icon))


def DlgNotificationMsg(line, time=5000, icon=AddonIcon()):
	try:
		if isinstance(line, int):
			msg = translate(line)
		else:
			code = int(line)
			msg = translate(code)
	except:
		if not isinstance(line, int):
			msg = line
		else:
			msg = ""
	xbmcgui.Dialog().notification(AddonName(), msg, time=time, icon=icon)


def AskRestart(msgid, s=0):
	if YesNoDialog(msgid):
		if s == 0:
			xbmc.executebuiltin("RestartApp")
		else:
			xbmc.executebuiltin("Reboot")


def YesNoDialog(line1="", line2="", line3=""):
	try:
		if isinstance(line1, int):
			code = int(line1)
			msg1 = translate(code)
		else:
			msg1 = line1
	except:
		msg1 = line1
	try:
		if isinstance(line2, int):
			code = int(line2)
			msg2 = translate(code)
		else:
			msg2 = line2
	except:
		msg2 = line2
	try:
		if isinstance(line3, int):
			code = int(line3)
			msg3 = translate(code)
		else:
			msg3 = line3
	except:
		msg3 = line3
	return xbmcgui.Dialog().yesno(AddonName(), line1=msg1, line2=msg2, line3=msg3)


def OkDialog(line1="", line2="", line3=""):
	try:
		if isinstance(line1, int):
			code = int(line1)
			msg1 = translate(code)
		else:
			msg1 = line1
	except:
		msg1 = line1
	try:
		if isinstance(line2, int):
			code = int(line2)
			msg2 = translate(code)
		else:
			msg2 = line2
	except:
		msg2 = line2
	try:
		if isinstance(line3, int):
			code = int(line3)
			msg3 = translate(code)
		else:
			msg3 = line3
	except:
		msg3 = line3
	return xbmcgui.Dialog().ok(AddonName(), line1=msg1, line2=msg2, line3=msg3)


# This functions displays select dialog
def SelectDialog(line='', options=None):
	try:
		if isinstance(line, int):
			code = int(line)
			msg = translate(code)
		else:
			msg = line
	except:
		msg = line
	if msg is None or msg == '':
		msg = AddonName()
	if not isinstance(options, list):
		if str(options).count('\n') > 0:
			options = str(options).split('\n')
		elif str(options).count(',') > 0:
			options = str(options).split(',')
		elif str(options).count(';') > 0:
			options = str(options).split(';')
		elif str(options).count(':') > 0:
			options = str(options).split(':')
	if isinstance(options, list) and len(options) > 0:
		return xbmcgui.Dialog().select(msg, options)
	else:
		return None


# This function raises a keyboard for user input
def StringInputDialog(title=u"Input", default=u"", hidden=False):
	result = None
	# Fix for when this functions is called with default=None
	if not default:
		default = u""
	try:
		if isinstance(title, int):
			code = int(title)
			msg = translate(code)
		else:
			msg = title
	except:
		msg = title
	keyboard = xbmc.Keyboard(default, msg)
	keyboard.setHiddenInput(hidden)
	keyboard.doModal()
	if keyboard.isConfirmed():
		result = keyboard.getText()
	return result


# This function raises a keyboard numpad for user input
def NumberInputDialog(title=u"Input", default=u""):
	result = None
	# Fix for when this functions is called with default=None
	if not default:
		default = u""
	try:
		if isinstance(title, int):
			code = int(title)
			msg = translate(code)
		else:
			msg = title
	except:
		msg = title
	keyboard = xbmcgui.Dialog()
	result = keyboard.numeric(0, msg, default)
	return str(result)


# Function: sleep
def sleep(ms=1000):
	xbmc.sleep(ms)


# Function: restart
def restart():
	xbmc.restart()


# Function: getSpecialPath
def getSpecialPath(path):
	if path is not None and path.startswith("special://"):
		return xbmc.translatePath(path)
	else:
		return path
