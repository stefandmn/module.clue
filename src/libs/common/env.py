# -*- coding: utf-8 -*-

import re
import sys
import json
import common
import requests
import subprocess
import traceback

if sys.version_info.major == 3:
	from urllib.parse import quote, unquote, parse_qsl
else:
	from urllib import quote, unquote
	from urlparse import parse_qsl


# Function: str2bool
def any2bool(v, error=False, none=True):
	if v is not None:
		if isinstance(v, bool):
			return v
		elif isinstance(v, int):
			return True if v > 0 else False
		elif isinstance(v, str):
			if v.lower() in ("on", "yes", "true", "0"):
				return True
			elif v.lower() in ("off", "no", "false", "1"):
				return False
			else:
				if error:
					raise RuntimeError("Invalid bool type: " + str(v))
				else:
					return False
		else:
			if error:
				raise RuntimeError("Invalid bool type: " + str(v))
			else:
				return False
	else:
		if none:
			return False
		else:
			raise RuntimeError("Invalid null value")


# Function: any2int
def any2int(v, error=False, none=True):
	if v is not None:
		if isinstance(v, int):
			return v
		else:
			try:
				return int(v)
			except:
				if error:
					raise RuntimeError("Invalid int type: " + str(v))
				else:
					return None
	else:
		if none:
			return None
		else:
			raise RuntimeError("Invalid null value")


# Function: any2float
def any2float(v, error=False, none=True):
	if v is not None:
		if isinstance(v, float):
			return v
		else:
			try:
				return float(v)
			except:
				if error:
					raise RuntimeError("Invalid float type: " + str(v))
				else:
					return None
	else:
		if none:
			return None
		else:
			raise RuntimeError("Invalid null value")


# Function: any2str
def any2str(v, error=False, none=True):
	if v is not None:
		if isinstance(v, bool):
			return str(v).lower()
		else:
			try:
				return str(v)
			except:
				if error:
					raise RuntimeError("Invalid str type: " + str(v))
				else:
					return None
	else:
		if none:
			return None
		else:
			raise RuntimeError("Invalid null value")


#Function isempty
def isempty(v):
	if v is None:
		return True
	else:
		if isinstance(v, str) and v == '':
			return True
		elif isinstance(v, bool):
			return v
		else:
			return False


#Function utf8
def utf8(v):
	if v is not None:
		if sys.version_info[0] == 2:
			return str(v).encode('utf-8', 'ignore')
	else:
		return v


# Function: procexec
def procexec(cmd):
	try:
		if isinstance(cmd, list):
			common.debug("Preparing command for execution: %s" % (" ".join(cmd)), "procexec")
			_output = subprocess.check_output(cmd)
		else:
			common.debug("Preparing command for execution: %s" % cmd)
			_output = subprocess.check_output(cmd, shell=True)
		_status = True
		if _output is not None:
			_output = _output.strip()
		common.debug("Command execution output: [%s] %s" % (str(_status), _output))
	except subprocess.CalledProcessError as grepexc:
		common.error("Exception while executing subprocess: [%s] %s" % (grepexc.returncode, grepexc.output), "procexec")
		_status = False
		_output = str(grepexc.output)
		if common.istrace:
			traceback.print_exc()
	except BaseException as err:
		common.error("Error while executing external process: %s" % str(err), "procexec")
		_status = False
		_output = str(err)
		if common.istrace:
			traceback.print_exc()
	return _status, _output


# Function: funcall
def funcall(cmd, *args, **kwargs):
	common.debug("Calling function: %s" % cmd), "funcall"
	try:
		function = globals()[cmd]
		_output = function(*args, **kwargs)
		_status = True
		if _output is not None:
			_output = _output.strip()
	except BaseException as err:
		common.error("Error while executing global function: %s" % str(err), "funcall")
		_status = False
		_output = str(err)
		if common.istrace:
			traceback.print_exc()
	return _status, _output


# Function: clscall
def clscall(cls, cmd, *args, **kwargs):
	try:
		if isinstance(cls, str):
			sig = type(cls, (), {})
			object = sig()
		else:
			object = cls
		common.debug("Calling method %s from class %s" %(cmd, type(object)), "clscall")
		method = getattr(object, cmd)
		_output = method(*args, **kwargs)
		_status = True
		if _output is not None:
			_output = _output.strip()
	except BaseException as err:
		common.error("Error while executing class function: %s" % str(err), "clscall")
		_status = False
		_output = str(err)
		if common.istrace:
			traceback.print_exc()
	return _status, _output


