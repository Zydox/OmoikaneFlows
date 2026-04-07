# Copyright (c) 2025-2026 Erik Persson
# Licensed for free use only. Copying, modification, or redistribution prohibited.

import builtins
from logging import exception, error
from Functions.Common import *
from Functions.DataHandling import *
for name in dir ():
	if not name.startswith ("_"):
		builtins.__dict__[name] = globals ()[name]
import copy
builtins.copy = copy
import reportlab
builtins.reportlab = reportlab
import reportlab.platypus
builtins.reportlab.platypus = reportlab.platypus
import reportlab.lib
builtins.reportlab.lib = reportlab.lib

class PDF:
	def __init__ (self, cls_steps):
		self.cls_steps = cls_steps
		self.objects = self.cls_steps.objects
	
	
	def dynamic_function (self, function, to_class = True):
		if to_class is True:
			func = {}
			exec (function['Code'], func)
			setattr (PDF, function['Function'], func[function['Function']])
		else:
			exec (function['Code'], globals ())
			builtins.__dict__[function['Function']] = globals ()[function['Function']]
	
	
	def execute (self, isolation = None, **opts):
		try:
			if opts['Function'] == 'PDF:Create':
				return self.step_create (isolation, **opts)
			elif opts['Function'] == 'PDF:Add.Paragraph':
				return self.step_add_paragraph (isolation, **opts)
			elif opts['Function'] == 'PDF:Add.Table':
				return self.step_add_table (isolation, **opts)
			elif opts['Function'] == 'PDF:Add.PageBreak':
				return self.step_add_pagebreak (isolation, **opts)
			elif opts['Function'] == 'PDF:Add.Image':
				return self.step_add_image (isolation, **opts)
			elif opts['Function'] == 'PDF:Document.Frames':
				return self.step_document_frames (isolation, **opts)
			elif opts['Function'] == 'PDF:Close':
				return self.step_close (isolation, **opts)
			else:
				return False, {'Status':'WARNING', 'Title':'PDF:execute: Aborted', 'Message':'Unknown execute:' + str (opts)}
		except Exception as e:
			st = internal_zyd_stacktrace (e, FunctionOpts=opts)
			return False, {'Status':'CRASH', 'Title':'PDF:execute: Crashed', 'Message':'Crashed with the error: ' + str (e) + ' for step:\n' + str (opts), 'StackTrace':st}

	
	def step_create (self, isolation, **opts):
		if 'ID' not in opts:
			return False, {'Status':'WARNING', 'Title':'PDF:step_create: Aborted', 'Message':'No ID was provided.'}
		elif opts['ID'] in self.objects['PDF']:
			return False, {'Status':'WARNING', 'Title':'PDF:step_create: Aborted', 'Message':'The ID "' + str (opts['ID']) + '" already exists.'}
		if 'File' not in opts:
			return False, {'Status':'WARNING', 'Title':'PDF:step_create: Aborted', 'Message':'No File was provided.'}
		
		template_opts = {
			'pagesize':reportlab.lib.pagesizes.letter,
			'leftMargin':0,
			'rightMargin':0,
			'topMargin':0,
			'bottomMargin':0,
		}
		if 'Width' in opts and isinstance (opts['Width'], int) and 'Height' in opts and isinstance (opts['Height'], int):
			template_opts['pagesize'] = (int (opts['Width'] * 2.834), int (opts['Height'] * 2.834))
		for field in [['Margin.Left', 'leftMargin', int], ['Margin.Right', 'rightMargin', int], ['Margin.Top', 'topMargin', int], ['Margin.Bottom', 'bottomMargin', int]]:
			if field[0] in opts and isinstance (opts[field[0]], field[2]):
				template_opts[field[1]] = opts[field[0]]
		
		self.objects['PDF'][opts['ID']] = {
			'Object': reportlab.platypus.BaseDocTemplate (opts['File'], **template_opts),
			'Frames':{},
			'Content':[],
			'Size':{
				'Margin.Left':template_opts['leftMargin'],
				'Margin.Right':template_opts['rightMargin'],
				'Margin.Top':template_opts['topMargin'],
				'Margin.Bottom':template_opts['bottomMargin'],
			}
		}
		self.objects['PDF'][opts['ID']]['Size']['Width'] = self.objects['PDF'][opts['ID']]['Object'].pagesize[0] - self.objects['PDF'][opts['ID']]['Object'].leftMargin - self.objects['PDF'][opts['ID']]['Object'].rightMargin
		self.objects['PDF'][opts['ID']]['Size']['Height'] = self.objects['PDF'][opts['ID']]['Object'].pagesize[1] - self.objects['PDF'][opts['ID']]['Object'].topMargin - self.objects['PDF'][opts['ID']]['Object'].bottomMargin
		return True, {'Status':'OK'}
	
	
	def step_add_paragraph (self, isolation, **opts):
		if 'ID' not in opts:
			return False, {'Status':'WARNING', 'Title':'PDF:step_add_paragraph: Aborted', 'Message':'No ID was provided.'}
		elif opts['ID'] not in self.objects['PDF']:
			return False, {'Status':'WARNING', 'Title':'PDF:step_add_paragraph: Aborted', 'Message':'The ID "' + str (opts['ID']) + '" doesn\'t exist.'}
		if 'Paragraph' not in opts:
			return False, {'Status':'WARNING', 'Title':'PDF:step_add_paragraph: Aborted', 'Message':'No Paragraph was provided.'}

		paragraph = reportlab.platypus.Paragraph (opts['Paragraph'], reportlab.lib.styles.getSampleStyleSheet ()['Heading1'])
		self.objects['PDF'][opts['ID']]['Content'].append (paragraph)
		return True, {'Status':'OK'}

	
	def step_add_table (self, isolation, **opts):
		if 'ID' not in opts:
			return False, {'Status':'WARNING', 'Title':'PDF:step_add_table: Aborted', 'Message':'No ID was provided.'}
		elif opts['ID'] not in self.objects['PDF']:
			return False, {'Status':'WARNING', 'Title':'PDF:step_add_table: Aborted', 'Message':'The ID "' + str (opts['ID']) + '" doesn\'t exist.'}
		if 'Data' not in opts or not isinstance (opts['Data'], list):
			return False, {'Status':'WARNING', 'Title':'PDF:step_add_table: Aborted', 'Message':'No Data was provided.'}
		if 'Style' in opts and not isinstance (opts['Style'], list):
			return False, {'Status':'WARNING', 'Title':'PDF:step_add_table: Aborted', 'Message':'Style needs to be a list.'}
		
		table_opts = {}
		if 'SpaceBefore' in opts and isinstance (opts['SpaceBefore'], int):
			table_opts['spaceBefore'] = opts['SpaceBefore']
		if 'SpaceAfter' in opts and isinstance (opts['SpaceAfter'], int):
			table_opts['spaceAfter'] = opts['SpaceAfter']
		if 'ColumnWidth' in opts and isinstance (opts['ColumnWidth'], (int, list)):
			table_opts['colWidths'] = copy.deepcopy (opts['ColumnWidth'])
			if isinstance (opts['ColumnWidth'], list) and len (opts['ColumnWidth']) < len (opts['Data'][0]):
				for x in range (len (opts['ColumnWidth']), len (opts['Data'][0])):
					table_opts['colWidths'].append (opts['ColumnWidth'][x % len (opts['ColumnWidth'])])
		if 'RowHeight' in opts and isinstance (opts['RowHeight'], (int, list)):
			table_opts['rowHeights'] = copy.deepcopy (opts['RowHeight'])
			if isinstance (opts['RowHeight'], list) and len (opts['RowHeight']) < len (opts['Data']):
				for x in range (len (opts['RowHeight']), len (opts['Data'])):
					table_opts['rowHeights'].append (opts['RowHeight'][x % len (opts['RowHeight'])])
		data = opts['Data']
		if 'Data.Convert' in opts and isinstance (opts['Data.Convert'], list):
			for rule in opts['Data.Convert']:
				status, data = datahandling_convert (data, **rule)
		table = reportlab.platypus.Table (data, **table_opts)

		style = []
		if 'Style' in opts:
			for row in opts['Style']:
				if row['Type'] == 'Background':
					style.append (('BACKGROUND', (row['Area'][1], row['Area'][0]), (row['Area'][3], row['Area'][2]), reportlab.lib.colors.HexColor (row['Color'])))
				elif row['Type'] == 'Text':
					style.append (('TEXTCOLOR', (row['Area'][1], row['Area'][0]), (row['Area'][3], row['Area'][2]), reportlab.lib.colors.HexColor (row['Color'])))
				elif row['Type'] == 'Grid':
					style.append (('GRID', (row['Area'][1], row['Area'][0]), (row['Area'][3], row['Area'][2]), row['Width'], reportlab.lib.colors.HexColor (row['Color'])))
				elif row['Type'] == 'Box':
					style.append (('BOX', (row['Area'][1], row['Area'][0]), (row['Area'][3], row['Area'][2]), row['Width'], reportlab.lib.colors.HexColor (row['Color'])))
				elif row['Type'] == 'Align':
					style.append (('ALIGN', (row['Area'][1], row['Area'][0]), (row['Area'][3], row['Area'][2]), row['Alignment'].upper ()))
				elif row['Type'] == 'VerticalAlign':
					style.append (('VALIGN', (row['Area'][1], row['Area'][0]), (row['Area'][3], row['Area'][2]), row['Alignment'].upper ()))
				elif row['Type'] == 'FontSize':
					style.append (('FONTSIZE', (row['Area'][1], row['Area'][0]), (row['Area'][3], row['Area'][2]), row['Size']))
		if 'Span' in opts:
			for row in opts['Span']:
				style.append (('SPAN', (row[1], row[0]), (row[3], row[2])))
		if len (style) > 0:
			table.setStyle (reportlab.platypus.TableStyle (style))
		self.objects['PDF'][opts['ID']]['Content'].append (table)
		return True, {'Status':'OK'}
	
	
	def step_add_pagebreak (self, isolation, **opts):
		if 'ID' not in opts:
			return False, {'Status':'WARNING', 'Title':'PDF:step_add_pagebreak: Aborted', 'Message':'No ID was provided.'}
		elif opts['ID'] not in self.objects['PDF']:
			return False, {'Status':'WARNING', 'Title':'PDF:step_add_pagebreak: Aborted', 'Message':'The ID "' + str (opts['ID']) + '" doesn\'t exist.'}
		self.objects['PDF'][opts['ID']]['Content'].append (reportlab.platypus.PageBreak ())
		return True, {'Status':'OK'}


	def step_add_image (self, isolation, **opts):
		if 'ID' not in opts:
			return False, {'Status':'WARNING', 'Title':'PDF:step_add_image: Aborted', 'Message':'No ID was provided.'}
		elif opts['ID'] not in self.objects['PDF']:
			return False, {'Status':'WARNING', 'Title':'PDF:step_add_image: Aborted', 'Message':'The ID "' + str (opts['ID']) + '" doesn\'t exist.'}
		if 'File' not in opts and 'FileIO' not in opts:
			return False, {'Status':'WARNING', 'Title':'PDF:step_add_image: Aborted', 'Message':'No File or FileIO was provided.'}
		if 'File' in opts and not os.path.exists (opts['File']):
			return False, {'Status':'WARNING', 'Title':'PDF:step_add_image: Aborted', 'Message':'The File "' + str (opts['File']) + '" does not exist.'}
		image_opts = {
		}
		for field in [['Width', 'width', int], ['Height', 'height', int]]:
			if field[0] in opts and isinstance (opts[field[0]], field[2]):
				image_opts[field[1]] = opts[field[0]]
		
		try:
			image = reportlab.platypus.Image ((opts['File'] if 'File' in opts else opts['FileIO']))
			if 'width' in image_opts and 'height' in image_opts:
				image._restrictSize (image_opts['width'], image_opts['height'])
		except Exception as e:
			return False, {'Status':'CRASH', 'Title':'PDF:step_add_image: Crashed', 'Message':'Adding image failed with the following error:\n' + str (e)}
		
		if ('ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str)) or ('ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str)):
			if 'ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str):
				self.cls_steps.internal_value_set_value (isolation, 'Variable', image, opts['ReturnVariable'])
			if 'ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str):
				self.cls_steps.internal_value_set_value (None, 'Variable', image, opts['ReturnVariable.Global'])
		else:
			self.objects['PDF'][opts['ID']]['Content'].append (image)
		return True, {'Status':'OK'}
	
	
	def step_document_frames (self, isolation, **opts):
		if 'ID' not in opts:
			return False, {'Status':'WARNING', 'Title':'PDF:step_document_frames: Aborted', 'Message':'No ID was provided.'}
		elif opts['ID'] not in self.objects['PDF']:
			return False, {'Status':'WARNING', 'Title':'PDF:step_document_frames: Aborted', 'Message':'The ID "' + str (opts['ID']) + '" doesn\'t exist.'}
		
		if 'Border.Color' in opts and isinstance (opts['Border.Color'], str):
			border = reportlab.lib.colors.HexColor (opts['Border.Color'])
		else:
			border = 0
		
		if 'Split' in opts and isinstance (opts['Split'], int):
			width = self.objects['PDF'][opts['ID']]['Size']['Width'] / opts['Split']
			height = self.objects['PDF'][opts['ID']]['Size']['Height']
			frames = []
			for x in range (0, opts['Split']):
				frames.append (reportlab.platypus.Frame (
					x1=self.objects['PDF'][opts['ID']]['Size']['Margin.Left'] + width * x,
					y1=self.objects['PDF'][opts['ID']]['Size']['Margin.Bottom'],
					width=width,
					height=height,
					showBoundary=border)
				)
			page_template = reportlab.platypus.PageTemplate (id='Frames', frames=frames)
			self.objects['PDF'][opts['ID']]['Object'].addPageTemplates ([page_template])
		else:
			return False, {'Status':'WARNING', 'Title':'PDF:step_document_frames: Aborted', 'Message':'No logic for how to use frames was provided.'}
		
		return True, {'Status':'OK'}
	
	
	def step_close (self, isolation, **opts):
		if 'ID' not in opts:
			return False, {'Status':'WARNING', 'Title':'PDF:step_close: Aborted', 'Message':'No ID was provided.'}
		elif opts['ID'] not in self.objects['PDF']:
			return False, {'Status':'WARNING', 'Title':'PDF:step_close: Aborted', 'Message':'The ID "' + str (opts['ID']) + '" doesn\'t exist.'}
		
		if not self.objects['PDF'][opts['ID']]['Object'].pageTemplates:
			self.objects['PDF'][opts['ID']]['Object'].addPageTemplates ([reportlab.platypus.PageTemplate (id='Default', frames=[reportlab.platypus.Frame (
				self.objects['PDF'][opts['ID']]['Size']['Margin.Left'], self.objects['PDF'][opts['ID']]['Size']['Margin.Bottom'],
				self.objects['PDF'][opts['ID']]['Size']['Width'], self.objects['PDF'][opts['ID']]['Size']['Height'],
				showBoundary=0
			)])])
		
		self.objects['PDF'][opts['ID']]['Object'].build (self.objects['PDF'][opts['ID']]['Content'])
		del (self.objects['PDF'][opts['ID']])
		return True, {'Status':'OK'}
