# Copyright (c) 2025-2026 Erik Persson
# Licensed for free use only. Copying, modification, or redistribution prohibited.

import copy

import sqlalchemy
#import sqlalchemy.orm
import flask
import os
import lzma
import json
import datetime
import math
import statistics
import threading
import time
from cryptography.fernet import Fernet
import uuid
import base36
import bz2
import subprocess
import traceback

global db_query_cache
global_zyd = {
	'Session.id':None,
	'Passwords.key':None,
	'Passwords.data':None,
}

def internal_zyd_post () -> tuple[bool, dict]:
	data = {}
	for key in flask.request.args:
		if key not in data:
			data[key] = flask.request.args.getlist (key)
#		elif data[key] != flask.request.args[key]:
#			print (1)
	for key in flask.request.form:
		if key not in data:
			data[key] = flask.request.form[key]
	if flask.request.get_json (silent=True) is not None:
		for key in flask.request.json:
			if key not in data:
				data[key] = flask.request.json[key]
	for key in data.keys ():
		if isinstance (data[key], list) and len (data[key]) == 1:
			data[key] = data[key][0]
	if len (data) == 0 and 'Post.JSON' in flask.request.files:
		json = flask.request.files['Post.JSON'].read ()
		if len (json) > 0:
			status, json = zyd_json (json, Decode=True)
			if status is True and isinstance (json, dict):
				data = json
#	print ('internal_zyd_post=' + str (data))
	return data


def zyd_ip (**opts: any) -> tuple[bool, any]:
	if 'Detailed' in opts and opts['Detailed'] == True:
		ip = None
		info = None
		if 'HTTP_X_FORWARDED_FOR' in flask.request.environ:
			ip = flask.request.environ['HTTP_X_FORWARDED_FOR']
			info = 'HTTP_X_FORWARDED_FOR'
		elif 'REMOTE_ADDR' in flask.request.environ:
			ip = flask.request.environ['REMOTE_ADDR']
			info = 'REMOTE_ADDR'
		return zyd_return (True, {'IP':ip, 'Info':info}, **opts)
	else:
		ip = (flask.request.environ['HTTP_X_FORWARDED_FOR'] if 'HTTP_X_FORWARDED_FOR' in flask.request.environ else flask.request.environ['REMOTE_ADDR'])
		return zyd_return (True, ip, **opts)


def zyd_db_query (**opts: any) -> tuple[bool, any]:
	# session_key is used to generate unique connections for each HTTP request...
	session_key = internal_zyd_session_key ()
	try:
		global db_query_cache
		if not 'db_query_cache' in globals ():
			db_query_cache = {session_key:{
				'CurrentConnection':None,
				'Engines':{},
				'Connections':{},
			}}
		elif session_key not in db_query_cache:
			db_query_cache[session_key] = {
				'CurrentConnection': None,
				'Engines': {},
				'Connections': {},
			}
	
		if 'DB' in opts or 'Database' in opts:
			db_query_cache[session_key]['CurrentConnection'] = (opts['DB'] if 'DB' in opts else opts['Database'])
			if db_query_cache[session_key]['CurrentConnection'] not in db_query_cache[session_key]['Connections']:
				if 'DB' in opts and 'sqlite' in opts['DB']:
