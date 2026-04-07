# Copyright (c) 2025-2026 Erik Persson
# Licensed for free use only. Copying, modification, or redistribution prohibited.

from Functions.Common import *
from Functions.DataHandling import *
from cryptography.fernet import Fernet
import builtins
import sys
import os
import json
import copy
import threading
import bz2
import socket
import importlib.util
import WinClasses.SQL
import WinClasses.Core
import WinClasses.GUI
import WinClasses.Data
import WinClasses.Logic
import WinClasses.IO
import WinClasses.Web
import WinClasses.PDF
import WinClasses.Image
import WinClasses.Excel
import WinClasses.Pandas
import WinClasses.Scripting
import WinClasses.Omoikane
import WinClasses.OmoikaneV2
import WinClasses.OmoikaneV3
import Classes.Flows

class Steps:

	def __init__ (self, **opts):
		self.version_core = None
		self.tds = False
		self.version = None
		self.userinfo = {
			'User':None,
			'IP':None,
			'Hostname':None,
			'Domain':None,
			'Python':None,
		}
		self.variables_global = {}
		self.variables_isolated = {}
		self.variables_internal = {
			'ExecuteSteps':0,
			'Steps':0,
			'Debug.Log':[],
		}
		self.objects = {
			'Lock':{
				'Debugging':threading.RLock (),
				'Variables':threading.RLock (),
			},
			'Excel':{},
			'Pandas':{},
			'PDF':{},
		}
		self.debug = {
			'Active':False,
			'File.Log':[],
			'File.Log.Size':0,
			'Output':[],
		}
		self.function_defaults = {}
		self.cls_flows = Classes.Flows.Flows ()
		self.cls_gui = WinClasses.GUI.GUI (self)
		self.cls_core = WinClasses.Core.Core (self)
		self.cls_sql = WinClasses.SQL.SQL (self)
		self.cls_data = WinClasses.Data.Data (self)
		self.cls_logic = WinClasses.Logic.Logic (self)
		self.cls_io = WinClasses.IO.IO (self)
		self.cls_web = WinClasses.Web.Web (self)
		self.cls_pdf = WinClasses.PDF.PDF (self)
		self.cls_image = WinClasses.Image.Image (self)
		self.cls_excel = WinClasses.Excel.Excel (self)
		self.cls_pandas = WinClasses.Pandas.Pandas (self)
		self.cls_scripting = WinClasses.Scripting.Scripting (self)
		self.cls_omoikanev2 = WinClasses.OmoikaneV2.OmoikaneV2 (self)
		self.cls_omoikanev3 = WinClasses.OmoikaneV3.OmoikaneV3 (self)
		self.cls_omoikane = WinClasses.Omoikane.Omoikane (self)
