# -*- coding: utf-8 -*-

import os
import sys
import json
import common


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
	if not code:
		msgid = "[%s]" % AddonId()
	else:
		msgid = "[%s] [%s]" % (AddonId(), code)
	try:
		message = u"%s: %s" % (msgid, txt)
		xbmc.log(message, level)
	except:
		message = u"%s: %s" % (msgid, repr(txt))
		xbmc.log(message, level)


#@property
def istrace():
	_TRACE = getSkinSetting("trace")
	if _TRACE is not None:
		return common.any2bool(_TRACE)
	else:
		return False


#@property
def isdebug():
	_DEBUG = getSkinSetting("debug")
	if _DEBUG is not None:
		return common.any2bool(_DEBUG)
	else:
		return False


def trace(txt, code=""):
	if common.istrace():
		if code is None or code == '':
			code = "TRACE"
		else:
			code = "%s] [%s" % ("TRACE", code)
		debug(txt, code)


def debug(txt, code=""):
	if common.isdebug() or common.istrace():
		if code is None or code == '':
			code = "DEBUG"
		else:
			if not code.startswith("TRACE"):
				code = "%s] [%s" % ("DEBUG", code)
		log(txt, code, xbmc.LOGNOTICE)
	else:
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
	_value = Addon().getLocalizedString(id)
	if _value is None or _value == '':
		_value = xbmc.getLocalizedString(id)
	if _value is not None and _value != '':
		_value = common.utf8(_value)
	else:
		_value = ''
	return _value


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


def getAddonSetting(id):
	_value = Addon().getSetting(id)
	if _value is None:
		_value = ''
	return _value


def setAddonSetting(id, _value=None):
	if _value is None:
		_value = ''
	Addon().setSetting(id, _value)


def PasswordDialog():
	pwd = ""
	keyboard = xbmc.Keyboard("", AddonName() + "," + translate(32016), True)
	keyboard.doModal()
	if keyboard.isConfirmed():
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
def StringInputDialog(title="Input", default="", hidden=False):
	result = None
	# Fix for when this functions is called with default=None
	if not default:
		default = ""
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
def NumberInputDialog(title="Input", default=""):
	if not default:
		default = ""
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


# This function raises a keyboard date for user input
def DateInputDialog(title="Input", default=""):
	if not default:
		default = ""
	try:
		if isinstance(title, int):
			code = int(title)
			msg = translate(code)
		else:
			msg = title
	except:
		msg = title
	keyboard = xbmcgui.Dialog()
	result = keyboard.numeric(1, msg, default)
	return str(result)


# This function raises a keyboard time for user input
def TimeInputDialog(title="Input", default=""):
	if not default:
		default = ""
	try:
		if isinstance(title, int):
			code = int(title)
			msg = translate(code)
		else:
			msg = title
	except:
		msg = title
	keyboard = xbmcgui.Dialog()
	result = keyboard.numeric(2, msg, default)
	return str(result)


# This function raises a keyboard ipaddr for user input
def IPAddrInputDialog(title="Input", default=""):
	if not default:
		default = ""
	try:
		if isinstance(title, int):
			code = int(title)
			msg = translate(code)
		else:
			msg = title
	except:
		msg = title
	keyboard = xbmcgui.Dialog()
	result = keyboard.numeric(3, msg, default)
	return str(result)


# Run builtin command implemented for GUI
def RunBuiltinCommand(command, param=None, value=None):
	if param is None and value is None:
		xbmc.executebuiltin(command)
	elif param is not None and value is None:
		xbmc.executebuiltin(command + '(' + param + ')')
	elif param is not None and value is not None:
		xbmc.executebuiltin(command + '(' + param + ',' + str(value) + ')')
	elif param is None and value is not None:
		xbmc.executebuiltin(command + '(' + str(value) + ')')


# Function: sleep
def sleep(ms=1000):
	xbmc.sleep(ms)


# Function: restart
def restart():
	xbmc.restart()


# Function: path
def path(*paths):
	if paths is not None and len(paths) > 0:
		if str(paths[0]).startswith("special://"):
			root = xbmc.translatePath(paths[0])
			if len(paths) > 1:
				return os.path.join(root, *paths[1:])
			else:
				return root
		elif str(paths[0]).startswith("/"):
			if len(paths) > 1:
				return os.path.join(paths[0], *paths[1:])
			else:
				return paths[0]
		else:
			return os.path.join(AddonPath(), *paths)
	else:
		return AddonPath()


# Function: setSkinProperty
def setSkinProperty(window, name, value=None):
	if value is None:
		value = ''
	xbmcgui.Window(window).setProperty(name, str(value))


# Function: getSkinProperty
def getSkinProperty(window, name):
	try:
		if isinstance(window, int):
			value = xbmc.getInfoLabel("Window(%i).Property(%s)" % (window, str(name)))
		else:
			value = xbmc.getInfoLabel("Window(%s).Property(%s)" % (str(window), str(name)))
	except:
		value = ''
	return value


# Function: setSkinConfiguration
def setSkinSetting(name, value=None):
	if value is not None:
		if isinstance(value, str):
			if value != "":
				xbmc.executebuiltin('Skin.SetString(' + name + ', ' + str(value) + ')')
			else:
				xbmc.executebuiltin('Skin.Reset(' + name + ')')
		elif isinstance(value, int) or isinstance(value, float):
			xbmc.executebuiltin('Skin.SetString(' + name + ', ' + str(value) + ')')
		elif isinstance(value, bool) and value == True:
			xbmc.executebuiltin('Skin.SetBool(' + name + ')')
		elif isinstance(value, bool) and value == False:
			xbmc.executebuiltin('Skin.SetBool(' + name + ')')
			xbmc.executebuiltin('Skin.ToggleSetting(' + name + ')')
	else:
		xbmc.executebuiltin('Skin.ToggleSetting(' + name + ')')


# Function: getSkinSetting
def getSkinSetting(name):
	try:
		value = xbmc.getInfoLabel("Skin.String(%s)" %name)
		if value is None or value == '':
			value = xbmc.getInfoLabel("Skin.HasSetting(%s)" % name)
	except:
		value = None
	return value


# Function: callJSON
def callJSON(request):
	response = None
	if request is not None and request != '':
		response = xbmc.executeJSONRPC(request)
	return json.loads(response)



def getSystemSetting(name):
	data = common.callJSON('{"jsonrpc":"2.0", "id":1, "method":"Settings.GetSettingValue", "params":{"setting":"%s"}}' % (name))
	if data is not None and data.has_key("result"):
		return data['result']['value']
	else:
		return None


def setSystemSetting(name, value):
	data = None
	if isinstance(value, str):
		data = common.callJSON('{"jsonrpc":"2.0", "id":1, "method":"Settings.SetSettingValue", "params":{"setting":"%s", "value":"%s"}}' % (name, value))
	elif isinstance(value, int):
		data = common.callJSON('{"jsonrpc":"2.0", "id":1, "method":"Settings.SetSettingValue", "params":{"setting":"%s", "value":%d}}' % (name, value))
	elif isinstance(value, float):
		data = common.callJSON('{"jsonrpc":"2.0", "id":1, "method":"Settings.SetSettingValue", "params":{"setting":"%s", "value":%f}}' % (name, value))
	if data is None:
		common.error("Invalid input value of invalid call")
	elif data is not None and data.has_key("error"):
		common.error("Error setting system configuration: %s - %s" %(str(data['error']['code']),str(data['error']['message'])))