# Function: sysinfo
def sysinfo():
	name = version = version_id = version_code = description = architecture = device  = ''
	release_fields = re.compile(r'(?!#)(?P<key>.+)=(?P<quote>[\'\"]?)(?P<value>.+)(?P=quote)$')
	release_unescape = re.compile(r'\\(?P<escaped>[\'\"\\])')
	release_info = {}
	try:
		with open('/etc/os-release') as f:
			for line in f:
				m = re.match(release_fields, line)
				if m is not None:
					key = m.group('key')
					value = re.sub(release_unescape, r'\g<escaped>', m.group('value'))
					release_info[key] = value
	except OSError:
		release_info = None
	if release_info is not None:
		if 'NAME' in release_info:
			name = release_info['NAME']
		if 'VERSION' in release_info:
			version = release_info['VERSION']
		if 'VERSION_ID' in release_info:
			version_id = release_info['VERSION_ID']
		if 'VERSION_CODE' in release_info:
			version_code = release_info['VERSION_CODE']
		if 'PRETTY_NAME' in release_info:
			description = release_info['PRETTY_NAME']
		if 'ARCH' in release_info:
			architecture = release_info['ARCH']
		if 'DEVICE' in release_info:
			device = release_info['DEVICE']
		return (name, version, version_id, version_code, description, architecture, device)
	else:
		return None


def getproxies():
	global PROXIES
	if PROXIES is None:
		if common.any2bool(common.getSystemSetting("network.usehttpproxy"), none=False):
			httpproxytype = common.getSystemSetting("network.httpproxytype")
			httpproxyserver = common.getSystemSetting("network.httpproxyserver")
			httpproxyport = common.getSystemSetting("network.httpproxyport")
			httpproxyusername = common.getSystemSetting("network.httpproxyusername")
			httpproxypassword = common.getSystemSetting("network.httpproxypassword")
			proxyurl = httpproxyserver + ":" + httpproxyport
			if httpproxyusername is not None and httpproxyusername != '':
				proxyurl = httpproxyusername + ":" + httpproxypassword + "@" + proxyurl
			if common.any2int(httpproxytype) == 0:
				if common.any2int(httpproxyport) == 443 or common.any2int(httpproxyport) == 8443:
					proxyurl = "https://" + proxyurl
				else:
					proxyurl = "http://" + proxyurl
			elif common.any2int(httpproxytype) == 1 or common.any2int(httpproxytype) == 2:
				proxyurl = "socks4://" + proxyurl
			elif common.any2int(httpproxytype) == 3 or common.any2int(httpproxytype) == 4:
				proxyurl = "socks4://" + proxyurl
			PROXIES = {'http': proxyurl, 'https': proxyurl}
			common.trace("Detecting proxy in Kodi: %s" % proxyurl, "urlcall")
		else:
			PROXIES = {}
	if PROXIES is not None and not bool(PROXIES):
		return PROXIES
	else:
		return None


# Function: urlcall
def urlcall(url, method='GET', payload=None, headers=None, proxies=None, timeout=None, output=None, certver=True):
	common.debug("Calling URL: %s" %url, "urlcall")
	if payload is not None and isinstance(payload, str):
		payload = json.loads(payload)
		payload = None if not bool(payload) else payload
	if payload is not None:
		common.trace("Using payload: %s" %str(payload))
	if headers is not None and isinstance(headers, str):
		headers = json.loads(headers)
		headers = None if not bool(payload) else headers
	if headers is not None:
		common.trace("Using headers: %s" %str(headers))
	if proxies is None:
		proxies = getproxies()
	elif proxies is not None and isinstance(proxies, str):
		proxies = json.loads(proxies)
		proxies = None if not bool(proxies) else proxies
	if proxies is not None:
		common.trace("Using proxies: %s" %str(proxies))
	try:
		if method is None or method.lower() == 'get':
			response = requests.get(url, params=payload, headers=headers, proxies=proxies, timeout=timeout, verify=certver)
		elif method.lower() == 'post':
			if payload is not None and ((isinstance(payload, str) and payload.find('"file":') >=0 or payload.find("'file':") >=0) or (isinstance(payload, dict) and payload.has_key("file"))):
				response = requests.post(url, file=payload, headers=headers, proxies=proxies, timeout=timeout, verify=certver)
			else:
				response = requests.post(url, data=payload, headers=headers, proxies=proxies, timeout=timeout, verify=certver)
		elif method.lower() == 'put':
			response = requests.put(url, data=payload, headers=headers, proxies=proxies, timeout=timeout, verify=certver)
		elif method.lower() == 'delete':
			response = requests.put(url, headers=headers, proxies=proxies, timeout=timeout, verify=certver)
		elif method.lower() == 'head':
			response = requests.put(url, headers=headers, proxies=proxies, timeout=timeout, verify=certver)
		elif method.lower() == 'options':
			response = requests.put(url, headers=headers, proxies=proxies, timeout=timeout, verify=certver)
		else:
			response = None
		if response is None:
			common.error("Invalid HTTP method or invalid HTTP call: %s" %str(method), "urlcall")
		elif response.status_code != requests.codes.ok:
			common.error("Error received from remote server: HTTP%s - %s" %(str(response.status_code), response.text), "urlcall")
		if output is None or output == '' or output == 'text' or output == 'string':
			return response.text
		elif output =='bin' or output == 'binary':
			return response.content
		elif output =='json':
			return response.json()
		elif output =='response' or output =='original':
			return response
	except BaseException as err:
		common.error("Error while executing HTTP request for [%s] url: %s" % (url, str(err)), "urlcall")
		response = None
		if common.istrace:
			traceback.print_exc()
	return response


def urlquote(text):
	return quote(text)


def urlunquote(text):
	return unquote(text)


def urlparsequery(qs):
	return parse_qsl(qs)