#		self.cls_example = self.internal_import ('Example', 'Example')
		self.fernet = Fernet (self.cls_flows.fernet_key)
		self.version_core = self.cls_flows.version_core
		self.online_steps = {}
		
	
	def start (self, **opts):
		steps = []
		external = {}
		if 'Debug.File' in opts and isinstance (opts['Debug.File'], str) and 'OmoikaneFlows' in opts['Debug.File']:
			self.debug['Active'] = True
			if 'Debug.File.Instant' in opts and opts['Debug.File.Instant'] is True:
				self.debug['Instant'] = True
			self.debug['Output'].append ({"Type":"File", "File":opts['Debug.File']})
			if 'Debug.File.Reset' in opts and opts['Debug.File.Reset'] is True:
				with open (opts['Debug.File'], 'w', encoding='UTF-8') as fp:
					pass
		if 'WindowsPos' in opts and '+' in opts['WindowsPos']:
			self.cls_gui.startpos = opts['WindowsPos']
		if 'StepsFile' in opts and os.path.exists (opts['StepsFile']):
			with open (opts['StepsFile'], 'r') as file:
				steps = json.loads (file.read ().replace ('\r', ''))
			external['Steps'] = {'File':opts['StepsFile'], 'Steps':steps}
		for ext_file in ['Scripting', 'External', 'OmoikaneV2', 'OmoikaneV3']:
			if ext_file in opts:
				with open (opts[ext_file]) as fp:
					file = fp.read ()
					if 'Classes' not in external:
						external['Classes'] = {ext_file:{'File':opts[ext_file], 'Class':file}}
					else:
						external['Classes'][ext_file] = {'File':opts[ext_file], 'Class':file}
					exec (file, globals ())
				if ext_file == 'Scripting':
					self.cls_scripting = Scripting (self)
				elif ext_file == 'External':
					self.cls_external = External (self)
				elif ext_file == 'OmoikaneV2':
					self.cls_omoikanev2 = OmoikaneV2 (self)
				elif ext_file == 'OmoikaneV3':
					self.cls_omoikanev3 = OmoikaneV3 (self)
				print ('EXTERNAL_LOGIC_LOADED=' + str (opts[ext_file]))
		if 'Online' in opts and opts['Online'] is True and len (external) > 0:
			if 'TDS' in opts and opts['TDS'] is True:
				self.tds = True
			try:
				print ('ONLINE.CHECKING_EXTERNAL_CLASSES')
				jsondata = zyd_json ({'VersionCore':self.cls_flows.version_core, 'Version':self.version, 'UserInfo':self.userinfo, 'External':external}, Encode=True, Internal=True)
				status, online = self.cls_web.step_url (None, **{'URL':'https://www.omoikane.se/APIs/Flows/ExternalComponents?' + ('TDS=1&' if 'TDS' in opts and opts['TDS'] is True else '') + 'DebugSave=' + str (self.userinfo['User']) + '@' + str (self.userinfo['Hostname']), 'Debug.Console':False, 'Method':'POST', 'Data':self.internal_bz2_encrypt (jsondata), 'Content':True, 'Verify':False, 'Verify.DisableWarnings':True})
				if status is True and isinstance (online, dict) and 'Status' in online and online['Status'] == 'OK' and 'Data' in online and isinstance (online['Data'], bytes):
					data = zyd_json (self.internal_bz2_decrypt (online['Data']), Decode=True, Internal=True)
					if 'Status' in data and 'Message' in data:
						print ('ONLINE.CHECKING_EXTERNAL_CLASSES=' + str (data['Status']) + '::' + str (data['Message']))
			except Exception as e:
				print ('ONLINE.CHECKING_EXTERNAL_CLASSES=CRAHSED=' + str (e))
		
		if 'License' in opts and opts['License'] is True:
			print ('Copyright (c) 2025-2026 Erik Persson')
			print ('')
			print ('Permission is hereby granted to any person to use this software free of charge,')
			print ('for personal or commercial purposes, provided that:')
			print ('')
			print ('1. The source code may not be copied, modified, distributed, or reused in any form.')
			print ('2. The software is provided "as is" without warranty of any kind, express or implied.')
			print ('3. The author retains all rights to the source code.')
			print ('')
			print ('By using this software, you agree to these terms.')
		elif 'Version' in opts and opts['Version'] is True:
			print ('OmoikaneFlows version ' + self.version)
		else:
			if 'Steps' in self.online_steps and len (steps) == 0 and len (self.online_steps['Steps']) > 0:
				steps = self.online_steps['Steps']
			if 'Steps.Append' in self.online_steps and len (self.online_steps['Steps.Append']) > 0:
				steps += self.online_steps['Steps.Append']
			if 'Steps.Override' in self.online_steps and len (self.online_steps['Steps.Override']) > 0:
				steps = self.online_steps['Steps.Override']
			
			self.execute_steps (steps)
			self.cls_gui.start ()

	
	def stop (self):
		import time
		print ('cls_steps.STOP')
		time.sleep (1)
		for thread in self.cls_logic.threads.keys ():
			print ('STOP=' + str (thread))
			self.cls_logic.threads[thread].join ()
		self.internal_debugging_buffer_write ()
	
	
	def execute_steps (self, steps, isolation = None, segment = '*'):
		executestepno = self.internal_value_get_value (None, 'InternalVariable', 'ExecuteSteps') + 1
		self.internal_value_set_value (None, 'InternalVariable', executestepno, 'ExecuteSteps')
		if self.debug['Active'] is True:
			self.internal_debugging (Function='execute_steps', ExecuteSteps=executestepno, Stage='Init', Isolation=isolation, Segment=segment)
		breaksegment = None
		while True:
			if self.debug['Active'] is True:
				self.internal_debugging (Function='execute_steps', ExecuteSteps=executestepno, Stage='Init.Steps', StepCount=len (steps))
			if len (steps) == 0:
				break
			step = steps.pop (0)