#					auth = opts['DB'].replace ('\\', '\\\\')
					auth = opts['DB'].replace ('\\', '\\\\')
					status = True
				else:
					status, auth = zyd_passwords ('SQL.' + db_query_cache[session_key]['CurrentConnection'])
				if status == True and len (auth) > 10:
					if 'sqlite' in auth:
						db_query_cache[session_key]['Engines'][db_query_cache[session_key]['CurrentConnection']] = sqlalchemy.create_engine (auth, echo=False, isolation_level="AUTOCOMMIT", poolclass=sqlalchemy.NullPool, connect_args={"check_same_thread": False})
					else:
						db_query_cache[session_key]['Engines'][db_query_cache[session_key]['CurrentConnection']] = sqlalchemy.create_engine (auth, echo=False, isolation_level="AUTOCOMMIT", poolclass=sqlalchemy.NullPool)
					db_query_cache[session_key]['Connections'][db_query_cache[session_key]['CurrentConnection']] = db_query_cache[session_key]['Engines'][db_query_cache[session_key]['CurrentConnection']].connect ()
				else:
					return False, {'Status':'ERROR', 'Title':'Common.zyd_db_query: Aborted', 'Message':'No DB auth string found for opts=' + str (opts)}
		elif 'InternalDB' in opts and opts['InternalDB'] is True:
			db_query_cache[session_key]['CurrentConnection'] = 'Internal'
			if db_query_cache[session_key]['CurrentConnection'] not in db_query_cache[session_key]['Engines']:
				db_query_cache[session_key]['Engines'][db_query_cache[session_key]['CurrentConnection']] = sqlalchemy.create_engine ("sqlite://", echo=False, isolation_level="AUTOCOMMIT", poolclass=sqlalchemy.NullPool, connect_args={"check_same_thread": False})
				db_query_cache[session_key]['Connections'][db_query_cache[session_key]['CurrentConnection']] = db_query_cache[session_key]['Engines'][db_query_cache[session_key]['CurrentConnection']].connect ()

		if 'Query' in opts:
	#		print (opts['Query'])
			db_query_cache[session_key]['CurrentResult'] = db_query_cache[session_key]['Connections'][db_query_cache[session_key]['CurrentConnection']].execute (sqlalchemy.text (opts['Query']))
			return True, db_query_cache[session_key]['CurrentResult']
		
		# Terminates all DB connections...
		if 'CloseAll' in opts and opts['CloseAll'] == True:
			for key in list (db_query_cache[session_key]['Connections'].keys ()):
				db_query_cache[session_key]['Connections'][key].close ()
				del (db_query_cache[session_key]['Connections'][key])
			for key in list (db_query_cache[session_key]['Engines'].keys ()):
				db_query_cache[session_key]['Engines'][key].dispose ()
				del (db_query_cache[session_key]['Engines'][key])
			if session_key in db_query_cache:
				del (db_query_cache[session_key])
			return True, {'Status':'OK'}
		
		return False, {'Status':'ERROR', 'Title':'Common.DB_Query: Unknown error', 'Message':'Unknown error encountered\nOpts=' + str (opts)}
	except Exception as e:
		if '(sqlite3.IntegrityError) UNIQUE constraint failed' in str (e):
			return False, {'Status':'ERROR', 'Title':'Common.DB_Query: INSERT error', 'Message':'Insert error:' + str (e), 'Error':str (e)}
		elif '(sqlite3.OperationalError)' in str (e):
			return False, {'Status':'ERROR', 'Title':'Common.DB_Query: SQLite error', 'Message':'SQLite error:' + str (e), 'Error':str (e)}

		time.sleep (0.2 * (opts['Crashed'] + 1 if 'Crashed' in opts else 1))
		print ('CRASH::zyd_db_query (' + str ((opts['Crashed'] + 1 if 'Crashed' in opts else 1)) + ')')
		if (opts['Crashed'] + 1 if 'Crashed' in opts else 1) > 2:
			print (opts)
			return False, {'Status':'CRASH', 'Title':'', 'Message':'Error=' + str (e) + '\n' + str (opts)}
		return zyd_db_query (**{**opts, 'Crashed':(opts['Crashed'] + 1 if 'Crashed' in opts else 1)})
		
	
def zyd_db_fetch (db_result, **opts: any) -> tuple[bool, any]:
	try:
		if 'OnlyClose' in opts and opts['OnlyClose'] is True:
			db_result.close ()
			return True, None
		elif 'Rows' in opts and opts['Rows'] == True:
			data = db_result.rowcount
		elif 'ID' in opts and opts['ID'] == True:
			data = db_result.lastrowid
		elif 'All' in opts and opts['All'] == True:
			data = db_result.mappings ().all ()
		else:
			data = db_result.mappings ().fetchone ()
		
		if 'Close' in opts and opts['Close'] == True:
			db_result.close ()
		if 'ToListDict' in opts and opts['ToListDict'] is True:
			data = [dict (row) for row in data]
		return zyd_return (True, data, **opts)
	except:
		time.sleep (0.2 * (opts['Crashed'] + 1 if 'Crashed' in opts else 1))
		print ('CRASH::zyd_db_fetch (' + str ((opts['Crashed'] + 1 if 'Crashed' in opts else 1)) + ')')
		if (opts['Crashed'] + 1 if 'Crashed' in opts else 1) > 20:
			return zyd_return (False, {}, **opts)
		return zyd_db_fetch (**{**opts, 'Crashed':(opts['Crashed'] + 1 if 'Crashed' in opts else 1)})


