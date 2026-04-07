# Copyright (c) 2025-2026 Erik Persson
# Licensed for free use only. Copying, modification, or redistribution prohibited.

import builtins
from Functions.Common import *
from Functions.DataHandling import *
from requests_negotiate_sspi import HttpNegotiateAuth
for name in dir ():
    if not name.startswith ("_"):
        builtins.__dict__[name] = globals ()[name]
#import pip_system_certs.wrapt_requests
import requests
builtins.requests = requests
import certifi
builtins.certifi = certifi
import json
builtins.json = json
import urllib3
builtins.urllib3 = urllib3
import subprocess
builtins.subprocess = subprocess
import os
builtins.os = os
import tempfile
builtins.tempfile = tempfile

class Web:
	def __init__ (self, cls_steps):
		self.cls_steps = cls_steps
		self.internal_web_defaults = {}
	
	
	def dynamic_function (self, function, to_class = True):
		if to_class is True:
			func = {}
			exec (function['Code'], func)
			setattr (Web, function['Function'], func[function['Function']])
		else:
			exec (function['Code'], globals ())
			builtins.__dict__[function['Function']] = globals ()[function['Function']]

	
	def execute (self, isolation = None, **opts):
		try:
			if opts['Function'] == 'WEB:URL':
				return self.step_url (isolation, **opts)
			elif opts['Function'] == 'WEB:URL.Encode':
				return self.step_url_encode (isolation, **opts)
			elif opts['Function'] == 'WEB:Default.Web.Interal':
				return self.step_default_web_internal (isolation, **opts)
			else:
				return False, {'Status':'WARNING', 'Title':'WEB:execute: Aborted', 'Message':'Unknown execute:' + str (opts)}
		except Exception as e:
			st = internal_zyd_stacktrace (e, FunctionOpts=opts)
			return False, {'Status':'CRASH', 'Title':'WEB:execute: Crashed', 'Message':'Crashed with the error: ' + str (e) + ' for step:\n' + str (opts), 'StackTrace':st}
	
	
	def step_url (self, isolation, **opts):
		if 'URL' not in opts:
			return False, {'Status':'WARNING', 'Title':'WEB:step_url_get: Aborted', 'Message':'No URL was provided.'}
		if 'Method' not in opts:
			return False, {'Status':'WARNING', 'Title':'WEB:step_url_get: Aborted', 'Message':'No Method was provided.'}
		if opts['Method'] not in ['GET', 'POST', 'PUT', 'Windows.Powershell']:
			return False, {'Status':'WARNING', 'Title':'WEB:step_url_get: Aborted', 'Message':'Unknown Method was provided ("' + str (opts['Method']) + '").'}
		statusvalid = (opts['ValidStatuses'] if 'ValidStatuses' in opts and isinstance (opts['ValidStatuses'], list) else [200])
		
		request_opts = {}
		if 'Redirects' in opts and opts['Redirects'] is False:
			request_opts['allow_redirects'] = False
		if 'Headers' in opts and isinstance (opts['Headers'], dict):
			request_opts['headers'] = opts['Headers']
		if 'Auth' in opts and opts['Auth'] is True:
			request_opts['auth'] = HttpNegotiateAuth ()
		if 'Data.JSON' in opts:
			request_opts['json'] = opts['Data.JSON']
		if 'Data' in opts:
			request_opts['data'] = opts['Data']
		if 'Verify' in opts and opts['Verify'] is False:
			request_opts['verify'] = False
		if 'Verify.DisableWarnings' in opts and opts['Verify.DisableWarnings'] is True:
			urllib3.disable_warnings (urllib3.exceptions.InsecureRequestWarning)
		if 'Verify.Certifi' in opts and opts['Verify.Certifi'] is True:
			request_opts['verify'] = certifi.where ()
		if 'Files' in opts and isinstance (opts['Files'], dict):
			request_opts['files'] = opts['Files']
		if 'Proxies' in opts and isinstance (opts['Proxies'], dict):
			request_opts['proxies'] = opts['Proxies']
		
		if 'Encrypt' in opts and opts['Encrypt'] is True:
			for field in ['']:
				if field in request_opts:
					try:
						request_opts[field] = self.cls_steps.internal_bz2_encrypt (request_opts[field])
					except Exception as e:
						return False, {'Status':'WARNING', 'Title':'WEB:step_url_get: Crashed', 'Message':'Encrypting crashed for key "' + str (field) + '"'}

		debug_console = (True if 'Debug.Console' in opts and opts['Debug.Console'] is True else False)
		
		if debug_console is True:
			print ('+==[ step_url ]==============================================================')
			print ('Method=' + str (opts['URL']))
			print ('Request_opts=' + str (request_opts))
		
		if opts['Method'] == 'GET':
			result = requests.get (opts['URL'], **request_opts)
		elif opts['Method'] == 'POST':
			result = requests.post (opts['URL'], **request_opts)
		elif opts['Method'] == 'PUT':
			result = requests.put (opts['URL'], **request_opts)
		elif opts['Method'] == 'Windows.Powershell':
			temp_file = (opts['Powershell.TempFile'] if 'Powershell.TempFile' in opts else os.path.join (tempfile.gettempdir (), 'OmoikaneFlows.' + internal_zyd_uniqueid () + '.tmp'))
			process = subprocess.Popen (["powershell.exe", "-Command", "(Invoke-WebRequest -Uri '" + opts['URL'] + "' -OutFile '" + temp_file + "' -MaximumRedirection 10).Content"], stdout=subprocess.PIPE)
			out, err = process.communicate ()
			with open (temp_file, 'rb') as file:
				value = file.read ()
			os.remove (temp_file)
			status = True
			if ('Powershell.Binary' not in opts or opts['Powershell.Binary'] is not True) and ('Decrypt' not in opts or opts['Decrypt'] is False):
				value = value.decode ('UTF-8')
		
		if opts['Method'] not in ['Windows.Powershell']:
			if debug_console is True:
				print ('Result=' + str (result))
			status = result.status_code
			if debug_console is True:
				print ('Status=' + str (status))
			if 'Status' in opts and opts['Status'] is True:
				value = result.status_code
			elif 'Content' in opts and opts['Content'] is True:
				value = result.content
			elif result.status_code in statusvalid:
				value = result.text
			else:
				return False, {'Status':'WARNING', 'Title':'WEB:step_url_get: Aborted', 'Message':'Invalid responce status "' + str (result.status_code) + '".', 'Result':result.text}
		
		if 'Decrypt' in opts and opts['Decrypt'] is True:
			try:
				value = self.cls_steps.internal_bz2_decrypt (value)
			except Exception as e:
				return False, {'Status':'WARNING', 'Title':'WEB:step_url_get: Crashed', 'Message':'Decryping crashed: ' + str (e)}
		
		if 'JSON' in opts and opts['JSON'] is True:
			try:
				value = json.loads (value)
			except Exception as e:
				return False, {'Status':'WARNING', 'Title':'WEB:step_url_get: Aborted', 'Message':'Responce could not be converted from JSON (error: ' + str (e) + ').', 'Input':value}
		
		if 'ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str):
			self.cls_steps.internal_value_set_value (isolation, 'Variable', value, opts['ReturnVariable'])
		if 'ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str):
			self.cls_steps.internal_value_set_value (None, 'Variable', value, opts['ReturnVariable.Global'])
		if 'ReturnVariable.Status' in opts and isinstance (opts['ReturnVariable.Status'], str):
			self.cls_steps.internal_value_set_value (isolation, 'Variable', status, opts['ReturnVariable.Status'])
		if 'ReturnVariable.Status.Global' in opts and isinstance (opts['ReturnVariable.Status.Global'], str):
			self.cls_steps.internal_value_set_value (None, 'Variable', status, opts['ReturnVariable.Status.Global'])
		if 'UpdateGUI.Value' in opts and isinstance (opts['UpdateGUI.Value'], str):
			self.cls_steps.cls_gui.internal_object_update (isolation, opts['UpdateGUI.Value'], Value=value, Trigger=(True if 'UpdateGUI.Value.Trigger' in opts and opts ['UpdateGUI.Value.Trigger'] is True else False))
		if debug_console is True:
			print ('-============================================================================')
		return True, {'Status':'OK', 'Data.Status':status, 'Data':value}
	
	
	def step_url_encode (self, isolation, **opts):
		if 'URL' not in opts:
			return False, {'Status':'WARNING', 'Title':'WEB:step_url_get: Aborted', 'Message':'No URL was provided.'}

		value = requests.utils.quote (opts['URL'])
		if value.startswith ('https%3A//'):
			value = 'https://' + value[10:]
		elif value.startswith ('http%3A//'):
			value = 'http://' + value[9:]
		if 'ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str):
			self.cls_steps.internal_value_set_value (isolation, 'Variable', value, opts['ReturnVariable'])
		if 'ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str):
			self.cls_steps.internal_value_set_value (None, 'Variable', value, opts['ReturnVariable.Global'])
		return True, {'Status':'OK', 'Data':value}
	
	
	def step_default_web_internal (self, isolation, **opts):
		updates = 0
		for field in [
			['Verify', bool],
			['Verify.DisableWarnings', bool],
			['Auth', bool],
		]:
			if field[0] in opts and isinstance (opts[field[0]], field[1]):
				updates += 1
				self.internal_web_defaults[field[0]] = copy.deepcopy (opts[field[0]])
		return True, {'Status':'OK', 'Message':str (updates) + ' defaults were updated.'}
	
	
	def internal_web (self, url, **opts):
		web_opts = copy.deepcopy (opts)
		web_opts['URL'] = url
		if 'Method' not in web_opts:
			web_opts['Method'] = 'GET'
		for field in ['Verify', 'Auth', 'Verify.DisableWarnings']:
			if field not in web_opts and field in self.internal_web_defaults:
				web_opts[field] = self.internal_web_defaults[field]
		for field in ['ReturnVariable', 'ReturnVariable.Global', 'ReturnVariable.Status', 'ReturnVariable.Status.Global', 'UpdateGUI.Value', 'UpdateGUI.Value.Trigger']:
			if field in web_opts:
				del (web_opts[field])
		
		status, result = self.step_url (None, **web_opts)
		if status is True:
			return result['Data']
		return {'Status':'ERROR', 'Message':'Failed with the following error:\n' + str (result)}