#			print (step)
#			print (steps)
			if self.debug['Active'] is True:
				self.internal_debugging (Function='execute_steps', ExecuteSteps=executestepno, Stage='Step.Init', Isolation=isolation, Segment=segment, Step=step)
			
			if not isinstance (step, dict):
				return False, {'Status':'ERROR', 'Title':'execute_steps: Aborted', 'Message':'Not a valid step:\n' + str (step)}
			if 'Function.Segment' not in step:
				step['Function.Segment'] = copy.deepcopy (segment)
			if len (self.function_defaults) > 0:
				for field in self.function_defaults.keys ():
					if field not in step:
						step[field] = copy.deepcopy (self.function_defaults[field])
			if self.debug['Active'] is True:
				self.internal_debugging (Function='execute_steps', ExecuteSteps=executestepno, Stage='Steps.StepCount.Before', StepCount=len (steps))
			status, result = self.execute_step (steps, isolation, **step)
#			print (status)
#			print (result)
			if self.debug['Active'] is True:
				self.internal_debugging (Function='execute_steps', ExecuteSteps=executestepno, Stage='Steps.StepCount.After', StepCount=len (steps), Steps=steps)
			
			if status is not True:
				if 'Functions.OnFailure' in step and isinstance (step['Functions.OnFailure'], list):
					rstatus, rresult = self.execute_steps (step['Functions.OnFailure'], isolation)
					if 'Break' in rresult and rresult['Break'] is True:
						return rstatus, rresult
				if isinstance (result, dict) and 'Status' in result:
					if result['Status'] == 'ERROR' and 'Functions.OnError' in step and isinstance (step['Functions.OnError'], list):
						rstatus, rresult = self.execute_steps (step['Functions.OnError'], isolation)
						if 'Break' in rresult and rresult['Break'] is True:
							return rstatus, rresult
					elif result['Status'] == 'WARNING' and 'Functions.OnWarning' in step and isinstance (step['Functions.OnWarning'], list):
						rstatus, rresult = self.execute_steps (step['Functions.OnWarning'], isolation)
						if 'Break' in rresult and rresult['Break'] is True:
							return rstatus, rresult
					elif result['Status'] == 'CRASH' and 'Functions.OnCrash' in step and isinstance (step['Functions.OnCrash'], list):
						rstatus, rresult = self.execute_steps (step['Functions.OnCrash'], isolation)
						if 'Break' in rresult and rresult['Break'] is True:
							return rstatus, rresult
				return status, result
			else:
				if 'Functions.OnSuccess' in step and isinstance (step['Functions.OnSuccess'], list):
					rstatus, rresult = self.execute_steps (step['Functions.OnSuccess'], isolation)
					if 'Break' in rresult and rresult['Break'] is True:
						return rstatus, rresult
				if isinstance (result, dict) and 'Status' in result:
					if result['Status'] == 'OK' and 'Functions.OnOK' in step and isinstance (step['Functions.OnOK'], list):
						rstatus, rresult = self.execute_steps (step['Functions.OnOK'], isolation)
						if 'Break' in rresult and rresult['Break'] is True:
							return rstatus, rresult
			if self.debug['Active'] is True:
				self.internal_debugging (Function='execute_steps', ExecuteSteps=executestepno, Stage='Step.End', Status=status, Result=result)
			if status is not True: 	
				if self.debug['Active'] is True:
					self.internal_debugging (Function='execute_steps', ExecuteSteps=executestepno, Stage='Step.End.Break', Status=status, Result=result)
				break
		if self.debug['Active'] is True:
			self.internal_debugging (Function='execute_steps', ExecuteSteps=executestepno, Stage='End', Isolation=isolation, Segment=segment)
		return True, {'Status':'OK'}


	def execute_step (self, steps, isolation = None, **opts):
		try:
			stepno = self.internal_value_get_value (None, 'InternalVariable', 'Steps') + 1
			self.internal_value_set_value (None, 'InternalVariable', stepno, 'Steps')
			if self.debug['Active'] is True:
				self.internal_debugging (Function='execute_step', StepNo=stepno, Stage='Init', Isolation=isolation, Opts=opts)
	#		print ('EXECUTE_STEP=' + str (opts))
			status = False
			result = {'Status':'ERROR', 'Title':'Steps.execute: Aborted', 'Message':'Unknown step:' + str (opts)}
			if 'Function' in opts:
				if opts['Function'].startswith ('GUI:'):
					status, result = self.cls_gui.execute (isolation, **self.internal_value (isolation, copy.deepcopy (opts)))
				elif opts['Function'].startswith ('CORE:'):
					status, result =  self.cls_core.execute (steps, isolation, **self.internal_value (isolation, copy.deepcopy (opts)))
				elif opts['Function'].startswith ('SQL:'):
					status, result =  self.cls_sql.execute (isolation, **self.internal_value (isolation, copy.deepcopy (opts)))
				elif opts['Function'].startswith ('DATA:'):
					status, result =  self.cls_data.execute (isolation, **self.internal_value (isolation, copy.deepcopy (opts)))
				elif opts['Function'].startswith ('LOGIC:'):
					status, result =  self.cls_logic.execute (steps, isolation, **self.internal_value (isolation, copy.deepcopy (opts)))
				elif opts['Function'].startswith ('IO:'):
					status, result =  self.cls_io.execute (isolation, **self.internal_value (isolation, copy.deepcopy (opts)))
				elif opts['Function'].startswith ('WEB:'):
					status, result =  self.cls_web.execute (isolation, **self.internal_value (isolation, copy.deepcopy (opts)))
				elif opts['Function'].startswith ('PDF:'):
					status, result =  self.cls_pdf.execute (isolation, **self.internal_value (isolation, copy.deepcopy (opts)))
				elif opts['Function'].startswith ('IMAGE:'):
					status, result =  self.cls_image.execute (isolation, **self.internal_value (isolation, copy.deepcopy (opts)))
				elif opts['Function'].startswith ('EXCEL:'):
					status, result =  self.cls_excel.execute (isolation, **self.internal_value (isolation, copy.deepcopy (opts)))
				elif opts['Function'].startswith ('PANDAS:'):
					status, result =  self.cls_pandas.execute (isolation, **self.internal_value (isolation, copy.deepcopy (opts)))
				elif opts['Function'].startswith ('SCRIPTING:'):
					status, result =  self.cls_scripting.execute (steps, isolation, **self.internal_value (isolation, copy.deepcopy (opts)))
				elif opts['Function'].startswith ('EXTERNAL:'):
					status, result =  self.cls_external.execute (isolation, **self.internal_value (isolation, copy.deepcopy (opts)))
				elif opts['Function'].startswith ('OMOIKANE:'):
					status, result = self.cls_omoikane.execute (steps, isolation, **self.internal_value (isolation, copy.deepcopy (opts)))
				elif opts['Function'].startswith ('OMOIKANEV2:'):
					status, result =  self.cls_omoikanev2.execute (isolation, **self.internal_value (isolation, copy.deepcopy (opts)))
				elif opts['Function'].startswith ('OMOIKANEV3:'):
					status, result =  self.cls_omoikanev3.execute (isolation, **self.internal_value (isolation, copy.deepcopy (opts)))
			elif '_Function' in opts:
				status = True
				result = {'Status':'OK', 'Title':'Steps.execute: Skipped', 'Message':'"_Function" logic used to skip the function'}
			elif '__Function' in opts:
				return True, {'Status':'OK'}
			
			
			if len (str (result)) <= 200 or ('Function.FullResult' in opts and opts['Function.FullResult'] is True):
				print (str (status) + '::' + str (result))
			elif isinstance (result, dict):
				disp = copy.deepcopy (result)
				for key in disp.keys ():
					if len (str (disp[key])) > 100:
						disp[key] = str (disp[key])[:100] + '...'
				print (str (status) + '::' + str (disp))
			else:
				print (str (status) + '::' + str (result)[:100] + '...')
			
			if isinstance (result, dict) and 'Status' in result and 'StackTrace' in result and result['Status'] == 'CRASH':
				print ('+==[ CRASHED: StackTrace ]==========================================================================')
				print (result['StackTrace'])
				print ('-==[ CRASHED: StackTrace ]==========================================================================')
			elif status is not True:
				if 'Function.OnFailure' in opts and isinstance (opts['Function.OnFailure'], list):
					rstatus, rresult = self.execute_steps (opts['Function.OnFailure'], isolation)
					if 'Break' in rresult and rresult['Break'] is True:
						return rstatus, rresult
			else:
				if 'Function.OnSuccess' in opts and isinstance (opts['Function.OnSuccess'], list):
					rstatus, rresult = self.execute_steps (opts['Function.OnSuccess'], isolation)
					if 'Break' in rresult and rresult['Break'] is True:
						return rstatus, rresult
				if 'Function.OnSuccess.DataTrue' in opts and isinstance (opts['Function.OnSuccess.DataTrue'], list) and isinstance (result, dict) and 'Data' in result and result['Data'] is True:
					rstatus, rresult = self.execute_steps (opts['Function.OnSuccess.DataTrue'], isolation)
					if 'Break' in rresult and rresult['Break'] is True:
						return rstatus, rresult
				if 'Function.OnSuccess.DataFalse' in opts and isinstance (opts['Function.OnSuccess.DataFalse'], list) and isinstance (result, dict) and 'Data' in result and result['Data'] is False:
					rstatus, rresult = self.execute_steps (opts['Function.OnSuccess.DataFalse'], isolation)
					if 'Break' in rresult and rresult['Break'] is True:
						return rstatus, rresult

			if self.debug['Active'] is True:
				self.internal_debugging (Function='execute_step', StepNo=stepno, Stage='End', Status=status, Result=result)
			return status, result
		except Exception as e:
			st = internal_zyd_stacktrace (e, FunctionOpts=opts)
			return False, {'Status':'CRASH', 'Title':'STEPS:execute_step: Crashed', 'Message':'Crashed with the error: ' + str (e) + ' for step:\n' + str (opts), 'StackTrace':st}

	
	def internal_value_get_value (self, isolation, type, key, subkey = None, valuekey = None):
		if type == 'GUI':
			if key == 'Table':
				if isinstance (valuekey, str) and ':' in valuekey:
					try:
						pos = valuekey.split (':')
						pos[0] = int (pos[0])
						pos[1] = int (pos[1])
						print (self.cls_gui.objects[key][subkey]['Value'])
						if len (self.cls_gui.objects[key][subkey]['Value']) > pos[0] and len (self.cls_gui.objects[key][subkey]['Value'][pos[0]]) > pos[1]:
							return self.cls_gui.objects[key][subkey]['Value'][pos[0]][pos[1]]
					except Exception as e:
						st = internal_zyd_stacktrace (e)
						print ('Crash::internal_value_get_value::' + str (valuekey) + '::' + str (st))
			else:
				return copy.deepcopy (self.cls_gui.objects[key][subkey]['Value'])
		elif type == 'Variable':
			if isolation is None or (isinstance (isolation, dict) and dict['Isolation'] is None):
				return copy.deepcopy (self.variables_global[key])
			else:
				return copy.deepcopy (self.variables_isolated[(str (isolation['Isolation']) if isinstance (isolation, dict) and 'Isolation' in isolation else str (isolation))][key])
		elif type == 'InternalVariable':
			return copy.deepcopy (self.variables_internal[key])


	def internal_value_set_value (self, isolation, type, value, key, subkey = None):
		with self.objects['Lock']['Variables']:
			if type == 'GUI':
				if key == 'Table':
					print ('MISSING_LOGIC::internal_value_set_value::' + str (type))
				else:
					self.cls_gui.objects[key][subkey]['Value'] = value
			elif type == 'Variable':
				if isolation is None or (isinstance (isolation, dict) and dict['Isolation'] is None):
					self.variables_global[key] = value
				else:
					isolationkey = (str (isolation['Isolation']) if isinstance (isolation, dict) and 'Isolation' in isolation else str (isolation))
					if isolationkey in self.variables_isolated:
						self.variables_isolated[isolationkey][key] = value
					else:
						self.variables_isolated[isolationkey] = {key:value}
			elif type == 'InternalVariable':
				self.variables_internal[key] = value
	
	
	def internal_value_exists (self, isolation, type, key, subkey = None, valuekey = None):
		if type == 'GUI':
			if key == 'Table':
				if isinstance (valuekey, str) and ':' in valuekey:
					try:
						pos = valuekey.split (':')
						pos[0] = int (pos[0])
						pos[1] = int (pos[1])
						return (True if key in self.cls_gui.objects and subkey in self.cls_gui.objects[key] and 'Value' in self.cls_gui.objects[key][subkey] and isinstance (self.cls_gui.objects[key][subkey]['Value'], list) and len (self.cls_gui.objects[key][subkey]['Value']) > pos[0] and len (self.cls_gui.objects[key][subkey]['Value'][pos[0]]) > pos[1] else False)
					except Exception as e:
						return False
			else:
				return (True if key in self.cls_gui.objects and subkey in self.cls_gui.objects[key] and 'Value' in self.cls_gui.objects[key][subkey] else False)
		elif type == 'Variable':
			if isolation is None or (isinstance (isolation, dict) and dict['Isolation'] is None):
				return (True if key in self.variables_global else False)
			else:
				isolationkey = (str (isolation['Isolation']) if isinstance (isolation, dict) and 'Isolation' in isolation else str (isolation))
				return (True if isolationkey in self.variables_isolated and key in self.variables_isolated[isolationkey] else False)
		elif type == 'InternalVariable':
			return (True if key in self.variables_internal else False)

	
	def internal_value (self, isolation, value, function = None):
		if isinstance (value, dict):
			for key in value.keys ():
				# Don't replace values for sub steps which might use dynamic values later on...
				if key == 'Function' and isinstance (value[key], str) and value[key] in self.cls_flows.functions:
					function = copy.deepcopy (value[key])
				if function is not None:
					if key in self.cls_flows.functions[function]['Input'] and 'Steps' in self.cls_flows.functions[function]['Input'][key] and self.cls_flows.functions[function]['Input'][key]['Steps'] is True and (isinstance (value[key], list) or ('Steps.Dict' in self.cls_flows.functions[function]['Input'][key] and self.cls_flows.functions[function]['Input'][key]['Steps.Dict'] is True and isinstance (value[key], dict))):
