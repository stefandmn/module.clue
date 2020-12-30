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



def Addon(code=None):
	"""
	Instantiates an addon object given by xbmcaddon library. Might be the current addon
	(when you call this method) or a particular one deployed in your Kodi environment
	in case code parameter is specified
	:param code: addon id in case you need the instance of a particular addon or none
	:return: instance of Kodi addon provided by xbmcaddon
	"""
	if code is None or code == '':
		return xbmcaddon.Addon()
	else:
		return xbmcaddon.Addon(code)


def AddonId(code=None):
	"""
	Provides addon id. This function is is mainly used in the addon when you don't want to
	hardcode the current addon id.
	:param code: addon id in case you need to take the data (addon id) from a particular
	addon instance
	:return: addon id returned by the instance of the requested addon
	"""
	return Addon(code).getAddonInfo('id')


def AddonName(code=None):
	"""
	Provides addon name.
	:param code: addon id in case you need to take the data (addon name) from a particular
	addon instance. For None value (the default one) it will return the name of the current addon.
	:return: addon name returned by the instance of the requested addon
	"""
	return Addon(code).getAddonInfo('name')


def AddonIcon(code=None):
	"""
	Provides addon icon.
	:param code: addon id in case you need to take the data (addon icon) from a particular
	addon instance. For None value (the default one) it will return the icon of the current addon.
	:return: addon icon returned by the instance of the requested addon
	"""
	return Addon(code).getAddonInfo('icon')


def AddonPath(code=None):
	"""
	Provides addon path - file system location where is installed.
	:param code: addon id in case you need to take the data (addon path) from a particular
	addon instance. For None value (the default one) it will return the path of the current addon.
	:return: addon file system installation location returned by the instance of the requested addon
	"""
	return Addon(code).getAddonInfo('path')


def AddonVersion(code=None):
	"""
	Provides addon version.
	:param code: addon id in case you need to take the data (addon version) from a particular
	addon instance. For None value (the default one) it will return the version of the current addon.
	:return: addon version returned by the instance of the requested addon
	"""
	return Addon(code).getAddonInfo('version')


def AddonProfile(code=None):
	"""
	Provides addon path - file system location where the addon has the configuration profile.
	:param code: addon id in case you need to take the data (addon profile location) from a particular
	addon instance. For None value (the default one) it will return the profile location of the current addon.
	:return: addon file system profile location returned by the instance of the requested addon
	"""
	return Addon(code).getAddonInfo('profile')


def agent():
	"""
	Provides the HTTP user agent, typically used in the header of various HTTP calls
	:return: KOdi user agent name aggregating many information about the system where the Kodi is running
	"""
	return xbmc.getUserAgent()


def log(txt, code="", level=0):
	"""
	INternal function to handle all type of logging
	:param txt: text message to be displayed in the log
	:param code: a particular log channel. In case the code is missing the channel is dictated by the c
	urrent addon id. if is not empty it the channel will be described by a master channel (addon id) and
	a sub channel (your custom channel - provided by your code)
	:param level: log level, it could be: TRACE, DEBUG, INFO, NOTICE, WARN and ERROR. There two levels
	(TRACE and DEBUG) that can be activated to the Skin level (in default skin configuration) that can
	work over NOTIVE level/channel in order to display in the log addon verbosity but in the same time to
	prevent verbosity provided by the whole system. The standard log level is activate by Kodi system
	settings (Logging area)
	"""
	if not code:
		msgid = "[%s]" % AddonId()
	else:
		msgid = "[%s] [%s]" % (AddonId(), code)
	try:
		message = "%s: %s" % (msgid, txt)
		xbmc.log(message, level)
	except:
		message = "%s: %s" % (msgid, repr(txt))
		xbmc.log(message, level)


def istrace():
	"""
	Checks if the TRACE level is activated. As it was mentioning in the log function, TRACE and DEBUG levels
	can be activated to the Skin level using "trace" skin setting property. In case TRACE level is activated
	to the Skin level will provide messages in the log over NOTICE level and through a particular TRACE channel,
	on top on the default and custom channels.
	:return: True is the TRACE level is active.
	"""
	_TRACE = getSkinSetting("trace")
	if _TRACE is not None:
		return common.any2bool(_TRACE)
	else:
		return False


def isdebug():
	"""
	Checks if the DEBUG level is activated. As it was mentioning in the log function, DEBUG level
	can be activated to the Skin level using 'debug' skin setting property, or to the Kodi system
	configuration. level (using Logging area). In case DEBUG level is activated to the Skin level
	will provide messages in the log over NOTICE level and through a particular DEBUG channel,
	on top on the default and custom channels.
	:return: True is the DEBUG level is active.
	"""
	_DEBUG = getSkinSetting("debug")
	if _DEBUG is not None:
		return common.any2bool(_DEBUG)
	else:
		return False


