# -*- coding: utf-8 -*-

import os
import re
import sys
import json
import common
import urllib3
import certifi
import subprocess
import unicodedata
import traceback

if sys.version_info.major == 3:
	from urllib.parse import quote, unquote, parse_qsl
else:
	from urllib import quote, unquote
	from urlparse import parse_qsl


PROXIES = None


# Function: str2bool
def any2bool(v, error=False, none=True):
	if v is not None:
		if isinstance(v, bool):
			return v
		elif isinstance(v, int):
			return True if v > 0 else False
		elif isinstance(v, str):
			if v.lower() in ("on", "yes", "true", "1"):
				return True
			elif v.lower() in ("off", "no", "false", "0"):
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
			if error:
				raise RuntimeError("Invalid null value")


# Function: any2int
def any2int(v, error=False, none=True):
	if v is not None:
		if isinstance(v, int):
			return v
		else:
			try:
				return int(v)
			except BaseException as be:
				if error:
					raise RuntimeError(be)
				else:
					if isinstance(none, int):
						return none
					elif isinstance(none, bool) and none:
						return None
					elif isinstance(none, bool) and not none:
						raise RuntimeError("Invalid value: " + str(v))
	else:
		if isinstance(none, int):
			return none
		elif isinstance(none, bool) and none:
			return None
		elif (isinstance(none, bool) and not none) or error:
			raise RuntimeError("Invalid null value")


# Function: any2float
def any2float(v, error=False, none=True):
	if v is not None:
		if isinstance(v, float):
			return v
		else:
			try:
				return float(v)
			except BaseException as be:
				if error:
					raise RuntimeError(be)
				else:
					if isinstance(none, float):
						return none
					elif isinstance(none, bool) and none:
						return None
					elif isinstance(none, bool) and not none:
						raise RuntimeError("Invalid value: " + str(v))
	else:
		if isinstance(none, float):
			return none
		elif isinstance(none, bool) and none:
			return None
		elif (isinstance(none, bool) and not none) or error:
			raise RuntimeError("Invalid null value")


# Function: any2str
def any2str(v, error=False, none=True):
	if v is not None:
		if isinstance(v, bool):
			return str(v).lower()
		else:
			try:
				return str(v)
			except BaseException as be:
				if error:
					raise RuntimeError(be)
				else:
					if isinstance(none, str):
						return none
					elif isinstance(none, bool) and none:
						return None
					elif isinstance(none, bool) and not none:
						raise RuntimeError("Invalid value: " + str(v))
	else:
		if isinstance(none, str):
			return none
		elif isinstance(none, bool) and none:
			return None
		elif (isinstance(none, bool) and not none) or error:
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
			if str(v) == '':
				return True
			else:
				return False


def bstr(text):
	"""
	Converts any type of str text into a byte string value
	:param text: input text to be converted
	:return: byte str value
	"""
	if sys.version_info[0] == 2:
		if isinstance(text, unicode):
			text = text.encode('utf-8')
	else:
		if isinstance(text, str):
			text = text.encode('utf-8', 'ignore')
	return text


def ustr(text):
	"""
	Converts any type of str text into a unicode value
	:param text: input text to be converted
	:return: unicode str value
	"""
	if sys.version_info[0] == 2:
		if isinstance(text, str):
			text = unicode(text, "utf-8")
	else:
		if isinstance(text, bytes):
			text = text.decode('utf-8', 'ignore')
	return text


def strstrip(text, u=True):
	"""
	Performs a trimming action to the input string, dropping all special characters.
	The function works for both Python versions returning a byte str value
	:param text: input text to be converted
	:return: byte str value without special chars
	"""
	if sys.version_info[0] == 2:
		if isinstance(text, str):
			text = text.decode('ascii', 'ignore').encode('ascii')
		elif isinstance(text, unicode):
			text = text.encode('ascii', 'ignore')
	else:
		text = text.encode('ascii', 'ignore')
	return ustr(text) if u else bstr(text)


