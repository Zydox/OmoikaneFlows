# Copyright (c) 2025-2026 Erik Persson
# Licensed for free use only. Copying, modification, or redistribution prohibited.

# -*- coding: utf-8 -*-
import builtins
from Functions.Common import *
from Functions.DataHandling import *
for name in dir ():
	if not name.startswith ("_"):
		builtins.__dict__[name] = globals ()[name]

class Core:
	def __init__ (self, cls_steps = None):
		self.objects = {
		}
		self.cls_steps = cls_steps
	
	
	def dynamic_function (self, function, to_class = True):
		if to_class is True:
			func = {}
			exec (function['Code'], func)
			setattr (Core, function['Function'], func[function['Function']])
		else:
			exec (function['Code'], globals ())
			builtins.__dict__[function['Function']] = globals ()[function['Function']]
	
	
	def execute (self, running_steps, isolation = None, **opts):
		try:
			if opts['Function'] == 'CORE:Break':
				return self.step_break (running_steps, isolation, **opts)
			elif opts['Function'] == 'CORE:Function.Defaults':
				return self.step_function_defaults (running_steps, isolation, **opts)
			elif opts['Function'] == 'CORE:Debug.Variables.Print':
				return self.step_debug_variables_print (running_steps, isolation, **opts)
			elif opts['Function'] == 'CORE:Debug.Variable.Print':
				return self.step_debug_variable_print (running_steps, isolation, **opts)
			elif opts['Function'] == 'CORE:Debug.Print':
				return self.step_debug_print (running_steps, isolation, **opts)
			return False, {'Status':'WARNING', 'Title':'CORE:execute: Aborted', 'Message':'Unknown step=' + str (opts)}
		except Exception as e:
			st = internal_zyd_stacktrace (e, FunctionOpts=opts)
			return False, {'Status':'CRASH', 'Title':'CORE:execute: Crashed', 'Message':'Crashed with the error: ' + str (e) + ' for step:\n' + str (opts), 'StackTrace':st}
	
	
	def step_break (self, running_steps, isolation, **opts):
		if self.cls_steps.debug['Active'] is True:
			self.cls_steps.internal_debugging (Function='step_break', Stage='Init', NoRunningSteps=len (running_steps))
		if 'Segment' in opts:
			if self.cls_steps.debug['Active'] is True:
				self.cls_steps.internal_debugging (Function='step_break', Stage='Segment.Init', Segment=opts['Segment'], Step=opts)
			for step in list (running_steps):
				if 'Function.Segment' in step and step['Function.Segment'] == opts['Segment']:
					if self.cls_steps.debug['Active'] is True:
						self.cls_steps.internal_debugging (Function='step_break', Stage='Segment.Remove', Segment=opts['Segment'], Step=step)
					running_steps.remove (step)
		else:
			if self.cls_steps.debug['Active'] is True:
				self.cls_steps.internal_debugging (Function='step_break', Stage='All.Init', Step=opts)
			for step in list (running_steps):
				if self.cls_steps.debug['Active'] is True:
					self.cls_steps.internal_debugging (Function='step_break', Stage='All.Remove', Step=step)
				running_steps.remove (step)
		if self.cls_steps.debug['Active'] is True:
			self.cls_steps.internal_debugging (Function='step_break', Stage='End', NoRunningSteps=len (running_steps))
		return True, {'Status':'OK'}
	
	
	def step_function_defaults (self, running_steps, isolation, **opts):
		self.cls_steps.function_defaults = {}
		if 'Defaults' not in opts or not isinstance (opts['Defaults'], dict):
			return False, {'Status':'WARNING', 'Title':'CORE:step_function_defaults: Aborted', 'Message':'No Defaults dict provided.'}
		for field in self.cls_steps.cls_flows.help['Functions'].keys ():
			if field in opts['Defaults'] and field not in ['Function', 'Function.Segment']:
				self.cls_steps.function_defaults[field] = opts['Defaults'][field]
		
		return True, {'Status':'OK'}
	
	
	def step_debug_variables_print (self, running_steps, isolation, **opts):
		if 'Output' not in opts:
			return False, {'Status':'WARNING', 'Title':'CORE:step_debug_variables_print: Aborted', 'Message':'No valid Output provided.'}
		
		if opts['Output'] == 'CONSOLE':
			if 'Variables' in opts and isinstance (opts['Variables'], list):
				print ('=====[ VARIABLES_GLOBAL ]=====')
				for key in opts['Variables']:
					if key in self.cls_steps.variables_global:
						print (str (key) + '=>' + str (type (self.cls_steps.variables_global[key])) + '=>' + self.internal_debug_variables_print_text (str (key), self.cls_steps.variables_global[key], **{**{'String':True}, **opts}))
				print ('=====[ VARIABLES_ISOLATED ]=====')
				for isolation_key in self.cls_steps.variables_isolated.keys ():
					for key in opts['Variables']:
						if key in self.cls_steps.variables_isolated[isolation_key]:
							print (str (isolation_key) + '=>' + str (key) + '=>' + str (type (self.cls_steps.variables_isolated[isolation_key][key])) + '=>' + self.internal_debug_variables_print_text (str (key), self.cls_steps.variables_isolated[isolation_key][key], **{**{'String':True}, **opts}))
				print ('=====[ VARIABLES_INTERNAL ]=====')
				for key in opts['Variables']:
					if key in self.cls_steps.variables_internal:
						print (str (key) + '=>' + str (type (self.cls_steps.variables_internal[key])) + '=>' + self.internal_debug_variables_print_text (str (key), self.cls_steps.variables_internal[key], **{**{'String':True}, **opts}))
				return True, {'Status':'OK'}
			
			print ('=====[ VARIABLES_GLOBAL (' + str (len (self.cls_steps.variables_global)) + ') ]=====')
			if 'Split' in opts and opts['Split'] is True:
				for key in self.cls_steps.variables_global.keys ():
					print (str (key) + '=>' + str (type (self.cls_steps.variables_global[key])) + '=>' + self.internal_debug_variables_print_text (str (key), self.cls_steps.variables_global[key], **{**{'String':True}, **opts}))
			else:
				print (self.cls_steps.variables_global)
			variables = 0
			for isolation_key in self.cls_steps.variables_isolated.keys ():
				variables += len (self.cls_steps.variables_isolated[isolation_key])
			print ('=====[ VARIABLES_ISOLATED (' + str (variables) + ') ]=====')
			if 'Split' in opts and opts['Split'] is True:
				for isolation_key in self.cls_steps.variables_isolated.keys ():
					for key in self.cls_steps.variables_isolated[isolation_key].keys ():
						print (str (isolation_key) + '=>' + str (key) + '=>' + str (type (self.cls_steps.variables_isolated[isolation_key][key])) + '=>' + self.internal_debug_variables_print_text (str (key), self.cls_steps.variables_isolated[isolation_key][key], **{**{'String':True}, **opts}))
			else:
				print (self.cls_steps.variables_isolated)
			print ('=====[ VARIABLES_INTERNAL (' + str (len (self.cls_steps.variables_internal)) + ') ]=====')
			if 'Split' in opts and opts['Split'] is True:
				for key in self.cls_steps.variables_internal.keys ():
					print (str (key) + '=>' + str (type (self.cls_steps.variables_internal[key])) + '=>' + self.internal_debug_variables_print_text (str (key), self.cls_steps.variables_internal[key], **{**{'String':True}, **opts}))
			else:
				print (self.cls_steps.variables_internal)
		elif opts['Output'] == 'LOG':
			if self.cls_steps.debug['Active'] is True:
				if 'Split' in opts and opts['Split'] is True:
					for key in self.cls_steps.variables_global.keys ():
						self.cls_steps.internal_debugging (Function='step_debug_variables_print', Global=key, Type=type (self.cls_steps.variables_global[key]), Value=self.internal_debug_variables_print_text (str (key), self.cls_steps.variables_global[key], **opts))
				else:
					self.cls_steps.internal_debugging (Function='step_debug_variables_print', Global=self.cls_steps.variables_global)
				if 'Split' in opts and opts['Split'] is True:
					for isolation_key in self.cls_steps.variables_isolated.keys ():
						for key in self.cls_steps.variables_isolated[isolation_key].keys ():
							self.cls_steps.internal_debugging (Function='step_debug_variables_print', Isolation=isolation_key, Variable=key, Type=type (self.cls_steps.variables_isolated[isolation_key][key]), Value=self.internal_debug_variables_print_text (str (key), self.cls_steps.variables_isolated[isolation_key][key], **opts))
				else:
					self.cls_steps.internal_debugging (Function='step_debug_variables_print', Isolated=self.cls_steps.variables_isolated)
				if 'Split' in opts and opts['Split'] is True:
					for key in self.cls_steps.variables_internal.keys ():
						self.cls_steps.internal_debugging (Function='step_debug_variables_print', Internal=key, Type=type (self.cls_steps.variables_internal[key]), Value=self.internal_debug_variables_print_text (str (key), self.cls_steps.variables_internal[key], **opts))
				else:
					self.cls_steps.internal_debugging (Function='step_debug_variables_print', Internal=self.cls_steps.variables_internal)
		return True, {'Status':'OK'}
	
	
	def step_debug_variable_print (self, running_steps, isolation, **opts):
		if 'Variable' not in opts:
			return False, {'Status':'WARNING', 'Title':'CORE:step_debug_variable_print: Aborted', 'Message':'No Variable provided.'}
		if opts['Variable'] in self.cls_steps.variables_global:
			variable = self.cls_steps.variables_global[opts['Variable']]
		elif opts['Variable'] in self.cls_steps.variables_internal:
			variable = self.cls_steps.variables_internal[opts['Variable']]
		elif isolation in self.cls_steps.variables_isolated and opts['Variable'] in self.cls_steps.variables_isolated[isolation]:
			variable = self.cls_steps.variables_isolated[isolation][opts['Variable']]
		else:
			return False, {'Status':'WARNING', 'Title':'CORE:step_debug_variable_print: Aborted', 'Message':'The variable "' + str (opts['Variable']) + '" was not found.'}
		print ('+=====[ ' + str (opts['Variable']) + ' (' + str (type (variable)) + ') ]===========================================================================')
		if isinstance (variable, list):
			for line in variable:
				print (line)
		elif isinstance (variable, dict):
			for key in variable.keys ():
				print (str (key) + '::' + str (variable[key]))
		else:
			print (variable)
		print ('-=====[ ' + str (opts['Variable']) + ' (' + str (type (variable)) + ') ]===========================================================================')
		return True, {'Status':'OK'}
	
	
	def step_debug_print (self, running_steps, isolation, **opts):
		if 'Output' not in opts:
			return False, {'Status':'WARNING', 'Title':'CORE:step_debug_print: Aborted', 'Message':'No valid Output provided.'}
		if 'Text' not in opts:
			return False, {'Status':'WARNING', 'Title':'CORE:step_debug_print: Aborted', 'Message':'No valid Text provided.'}
		
		if opts['Output'] == 'CONSOLE':
			if 'CONSOLE.Containment' in opts and opts['CONSOLE.Containment'] is True:
				print ('+==[ Console debug: ' + str (isolation) + ' ]=====================================================')
			print (opts['Text'])
		if 'CONSOLE.Containment' in opts and opts['CONSOLE.Containment'] is True:
			print ('-==[ Console debug: ' + str (isolation) + ' ]=====================================================')
		return True, {'Status':'OK'}

	
	def internal_debug_variables_print_text (self, variable, original_text, **opts):
		if 'String' in opts and opts['String'] is True:
			original_text = str (original_text)
		text = internal_zyd_shorten (original_text)
		if 'Print.Variable.Full' in opts and isinstance (opts['Print.Variable.Full'], list) and variable in opts['Print.Variable.Full']:
			return text
		if 'Print.Variable.MaxLength' in opts and isinstance (opts['Print.Variable.MaxLength'], int) and isinstance (text, str) and len (text) > opts['Print.Variable.MaxLength']:
			text = internal_zyd_shorten (text, Length=opts['Print.Variable.MaxLength'], Sufix='... (max length of ' + str (opts['Print.Variable.MaxLength']) + ' exceeded, variable contains ' + str (len (original_text)) + '.)')
		return text