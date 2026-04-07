# Copyright (c) 2025-2026 Erik Persson
# Licensed for free use only. Copying, modification, or redistribution prohibited.

import builtins
from logging import exception, error
from Functions.Common import *
from Functions.DataHandling import *
for name in dir ():
	if not name.startswith ("_"):
		builtins.__dict__[name] = globals ()[name]
import io
builtins.io = io
import PIL
builtins.PIL = PIL
import PIL.Image
builtins.PIL.Image = PIL.Image
import qrcode
builtins.qrcode = qrcode
import treepoem
builtins.treepoem = treepoem

class Image:
	def __init__ (self, cls_steps):
		self.cls_steps = cls_steps
		self.objects = self.cls_steps.objects
	
	
	def dynamic_function (self, function, to_class = True):
		if to_class is True:
			func = {}
			exec (function['Code'], func)
			setattr (Image, function['Function'], func[function['Function']])
		else:
			exec (function['Code'], globals ())
			builtins.__dict__[function['Function']] = globals ()[function['Function']]
	
	
	def execute (self, isolation = None, **opts):
		try:
			if opts['Function'] == 'IMAGE:QR.Generate':
				return self.step_qr_generate (isolation, **opts)
			else:
				return False, {'Status':'WARNING', 'Title':'IMAGE:execute: Aborted', 'Message':'Unknown execute:' + str (opts)}
		except Exception as e:
			st = internal_zyd_stacktrace (e, FunctionOpts=opts)
			return False, {'Status':'CRASH', 'Title':'IMAGE:execute: Crashed', 'Message':'Crashed with the error: ' + str (e) + ' for step:\n' + str (opts), 'StackTrace':st}

	
	def step_qr_generate (self, isolation, **opts):
		if 'Content' not in opts:
			return False, {'Status':'WARNING', 'Title':'IMAGE:step_qr_generate: Aborted', 'Message':'No Content was provided.'}
		if not isinstance (opts['Content'], str):
			return False, {'Status':'WARNING', 'Title':'IMAGE:step_qr_generate: Aborted', 'Message':'The Content needs to be a string.'}
		if 'File' in opts:
			if not isinstance (opts['File'], str):
				return False, {'Status':'WARNING', 'Title':'IMAGE:step_qr_generate: Aborted', 'Message':'The File "' + str (opts['File']) + '" is not a string.'}
			elif os.path.exists (opts['File']):
				return False, {'Status':'WARNING', 'Title':'IMAGE:step_qr_generate: Aborted', 'Message':'The File "' + str (opts['File']) + '" already exists.'}
		elif ('ReturnVariable' not in opts or not isinstance (opts['ReturnVariable'], str)) and ('ReturnVariable.Global' not in opts or not isinstance (opts['ReturnVariable.Global'], str)):
			return False, {'Status':'WARNING', 'Title':'IMAGE:step_qr_generate: Aborted', 'Message':'Neither File, ReturnVariable or ReturnVariable.Global provided.'}
		qr_opts = {
			'box_size':10,
			'border':4,
			'error_correction':qrcode.constants.ERROR_CORRECT_M,
		}
		for field in [['Size', 'box_size', int], ['Border', 'border', int]]:
			if field[0] in opts and isinstance (opts[field[0]], field[2]):
				qr_opts[field[1]] = opts[field[0]]
		qr = qrcode.QRCode (**qr_opts)
		qr.add_data (opts['Content'])
		qr.make (fit=True)
		
		if 'File' in opts:
			qr.make_image (fill_color="black", back_color="white").save (opts['File'])
		else:
			image_io = io.BytesIO ()
			qr.make_image (fill_color="black", back_color="white").save (image_io, format="PNG")
			image_io.seek (0)
			if 'ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str):
				self.cls_steps.internal_value_set_value (isolation, 'Variable', image_io, opts['ReturnVariable'])
			if 'ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str):
				self.cls_steps.internal_value_set_value (None, 'Variable', image_io, opts['ReturnVariable.Global'])
		
		return True, {'Status':'OK'}