def strconvert(text, u=True):
	"""
	Performs a conversion action to the input string, tranform chans with accents or special
	termination into standard ascii chars
	:param text: input text to be converted
	:return: unicode str value replacing special chars with standard chars
	"""
	if sys.version_info[0] == 2:
		if isinstance(text, str):
			text = unicode(text, "utf-8")
	else:
		if isinstance(text, bytes):
			text = text.decode('utf-8', 'ignore')
	text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")
	return ustr(text) if u else bstr(text)


def procexec(cmd):
	"""
	Executes an operating system process to the file system  and shell level. The output
	is capture and returned as tuples, containing status (usually obtained from $?
	shell variable) and output value (standard output and/or error)
	:param cmd:	shell command to be executed.
	:return: tuples value with status and standard output
	"""
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
		common.trace("Command execution output: [%s] %s" % (str(_status), _output))
	except subprocess.CalledProcessError as grepexc:
		common.info("Unexpected exit code while executing subprocess: [%s] - %s" % (grepexc.returncode, grepexc.output), "procexec")
		_status = False
		_output = str(grepexc.output)
	except BaseException as err:
		common.error("Error while executing external process: %s" % str(err), "procexec")
		_status = False
		_output = str(err)
		if common.istrace:
			traceback.print_exc()
	return _status, _output



def funcall(fnc, *args, **kwargs):
	"""
	Executes a function referred like a string that is published into a package
	which is part of the running environment.
	:param fnc:	function name
	:return:	tuples value containing the status and the output of the called function
	"""
	common.debug("Calling function: %s" % fnc), "funcall"
	try:
		function = globals()[fnc]
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



def clscall(cls, mtd, *args, **kwargs):
	"""
	Executes a class method referred like strings that is published into a package
	which is part of the running environment.
	:param cls:	class name. could the name of the class of the instance
	:param mtd:	method name
	:return:	tuples value containing the status and the output of the called function
	"""
	try:
		if isinstance(cls, str):
			sig = type(cls, (), {})
			object = sig()
		else:
			object = cls
		common.debug("Calling method %s from class %s" % (mtd, type(object)), "clscall")
		method = getattr(object, mtd)
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


def sysinfo():
	"""
	Read system information details and return a dictionary with the following keys:
	NAME, VERSION, ID, ID_LIKE, PRETTY_NAME, VERSION_ID, VERSION_CODE, HOME_URL,
	BUILD_ID=, DEVICE, ARCH.
	For more details please check CLue-2 project CCM process
	"""
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
	return release_info


def getproxies():
	"""
	Get and merge the proxy configuration defined to the OS level and to Kodi level, over
	Kodi graphical interface.
	"""
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
	return PROXIES