#						print ('\tSKIP(' + str (function) + ')=' + str (key) + '::' + str (value))
						continue
					elif isinstance (value, dict):
						if 'Function.Opts.Steps' in value and key in value['Function.Opts.Steps']:
							print ('Function.STEPS::' + str (key))
							continue
				value[key] = self.internal_value (isolation, value[key], function)
		elif isinstance (value, list):
			for key in range (0, len (value)):
				value[key] = self.internal_value (isolation, value[key], function)
		elif isinstance (value, str) and len (value) > 5 and '<' in value and '>' in value:
#			if value[:2] + value[-2:] == '<$$>' and value[2:-2] in self.variables:
			if value[:2] + value[-2:] == '<$$>' and self.internal_value_exists (isolation, 'Variable', value[2:-2]):
#				return copy.deepcopy (self.variables[value[1:-1]])
				return self.internal_value_get_value (isolation, 'Variable', value[2:-2])
			elif value[:3] + value[-3:] == '<$##$>' and '##' in value:
				gui = value[3:-3].split ('##')
#				if gui[0] in self.cls_gui.objects and gui[1] in self.cls_gui.objects[gui[0]] and 'Value' in self.cls_gui.objects[gui[0]][gui[1]]:
				if len (gui) == 2:
					if self.internal_value_exists (isolation, 'GUI', gui[0], gui[1]):
