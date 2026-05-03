# Copyright (c) 2025-2026 Erik Persson
# Licensed for free use only. Copying, modification, or redistribution prohibited.

import builtins
from Functions.Common import *
from Functions.DataHandling import *
for name in dir ():
    if not name.startswith ("_"):
        builtins.__dict__[name] = globals ()[name]
import time
builtins.time = time
import threading
builtins.threading = threading
import queue
builtins.queue = queue
import math
builtins.math = math

class Logic:
	def __init__ (self, cls_steps):
		self.cls_steps = cls_steps
		self.threads = {}
		self.templates = {}
		self.objects = self.cls_steps.objects
		self.objects['Locks'] = {}
		self.objects['ThreadingQueues'] = {}
	
	
	def dynamic_function (self, function, to_class = True):
		if to_class is True:
			func = {}
			exec (function['Code'], func)
			setattr (Logic, function['Function'], func[function['Function']])
		else:
			exec (function['Code'], globals ())
			builtins.__dict__[function['Function']] = globals ()[function['Function']]
	
	
	def execute (self, steps, isolation = None, **opts):
		try:
			if opts['Function'] == 'LOGIC:Sleep':
				return self.step_sleep (isolation, **opts)
			elif opts['Function'] == 'LOGIC:Threading':
				return self.step_threading (isolation, **opts)
			elif opts['Function'] == 'LOGIC:Threading.Wait':
				return self.step_threading_wait (isolation, **opts)
			elif opts['Function'] == 'LOGIC:Threading.Queue':
				return self.step_threading_queue (isolation, **opts)
			elif opts['Function'] == 'LOGIC:Threading.Lock':
				return self.step_threading_lock (isolation, **opts)
			elif opts['Function'] == 'LOGIC:Template.Create':
				return self.step_template_create (isolation, **opts)
			elif opts['Function'] == 'LOGIC:Template':
				return self.step_template (isolation, **opts)
			elif opts['Function'] == 'LOGIC:Steps':
				return self.step_steps (isolation, **opts)
			elif opts['Function'] == 'LOGIC:Loop':
				return self.step_loop (isolation, **opts)
			else:
				return False, {'Status':'WARNING', 'Title':'LOGIC:execute: Aborted', 'Message':'Unknown execute:' + str (opts)}
		except Exception as e:
			st = internal_zyd_stacktrace (e, FunctionOpts=opts)
			return False, {'Status':'CRASH', 'Title':'LOGIC:execute: Crashed', 'Message':'Crashed with the error: ' + str (e) + ' for step:\n' + str (opts), 'StackTrace':st}

	
	def step_sleep (self, isolation, **opts):
		time.sleep (opts['Seconds'])
		return True, {'Status':'OK'}
	
	
	def step_threading_wait (self, isolation, **opts):
		if 'Wait.Max' in opts and not isinstance (opts['Wait.Max'], float):
			return False, {'Status':'WARNING', 'Function':'step_threading_wait', 'Title':'LOGIC:step_threading_wait: Aborted', 'Message':'The input Wait.Max has to be a decimal value (not "' + str (opts['Wait.Max']) + '", type:' + str (type (opts['Wait.Max'])) + ').'}
		if 'Wait.Sleep' in opts and not isinstance (opts['Wait.Sleep'], (float, int)):
			return False, {'Status':'WARNING', 'Function':'step_threading_wait', 'Title':'LOGIC:step_threading_wait: Aborted', 'Message':'The input Wait.Sleep has to be a decimal or integer value (not "' + str (opts['Wait.Sleep']) + '", type:' + str (type (opts['Wait.Sleep'])) + ').'}
		if 'Threads' not in opts or not isinstance (opts['Threads'], list):
			return False, {'Status':'WARNING', 'Function':'step_threading_wait', 'Title':'LOGIC:step_threading_wait: Aborted', 'Message':'The input Threads needs to contain a list of threads to wait for.'}

		start = internal_zyd_time (Decimals=3)
		loop = True
		threads = copy.deepcopy (opts['Threads'])
		while loop:
			for thread in threads:
				if thread not in self.threads:
					threads.remove (thread)
					continue
			if len (threads) == 0:
				loop = False
			else:
				if 'Wait.Max' in opts and internal_zyd_time (Decimals=3) - start >= opts['Wait.Max']:
					break
				else:
					time.sleep ((opts['Wait.Sleep'] if 'Wait.Sleep' in opts else 1))
		if loop is True:
			message = 'Wait loop exceeded (' + str (internal_zyd_ceil (internal_zyd_time (Decimals=3) - start, Decimals=3)) + ' seconds).'
			if opts['Return.Status'] == 'OK':
				return True, {'Status':'OK', 'Message':message}
			return False, {'Status':(opts['Return.Status'] if 'Return.Status' in opts and isinstance (opts['Return.Status'], str) else 'WARNING'), 'Function':'step_threading_wait', 'Title':'LOGIC:step_threading_wait: Aborted', 'Message':message}
		return True, {'Status':'OK'}
	
	
	def step_threading (self, isolation, **opts):
		if 'Steps' not in opts or not isinstance (opts['Steps'], list):
			return False, {'Status':'WARNING', 'Function':'step_threading', 'Title':'LOGIC:step_threading: Aborted', 'Message':'The input Steps needs to contain a list of steps to execute in the thread.'}
		
		if 'Thread' in opts and isinstance (opts['Thread'], str):
			key = opts['Thread']
		else:
			key = internal_zyd_uniqueid ()
		if 'Isolated' in opts and opts['Isolated'] is True:
			isolation = key
		self.threads[key] = threading.Thread (target=self.internal_step_threading, args=(isolation, key, opts['Steps'], ))
		self.threads[key].start ()
		
		if 'ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str):
			self.cls_steps.internal_value_set_value (isolation, 'Variable', key, opts['ReturnVariable'])
		if 'ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str):
			self.cls_steps.internal_value_set_value (None, 'Variable', key, opts['ReturnVariable.Global'])
		return True, {'Status':'OK', 'Message':'Thread started: ' + str (key)}
	
	
	def step_template_create (self, isolation, **opts):
		if 'Steps' not in opts or not isinstance (opts['Steps'], list):
			return False, {'Status':'WARNING', 'Title':'LOGIC:step_template_create: Aborted', 'Message':'Steps needs to contain a list of steps to be executed.'}
		template = {'Steps':opts['Steps']}
		if 'Input' in opts:
			if not isinstance (opts['Input'], dict):
				return False, {'Status':'WARNING', 'Title':'LOGIC:step_template_create: Aborted', 'Message':'Input needs to contain a dict.'}
			template['Input'] = opts['Input']
		if 'Input.Recurrences' in opts and isinstance (opts['Input.Recurrences'], int):
			template['Recurrences'] = opts['Input.Recurrences']
		
		self.templates[opts['ID']] = template
		return True, {'Status':'OK'}
	
	
	
	def step_template (self, isolation, **opts):
		if 'ID' not in opts:
			return False, {'Status':'WARNING', 'Title':'LOGIC:step_template: Aborted', 'Message':'No ID was provided.'}
		elif opts['ID'] not in self.templates:
			return False, {'Status':'WARNING', 'Title':'LOGIC:step_template: Aborted', 'Message':'No template with the ID "' + str (opts['ID']) + '" exists.'}
		
		input = {}
		if 'Input' in self.templates[opts['ID']]:
			for field in self.templates[opts['ID']]['Input'].keys ():
				if field in opts['Input']:
					input['%%' + field + '%%'] = opts['Input'][field]
				elif 'Default' in self.templates[opts['ID']]['Input'][field]:
					input['%%' + field + '%%'] = self.templates[opts['ID']]['Input'][field]['Default']
				else:
					return False, {'Status':'WARNING', 'Title':'LOGIC:step_template: Aborted', 'Message':'Template "' + str (opts['ID']) + '" is missing input for "' + str (field) + '".'}
		steps = copy.deepcopy (self.templates[opts['ID']]['Steps'])
		if len (input) > 0:
			steps = internal_zyd_arrayreplace (Array=steps, ReplaceArray=copy.deepcopy (input))
			if 'Recurrences' in self.templates[opts['ID']]:
				for x in range (0, self.templates[opts['ID']]['Recurrences']):
					if str (steps).count ('%') >= 4:
						steps = internal_zyd_arrayreplace (Array=steps, ReplaceArray=copy.deepcopy (input))
		if 'Debug.Console' in opts and opts['Debug.Console'] is True:
			print ('+============================================================================')
			print ('Input=' + str (input))
			print ('Steps=' + str (steps))
			print ('-============================================================================')
		return self.cls_steps.execute_steps (steps, isolation)

	
	def step_steps (self, isolation, **opts):
		if 'Steps' not in opts:
			return False, {'Status':'WARNING', 'Title':'LOGIC:step_steps: Aborted', 'Message':'No steps provided.'}
		elif not isinstance (opts['Steps'], list):
			return False, {'Status':'WARNING', 'Title':'LOGIC:step_steps: Aborted', 'Message':'Steps needs to be a list, not "' + str (type (opts['Steps'])) + '" with the value "' + str (opts['Steps']) + '".'}
		if 'Isolation' in opts:
			if isinstance (opts['Isolation'], str):
				isolation = opts['Isolation']
			elif isinstance (opts['Isolation'], bool) and opts['Isolation'] is True:
				isolation = internal_zyd_uniqueid ()
			else:
				return False, {'Status':'WARNING', 'Title':'LOGIC:step_steps: Aborted', 'Message':'The input Isolation needs to be either a Key or a True value.'}
		if 'Debug.Console' in opts and opts['Debug.Console'] is True:
			print ('+==[ step_steps ] ===========================================================')
			print ('Ssolation=' + str (isolation))
			for step in steps:
				print ('Step[]=' + str (step))
			print ('-============================================================================')
		status, result = self.cls_steps.execute_steps (opts['Steps'], isolation)
		if 'ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str):
			self.cls_steps.internal_value_set_value (isolation, 'Variable', result, opts['ReturnVariable'])
		if 'ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str):
			self.cls_steps.internal_value_set_value (None, 'Variable', result, opts['ReturnVariable.Global'])
		if 'ReturnVariable.Status' in opts and isinstance (opts['ReturnVariable.Status'], str):
			self.cls_steps.internal_value_set_value (isolation, 'Variable', status, opts['ReturnVariable.Status'])
		if 'ReturnVariable.Status.Global' in opts and isinstance (opts['ReturnVariable.Status.Global'], str):
			self.cls_steps.internal_value_set_value (None, 'Variable', status, opts['ReturnVariable.Status.Global'])
		if 'Steps.IgnoreResult' in opts and opts['Steps.IgnoreResult'] is True:
			return True, {'Status':'OK'}
		return status, result
	
	
	def step_loop (self, isolation, **opts):
		if 'Steps' not in opts:
			return False, {'Status':'WARNING', 'Title':'LOGIC:step_loop: Aborted', 'Message':'No steps provided.'}
		if 'Data.ListList' in opts and isinstance (opts['Data.ListList'], list):
			entries = opts['Data.ListList']
			logic = 'LIST.LIST'
		elif 'Data.DictList' in opts and isinstance (opts['Data.DictList'], dict):
			entries = opts['Data.DictList']
			logic = 'DICT.LIST'
		elif 'Data.ListDict' in opts and isinstance (opts['Data.ListDict'], list):
			entries = opts['Data.ListDict']
			logic = 'LIST.DICT'
		elif 'Data.DictDict' in opts and isinstance (opts['Data.DictDict'], dict):
			entries = opts['Data.DictDict']
			logic = 'DICT.DICT'
		elif 'Data.List' in opts and isinstance (opts['Data.List'], list):
			entries = opts['Data.List']
			logic = 'LIST'
		elif 'Range.List' in opts and isinstance (opts['Range.List'], list) and len (opts['Range.List']) >= 2 and len (opts['Range.List']) <= 3:
			for x in opts['Range.List']:
				if not isinstance (x, int):
					return False, {'Status':'WARNING', 'Title':'LOGIC:step_loop: Aborted', 'Message':'"Range.List" contains values which are not integers ("' + str (x) + '" has the type "' + str (type (x)) + '")."'}
			entries = []
			for x in range (opts['Range.List'][0], opts['Range.List'][1], (opts['Range.List'][2] if len (opts['Range.List']) == 3 else 1)):
				entries.append (x)
			logic = 'LIST'
		else:
			return False, {'Status':'WARNING', 'Title':'LOGIC:step_loop: Aborted', 'Message':'No valid source data found.'}
		
		debug = (True if 'Debug.Console' in opts and opts['Debug.Console'] is True else False)
		
		basereplace = {}
		if 'Loop.Mapping' in opts and isinstance (opts['Loop.Mapping'], dict):
			for key in opts['Loop.Mapping'].keys ():
				basereplace[(opts['Loop.MappingKey'] if 'Loop.MappingKey' in opts else '') + str (key) + (opts['Loop.MappingKey'] if 'Loop.MappingKey' in opts else '')] = copy.deepcopy (opts['Loop.Mapping'][key])
		for rowkey in (range (0, len (entries)) if (logic.startswith ('LIST.') or logic == 'LIST') else (entries.keys () if logic.startswith ('DICT.') else None)):
			entry = entries[rowkey]
			replace = copy.deepcopy (basereplace)
			for key in replace.keys ():
				if replace[key] == '$LOOP.ROW$':
					replace[key] = copy.deepcopy (rowkey)
				elif replace[key] == '$LOOP.ROW+1$' and logic.endswith ('LIST'):
					replace[key] = copy.deepcopy (rowkey) + 1
				elif replace[key] == '$DATA.ROW$':
					replace[key] = entry
				elif replace[key].startswith ('$DATA.LIST=') and replace[key][-1] == '$' and replace[key][11:-1].isdigit () and logic.endswith ('LIST'):
					replace[key] = entry[int (replace[key][11:-1])]
				elif replace[key].startswith ('$DATA.DICT=') and replace[key][-1] == '$' and logic.endswith ('DICT'):
					replace[key] = entry[replace[key][11:-1]]
					
			steps = internal_zyd_arrayreplace (Array=copy.deepcopy (opts['Steps']), ReplaceArray=replace)
			status, result = self.cls_steps.execute_steps (steps, isolation)

			if debug is True:
				if 'Debug.Console' in opts and opts['Debug.Console'] is True:
					print ('+============================================================================')
					print ('RowKey=' + str (rowkey))
					print ('Replace=' + str (replace))
					print ('Steps=' + str (steps))
					print ('Result=' + str (status) + '::' + str (result))
					print ('-============================================================================')

		return True, {'Status':'OK'}
		
	
	def step_threading_queue (self, isolation, **opts):
		if 'Workers' not in opts:
			return False, {'Status':'WARNING', 'Title':'LOGIC:step_threading_queue: Aborted', 'Message':'No Workers provided.'}
		elif not isinstance (opts['Workers'], int):
			return False, {'Status':'WARNING', 'Title':'LOGIC:step_threading_queue: Aborted', 'Message':'The Workers value was not an integer.'}
		
		queue_key = internal_zyd_uniqueid ()
		if queue_key not in self.objects['ThreadingQueues']:
			self.objects['ThreadingQueues'][queue_key] = {'Threads':[], 'Queue':queue.Queue ()}
		
		if 'List.Steps' in opts and isinstance (opts['List.Steps'], list):
			for task in opts['List.Steps']:
				if isinstance (task, list) and len (task) > 0 and isinstance (task[0], dict):
					self.objects['ThreadingQueues'][queue_key]['Queue'].put (task)
		elif 'Steps' in opts and isinstance (opts['Steps'], list):
			if 'Data.ListList' in opts and isinstance (opts['Data.ListList'], list):
				entries = opts['Data.ListList']
				logic = 'LIST.LIST'
			elif 'Data.DictList' in opts and isinstance (opts['Data.DictList'], dict):
				entries = opts['Data.DictList']
				logic = 'DICT.LIST'
			elif 'Data.ListDict' in opts and isinstance (opts['Data.ListDict'], list):
				entries = opts['Data.ListDict']
				logic = 'LIST.DICT'
			elif 'Data.DictDict' in opts and isinstance (opts['Data.DictDict'], dict):
				entries = opts['Data.DictDict']
				logic = 'DICT.DICT'
			elif 'Data.List' in opts and isinstance (opts['Data.List'], list):
				entries = opts['Data.List']
				logic = 'LIST'
			else:
				return False, {'Status':'WARNING', 'Title':'LOGIC:step_threading_queue: Aborted', 'Message':'No valid source data found for Steps logic.'}
			basereplace = {}
			if 'Queue.Mapping' in opts and isinstance (opts['Queue.Mapping'], dict):
				for key in opts['Queue.Mapping'].keys ():
					basereplace[(opts['Queue.MappingKey'] if 'Queue.MappingKey' in opts else '') + str (key) + (opts['Queue.MappingKey'] if 'Queue.MappingKey' in opts else '')] = copy.deepcopy (opts['Queue.Mapping'][key])
			for rowkey in (range (0, len (entries)) if (logic.startswith ('LIST.') or logic == 'LIST') else (entries.keys () if logic.startswith ('DICT.') else None)):
				entry = entries[rowkey]
				replace = copy.deepcopy (basereplace)
				for key in replace.keys ():
					if replace[key] == '$LOOP.ROW$':
						replace[key] = copy.deepcopy (rowkey)
					elif replace[key] == '$LOOP.ROW+1$' and logic.endswith ('LIST'):
						replace[key] = copy.deepcopy (rowkey) + 1
					elif replace[key] == '$DATA.ROW$':
						replace[key] = entry
					elif replace[key].startswith ('$DATA.LIST=') and replace[key][-1] == '$' and replace[key][11:-1].isdigit () and logic.endswith ('LIST'):
						replace[key] = entry[int (replace[key][11:-1])]
					elif replace[key].startswith ('$DATA.DICT=') and replace[key][-1] == '$' and logic.endswith ('DICT'):
						replace[key] = entry[replace[key][11:-1]]
				task = internal_zyd_arrayreplace (Array=copy.deepcopy (opts['Steps']), ReplaceArray=replace)
				if isinstance (task, list):
					self.objects['ThreadingQueues'][queue_key]['Queue'].put (task)
		else:
			return False, {'Status':'WARNING', 'Title':'LOGIC:step_threading_queue: Aborted', 'Message':'No valid source data found.'}

		if self.objects['ThreadingQueues'][queue_key]['Queue'].qsize () == 0:
			return False, {'Status':'WARNING', 'Title':'LOGIC:step_threading_queue: Aborted', 'Message':'No queue tasks were captured.'}
		
		for i in range (opts['Workers']):
			thread_isolation = (copy.deepcopy (isolation) if 'Isolated' not in opts or opts['Isolated'] is not True else 'WorkerThread#' + str (i) + '::' + internal_zyd_uniqueid ())
			t = threading.Thread (target=self.internal_step_threading_queue_worker, name='WorkerThread#' + str (i), args=(thread_isolation, queue_key))
			t.daemon = True
			t.start ()
			self.objects['ThreadingQueues'][queue_key]['Threads'].append (t)
		
		self.objects['ThreadingQueues'][queue_key]['Queue'].join ()
		
		return True, {'Status':'OK'}
	
	
	def step_threading_lock (self, isolation, **opts):
		if 'Lock' not in opts:
			return False, {'Status':'WARNING', 'Title':'LOGIC:step_threading_lock: Aborted', 'Message':'No Lock provided.'}
		if 'Steps' not in opts:
			return False, {'Status':'WARNING', 'Title':'LOGIC:step_threading_lock: Aborted', 'Message':'No Steps provided.'}
		if not isinstance (opts['Steps'], list):
			return False, {'Status':'WARNING', 'Title':'LOGIC:step_threading_lock: Aborted', 'Message':'The provided Steps was not a list.'}
		if opts['Lock'] not in self.objects['Locks']:
			self.objects['Locks'][opts['Lock']] = threading.RLock ()
		
		with self.objects['Locks'][opts['Lock']]:
			status, result = self.cls_steps.execute_steps (opts['Steps'], isolation)
		return True, {'Status':'OK'}
	
	
	def internal_step_threading_queue_worker (self, isolation, queue_key):
		while True:
			try:
				task = self.objects['ThreadingQueues'][queue_key]['Queue'].get (timeout=1)
			except queue.Empty:
				if queue_key in self.objects['ThreadingQueues']:
					del (self.objects['ThreadingQueues'][queue_key])
				break
			
			if isinstance (task, (list, dict)):
				task = internal_zyd_arrayreplace (Array=task, ReplaceArray={'$THREAD$':str (threading.current_thread())})
			else:
				task = internal_zyd_arrayreplace (Value=task, ReplaceArray={'$THREAD$':str (threading.current_thread())})
			status, result = self.cls_steps.execute_steps (task, isolation)
			self.objects['ThreadingQueues'][queue_key]['Queue'].task_done ()
	
	
	def internal_step_threading (self, isolation, key, steps):
		self.cls_steps.execute_steps (steps, isolation)
		print ('Thread ended [' + str (key) + ']')
		del (self.threads[key])
		
