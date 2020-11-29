# -*- coding: utf-8 -*-

import sys
import common
import urllib3
import subprocess


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
			common.debug("Preparing command for execution: %s" % (" ".join(cmd)), "commons")
			_output = subprocess.check_output(cmd)
		else:
			common.debug("Preparing command for execution: %s" % cmd)
			_output = subprocess.check_output(cmd, shell=True)
		_status = True
		if _output is not None:
			_output = _output.strip()
		common.debug("Command execution output: [%s] %s" % (str(_status), _output))
	except subprocess.CalledProcessError as grepexc:
		common.error("Exception while executing shell command: [%s] %s" % (grepexc.returncode, grepexc.output))
		_status = False
		_output = str(grepexc.output)
	except BaseException as err:
		common.error("Error while executing shell command: %s" % str(err))
		_status = False
		_output = str(err)
	return _status, _output


# Function: urlcall
def urlcall(url, method='GET', fields=None, headers=None, timeout=None, retries=3, certver=True, showerr=False):
	common.debug("Calling URL: %s" % url)
	http = urllib3.PoolManager()
	if certver is False:
		http = urllib3.PoolManager(cert_reqs = 'CERT_NONE')
	if method is None:
		method = "GET"
	try:
		if timeout is not None and timeout > 0.0:
			request = http.request(method, url, fields=fields, headers=headers, timeout=timeout, retries=retries)
		else:
			request = http.request(method, url, fields=fields, headers=headers, retries=retries)
		response = request.data
		request.close()
	except BaseException as err:
		response = None
		if not showerr:
			common.error("Error while executing HTTP request: %s" % str(err))
		else:
			raise err
	return response