def internal_zyd_db_value (value, **opts) -> str:
	if (('ArrayToIN' in opts and opts['ArrayToIN'] is True) or ('ArrayToRegExp' in opts and opts['ArrayToRegExp'] is True)) and isinstance (value, (list, dict)):
		values = []
		for v in value:
			if isinstance (v, (int, float)) or ('ArrayToRegExp' in opts and opts['ArrayToRegExp'] is True):
				values.append (str (v))
			else:
				values.append (internal_zyd_db_value (v))
		if 'ArrayToIN' in opts and opts['ArrayToIN'] is True:
			return "(" + ",".join (values) + ")"
		return "'" + "|".join (values) + "'"
	elif (('IfNumeric' in opts and opts['IfNumeric'] is True) or ('Numeric' in opts and opts['Numeric'] is True)) and isinstance (value, (int, float)):
		return str (value)
	if 'NULL' in opts and opts['NULL'] is True and value is None:
		return "NULL"
	if 'Binary' in opts and opts['Binary'] == True and isinstance (value, bytes):
		return "UNHEX('" + value.hex () + "')"
	return "'" + str (value).replace ("'", "\\'") + "'"


def internal_zyd_ceil (value: int|float, **opts) -> int|float:
	if 'Decimals' not in opts or opts['Decimals'] == 0:
		return math.ceil (value)
	elif opts['Decimals'] > 0:
		return math.ceil (value * pow (10, opts['Decimals'])) / pow (10, opts['Decimals'])


def internal_zyd_floor (value: int|float, **opts) -> int|float:
	if 'Decimals' not in opts or opts['Decimals'] == 0:
		return math.floor (value)
	elif opts['Decimals'] > 0:
		return math.floor (value * pow (10, opts['Decimals'])) / pow (10, opts['Decimals'])


def internal_zyd_date (**opts) -> any:
	if 'Time' in opts and (isinstance (opts['Time'], (int, float)) or opts['Time'].__class__.__name__ == 'Decimal'):
		dt = datetime.datetime.fromtimestamp (int (opts['Time']))
	else:
		dt = datetime.datetime.now ()
		if 'Time' in opts and isinstance (opts['Time'], str) and opts['Time'][0] in ['-', '+']:
			if opts['Time'][0] == '-':
				dt = dt - datetime.timedelta (seconds=int (opts['Time'][1:]))
			elif opts['Time'][0] == '+':
				dt = dt + datetime.timedelta (seconds=int (opts['Time'][1:]))
	
	
	if 'Format' in opts:
		if opts['Format'] == 'ISO':
			format = '%Y-%m-%d'
		elif opts['Format'] == 'DateTime':
			format = '%Y-%m-%d %H:%M:%S'
		else:
			format = opts['Format']
	else:
		format = '%Y-%m-%d %H:%M:%S'
	
	return dt.strftime (format)
		

def internal_zyd_uniqueid (**opts) -> str:
	if 'UUID' not in opts:
		uid = str (uuid.uuid4 ())
	else:
		uid = str (opts['UUID'])
	
	if 'Base' in opts:
		return str (base36.dumps (int (uid.replace ('-', ''), int (opts['Base']))))
	return uid


def internal_zyd_ucfirst (**opts) -> str:
	value = copy.deepcopy (opts['Value'])
	if 'Trim' in opts and opts['Trim'] is True:
		value = value.strip ()
	value = value.capitalize ()
	for char in (opts['TriggerChars'] if 'TriggerChars' in opts and isinstance (opts['TriggerChars'], list) else [' ']):
		if char in value:
			for i in range (1, len (value)):
				if value[i - 1] == char:
					value = value[:i] + value[i].capitalize () + value[i + 1:]
	return value
	

def internal_zyd_stacktrace (error, **opts):
	content = []
	content.append ('OPTS=' + str (opts))
	content.append ('ERROR=' + str (error))
	content.append ('TRACEBACK.STRING=' + str (traceback.format_exc ()))
	return '\n'.join (content)


def internal_zyd_arrayreplace (**opts) -> any:
	if 'Value' in opts and 'ReplaceArray' in opts and isinstance (opts['Value'], str) and isinstance (opts['ReplaceArray'], dict):
		value = copy.deepcopy (opts['Value'])
		for key in opts['ReplaceArray'].keys ():
			if value == key:
				value = opts['ReplaceArray'][key]