def urlcall(url, method='GET', payload=None, headers=None, proxies=None, timeout=None, retries=3, output=None, certver=None):
	"""
	Runs HTTP(s) calls with all type of methods , with input data in HTTP query format for GET
	calls or using data pack prepared for POST call, and using various HTTP configurations (proxies,
	custom headers, etc.)
	:param url:		HTTP reference (URL) to be called
	:param method:	HTTP method to be executed. BY default it has GET value, the possible values are:
	GET, POST, PUT, PATCH,DELETE, HEAD
	:param payload: HTTP query or data to be send to the server over POST method. THe data has to
	be in dictionary format, providing the key and the corresponding value
	:param proxies:	describes the proxy configuration (dictionary format)
	:param timeout: indicates the HTTP connection timeout
	:param retries:	in case the HTTP connection fails, the process will retry how many times is specified
	by this parameter
	:param output:	shows the data output format: the possible values could be: None (it returns the
	original format, teext/string, bin/binary, json, response/original
	:param certver: describes the certification authority or a local or referred keystore containing
	certificate(s) to validate and trust the HTTPS (SSL) connection wit the target server.
	:return: data content (test or binary) obtained by the call and HTTP method. IN case the value
	is null might be the case to obtain an HTTP answer, other than 200 (the potential errors are
	logged into the logging channel)
	"""
	common.debug("Calling URL: %s" %url, "urlcall")
	# ssl validation
	if certver is not None and isinstance(certver, bool) and certver is False:
		urllib3.disable_warnings()
		http = urllib3.PoolManager(cert_reqs='CERT_NONE')
	else:
		if certver is not None and isinstance(certver, bool) and certver is True:
			http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
		elif certver is not None and isinstance(certver, str) and os.path.exists(certver):
			http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certver)
		else:
			http = urllib3.PoolManager()
	common.trace("Using HTTP Manager %s SSL validation: %s" %('without' if certver is not None and isinstance(certver, bool) and certver is False else 'with', str(certver)), "urlcall")
	# method identification
	if method is None or method.lower() not in ["get", "post", "head", "delete", "put", "patch"]:
		method = "GET"
	else:
		method = method.upper()
	common.trace("Using method: %s" % str(method), "urlcall")
	# payload validation
	if payload is not None and isinstance(payload, str):
		payload = json.loads(payload)
		payload = None if not bool(payload) else payload
	if payload is not None:
		common.trace("Using payload: %s" %str(payload), "urlcall")
	# header validation
	if headers is not None and isinstance(headers, str):
		headers = json.loads(headers)
		headers = None if not bool(headers) else headers
	if headers is not None:
		common.trace("Using headers: %s" %str(headers), "urlcall")
	# proxies considerations
	if proxies is None:
		proxies = getproxies()
	elif proxies is not None and isinstance(proxies, str):
		proxies = json.loads(proxies)
		proxies = None if not bool(proxies) else proxies
	if proxies is not None and len(proxies) >0:
		common.trace("Using proxies: %s" % str(proxies), "urlcall")
		if proxies["http"].startswith("http"):
			http = urllib3.ProxyManager(self=http, proxy_url=proxies["http"])
		elif proxies["http"].startswith("https"):
			http = urllib3.ProxyManager(self=http, proxy_url=proxies["https"])
		elif proxies["http"].startswith("socks4"):
			http = urllib3.contrib.socks.SOCKSProxyManager(self=http, proxy_url=proxies["socks4"])
		elif proxies["http"].startswith("socks5"):
			http = urllib3.contrib.socks.SOCKSProxyManager(self=http, proxy_url=proxies["socks5"])
	try:
		# process the request
		if timeout is not None and timeout > 0.0:
			response = http.request(method, url, fields=payload, headers=headers, timeout=timeout, retries=retries)
		else:
			response = http.request(method, url, fields=payload, headers=headers, retries=retries)
		# check the response
		if response is not None and response.status != 200:
			common.error("Error received from remote server: HTTP%s - %s" %(str(response.status), response.data), "urlcall")
			data = None
		elif response is not None:
			if output is None or output == '' or output == 'text' or output == 'string':
				data = str(response.data)
			elif output =='bin' or output == 'binary':
				data = response.data
			elif output =='json':
				data = json.loads(response.data.decode('utf-8'))
			elif output =='response' or output =='original':
				data = response
			else:
				common.error("Invalid output format: %s" %output, "urlcall")
				data = None
		else:
			common.error("Null response", "urlcall")
			data = None
	except BaseException as err:
		common.error("Error while executing HTTP request for [%s] url: %s" % (url, str(err)), "urlcall")
		data = None
		if common.istrace:
			traceback.print_exc()
	return data


def urlquote(text):
	"""
	Encode URLs or text content e.g. the path info, the query, etc., transforming the set of reserved
	characters that must be quoted.
	quote('abc def') -> 'abc%20def'
	:param text: path info or queries
	:return: quoted value
	"""
	return quote(text)


def urlunquote(text):
	"""
	Reverse of 'urlquote'
	unquote('abc%20def') -> 'abc def'
	"""
	return unquote(text)


def urlparsequery(qs):
	"""
	Parse a query given as a string argument.
	:param qs:	qs: percent-encoded query string to be parsed
	:return: 	parsed query described like a list of tuples elements
	"""
	return parse_qsl(qs)