#						return copy.deepcopy (self.cls_gui.objects[gui[0]][gui[1]]['Value'])
						return self.internal_value_get_value (isolation, 'GUI', gui[0], gui[1])
				elif len (gui) == 3:
					if self.internal_value_exists (isolation, 'GUI', gui[0], gui[1], gui[2]):
						print ('EXISTS')
#						return copy.deepcopy (self.cls_gui.objects[gui[0]][gui[1]]['Value'])
						return self.internal_value_get_value (isolation, 'GUI', gui[0], gui[1], gui[2])
#			elif value[:2] + value[-2:] == '<@@>' and value[2:-2] in self.variables_internal:
			elif value[:2] + value[-2:] == '<@@>' and self.internal_value_exists (isolation, 'InternalVariable', value[2:-2]):
				return self.internal_value_get_value (isolation, 'InternalVariable', value[2:-2])
#				return copy.deepcopy (self.variables_internal[value[1:-1]])
			elif value[:2] + value[-2:] == '<##>' and self.internal_value_exists (None, 'Variable', value[2:-2]):
#				print ('\tISOLATED:' + str (value))
#				return copy.deepcopy (self.variables[value[1:-1]])
				return self.internal_value_get_value (None, 'Variable', value[2:-2])
			
			changed = False
			if '<$#' in value and '#$>' in value:
				for object_type in self.cls_gui.objects.keys ():
					if isinstance (self.cls_gui.objects[object_type], dict):
						for object_id in self.cls_gui.objects[object_type].keys ():
