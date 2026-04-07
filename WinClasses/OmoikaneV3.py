# Copyright (c) 2025-2026 Erik Persson
# Licensed for free use only. Copying, modification, or redistribution prohibited.

# -*- coding: utf-8 -*-
import builtins
from Functions.Common import *
from Functions.DataHandling import *
for name in dir ():
    if not name.startswith ("_"):
        builtins.__dict__[name] = globals ()[name]

class OmoikaneV3:
	def __init__ (self, cls_steps = None):
		self.objects = {
		}
		self.cls_steps = cls_steps
	
	
	def dynamic_function (self, function, to_class = True):
		if to_class is True:
			func = {}
			exec (function['Code'], func)
			setattr (OmoikaneV3, function['Function'], func[function['Function']])
		else:
			exec (function['Code'], globals ())
			builtins.__dict__[function['Function']] = globals ()[function['Function']]

	
	def execute (self, isolation = None, **opts):
		try:
			if opts['Function'] == 'OMOIKANEV3:':
				return self.step_sap_process_transform (isolation, **opts)
			return False, {'Status':'WARNING', 'Title':'', 'Message':'Unknown step=' + str (opts)}
		except Exception as e:
			st = internal_zyd_stacktrace (e, FunctionOpts=opts)
			return False, {'Status':'CRASH', 'Title':'OMOIKANEV3:execute: Crashed', 'Message':'Crashed with the error: ' + str (e) + ' for step:\n' + str (opts), 'StackTrace':st}