#			elif isinstance (value, str) and isinstance (opts['ReplaceArray'][key], str):
			elif isinstance (value, str):
				value = value.replace (key, str (opts['ReplaceArray'][key]))
		return value
	elif 'Array' in opts and 'ReplaceArray' in opts and isinstance (opts['Array'], (list, dict)) and isinstance (opts['ReplaceArray'], dict):
		value = copy.deepcopy (opts['Array'])
		for key in (value.keys () if isinstance (value, dict) else range (0, len (value))):
			if isinstance (value[key], (list, dict)):
				value[key] = internal_zyd_arrayreplace (Array=value[key], ReplaceArray=opts['ReplaceArray'])
			elif isinstance (value[key], str):
				value[key] = internal_zyd_arrayreplace (Value=value[key], ReplaceArray=opts['ReplaceArray'])
		return value


def internal_zyd_session_key () -> str:
	return (str (flask.request.environ['werkzeug.socket']) if flask.request else None)


def internal_zyd_time (**opts) -> float:
	time = datetime.datetime.now ().timestamp ()
	if 'Decimals' in opts and isinstance (opts['Decimals'], int):
		return (int (time) if opts['Decimals'] == 0 else math.ceil (time * pow (10, opts['Decimals'])) / pow (10, opts['Decimals']))
	return time


#	def ZydDateTime(Time=None, Format='%Y-%m-%d %H:%M:%S'):
#		if Time == None:
#			#		return (datetime.datetime.now ())
#			return (datetime.datetime.strptime(ZydDate('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))
#		return (datetime.datetime.strptime(Time, Format))


def zyd_json (data, **opts) -> tuple[bool, any]:
	encode = (True if 'Decode' not in opts or opts['Decode'] != True else False)
	compressed = (False if 'Compressed' not in opts or opts['Compressed'] != True else True)
	try:
		if encode:
			return zyd_return (True, (json.dumps (data) if not compressed else lzma.compress (json.dumps (data).encode ('utf-8'), preset=9)), **opts)
		else:
			return zyd_return (True, (json.loads (data) if not compressed else json.loads (lzma.decompress (data))), **opts)
	except Exception as e:
		return zyd_return (False, {'Status':'CRASH', 'Title':'Common.zyd_json: Crashed', 'Message':'JSON crashed with the following error: ' + str (e)})


def zyd_passwords (key, **opts: any) -> tuple[bool, any]:
	global global_zyd
	filepath = '/home/Zydox/'
	if not os.path.exists (filepath):
		if os.path.exists ('O:\\'):
			filepath = 'O:\\'
		else:
			return False, {'Status':'ERROR', 'Title':'Common.zyd_passwords: Aborted', 'Message':'No filepath found.'}
	key_file = filepath + 'Passwords.key'
	file = filepath + 'Passwords.dat'
	if 'File' in opts and opts['File'] == True:
		return file
	if 'Passwords.key' not in global_zyd or global_zyd['Passwords.key'] == None:
		if 'Debug' in opts and opts['Debug'] == True:
			print ('Common.zyd_passwords::READ_KEY=' + str (key_file))
		if not os.path.exists (key_file):
			print ('Common.zyd_passwords::READ_KEY_MISSING=' + str (key_file))
			return False, {'Status':'ERROR', 'Title':'Common.zyd_passwords: Aborted', 'Message':'No key file found.'}
		global_zyd['Passwords.key'] = open (key_file, 'rb').read ()
	
	if 'Passwords.data' not in global_zyd or global_zyd['Passwords.data'] == None:
		if os.path.exists (file):
			if 'Debug' in opts and opts['Debug'] == True:
				print ('Common.zyd_passwords::READ_FILE=' + str (file))
			fp = open (file, 'rb')
			global_zyd['Passwords.data'] = fp.read ()
			fp.close ()
		else:
			return False, {'Status':'ERROR', 'Title':'Common.zyd_passwords: Aborted', 'Message':'No data file found.'}
	if len (global_zyd['Passwords.data']) == 0:
		data = {}
	else:
		decrypt = Fernet (global_zyd['Passwords.key'])
		status, data = zyd_json (decrypt.decrypt (global_zyd['Passwords.data']), Decode=True, Compressed=True)
		
	if 'Write' in opts and opts['Write'] == True:
		if 'Debug' in opts and opts['Debug'] == True:
			print('Common.zyd_passwords::WRITE_FILE=' + str (file))
		encrypt = Fernet (global_zyd['Passwords.key'])
		if 'Delete' in opts and opts['Delete'] == True:
			if key in data:
				del (data[key])
			else:
				return False, {'Status':'ERROR', 'Title':'Common.zyd_passwords: Aborted', 'Message':'The key "' + str (key) + '" wasn\'t found and can\'t be deleted.'}
		else:
			data[key] = opts['Value']
		
		fp = open (file, 'wb')
		status, json = zyd_json (data, Compressed=True)
		global_zyd['Passwords.data'] = encrypt.encrypt (json)
		fp.write (global_zyd['Passwords.data'])
		fp.close ()
		return True, {'Status':'OK'}
	if 'Keys' in opts and opts['Keys'] == True:
		return True, list (data.keys ())
	if key in data:
		return True, data[key]
	return False, {'Status':'ERROR', 'Title':'Common.zyd_passwords: Aborted', 'Message':'The key "' + str (key) + '" wasn\'t found.'}
	
	
