# -*- coding: utf-8 -*-

__all__ = ['run']

import commons
import platform
import traceback
from modshell.impl.ShellRunner import ShellRunner as Runner
from modshell.impl.ShellContext import ShellContext as Context


def run(provider, context=None):
	try:
		if not context:
			context = Context()
		runner = Runner()
		context.debug('Starting module shell..')
		py_version = 'Python %s' % str(platform.python_version())
		cx_version = context.getSystemVersion()
		context.notice('Starting %s (%s) on %s with %s' % (context.getName(), context.getVersion(), cx_version, py_version))
		context.debug('Execution details: path = %s, parameters = %s' %(context.getPath(), unicode(context.getParams())))
		# Run provider
		runner.run(provider, context)
		context.debug('Shutting down module shell..')
	except BaseException as bex:
		traceback.print_exc()
		commons.error("Error running module shell: " + str(bex))
		if context is not None:
			context.getUI().closeBusyDialog()
			context.getUI().onOk(context.getName(), "Error in module shell: " + str(bex))
		else:
			commons.OkDialog("Error in module shell: " + str(bex))
	pass
