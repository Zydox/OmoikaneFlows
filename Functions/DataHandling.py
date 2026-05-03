# Copyright (c) 2025-2026 Erik Persson
# Licensed for free use only. Copying, modification, or redistribution prohibited.

# -*- coding: utf-8 -*-

import datetime
import copy
from Functions.Common import *

def datahandling_convert (value, **opts) -> tuple[bool, any]:
	if 'Type' not in opts:
		return zyd_return (False, {'Status':'WARNING', 'Function':'datahandling_convert', 'Title':'Aborted: Missing type', 'Message':'The Type option was empty.'}, **opts)
	
	try:
		if 'ConvertOpts' in opts and opts['ConvertOpts'] is True:
			for opt in list (opts.keys ()):
				if '_' in opt:
					opts[opt.replace ('_', '.')] = opts[opt]
					del (opts[opt])
		
		value = copy.deepcopy (value)
		if isinstance (value, str):
			if 'Trim' in opts and opts['Trim'] is True:
				value = value.strip ()
			if 'Trim.Left' in opts:
				if opts['Trim.Left'] is True:
					value = value.lstrip ()
				elif isinstance (opts['Trim.Left'], str):
					value = value.lstrip (opts['Trim.Left'])
			if 'Trim.Right' in opts:
				if opts['Trim.Right'] is True:
					value = value.lstrip ()
				elif isinstance (opts['Trim.Right'], str):
					value = value.lstrip (opts['Trim.Right'])
			if len (value) == 0 and 'Replace.Empty' in opts:
				value = opts['Replace.Empty']
			if 'Canonicalize.Negative' in opts and opts['Canonicalize.Negative'] is True and '-' in value:
				if len (value) > 2 and value[:2] == '-+':
					value = '-' + value[2:]
				if value[-1] == '-':
					if value[0] == '+':
						value = value[1:]
					value = '-' + value[:-1]
			if 'Canonicalize.Positive' in opts and opts['Canonicalize.Positive'] is True and '+' in value:
				if len (value) > 2 and value[0] == '-' and value[-1] == '+':
					value = value[1:-1]
				elif value[0] == '+':
					value = value[1:]
				elif len (value) > 1 and value[-1] == '+':
					value = value[:-1]
			if 'NumberFormat.From' in opts and isinstance (opts['NumberFormat.From'], str):
				if opts['NumberFormat.From'] == 'X,XXX,XXX.XX':
					value = value.replace (',', '').replace (' ', '')
				elif opts['NumberFormat.From'] == 'X XXX XXX,XX':
					value = value.replace (' ', '').replace (',', '.')
				elif opts['NumberFormat.From'] == 'X.XXX.XXX,XX':
					value = value.replace ('.', '').replace (' ', '').replace (',', '.')
				else:
					return zyd_return (False, {'Status': 'WARNING', 'Function':'datahandling_convert', 'Title':'Aborted: Unknown NumberFormat.From', 'Message':'The number format "' + opts['NumberFormat.From'] + '" is not known.'}, **opts)
			if 'DateFormat.From' in opts and isinstance (opts['DateFormat.From'], str) and len (value) >= 8:
				if opts['DateFormat.From'] == 'DD.MM.YYYY' and value[2] + value[5] == '..':
					value = value[6:10] + '-' + value[3:5] + '-' + value[:2]
				elif (opts['DateFormat.From'] == 'MM/DD/YYYY' and value[2] + value[5] == '//') or (opts['DateFormat.From'] == 'MM-DD-YYYY' and value[2] + value[5] == '--'):
					value = value[6:10] + '-' + value[:2] + '-' + value[3:5]
				elif (opts['DateFormat.From'] == 'YYYY.MM.DD' and value[4] + value[7] == '..') or (opts['DateFormat.From'] == 'YYYY/MM/DD' and value[4] + value[7] == '//'):
					value = value[:4] + '-' + value[5:7] + '-' + value[8:10]
				elif opts['DateFormat.From'] != 'YYYY-MM-DD':
					return zyd_return (False, {'Status': 'WARNING', 'Function':'datahandling_convert', 'Title':'Aborted: Unknown DateFormat.From', 'Message':'The date format "' + opts['DateFormat.From'] + '" is not known or the value "' + str (value) + '" is not a date.'}, **opts)
			if 'Encode' in opts and isinstance (opts['Encode'], str):
				value = value.encode (opts['Encode'])
			if 'Decode' in opts and isinstance (opts['Decode'], str):
				value = value.decode (opts['Decode'])
			if opts['Type'] in ['Integer', 'Decimal', 'Numeric']:
				if not set (value).issubset (set ("0123456789.+-")):
					return zyd_return (False, {'Status': 'WARNING', 'Function':'datahandling_convert', 'Title':'Aborted: Unknown chars in number value', 'Message':'The number "' + str (value) + '" contains invalid characters.'}, **opts)
		elif value is None and 'Replace.NULL' in opts:
			value = opts['Replace.NULL']
		
		if opts['Type'] in ['Integer']:
			return zyd_return (True, int (float (value)), **opts)
		elif opts['Type'] in ['Decimal']:
			if 'Decimals' in opts and isinstance (opts['Decimals'], int):
				return zyd_return (True, round (float (value), opts['Decimals']), **opts)
			else:
				return zyd_return (True, float (value), **opts)
		elif opts['Type'] in ['Numeric']:
#			print ('CONVERT=' + str (value))
			cvalue = copy.deepcopy (float (value))
			if '.' not in str (value) or str (value)[-1] == '.':
#				print ('CONVERT_CHECK=' + str (cvalue))
				if cvalue.is_integer ():
#					print ('CONVERT_INT=' + str (cvalue))
					cvalue = int (cvalue)
#			print ('RETURN=' + str (cvalue) + '::' + str (type (cvalue)))
			if 'Decimals' in opts and isinstance (opts['Decimals'], int) and isinstance (cvalue, float):
				cvalue = round (cvalue, opts['Decimals'])
			return zyd_return (True, cvalue, **opts)
		elif opts['Type'] == 'Date':
			cvalue = str (value)
			if 'DateFormat.To' in opts and isinstance (opts['DateFormat.To'], str) and len (cvalue) >= 10 and cvalue[4] + cvalue[7] == '--':
				if opts['DateFormat.To'] == 'DD.MM.YYYY':
					cvalue = cvalue[8:10] + '.' + cvalue[5:7] + '.' + cvalue[:4]
				elif opts['DateFormat.To'] == 'MM/DD/YYYY' or opts['DateFormat.To'] == 'MM-DD-YYYY':
					cvalue = cvalue[5:7] + opts['DateFormat.To'][2] + cvalue[8:10] + opts['DateFormat.To'][5] + cvalue[:4]
				elif opts['DateFormat.To'] == 'YYYY.MM.DD' or opts['DateFormat.To'] == 'YYYY/MM/DD':
					cvalue = cvalue[:4] + opts['DateFormat.To'][4] + cvalue[5:7] + opts['DateFormat.To'][7] + cvalue[8:10]
				elif opts['DateFormat.To'] != 'YYYY-MM-DD':
					return zyd_return (False, {'Status': 'WARNING', 'Function':'datahandling_convert', 'Title':'Aborted: Unknown DateFormat.To', 'Message':'The date format "' + opts['DateFormat.To'] + '" is not known or the value "' + str (value) + '" is not a date.'}, **opts)
			check = cvalue[:10].replace ('.', '').replace ('-', '').replace ('/', '')
			if check.isdigit () and len (check) == 8:
				return zyd_return (True, cvalue, **opts)
			return zyd_return (False, {'Status': 'WARNING', 'Function':'datahandling_convert', 'Title':'Aborted: Failed to convert', 'Message':'The value "' + str (value) + '" could not be converted (tried result "' + str (cvalue) + '" for format "' + (str (opts['DateFormat.To']) if 'DateFormat.To' in opts else 'YYYY-MM-DD') + '").'}, **opts)
		elif opts['Type'] == 'Number':
			if 'NumberFormat.To' in opts and isinstance (opts['NumberFormat.To'], str):
				if not isinstance (value, (int, float)):
					return zyd_return (False, {'Status': 'WARNING', 'Function':'datahandling_convert', 'Title':'Aborted: Number', 'Message':'The Number conversion requires an integer or float as input.'}, **opts)
				elif opts['NumberFormat.To'] == 'X,XXX,XXX.XX':
					value = f"{value:,.{(opts['Decimals'] if 'Decimals' in opts and isinstance (opts['Decimals'], int) else 2)}f}"
				elif opts['NumberFormat.To'] == 'X XXX XXX,XX':
					value = f"{value:,.{(opts['Decimals'] if 'Decimals' in opts and isinstance (opts['Decimals'], int) else 2)}f}".replace(',', ' ').replace('.', ',')
				elif opts['NumberFormat.To'] == 'X.XXX.XXX,XX':
					value = f"{value:,.{(opts['Decimals'] if 'Decimals' in opts and isinstance (opts['Decimals'], int) else 2)}f}".replace(',', ' ').replace('.', ',').replace(' ', '.')
				else:
					return zyd_return (False, {'Status': 'WARNING', 'Function':'datahandling_convert', 'Title':'Aborted: Unknown NumberFormat.To', 'Message':'The number format "' + opts['NumberFormat.To'] + '" is not known.'}, **opts)
			elif 'Decimals' in opts and isinstance (opts['Decimals'], int):
				if not isinstance (value, (int, float)):
					return zyd_return (False, {'Status': 'WARNING', 'Function':'datahandling_convert', 'Title':'Aborted: Number', 'Message':'The Number conversion requires an integer or float as input.'}, **opts)
				value = round (value, opts['Decimals'])
			return zyd_return (True, str (value), **opts)
		elif opts['Type'] == 'Datetime':
			if isinstance (value, str):
				if len (value) == 19 and value[4] + value[7] + value[10] + value[13] + value[16] == '-- ::':
					return zyd_return (True, datetime.datetime (int (value[0:4]), int (value[5:7]), int (value[8:10]), int (value[11:13]), int (value[14:16]), int (value[17:19])), **opts)
				elif len (value) == 16 and value[4] + value[7] + value[10] + value[13] == '-- :':
					return zyd_return (True, datetime.datetime (int (value[0:4]), int (value[5:7]), int (value[8:10]), int (value[11:13]), int (value[14:16]), 0), **opts)
		elif opts['Type'] == 'DBDatetime':
			if value.__class__.__name__ == 'datetime':
				return zyd_return (True, str (value), **opts)
		elif opts['Type'] == 'Enum':
			return zyd_return (True, str (value), **opts)
		elif opts['Type'] == 'String':
			if 'Glue' in opts and isinstance (opts['Glue'], str) and isinstance (value, (list, dict)):
				values = []
				for key in (range (0, len (value)) if isinstance (value, list) else values.keys ()):
					values.append (str (value[key]))
			if 'Replace' in opts and isinstance (opts['Replace'], dict):
				value = internal_zyd_arrayreplace (Value=str (value), ReplaceArray=opts['Replace'])
			if 'Path.Basename' in opts and opts['Path.Basename'] is True:
				value = os.path.basename (str (value))
			if 'Path.Dirname' in opts and opts['Path.Dirname'] is True:
				value = os.path.dirname (str (value))
			if value == '' and 'NULL' in opts and opts['NULL'] is True:
				return zyd_return (True, None, **opts)
			if 'JSON' in opts and opts['JSON'] is True:
				return zyd_return ((zyd_json (value, Encode=True)), **opts)
			return zyd_return (True, str (value), **opts)
		elif opts['Type'] == 'JSON':
			status, result = zyd_json (value, Decode=True)
			return zyd_return (status, result, **opts)
		elif opts['Type'] == 'Boolean':
			return zyd_return (True, (False if value is None or value is False or str (value) == '0' or len (str (value)) == 0 else True))
		elif opts['Type'] == 'Array':
			if 'Array.Convert' in opts and isinstance (opts['Array.Convert'], dict):
				value = internal_datahandling_convert_array_convert (value, opts['Array.Convert'])
			return zyd_return (True, value, **opts)

		return zyd_return (False, {'Status': 'WARNING', 'Function':'datahandling_convert', 'Title':'Aborted: Unknown conversion type/rule', 'Message':'The conversion type "' + str (opts['Type']) + '" for the value "' + str (value) + '" (type: "' + str (type (value)) + '")can\'t be handled.'}, **opts)
	except BaseException as ex:
		return zyd_return (False, {'Status': 'ERROR', 'Function':'datahandling_convert', 'Title':'Crash', 'Message':'The conversion for type "' + str (opts['Type']) + '" and the value "' + str (value) + '" crashed with the following error:\n' + str (ex)}, **opts)