def zyd_tempstorage (**opts:any) -> tuple[bool, any]:
	db = (opts['DB'] if 'DB' in opts and isinstance (opts['DB'], str) else 'Omoikane')
	if 'System' in opts and isinstance (opts['System'], str):
		system = opts['System']
	else:
		return False, {'Status':'WARNING', 'SubStatus':'NOT_OK', 'Title':'', 'Message':''}
	if 'Process' in opts and isinstance (opts['Process'], str):
		process = opts['Process']
	else:
		return False, {'Status':'WARNING', 'SubStatus':'NOT_OK', 'Title':'', 'Message':''}
	if 'Key' in opts and isinstance (opts['Key'], (str, int, float)):
		key = str (opts['Key'])
	else:
		key = 'None'
		
	
	if 'Data' in opts and isinstance (opts['Data'], (str, dict, list, bytes)):
		query = "REPLACE INTO Common_TempData SET System=" + internal_zyd_db_value (system) + ", SystemProcess=" + internal_zyd_db_value (process) + ", SystemKey=" + internal_zyd_db_value (key) + ", CreateDatetime=NOW()"
		if 'TTL' in opts and isinstance (opts['TTL'], int):
			query += ", TTL_Hours=" + internal_zyd_db_value (opts['TTL'])
		if 'UserID' in opts and isinstance (opts['UserID'], int):
			query += ", CreateUserID=" + internal_zyd_db_value (opts['UserID'])
		
		if isinstance (opts['Data'], str):
			data = bz2.compress (str.encode (opts['Data']), compresslevel=9)
			query += ", DataSize=" + internal_zyd_db_value (len (opts['Data'])) + ", DataFormat='String'"
			if len (data) >= len (str.encode (opts['Data'])):
				data = str.encode (opts['Data'])
			else:
				query += ", DataCompressedSize=" + internal_zyd_db_value (len (data))
		elif isinstance (opts['Data'], (dict, list)):
			status, datajson = zyd_json (opts['Data'])
			if status is not True:
				return False, datajson
			query += ", DataSize=" + internal_zyd_db_value (len (datajson)) + ", DataFormat='Array'"
			data = bz2.compress (str.encode (datajson), compresslevel=9)
			if len (data) >= len (str.encode (datajson)):
				data = str.encode (datajson)
			else:
				query += ", DataCompressedSize=" + internal_zyd_db_value (len (data))
		else:
			data = bz2.compress (opts['Data'], compresslevel=9)
			query += ", DataSize=" + internal_zyd_db_value (len (opts['Data'])) + ", DataFormat='Bytes'"
			if len (data) >= len (opts['Data']):
				data = opts['Data']
			else:
				query += ", DataCompressedSize=" + internal_zyd_db_value (len (data))
		
		query += ", Data=" + internal_zyd_db_value (data, Binary=True)
#		print (query)
		s, r = zyd_db_query (Query=query, DB=db)
		if s is True:
			zyd_db_fetch (r, OnlyClose=True)