#								if 'Value' in self.cls_gui.objects[object_type][object_id] and '<$#' + object_type + '##' + object_id + '#$>' in value:
							if '<$#' + object_type + '##' + object_id + '#$>' in value and self.internal_value_exists (isolation, 'GUI', object_type, object_id):
								changed = True
								value = value.replace ('<$#' + object_type + '##' + object_id + '#$>', str (self.internal_value_get_value (isolation, 'GUI', object_type, object_id)))
#								value = value.replace ('<$#' + object_type + '##' + object_id + '#$>', str (self.cls_gui.objects[object_type][object_id]['Value']))
			if '<$' in value and '$>' in value:
#				isolationkey = (str (isolation['Isolation']) if isinstance (isolation, dict) and 'Isolation' in isolation else str (isolation))		# Removed 2025-05-22, probably shouldn't be str?
				isolationkey = (isolation['Isolation'] if isinstance (isolation, dict) and 'Isolation' in isolation else isolation)
				for variable in (self.variables_global.keys () if isolationkey is None else (self.variables_isolated[isolationkey].keys () if isolationkey in self.variables_isolated else [])):
					if '<$' + variable + '$>' in value:
						changed = True
						value = value.replace ('<$' + variable + '$>', str (self.internal_value_get_value (isolation, 'Variable', variable)))