def datahandling_verify (value, **opts) -> tuple[bool, dict]:
	issue = False
	if 'Type' not in opts:
		return zyd_return (False, {'Status':'WARNING', 'Function':'datahandling_verify', 'Title':'Aborted: Missing type', 'Message':'The Type option was empty.'}, **opts)
	
	try:
		if opts['Type'] == 'Integer':
			if not isinstance (value, int):
				issue = True
			else:
				if ('Min' in opts and opts['Min'] is not None and value < opts['Min']) or ('Max' in opts and opts['Max'] is not None and value > opts['Max']) or ('Greater' in opts and opts['Greater'] is not None and value <= opts['Greater']) or ('Less' in opts and opts['Less'] is not None and value >= opts['Less']) or ('Equal' in opts and opts['Equal'] is not None and value != opts['Equal']) or ('NotEqual' in opts and opts['NotEqual'] is not None and value == opts['NotEqual']):
					issue = True
		elif opts['Type'] == 'Decimal':
#			print ('CHECKDEC=' + str (value) + '::' + str (type (value)))
			if (not isinstance (value, float) and value.__class__.__name__ != 'Decimal') or (value.is_integer () is True and ('.' not in str (value) or str (value)[-1] == '.')):
#				print ('CHECKDEC.ISSUE')
				issue = True
			else:
				if ('Min' in opts and opts['Min'] is not None and value < opts['Min']) or ('Max' in opts and opts['Max'] is not None and value > opts['Max']) or ('Greater' in opts and opts['Greater'] is not None and value <= opts['Greater']) or ('Less' in opts and opts['Less'] is not None and value >= opts['Less']) or ('Equal' in opts and opts['Equal'] is not None and value != opts['Equal']) or ('NotEqual' in opts and opts['NotEqual'] is not None and value == opts['NotEqual']):
					issue = True
		elif opts['Type'] == 'Numeric':
			if not isinstance (value, (float, int)) and value.__class__.__name__ != 'Decimal':
				issue = True
			else:
				if ('Min' in opts and opts['Min'] is not None and value < opts['Min']) or ('Max' in opts and opts['Max'] is not None and value > opts['Max']) or ('Greater' in opts and opts['Greater'] is not None and value <= opts['Greater']) or ('Less' in opts and opts['Less'] is not None and value >= opts['Less']) or ('Equal' in opts and opts['Equal'] is not None and value != opts['Equal']) or ('NotEqual' in opts and opts['NotEqual'] is not None and value == opts['NotEqual']):
					issue = True
		elif opts['Type'] == 'Datetime':
			if value.__class__.__name__ != 'datetime':
				issue = True
		elif opts['Type'] == 'Enum':
			print ('\tCommon.datahandling_verify: Invalid use of "Enum".')
			if 'Values' not in opts or value not in opts['Values']:
				issue = True
		elif opts['Type'] == '!Enum':
			print ('\tCommon.datahandling_verify: Invalid use of "!Enum".')
			if 'Values' not in opts or value in opts['Values']:
				issue = True
		elif opts['Type'] == 'Array=Array':
			if 'Values' not in opts or value.__class__.__name__ != opts['Values'].__class__.__name__ or not (isinstance (value, (dict, list))):
				issue = True
			else:
				for key in (value if isinstance (value, list) else value.keys ()):
					if key not in opts['Values']:
						issue = True
				if issue is False:
					for key in (opts['Values'] if isinstance (opts['Values'], list) else opts['Values'].keys ()):
						if key not in value:
							issue = True
		elif opts['Type'] == 'String':
			if not isinstance (value, str):
				issue = True
			elif 'LengthMax' in opts and len (value) > opts['LengthMax']:
				issue = True
			elif 'LengthMin' in opts and len (value) < opts['LengthMin']:
				issue = True
			elif 'Contains' in opts and opts['Contains'] not in value:
				issue = True
			elif 'NotContains' in opts and opts['NotContains'] in value:
				issue = True
			if 'StartWith' in opts and not value.startswith (opts['StartWith']):
				issue = True
			if 'NotStartWith' in opts and value.startswith (opts['NotStartWith']):
				issue = True
			if 'EndWith' in opts and not value.endswith (opts['EndWith']):
				issue = True
			if 'NotEndWith' in opts and value.endswith (opts['NotEndWith']):
				issue = True
			if 'Values' in opts and isinstance (opts['Values'], list) and value not in opts['Values']:
				issue = True
			if 'Value' in opts and opts['Value'] != value:
				issue = True
		elif opts['Type'] == 'Value':
			if type (value) != type (opts['Value']) or value != opts['Value']:
				issue = True
			elif 'Values' in opts and isinstance (opts['Values'], list) and value not in opts['Values']:
					issue = True
		elif opts['Type'] == 'Date':
			try:
				if isinstance (value, str) and len (value) == 10 and value != '0000-00-00':
					datetime.datetime.strptime (value, '%Y-%m-%d')
				else:
					issue = True
			except:
				issue = True
		elif opts['Type'] == 'Boolean':
			if not isinstance (value, bool):
				issue = True
			else:
				if 'Value' in opts and value != opts['Value']:
					issue = True
		elif opts['Type'] == 'List':
			if not isinstance (value, list):
				issue = True
			if 'EntriesMin' in opts and isinstance (opts['EntriesMin'], int) and len (value) < opts['EntriesMin']:
				issue = True
			if 'EntriesMax' in opts and isinstance (opts['EntriesMax'], int) and len (value) > opts['EntriesMax']:
				issue = True
		elif opts['Type'] == 'NULL':
			if value is not None:
				issue = True
		elif opts['Type'] == '!NULL':
			if value is None:
				issue = True
		elif opts['Type'] == 'Dict':
			if not isinstance (value, dict):
				issue = True
			if 'Keys' in opts and isinstance (opts['Keys'], list) and len (opts['Keys']) > 0:
				for key in opts['Keys']:
					if key not in value:
						issue = True
			if 'Key' in opts:
				if isinstance (opts['Key'], list):
					valid = False
					for key in opts['Key']:
						if key in value:
							valid = True
					if valid is False:
						issue = True
				elif isinstance (opts['Key'], (int, float, str)):
					if opts['Key'] not in value:
						issue = True
		else:
			return zyd_return (False, {'Status': 'WARNING', 'Function':'datahandling_verify', 'Aborted':True, 'Title':'Aborted: Unknown type', 'Message':'The verification for the type "' + str (opts['Type']) + '" doesn\'t exist.'}, **opts)

		if issue is True:
#			print ('CHECK.ISSUE=' + str (value) + '::' + str (type (value)) + '::' + str (opts))
			return zyd_return (False, {'Status': 'WARNING', 'Function':'datahandling_verify', 'Title':'Verification failed', 'Message':'The verification for the value "' + str (value) + '" with the type "' + str (type (value)) + '" and the check rules "' + str (opts) + '" failed.'}, **opts)
	except BaseException as ex:
		return zyd_return (False, {'Status': 'CRASH', 'Function':'datahandling_verify', 'Title':'Crash', 'Message':'The verification for the value "' + str (value) + '" with the type "' + str (type (value)) + '" and the check rules "' + str (opts) + '" crashed.', 'Crash':str (ex)}, **opts)

	return zyd_return (True, {'Status':'OK'}, **opts)


def datahandling_verify_entry (entry, rules, **opts):
	for rule in rules:
		success = False
		for sub_rule in rule:
			if 'Field' in sub_rule and sub_rule['Field'] in entry:
				status, result = datahandling_verify (entry[sub_rule['Field']], **sub_rule['Verify'])
				if status is True:
					success = True
					break
			elif 'Calc' in sub_rule:
				status, result = zyd_calc (sub_rule['Calc'])
				if status is True:
					status, result = datahandling_verify (result, **sub_rule['Verify'])
					if status is True:
						success = True
						break
			elif 'Logic' in sub_rule and 'FIELD_MISSING' in sub_rule['Logic']:
				if sub_rule['Logic']['FIELD_MISSING'] == 'CHECK=FALSE':
					continue
				elif sub_rule['Logic']['FIELD_MISSING'] == 'CHECK=TRUE':
					success = True
					break
				elif sub_rule['Logic']['FIELD_MISSING'] == 'RULE=TRUE':
					return zyd_return (True, {'Status':'OK'}, **opts)
				elif sub_rule['Logic']['FIELD_MISSING'] == 'RULE=FALSE':
					return zyd_return (False, {'Status':'WARNING', 'Title':'Aborted', 'Message':'The field "' + str (sub_rule['Field']) + '" wasn\'t found in the entry.'}, **opts)
			else:
				return zyd_return (False, {'Status':'ERROR', 'Title':'', 'Message':'The field "' + str (sub_rule['Field']) + '" isn\'t in the entry=' + str (entry) + '\nopts=' + str (opts)})
		if 'Logic' in sub_rule:
			pass
		if success is False:
			return zyd_return (False, {'Status':'WARNING'}, **opts)
	
	return zyd_return (True, {'Status':'OK'}, **opts)


