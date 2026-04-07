# Copyright (c) 2025-2026 Erik Persson
# Licensed for free use only. Copying, modification, or redistribution prohibited.

import builtins
from logging import exception, error
from Functions.Common import *
from Functions.DataHandling import *
for name in dir ():
	if not name.startswith ("_"):
		builtins.__dict__[name] = globals ()[name]
import pandas
builtins.pandas = pandas
import numpy
builtins.numpy = numpy
import csv
builtins.csv = csv
import copy
builtins.copy = copy
import math
builtins.math = math


class Pandas:
	def __init__ (self, cls_steps):
		self.cls_steps = cls_steps
		self.objects = self.cls_steps.objects
	
	
	def dynamic_function (self, function, to_class = True):
		if to_class is True:
			func = {}
			exec (function['Code'], func)
			setattr (Pandas, function['Function'], func[function['Function']])
		else:
			exec (function['Code'], globals ())
			builtins.__dict__[function['Function']] = globals ()[function['Function']]
	
	
	def execute (self, isolation = None, **opts):
		try:
			if opts['Function'] == 'PANDAS:Open':
				return self.step_open (isolation, **opts)
			elif opts['Function'] == 'PANDAS:Read':
				return self.step_read (isolation, **opts)
			elif opts['Function'] == 'PANDAS:Column.Change':
				return self.step_column_change (isolation, **opts)
			elif opts['Function'] == 'PANDAS:Column.Value':
				return self.step_column_value (isolation, **opts)
			elif opts['Function'] == 'PANDAS:Create.File':
				return self.step_create_file (isolation, **opts)
			else:
				return False, {'Status':'WARNING', 'Title':'PANDAS:execute: Aborted', 'Message':'Unknown execute:' + str (opts)}
		except Exception as e:
			st = internal_zyd_stacktrace (e, FunctionOpts=opts)
			return False, {'Status':'CRASH', 'Title':'PANDAS:execute: Crashed', 'Message':'Crashed with the error: ' + str (e) + ' for step:\n' + str (opts), 'StackTrace':st}

	
	def step_open (self, isolation, **opts):
		if 'ID' not in opts:
			return False, {'Status':'WARNING', 'Title':'PANDAS:step_open: Aborted', 'Message':'No ID provided.'}
		if 'File' in opts and not os.path.exists (opts['File']):
			return False, {'Status':'WARNING', 'Title':'PANDAS:step_open: Aborted', 'Message':'The file "' + str (opts['File']) + '" does not exist.'}
		debug_console = (True if 'Debug.Console' in opts and opts['Debug.Console'] is True else False)
		
		pandas_opts = {}
		if 'HeaderRow' in opts and isinstance (opts['HeaderRow'], int):
			pandas_opts['header'] = opts['HeaderRow']
		else:
			pandas_opts['header'] = None
		
		if debug_console is True:
			print ('+==[ step_open ]======================================================')
			print ('Opts=' + str (opts))
			print ('Pandas_opts=' + str (pandas_opts))
		
		try:
			self.objects['Pandas'][opts['ID']] = pandas.read_excel (opts['File'], **pandas_opts)
			if debug_console is True:
				print ('Dataframe=' + str (self.objects['Pandas'][opts['ID']])[:1000])
				print ('-============================================================================')
		except Exception as e:
			if 'Can\'t find workbook in OLE2 compound document' in str (e):
				return False, {'Status':'CRASH', 'Title':'PANDAS:step_open: Crashed', 'Message':'Possible encrypted Excel file, Pandas.read_excel crashed with the following error: ' + str (e)}
			return False, {'Status':'CRASH', 'Title':'PANDAS:step_open: Crashed', 'Message':'Pandas.read_excel crashed with the following error: ' + str (e)}
		
		return True, {'Status':'OK'}
	
	
	def step_read (self, isolation, **opts):
		if 'ID' not in opts:
			return False, {'Status':'WARNING', 'Title':'PANDAS:step_read: Aborted', 'Message':'No ID provided.'}
		elif opts['ID'] not in self.objects['Pandas']:
			return False, {'Status':'WARNING', 'Title':'PANDAS:step_read: Aborted', 'Message':'ID "' + str (opts['ID']) + ' does not exist.'}
		if 'Filters' in opts and not isinstance (opts['Filters'], list):
			return False, {'Status':'WARNING', 'Title':'PANDAS:step_read: Aborted', 'Message':'Filters needs to be a list of dicts.'}

		if 'Filters' in opts and isinstance (opts['Filters'], list):
			status, mask = self.internal_pandas_create_filter_mask (opts['ID'], opts['Filters'])
			if status is False:
				return False, {'Status':mask['Status'], 'Title':'PANDAS:step_read: Aborted', 'Message':mask['Message']}
			object = self.objects['Pandas'][opts['ID']][mask]
		else:
			object = self.objects['Pandas'][opts['ID']]
		
		if 'Nan2None' in opts and opts['Nan2None'] is True:
			value = object.replace ({numpy.nan: None}).values.tolist ()
		else:
			value = object.values.tolist ()
		
		if 'ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str):
			self.cls_steps.internal_value_set_value (isolation, 'Variable', value, opts['ReturnVariable'])
		if 'ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str):
			self.cls_steps.internal_value_set_value (None, 'Variable', value, opts['ReturnVariable.Global'])
		return True, {'Status':'OK'}

	
	def step_column_change (self, isolation, **opts):
		if 'ID' not in opts:
			return False, {'Status':'WARNING', 'Title':'PANDAS:step_column_change: Aborted', 'Message':'No ID provided.'}
		elif opts['ID'] not in self.objects['Pandas']:
			return False, {'Status':'WARNING', 'Title':'PANDAS:step_column_change: Aborted', 'Message':'ID "' + str (opts['ID']) + ' does not exist.'}
		
		if 'Columns.Fill' in opts:
			if not isinstance (opts['Columns.Fill'], list):
				return False, {'Status':'WARNING', 'Title':'PANDAS:step_column_change: Aborted', 'Message':'Columns.Fill needs to be a list of columns.'}
			self.objects['Pandas'][opts['ID']][opts['Columns.Fill']] = self.objects['Pandas'][opts['ID']][opts['Columns.Fill']].ffill ()
		if 'Columns.Convert.Integer' in opts:
			if not isinstance (opts['Columns.Convert.Integer'], list):
				return False, {'Status':'WARNING', 'Title':'PANDAS:step_column_change: Aborted', 'Message':'Columns.Convert.Integer needs to be a list of columns.'}
			self.objects['Pandas'][opts['ID']][opts['Columns.Convert.Integer']] = self.objects['Pandas'][opts['ID']][opts['Columns.Convert.Integer']].astype ('int')
		
		return True, {'Status':'OK'}


	def step_column_value (self, isolation, **opts):
		if 'ID' not in opts:
			return False, {'Status':'WARNING', 'Title':'PANDAS:step_column_value: Aborted', 'Message':'No ID provided.'}
		elif opts['ID'] not in self.objects['Pandas']:
			return False, {'Status':'WARNING', 'Title':'PANDAS:step_column_value: Aborted', 'Message':'ID "' + str (opts['ID']) + '" does not exist.'}
		
		if 'Column' in opts and 'Logic' in opts:
			return self.internal_step_column_value (isolation, **opts)
		elif 'Multiple' in opts and isinstance (opts['Multiple'], list):
			for value in opts['Multiple']:
				if not isinstance (value, dict):
					return False, {'Status':'WARNING', 'Title':'PANDAS:step_column_value: Aborted', 'Message':'All entries in the Multiple list must be dicts.'}
				status, result = self.internal_step_column_value (isolation, **{**{'ID':opts['ID']}, **value})
				if status is not True:
					return status, result
			return True, {'Status':'OK', 'Message':str (len (opts['Multiple'])) + ' values captured.'}
		return False, {'Status':'WARNING', 'Title':'PANDAS:step_column_value: Aborted', 'Message':'A Column+Column or Multiple config needs to be provided.'}

		
	def internal_step_column_value (self, isolation, **opts):
		pd = self.objects['Pandas'][opts['ID']]
		if 'Column' not in opts:
			return False, {'Status':'WARNING', 'Title':'PANDAS:step_column_value: Aborted', 'Message':'No Column to sum was provided.'}
		if 'Logic' not in opts or opts['Logic'] not in ['Sum', 'Count', 'Min', 'Max', 'Average', 'Median', 'CountUnique', 'ListUnique']:
			return False, {'Status':'WARNING', 'Title':'PANDAS:step_column_value: Aborted', 'Message':'No valid Logic provided.'}
		if 'Filters' in opts and not isinstance (opts['Filters'], list):
			return False, {'Status':'WARNING', 'Title':'PANDAS:step_column_value: Aborted', 'Message':'Filters needs to be a list of dicts.'}
		
		status, mask = self.internal_pandas_create_filter_mask (opts['ID'], (opts['Filters'] if 'Filters' in opts else []))
		if status is not True:
			return False, {'Status':mask['Status'], 'Title':'PANDAS:step_column_value: Aborted', 'Message':mask['Message']}
		
		if opts['Logic'] == 'Sum':
			value = pd.loc[mask, opts['Column']].sum ()
		elif opts['Logic'] == 'Count':
			value = pd.loc[mask, opts['Column']].count ()
		elif opts['Logic'] == 'Min':
			value = pd.loc[mask, opts['Column']].min ()
		elif opts['Logic'] == 'Max':
			value = pd.loc[mask, opts['Column']].max ()
		elif opts['Logic'] == 'Average':
			value = pd.loc[mask, opts['Column']].mean ()
		elif opts['Logic'] == 'Median':
			value = pd.loc[mask, opts['Column']].median ()
		elif opts['Logic'] == 'CountUnique':
			value = pd.loc[mask, opts['Column']].nunique ()
		elif opts['Logic'] == 'ListUnique':
			value = pd.loc[mask, opts['Column']].unique ().tolist ()
			value = [None if isinstance (x, (float, int)) and math.isnan (x) else x for x in value]
		
		if type (value) == numpy.float64:
			value = float (value)
		elif type (value) == numpy.int64:
			value = int (value)
		elif type (value) not in [int, str, list]:
			return False, {'Status':'ERROR', 'Title':'PANDAS:step_column_value: Aborted', 'Message':'Unknown Pandas return type:' + str (type (value))}
		
		if 'Convert' in opts and isinstance (opts['Convert'], list):
			for convert in opts['Convert']:
				status, value = datahandling_convert (value, **convert)
				if status is not True:
					return False, {'Status':'ERROR', 'Title':'PANDAS:step_column_value: Aborted', 'Message':'The conversion rule "' + str (convert) + '" failed with the error:\n' + str (value)}
					
		if 'ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str):
			self.cls_steps.internal_value_set_value (isolation, 'Variable', value, opts['ReturnVariable'])
		if 'ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str):
			self.cls_steps.internal_value_set_value (None, 'Variable', value, opts['ReturnVariable.Global'])
		if 'UpdateGUI.Value' in opts and isinstance (opts['UpdateGUI.Value'], str):
			self.cls_steps.cls_gui.internal_object_update (isolation, opts['UpdateGUI.Value'], Value=value, Trigger=(True if 'UpdateGUI.Value.Trigger' in opts and opts ['UpdateGUI.Value.Trigger'] is True else False))
		return True, {'Status':'OK', 'Data':value}
	
	
	def internal_pandas_create_filter_mask (self, id, filters):
		pd = self.objects['Pandas'][id]
		mask = pandas.Series ([True] * len (self.objects['Pandas'][id]))
		for filter in filters:
			if filter['Logic'] == '=':
				if 'Values' in filter and isinstance (filter['Values'], list):
					mask &= pd[filter['Column']].isin (filter['Values'])
				elif 'Value' in filter:
					mask &= pd[filter['Column']] == filter['Value']
				else:
					return False, {'Status':'WARNING', 'Message':'Filter logic for "=" missing values.\nFilter=' + str (filter)}
			elif filter['Logic'] == '!=':
				if 'Values' in filter and isinstance (filter['Values'], list):
					mask &= ~pd[filter['Column']].isin (filter['Values'])
				elif 'Value' in filter:
					mask &= pd[filter['Column']] != filter['Value']
				else:
					return False, {'Status':'WARNING', 'Message':'Filter logic for "!=" missing values.\nFilter=' + str (filter)}
			elif filter['Logic'] == '(!=)':
				if 'Values' in filter and isinstance (filter['Values'], list):
					for value in filter['Values']:
						mask &= ~pd[filter['Column']].str.contains (value, na=False)
				elif 'Value' in filter:
					mask &= ~pd[filter['Column']].str.contains (filter['Value'], na=False)
				else:
					return False, {'Status':'WARNING', 'Message':'Filter logic for "(!=)" missing values.\nFilter=' + str (filter)}
			elif filter['Logic'] == '(=)':
				if 'Values' in filter and isinstance (filter['Values'], list):
					for value in filter['Values']:
						mask &= pd[filter['Column']].str.contains (value, na=False)
				elif 'Value' in filter:
					mask &= pd[filter['Column']].str.contains (filter['Value'], na=False)
				else:
					return False, {'Status':'WARNING', 'Message':'Filter logic for "(=)" missing values.\nFilter=' + str (filter)}
			elif filter['Logic'] == '<':
				if 'Value' in filter:
					mask &= pd[filter['Column']] < filter['Value']
				else:
					return False, {'Status':'WARNING', 'Message':'Filter logic for "<" missing value.\nFilter=' + str (filter)}
			elif filter['Logic'] == '>':
				if 'Value' in filter:
					mask &= pd[filter['Column']] > filter['Value']
				else:
					return False, {'Status':'WARNING', 'Message':'Filter logic for ">" missing value.\nFilter=' + str (filter)}
			else:
				return False, {'Status':'WARNING', 'Message':'Unknown filter logic.\nFilter=' + str (filter)}
		return True, mask
	
	
	def step_create_file (self, isolation, **opts):
		if 'File' not in opts:
			return False, {'Status':'WARNING', 'Title':'PANDAS:step_create_file: Aborted', 'Message':'A File needs to be provided.'}
		if 'File.Type' not in opts:
			return False, {'Status':'WARNING', 'Title':'PANDAS:step_create_file: Aborted', 'Message':'A File.Type needs to be provided.'}
		
		writer_opts = {
			'mode':'w',
		}
		df_create_opts = {
		}
		df_write_opts = {
			'index':False,
			'header':False,
		}
		
		if 'File.Append' in opts and opts['File.Append'] is True:
			if os.path.exists (opts['File']):
				writer_opts['mode'] = 'a'
		if opts['File.Type'] == 'CSV':
			df_write_opts['lineterminator'] = '\n'
			if 'CSV.Separator' in opts and isinstance (opts['CSV.Separator'], str):
				df_write_opts['sep'] = opts['CSV.Separator']
			if 'CSV.QuoteCharacter' in opts and isinstance (opts['CSV.QuoteCharacter'], str) and len (opts['CSV.QuoteCharacter']) == 1:
				df_write_opts['quotechar'] = opts['CSV.QuoteCharacter']
			if 'CSV.Quoting' in opts:
				if opts['CSV.Quoting'] == 'Minimal':
					df_write_opts['quoting'] = csv.QUOTE_MINIMAL
				if opts['CSV.Quoting'] == 'All':
					df_write_opts['quoting'] = csv.QUOTE_ALL
				if opts['CSV.Quoting'] == 'NonNumeric':
					df_write_opts['quoting'] = csv.QUOTE_NONNUMERIC
				if opts['CSV.Quoting'] == 'None':
					df_write_opts['quoting'] = csv.QUOTE_NONE
		else:
			if 'Sheet' in opts and isinstance (opts['Sheet'], str):
				df_write_opts['sheet_name'] = opts['Sheet']
			if 'Sheet.Replace' in opts and opts['Sheet.Replace'] is True:
				if 'mode' in writer_opts and writer_opts['mode'] == 'a':
					writer_opts['if_sheet_exists'] = 'replace'
		
		if 'Data.List' in opts and isinstance (opts['Data.List'], list):
			data = []
			for row in opts['Data.List']:
				if isinstance (row, (dict, list)):
					return False, {'Status':'WARNING', 'Title':'PANDAS:step_create_file: Aborted', 'Message':'"Data.List" did not only contain lists.'}
				data.append ([row])
		elif 'Data.ListList' in opts and isinstance (opts['Data.ListList'], list):
			for row in opts['Data.ListList']:
				if not isinstance (row, list):
					return False, {'Status':'WARNING', 'Title':'PANDAS:step_create_file: Aborted', 'Message':'"Data.ListList" did not only contain lists in the 2nd level.'}
			data = opts['Data.ListList']
		elif 'Data.DictList' in opts and isinstance (opts['Data.DictList'], dict):
			length = 0
			for row in opts['Data.DictList'].values ():
				length = max (length, len (row))
				if not isinstance (row, list):
					return False, {'Status':'WARNING', 'Title':'PANDAS:step_create_file: Aborted', 'Message':'"Data.DictList" did not only contain lists in the 2nd level.'}
			data = [[] for _ in range (length + 1)]
			data[0] = list (opts['Data.DictList'].keys ())
			for column in range (0, len (data[0])):
				for row in range (0, length):
					if len (opts['Data.DictList'][data[0][column]]) > row:
						data[row + 1].append (opts['Data.DictList'][data[0][column]][row])
					else:
						data[row + 1].append (numpy.nan)
		elif 'Data.Dict' in opts and isinstance (opts['Data.Dict'], dict):
			data = []
			for key in opts['Data.Dict'].keys ():
				data.append ([key, opts['Data.Dict'][key]])
		else:
			return False, {'Status':'WARNING', 'Title':'PANDAS:step_create_file: Aborted', 'Message':'No valid Data provided.'}
		
		
		if 'Header.List' in opts and isinstance (opts['Header.List'], list):
			data.insert (0, opts['Header.List'])
		
		# Pad list with #NaN to make the size even...
		length = max (len (row) for row in data)
		data = [row + [numpy.nan] * (length - len (row)) for row in data]
		data = self.internal_transform_list_data (data, **opts)
		if 'Transpose' in opts and opts['Transpose'] is True:
			data = list (map (list, zip (*data)))
		df = pandas.DataFrame (data=(self.internal_convert_list_data (data) if 'Convert' in opts and opts['Convert'] is True else data), **df_create_opts)
		
		if opts['File.Type'] != 'CSV':
			if 'Header.Style' in opts and isinstance (opts['Header.Style'], str):
				style_opts = {}
				if 'Transpose' in opts and opts['Transpose'] is True:
					header_func = lambda col:[opts['Header.Style'] if df.columns.get_loc (col.name) == 0 else '' for _ in col]
					style_opts['axis'] = 0
				else:
					header_func = lambda row:[opts['Header.Style'] if row.name == 0 else '' for _ in row]
					style_opts['axis'] = 1
				df = df.style.apply (header_func, **style_opts)
		try:
			if opts['File.Type'] == 'Excel':
				df_write_opts['engine'] = 'openpyxl'
				with pandas.ExcelWriter (opts['File'], **writer_opts) as writer:
					df.to_excel (writer, **df_write_opts)
			elif opts['File.Type'] == 'CSV':
				with open (opts['File'], **writer_opts) as fp:
					df.to_csv (fp, **df_write_opts)
		
		except Exception as e:
			return False, {'Status':'ERROR', 'Title':'PANDAS:step_create_file: Crashed', 'Message':'The file write logic crashed with the following error:\n' + str (e)}
		return True, {'Status':'OK'}


	def internal_transform_list_data (self, data, **opts):
		if isinstance (data, list):
			for key in range (0, len (data)):
				data[key] = self.internal_transform_list_data (data[key], **opts)
		elif isinstance (data, dict):
			for key in data.keys ():
				data[key] = self.internal_transform_list_data (data[key], **opts)
		elif isinstance (data, (int, float)) or data.__class__.__name__ == 'Decimal':
			if 'Data.RoundDecimals' in opts and isinstance (opts['Data.RoundDecimals'], int):
				data = round (data, opts['Data.RoundDecimals'])
			if 'Data.DecimalCharacter' in opts and isinstance (opts['Data.DecimalCharacter'], str):
				data = str (data).replace ('.', opts['Data.DecimalCharacter'])
		return data


	def internal_convert_list_data (self, data):
		if isinstance (data, list):
			for key in range (0, len (data)):
				data[key] = self.internal_convert_list_data (data[key])
		elif isinstance (data, dict):
			if 'Convert' in data and 'Value' in data and isinstance (data['Convert'], list):
				value = copy.deepcopy (data['Value'])
				for convert in data['Convert']:
					status, value = datahandling_convert (value, **convert)
					if status is not True:
						print ('internal_convert_list_data.BREAK::' + str (data) + '::' + str (value))
						return data['Value']
				return value
		return data