#						value = value.replace ('<$' + variable + '$>', str (self.variables[variable]))
			if '<#' in value and '#>' in value:
				for variable in self.variables_global.keys ():
					if '<#' + variable + '#>' in value:
						changed = True
						value = value.replace ('<#' + variable + '#>', str (self.internal_value_get_value (None, 'Variable', variable)))
#						value = value.replace ('<$' + variable + '$>', str (self.variables[variable]))
			if '<@' in value and '@>' in value:
				for variable in self.variables_internal.keys ():
					if '<@' + variable + '@>' in value:
						changed = True
						value = value.replace ('<@' + variable + '@>', str (self.internal_value_get_value (isolation, 'InternalVariable', variable)))
#						value = value.replace ('<@' + variable + '@>', str (self.variables_internal[variable]))
			if changed is True:
				return self.internal_value (isolation, value, function)
		return value
	
	
	def internal_debug (self, isolation = None, **opts):
		self.internal_value_set_value (isolation, 'InternalVariable', self.internal_value_get_value (isolation, 'InternalVariable', 'Debug.Log') + [opts], 'Debug.Log')
	
	
	def internal_debugging (self, **opts_orig):
		opts = self.internal_debugging_clean (copy.deepcopy (opts_orig))
		if self.debug['Active'] is True and len (self.debug['Output']) > 0:
			with self.objects['Lock']['Debugging']:
				for output in self.debug['Output']:
					if 'Type' in output:
						if output['Type'] == 'Console':
							print (opts)
						elif output['Type'] == 'File':
							line = internal_zyd_date () + '\t' + str (opts) + '\r\n'
							if 'Instant' in self.debug and self.debug['Instant'] is True:
								with open (output['File'], 'a', encoding='UTF-8') as fp:
									fp.write (line)
							else:
								self.debug['File.Log'].append (line)
								self.debug['File.Log.Size'] += len (line)
								if self.debug['File.Log.Size'] >= 1048576:
									self.internal_debugging_buffer_write ()
	
	
	def internal_console_debugging (self, **opts_orig):
		print (internal_zyd_date () + '\t' + str (opts_orig))
	
	
	def internal_debugging_buffer_write (self):
		if self.debug['Active'] is True and len (self.debug['File.Log']) > 0:
			with self.objects['Lock']['Debugging']:
				for output in self.debug['Output']:
					if 'Type' in output and output['Type'] == 'File':
						with open (output['File'], 'a', encoding='UTF-8') as fp:
							for line in self.debug['File.Log']:
								fp.write (line)
				self.debug['File.Log.Size'] = 0
				self.debug['File.Log'] = []
	
	
	def internal_debugging_clean (self, data):
		if isinstance (data, (dict, list)):
			for key in (data.keys () if isinstance (data, dict) else range (0, len (data))):
				data[key] = self.internal_debugging_clean (data[key])
		elif isinstance (data, bytes):
			data = '<BYTES=' + str (len (data)) + '>'
		return data
	
	
	def internal_local_ip (self):
		tempsocket = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
		try:
			tempsocket.connect (('10.255.255.255', 1))
			ip = tempsocket.getsockname()[0]
		except Exception:
			ip = '127.0.0.1'
		finally:
			tempsocket.close ()
		return ip
	
	
	def internal_import (self, module_name, class_name):
		print ('INTERNAL_IMPORT=' + str (module_name) + '::' + str (class_name))
		try:
#			print (__file__)
			base_path = os.path.dirname (os.path.abspath (__file__))
#			print (base_path)
		except NameError:
			if sys.argv and sys.argv[0]:
				base_path = os.path.dirname (os.path.abspath (sys.argv[0]))
#		base_path = '../'
#		print (base_path)
		file_path = os.path.join (base_path, "WinClasses", module_name + '.py')
		if not os.path.exists (file_path) and os.path.exists (os.path.join (base_path, module_name + '.py')):
			file_path = os.path.join (base_path, module_name + '.py')
		print ('\t' + str (file_path))
		if os.path.exists (file_path):
			spec = importlib.util.spec_from_file_location (module_name, file_path)
			module = importlib.util.module_from_spec (spec)
			spec.loader.exec_module (module)
			cls = getattr (module, class_name, None)
			return cls (self)
		print ('NOT_FOUND=' + str (file_path))
		return None
	
	
	def internal_bz2_encrypt (self, data):
		return bz2.compress (self.fernet.encrypt (data.encode ('UTF-8')), 9)
	
	
	def internal_bz2_decrypt (self, data):
		print ('internal_bz2_decrypt')
		print (bz2.decompress (data)[:100])
		return self.fernet.decrypt (bz2.decompress (data))