#		print (s)
#		print (r)
		return True, True
	else:
		status, db_result = zyd_db_query (Query="SELECT * FROM Common_TempData WHERE System=" + internal_zyd_db_value (system) + " AND SystemProcess=" + internal_zyd_db_value (process) + " AND SystemKey=" + internal_zyd_db_value (key), DB=db)
		status, result = zyd_db_fetch (db_result, Close=True)
		if status == True and result is not None:
			if 'DataCompressedSize' in result and result['DataCompressedSize'] is not None:
				data = bz2.decompress (result['Data'])
			else:
				data = result['Data']
			
			if 'DataFormat' in result:
				if result['DataFormat'] == 'String':
					data = data.decode ()
				elif result['DataFormat'] == 'Array':
					status, data = zyd_json (data, Decode=True)
					if status is False:
						return False, data
			return True, data
		elif result is None:
			return False, {'Status':'WARNING', 'SubStatus':'EMPTY', 'Title':'Aborted: No data found', 'Message':''}
		else:
			return False, {'Status':'WARNING', 'SubStatus':'NOT_OK', 'Title':'', 'Message':''}


def zyd_download (**opts:any) -> tuple[bool, any]:
	method = 'powershell'
	if 'URL' in opts and isinstance (opts['URL'], str) and ('http://' in opts['URL'] or 'https://' in opts['URL']):
		url = opts['URL']
	else:
		return False, {'Status':'WARNING', 'Title':'', 'Message':''}
	
	binary = (True if 'Binary' in opts and opts['Binary'] == True else False)
	try:
		if method == 'powershell':
			tempfile = '\\\\192.168.1.15/Shared_Temp/' + str (uuid.uuid4 ())
			subprocess.run (["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", f"Invoke-WebRequest -Uri '{opts['URL']}' -OutFile '{tempfile}' -MaximumRedirection 10"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
			with open (tempfile, ('rb' if binary == True else 'r')) as File:
				data = File.read ()
			os.remove (tempfile)
			return True, data
	except Exception as error:
		print ('zyd_download_CRASHED::' + str (url) + '::' + str (error))
		return False, {'Status':'ERROR', 'Title':'', 'Message':''}


def zyd_return (status, result, **opts):
	if 'Internal' in opts and opts['Internal'] is True:
		return result
	elif 'InternalData' in opts and opts['InternalData'] is True and isinstance (result, dict) and 'Data' in result:
		return result['Data']
	return status, result


def zyd_print (value=None, **opts):
	global global_zyd_print
	if not 'global_zyd_print' in globals ():
		global_zyd_print = {}
	id = zyd_flask_requestid (Internal=True)
	if id not in global_zyd_print:
		global_zyd_print[id] = {'Time':internal_zyd_time (), 'Data':[]}
	
	if 'Return' in opts and opts['Return'] is True:
		data = '\n'.join (global_zyd_print[id]['Data'])
		del (global_zyd_print[id])
		return data
	elif 'Reset' in opts and opts['Reset'] is True:
		global_zyd_print[id] = {'Time':internal_zyd_time (), 'Data':[]}
	else:
		global_zyd_print[id]['Time'] = internal_zyd_time ()
		global_zyd_print[id]['Data'].append (str (value))


def internal_zyd_shorten (input_text, **opts):
	text = copy.deepcopy (input_text)
	if 'Length' in opts and isinstance (opts['Length'], int) and isinstance (text, str) and len (text) > opts['Length']:
		text = text[:opts['Length']] + (opts['Sufix'] if 'Sufix' in opts and isinstance (opts['Sufix'], str) else '')
	return text


def zyd_flask_requestid (**opts):
	return zyd_return (True, (flask.request.environ.get ('REQUEST_ID', '') if flask.has_request_context () is True else None), **opts)


def zyd_calc (calculation, **opts):
	calc = copy.deepcopy (calculation)
	for value in ['int', 'float', 'round', 'abs', 'min', 'max', 'math.ceil', 'math.floor', 'statistics.median', '([', '])', '(', ')', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '/', '*', ',', '.', '%', ' ']:
		calc = calc.replace (value, '')
	if len (calc) == 0:
		try:
			value = eval (calculation)
		except:
			return zyd_return (False, {'Status':'CRASH', 'Title':'zyd_calc: Crashed', 'Message':'Calculation for "' + str (calculation) + '" ("' + str (calc) + '") crashed.'}, **opts)
	else:
		return zyd_return (False, {'Status':'WARNING', 'Title':'zyd_calc: Aborted', 'Message':'The Calculation "' + str (calculation) + '" contained these invalid characters "' + str (calc) + '".'}, **opts)
	return zyd_return (True, value, **opts)


def internal_zyd_crashreport (**opts) -> bool:
	try:
		print ('CRASH=' + str (opts))
	except:
		print (opts)
	return True