def internal_datahandling_verify (value, **opts) -> None|dict:
	status, result = datahandling_verify (value, **opts)
#	print ('INTERNAL=' + str (status) + '::' + str (result))
	if status is False:
		return result
	return None


def internal_datahandling_configconvert (value, **opts) -> any:
	if 'Type' in opts:
		if opts['Type'] == 'Decimal' and 'Decimals' in opts:
			if isinstance (value, str):
				status, value = datahandling_convert (value, **opts)
			return round (value, opts['Decimals'])
	return value


def internal_datahandling_convert_array_convert (value, rules):
	if isinstance (value, (list, dict)):
		for key in (range (0, len (value)) if isinstance (value, list) else value.keys ()):
			value[key] = internal_datahandling_convert_array_convert (value[key], rules)
	elif isinstance (value, str) and 'String' in rules:
		for rule in rules['String']:
			value = datahandling_convert (value, **{**rule, **{'Internal':True}})
	elif isinstance (value, int) and 'Integer' in rules:
		for rule in rules['Integer']:
			value = datahandling_convert (value, **{**rule, **{'Internal':True}})
	elif isinstance (value, float) and 'Float' in rules:
		for rule in rules['Float']:
			value = datahandling_convert (value, **{**rule, **{'Internal':True}})
	elif value.__class__.__name__ == 'Decimal' and 'Decimal' in rules:
		for rule in rules['Decimal']:
			value = datahandling_convert (value, **{**rule, **{'Internal':True}})
	return value