def trace(txt, code=""):
	"""
	Writes TRACE text messages in the log over TRACE custom channel.
	:param txt: text message to be written in the log
	:param code: custom log channel that might be used to recognize easily your messages.
	"""
	if common.istrace():
		if code is None or code == '':
			code = "TRACE"
		else:
			code = "%s] [%s" % ("TRACE", code)
		debug(txt, code)


def debug(txt, code=""):
	"""
	Writes DEBUG text messages in the log over DEBUG custom channel (in case the level is activated
	to the SKin level) or over standard channel using DEBUG system level.
	:param txt: text message to be written in the log
	:param code: addition custom log channel that might be used to recognize easily your messages.
	"""
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
	"""
	Write INFO text messages in the log over standard INFO logging level
	:param txt: text message to be written in the log
	:param code: custom log channel that might be used to recognize easily your messages.
	"""
	log(txt, code, xbmc.LOGINFO)


def notice(txt, code=""):
	"""
	Write NOTICE text messages in the log over standard NOTICE logging level. NOTICE is the default
	logging level within the Kodi system
	:param txt: text message to be written in the log
	:param code: custom log channel that might be used to recognize easily your messages.
	"""
	log(txt, code, xbmc.LOGNOTICE)


def warn(txt, code=""):
	"""
	Write WARNING text messages in the log over standard WARN logging level
	:param txt: text message to be written in the log
	:param code: custom log channel that might be used to recognize easily your messages.
	"""
	log(txt, code, xbmc.LOGWARNING)


def error(txt, code=""):
	"""
	Write ERROR text messages in the log over standard ERROR logging level
	:param txt: text message to be written in the log
	:param code: custom log channel that might be used to recognize easily your messages.
	"""
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
	return common.getAddonSetting(None, id)


def setsetting(id, _value=None):
	common.setAddonSetting(None, id, _value)


def getAddonSetting(code, id):
	_addon = Addon(code)
	_value = _addon.getSetting(id)
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


def setAddonSetting(code, id, _value=None):
	_addon = Addon(code)
	if _value is None:
		_value = ''
	if isinstance(_value, bool):
		_addon.setSettingBool(id, _value)
	elif isinstance(_value, int):
		_addon.setSettingInt(id, _value)
	elif isinstance(_value, float):
		_addon.setSettingNumber(id, _value)
	elif isinstance(_value, str):
		_addon.setSettingString(id, _value)
	else:
		_addon.setSetting(id, _value)


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
def runBuiltinCommand(command, param=None, values=None, wait=False):
	if param is None and values is None:
		xbmc.executebuiltin(command, wait)
	elif param is not None and values is None:
		xbmc.executebuiltin(command + '(' + param + ')', wait)
	elif param is not None and values is not None:
		xbmc.executebuiltin(command + '(' + param + ',' + str(values) + ')', wait)
	elif param is None and values is not None:
		xbmc.executebuiltin(command + '(' + str(values) + ')', wait)


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
def callJSON(request=None, method=None, params=None):
	response = None
	if request is not None and request != '':
		response = xbmc.executeJSONRPC(request)
		return json.loads(response)
	elif method is not None and method != '':
		if params is None or params == '':
			params = "{}"
		elif isinstance(params, dict):
			params = json.dumps(params)
		else:
			params = str(params)
			if not params.startswith("{"):
				params = "{" + params
			if not params.endswith("}"):
				params = params + "}"
		request = '{"jsonrpc":"2.0", "id":1, "method":"%s", "params":%s}' % (method, params)
		response = xbmc.executeJSONRPC(request)
		return json.loads(response)
	else:
		return response



def getSystemSetting(name):
	data = common.callJSON(method="Settings.GetSettingValue", params={"setting":name})
	if data is not None and "result" in data:
		return data['result']['value']
	else:
		return None


def setSystemSetting(name, value):
	if value is None:
		value = ""
	data = common.callJSON(method="Settings.SetSettingValue", params={"setting":name, "value":value})
	if data is None:
		common.error("Invalid [%s] system configuration or invalid [%s] input value" %(name,value), "systemsetting")
	elif data is not None and "error" in data:
		common.error("Error setting [%s] system configuration with [%s] value: %s - %s" %(name, value, str(data['error']['code']),str(data['error']['message'])), "systemsetting")
