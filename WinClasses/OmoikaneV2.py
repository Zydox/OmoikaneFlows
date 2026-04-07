# Copyright (c) 2025-2026 Erik Persson
# Licensed for free use only. Copying, modification, or redistribution prohibited.

# -*- coding: utf-8 -*-
import builtins
from Functions.Common import *
from Functions.DataHandling import *
for name in dir ():
    if not name.startswith ("_"):
        builtins.__dict__[name] = globals ()[name]
import tempfile
builtins.tempfile = tempfile
import hashlib
builtins.hashlib = hashlib

class OmoikaneV2:
	def __init__ (self, cls_steps = None):
		self.objects = {
			'SAP':{},
		}
		self.cls_steps = cls_steps
	
	
	def dynamic_function (self, function, to_class = True):
		if to_class is True:
			func = {}
			exec (function['Code'], func)
			setattr (OmoikaneV2, function['Function'], func[function['Function']])
		else:
			exec (function['Code'], globals ())
			builtins.__dict__[function['Function']] = globals ()[function['Function']]
	
	
	def execute (self, isolation = None, **opts):
		try:
			if opts['Function'] == 'OMOIKANEV2:SAP_Process.Transform':
				return self.step_sap_process_transform (isolation, **opts)
			elif opts['Function'] == 'OMOIKANEV2:SAP_Process.List':
				return self.step_sap_process_list (isolation, **opts)
			elif opts['Function'] == 'OMOIKANEV2:LoadToDB.Upload':
				return self.step_loadtodb_upload (isolation, **opts)
			elif opts['Function'] == 'OMOIKANEV2:DatabaseQuery':
				return self.step_databasequery (isolation, **opts)
			elif opts['Function'] == 'OMOIKANEV2:TimeCapture.Upload':
				return self.step_timecapture_upload (isolation, **opts)
			return False, {'Status':'WARNING', 'Title':'', 'Message':'Unknown step=' + str (opts)}
		except Exception as e:
			st = internal_zyd_stacktrace (e, FunctionOpts=opts)
			return False, {'Status':'CRASH', 'Title':'OMOIKANEV2:execute: Crashed', 'Message':'Crashed with the error: ' + str (e) + ' for step:\n' + str (opts), 'StackTrace':st}

	
	def step_sap_process_list (self, isolation, **opts):
		if 'OmoikaneV2.URL' not in opts or not isinstance (opts['OmoikaneV2.URL'], str):
			return False, {'Status':'WARNING', 'Title':'OMOIKANEV2:step_sap_process_list: Aborted', 'Message':'No OmoikaneV2.URL provided.'}
		if 'Format' not in opts or not isinstance (opts['Format'], str):
			return False, {'Status':'WARNING', 'Title':'OMOIKANEV2:step_sap_process_list: Aborted', 'Message':'No Format provided.'}
		if 'Systems' not in opts or not isinstance (opts['Systems'], dict):
			return False, {'Status':'WARNING', 'Title':'OMOIKANEV2:step_sap_process_list: Aborted', 'Message':'No Systems provided.'}
		
		result_web = self.cls_steps.cls_web.internal_web ('https://' + opts['OmoikaneV2.URL'] + '.emea.tdworldwide.com/?API.OmoikaneSAP&Action=ProcessesList', **{
			'Auth':True,
			'Verify':(False if 'OmoikaneV2.URL.Verify' in opts and opts['OmoikaneV2.URL.Verify'] is False else True),
			'Verify.DisableWarnings':(True if 'OmoikaneV2.URL.Verify' in opts and opts['OmoikaneV2.URL.Verify'] is False else False),
			'JSON':True,
		})
		if not isinstance (result_web, (dict, list)):
			return False, {'Status':'ERROR', 'Title':'OMOIKANEV2:step_sap_process_list: Aborted', 'Message':'Unknown web reply:' + str (result_web)}

		if opts['Format'] == '{%ID%{%TITLE%,%SYSTEM%}}':
			data = {}
			for entry in result_web:
				if len (entry['Systems']) != 1:
					return False, {'Status':'WARNING', 'Title':'OMOIKANEV2:step_sap_process_list: Aborted', 'Message':'Process ID "' + str (entry['ID']) + '" doesm\'t have a single system "' + str (entry['Systems']) + '" which doesn\'t work with the Format "{%ID%{%TITLE%,%SYSTEM%}}".'}
				if entry['Systems'][0] not in opts['Systems']:
					return False, {'Status':'WARNING', 'Title':'OMOIKANEV2:step_sap_process_list: Aborted', 'Message':'Process ID "' + str (entry['ID']) + '" with System "' + str (entry['Systems'][0]) + '" is not provided in the Systems option.'}
				data[entry['ID']] = {'Title':entry['Title'], 'System':opts['Systems'][entry['Systems'][0]]}
		else:
			return False, {'Status':'WARNING', 'Title':'OMOIKANEV2:step_sap_process_list: Aborted', 'Message':'Unknown Format "' + str (opts['Format']) + '".'}
		
		
		if 'ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str):
			self.cls_steps.internal_value_set_value (isolation, 'Variable', data, opts['ReturnVariable'])
		if 'ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str):
			self.cls_steps.internal_value_set_value (None, 'Variable', data, opts['ReturnVariable.Global'])
		
		return True, {'Status':'OK', 'Data':data}
	
	
	def step_timecapture_upload (self, isolation, **opts):
		if 'File' not in opts or not isinstance (opts['File'], str):
			return False, {'Status':'WARNING', 'Title':'OMOIKANEV2:step_timecapture_upload: Aborted', 'Message':'No File provided.'}
		elif not os.path.exists (opts['File']):
			return False, {'Status':'WARNING', 'Title':'OMOIKANEV2:step_timecapture_upload: Aborted', 'Message':'The file "' + str (opts['File']) + '" does not exist.'}
		if 'Template' not in opts or not isinstance (opts['Template'], str):
			return False, {'Status':'WARNING', 'Title':'OMOIKANEV2:step_timecapture_upload: Aborted', 'Message':'No Template provided.'}
		if 'OmoikaneV2.URL' not in opts or not isinstance (opts['OmoikaneV2.URL'], str):
			return False, {'Status':'WARNING', 'Title':'OMOIKANEV2:step_timecapture_upload: Aborted', 'Message':'No OmoikaneV2.URL provided.'}
		
		
		with open (opts['File'], "rb") as fp:
			file = fp.read ()
		url = 'https://' + opts['OmoikaneV2.URL'] + '.emea.tdworldwide.com/?API.TimeCapture&Action=Upload&Template=' + opts['Template'] + ('&Debug=1' if 'OmoikaneV2.Debug' in opts and opts['OmoikaneV2.Debug'] is True else '') + ('&Debug.Database=1' if 'OmoikaneV2.Debug.Database' in opts and opts['OmoikaneV2.Debug.Database'] is True else '') + '&File.filename=' + os.path.basename (opts['File'])
		result_web = self.cls_steps.cls_web.internal_web (url, **{
			'Auth':True,
			'Method':'PUT',
			'JSON':(opts['OmoikaneV2.JSON'] if 'OmoikaneV2.JSON' in opts and isinstance (opts['OmoikaneV2.JSON'], bool) else True),
			'Verify':(False if 'OmoikaneV2.URL.Verify' in opts and opts['OmoikaneV2.URL.Verify'] is False else True),
			'Verify.DisableWarnings':(True if 'OmoikaneV2.URL.Verify' in opts and opts['OmoikaneV2.URL.Verify'] is False else False),
			'JSON':True,
			'Files':{'File':file},
		})
		if not isinstance (result_web, (dict, list)):
			return False, {'Status':'WARNING', 'Title':'OMOIKANEV2:step_timecapture_upload: Warning', 'Message':'Web post failed with the following error:' + str (result_web)}
		
		if isinstance (result_web, dict) and 'Status' in result_web and 'Message' in result_web:
			if 'ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str):
				self.cls_steps.internal_value_set_value (isolation, 'Variable', result_web['Message'], opts['ReturnVariable'])
			if 'ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str):
				self.cls_steps.internal_value_set_value (isolation, 'Variable', result_web['Message'], opts['ReturnVariable.Global'])
		if isinstance (result_web, dict) and 'Status' in result_web and result_web['Status'] == 'OK' and 'Message' in result_web:
			return True, {'Status':'OK', 'Message':result_web['Message']}
		if isinstance (result_web, dict) and 'Status' in result_web and result_web['Status'] != 'OK' and 'Message' in result_web:
			return False, {'Status':'WARNING', 'Title':'OMOIKANEV2:step_timecapture_upload: Warning', 'Message':'OmoikaneV2 failed with the status "' + str (result_web['Status']) + '" and the Message:\n' + str (result_web['Message'])}
		return False, {'Status':'ERROR', 'Title':'OMOIKANEV2:step_timecapture_upload: Error', 'Message':'Unknown error, Steps result=\n' + str (status) + '::' + str (result) + '\nOmoikaneV2 result=\n' + str (result_web)}
	
	
	def step_databasequery (self, isolation, **opts):
		if 'Query' not in opts or not isinstance (opts['Query'], str):
			return False, {'Status':'WARNING', 'Title':'OMOIKANEV2:step_databasequery: Aborted', 'Message':'No Query provided.'}
		if 'OmoikaneV2.URL' not in opts or not isinstance (opts['OmoikaneV2.URL'], str):
			return False, {'Status':'WARNING', 'Title':'OMOIKANEV2:step_databasequery: Aborted', 'Message':'No OmoikaneV2.URL provided.'}
		result_web = self.cls_steps.cls_web.internal_web ('https://' + opts['OmoikaneV2.URL'] + '.emea.tdworldwide.com/?API.DatabaseQuery', **{
			'Auth':True,
			'Method':'POST',
			'JSON':(opts['OmoikaneV2.JSON'] if 'OmoikaneV2.JSON' in opts and isinstance (opts['OmoikaneV2.JSON'], bool) else True),
			'Verify':(False if 'OmoikaneV2.URL.Verify' in opts and opts['OmoikaneV2.URL.Verify'] is False else True),
			'Verify.DisableWarnings':(True if 'OmoikaneV2.URL.Verify' in opts and opts['OmoikaneV2.URL.Verify'] is False else False),
			'JSON':True,
			'Data':{'Query':opts['Query']},
		})
		if not isinstance (result_web, (dict, list)):
			return False, {'Status':'WARNING', 'Title':'OMOIKANEV2:step_databasequery: Aborted', 'Message':'No valid result provided by OmoikaneV2:\n' + str (result_web)}

		if isinstance (result_web, dict) and 'Status' in result_web and result_web['Status'] == 'OK' and 'Headers' in result_web and 'Data' in result_web:
			if 'SQLite.Table' in opts and isinstance (opts['SQLite.Table'], str):
				status, result = self.cls_steps.execute_steps ([
					{
						'Function':'SQL:Table.DataColumnDetermination',
						'Data':result_web['Data'],
						'Columns':result_web['Headers'],
						'ReturnVariable':'INTERNAL:SQL:TableColumns',
					},
					{
						'Function':'SQL:Table.Create',
						'Table':opts['SQLite.Table'],
						'Columns':'<$INTERNAL:SQL:TableColumns$>',
						'Create.IfNotExists':True
					},
					{
						'Function':'SQL:Table.Insert',
						'Table':opts['SQLite.Table'],
						'Columns':result_web['Headers'],
						'Values':result_web['Data']
					}
				], temp_isolation)
				if status is not True:
					return status, result
				result_sql = self.cls_steps.internal_value_get_value (temp_isolation, 'Variable', 'INTERNAL:SQL:TableColumns')
			if 'Return.1D' in opts and isinstance (opts['Return.1D'], dict):
				if len (result_web['Data']) == 1:
					for field in opts['Return.1D'].keys ():
						if field not in result_web['Headers']:
							return False, {'Status':'WARNING', 'Title':'OMOIKANEV2:step_databasequery: Aborted', 'Message':'Return.1D logic used, but the field "' + str (field) + '" is not in the result.'}
					for field in opts['Return.1D'].keys ():
						value = result_web['Data'][0][result_web['Headers'].index (field)]
						if 'ReturnVariable' in opts['Return.1D'][field] and isinstance (opts['Return.1D'][field]['ReturnVariable'], str):
							self.cls_steps.internal_value_set_value (isolation, 'Variable', value, opts['Return.1D'][field]['ReturnVariable'])
						if 'ReturnVariable.Global' in opts['Return.1D'][field] and isinstance (opts['Return.1D'][field]['ReturnVariable.Global'], str):
							self.cls_steps.internal_value_set_value (None, 'Variable', value, opts['Return.1D'][field]['ReturnVariable.Global'])
						if 'UpdateGUI.Value' in opts['Return.1D'][field] and isinstance (opts['Return.1D'][field]['UpdateGUI.Value'], str):
							self.cls_steps.cls_gui.internal_object_update (isolation, opts['Return.1D'][field]['UpdateGUI.Value'], Value=value, Trigger=(True if 'UpdateGUI.Value.Trigger' in opts['Return.1D'][field] and opts['Return.1D'][field]['UpdateGUI.Value.Trigger'] is True else False))
				else:
					return False, {'Status':'WARNING', 'Title':'OMOIKANEV2:step_databasequery: Aborted', 'Message':'Return.1D logic used, but returned result was ' + str (len (len (result_web['Data']))) + ' rows (required to be 1).'}
			
			if 'ReturnVariable.Data' in opts and isinstance (opts['ReturnVariable.Data'], str):
				self.cls_steps.internal_value_set_value (isolation, 'Variable', result_web['Data'], opts['ReturnVariable.Data'])
			if 'ReturnVariable.Data.Global' in opts and isinstance (opts['ReturnVariable.Data.Global'], str):
				self.cls_steps.internal_value_set_value (None, 'Variable', result_web['Data'], opts['ReturnVariable.Data.Global'])
			if 'ReturnVariable.Headers' in opts and isinstance (opts['ReturnVariable.Headers'], str):
				self.cls_steps.internal_value_set_value (isolation, 'Variable', result_web['Headers'], opts['ReturnVariable.Data'])
			if 'ReturnVariable.Headers.Global' in opts and isinstance (opts['ReturnVariable.Headers.Global'], str):
				self.cls_steps.internal_value_set_value (None, 'Variable', result_web['Headers'], opts['ReturnVariable.Data.Global'])
			if ('ReturnVariable.1D' in opts and opts['ReturnVariable.1D'] is True) or ('ReturnVariable.1D.Global' in opts and opts['ReturnVariable.1D.Global'] is True):
				if len (result_web['Data']) == 1:
					for field in result_web['Headers']:
						value = result_web['Data'][0][result_web['Headers'].index (field)]
						if 'ReturnVariable.1D' in opts and opts['ReturnVariable.1D'] is True and isinstance (field, str):
							self.cls_steps.internal_value_set_value (isolation, 'Variable', value, field)
						if 'ReturnVariable.1D.Global' in opts and opts['ReturnVariable.1D.Global'] is True and isinstance (field, str):
							self.cls_steps.internal_value_set_value (None, 'Variable', value, field)
		else:
			return status, result
		return True, {'Status':'OK'}
		
	
	def step_loadtodb_upload (self, isolation, **opts):
		if 'File' not in opts:
			return False, {'Status':'WARNING', 'Title':'OMOIKANEV2:step_loadtodb_upload: Aborted', 'Message':'No File provided.'}
		elif not os.path.exists (opts['File']):
			return False, {'Status':'WARNING', 'Title':'OMOIKANEV2:step_loadtodb_upload: Aborted', 'Message':'The file "' + str (opts['File']) + '" does not exist.'}
		if 'OmoikaneV2.URL' not in opts or not isinstance (opts['OmoikaneV2.URL'], str):
			return False, {'Status':'WARNING', 'Title':'OMOIKANEV2:step_loadtodb_upload: Aborted', 'Message':'No OmoikaneV2.URL provided.'}
		
		url = 'https://' + opts['OmoikaneV2.URL'] + '.emea.tdworldwide.com/' + opts['Page']
		
		md5 = hashlib.md5 ()
		with open (opts['File'], "rb") as fp:
			file = fp.read ()
			md5.update (file)
		url+= '&FileMD5=' + md5.hexdigest ()
		
		if 'Compression' in opts and isinstance (opts['Compression'], str):
			compression = opts['Compression'].split (':')
			if compression[0] == 'LZMA':
				url += '&FileComp=LZMA'
				file = lzma.compress (file, preset=int (compression[1]))
		result_web = self.cls_steps.cls_web.internal_web (url, **{
			'Auth':True,
			'Method':'PUT',
			'Verify':(False if 'OmoikaneV2.URL.Verify' in opts and opts['OmoikaneV2.URL.Verify'] is False else True),
			'Verify.DisableWarnings':(True if 'OmoikaneV2.URL.Verify' in opts and opts['OmoikaneV2.URL.Verify'] is False else False),
			'JSON':True,
			'Files':{'File':file},
		})
		if isinstance (result_web, dict) and 'Status' in result_web and 'Status' in result_web and 'Message' in result_web:
			if 'ReturnVariable.Status' in opts and isinstance (opts['ReturnVariable.Status'], str):
				self.cls_steps.internal_value_set_value (isolation, 'Variable', str (result_web['Status']), opts['ReturnVariable.Status'])
			if 'ReturnVariable.Status.Global' in opts and isinstance (opts['ReturnVariable.Status.Global'], str):
				self.cls_steps.internal_value_set_value (None, 'Variable', str (result_web['Status']), opts['ReturnVariable.Status.Global'])
			if 'ReturnVariable.Message' in opts and isinstance (opts['ReturnVariable.Message'], str):
				self.cls_steps.internal_value_set_value (isolation, 'Variable', str (result_web['Message']), opts['ReturnVariable.Message'])
			if 'ReturnVariable.Message.Global' in opts and isinstance (opts['ReturnVariable.Message.Global'], str):
				self.cls_steps.internal_value_set_value (None, 'Variable', str (result_web['Message']), opts['ReturnVariable.Message.Global'])
		else:
			if 'ReturnVariable.Status' in opts and isinstance (opts['ReturnVariable.Status'], str):
				self.cls_steps.internal_value_set_value (isolation, 'Variable', 'ERROR', opts['ReturnVariable.Status'])
			if 'ReturnVariable.Status.Global' in opts and isinstance (opts['ReturnVariable.Status.Global'], str):
				self.cls_steps.internal_value_set_value (None, 'Variable', 'ERROR', opts['ReturnVariable.Status.Global'])
			if 'ReturnVariable.Message' in opts and isinstance (opts['ReturnVariable.Message'], str):
				self.cls_steps.internal_value_set_value (isolation, 'Variable', str (result_web), opts['ReturnVariable.Message'])
			if 'ReturnVariable.Message.Global' in opts and isinstance (opts['ReturnVariable.Message.Global'], str):
				self.cls_steps.internal_value_set_value (None, 'Variable', str (result_web), opts['ReturnVariable.Message.Global'])
			return False, {'Status':'ERROR', 'Title':'OMOIKANEV2:step_loadtodb_upload: Error', 'Message':'WEB:URL failed with the following result: ' + str (result_web)}
		
		if 'Steps' in opts and isinstance (opts['Steps'], list):
			steps_status, steps_result = self.cls_steps.execute_steps (opts['Steps'], isolation)
		return status, {'Status':'OK'}
	
	
	def step_sap_process_transform (self, isolation, **opts):
		if 'Data' not in opts:
			return False, {'Status':'WARNING', 'Title':'OMOIKANEV2:step_sap_process_transform: Aborted', 'Message':'No input Data provided.'}
		elif 'System' not in opts:
			return False, {'Status':'WARNING', 'Title':'OMOIKANEV2:step_sap_process_transform: Aborted', 'Message':'No input System provided.'}
		elif isinstance (opts['Data'], dict) and 'Status' in opts['Data'] and opts['Data']['Status'] == 'OK' and 'Steps' in opts['Data'] and isinstance (opts['Data']['Steps'], list):
			opts['Data'] = opts['Data']['Steps']
		elif not isinstance (opts['Data'], list):
			return False, {'Status':'WARNING', 'Title':'OMOIKANEV2:step_sap_process_transform: Aborted', 'Message':'Input data was not a list.'}
		
		use_threading = (False if 'Threading' not in opts or opts['Threading'] is not True else True)
		workload = {}
		thread = ''
		segment = ''
		replace_array = {}
		for step in opts['Data']:
			segment_prev = copy.deepcopy (segment)
			segment = (step['Segment'] if 'Segment' in step else '*')
			thread_prev = copy.deepcopy (thread)
			thread = (step['MetaSegment'] if 'MetaSegment' in step else 'STD')
			prev_replace_array = copy.deepcopy (replace_array)
			replace_array = {
				'%%SEGMENT.META%%':thread,
				'%%SEGMENT%%':segment,
			}
			if thread not in workload:
				if 'Steps.Before' in opts and isinstance (opts['Steps.Before'], list):
					workload[thread] = internal_zyd_arrayreplace (Array=copy.deepcopy (opts['Steps.Before']), ReplaceArray=replace_array)
				else:
					workload[thread] = []
			if 'Steps.After.Segment' in opts and thread_prev != '' and (thread != thread_prev or segment != segment_prev):
#				if isinstance (opts['Steps.After.Segment'], dict) and (segment if thread != thread_prev else segment_prev) in opts['Steps.After.Segment'] and isinstance (opts['Steps.After.Segment'][(segment if thread != thread_prev else segment_prev)], list):
#					workload[thread_prev] += internal_zyd_arrayreplace (Array=copy.deepcopy (opts['Steps.After.Segment'][(segment if thread != thread_prev else segment_prev)]), ReplaceArray=replace_array)
				if isinstance (opts['Steps.After.Segment'], dict) and segment_prev in opts['Steps.After.Segment'] and isinstance (opts['Steps.After.Segment'][segment_prev], list):
					workload[thread_prev] += internal_zyd_arrayreplace (Array=copy.deepcopy (opts['Steps.After.Segment'][segment_prev]), ReplaceArray=prev_replace_array)
			if 'Steps.Before.Segment' in opts and (thread != thread_prev or segment != segment_prev):
				if isinstance (opts['Steps.Before.Segment'], dict) and segment in opts['Steps.Before.Segment'] and isinstance (opts['Steps.Before.Segment'][segment], list):
					workload[thread] += internal_zyd_arrayreplace (Array=copy.deepcopy (opts['Steps.Before.Segment'][segment]), ReplaceArray=replace_array)
			
			result = self.internal_step_sap_process_transform (step, opts['OmoikaneV2.URL'], (opts['OmoikaneV2.URL.Verify'] if 'OmoikaneV2.URL.Verify' in opts else True), thread, use_threading)
			if isinstance (result, dict):
				workload[thread].append (result)
			elif isinstance (result, list):
				for subresult in result:
					if isinstance (subresult, dict):
						workload[thread].append (subresult)
					elif subresult == None:
						return False, {'Status':'WARNING', 'Title':'OMOIKANEV2:step_sap_process_transform: Aborted', 'Message':'Unknown sub step logic:\n' + str (subresult) + '\nStep:\n' + str (step)}
			elif result == None:
				return False, {'Status':'WARNING', 'Title':'OMOIKANEV2:step_sap_process_transform: Aborted', 'Message':'Unknown step logic:\n' + str (step)}
		if 'Steps.After.Segment' in opts and isinstance (opts['Steps.After.Segment'], dict) and segment in opts['Steps.After.Segment'] and isinstance (opts['Steps.After.Segment'][segment], list):
			workload[thread] += internal_zyd_arrayreplace (Array=copy.deepcopy (opts['Steps.After.Segment'][segment]), ReplaceArray=replace_array)
		if 'Steps.After' in opts:
			if isinstance (opts['Steps.After'], dict) and segment in opts['Steps.After'] and isinstance (opts['Steps.After'][segment], list):
				for step_after in internal_zyd_arrayreplace (Array=copy.deepcopy (opts['Steps.After'][segment]), ReplaceArray=replace_array):
					workload[thread_prev].append (step_after)
			elif isinstance (opts['Steps.After'], list):
				for step_after in opts['Steps.After']:
					workload[thread_prev].append (step_after)
		
		wait = False
		wait_threads = []
		for thread in workload.keys ():
			if 'SCRIPTING:SAP' in str (workload[thread]):
				wait_threads.append (thread)
				workload[thread].insert (0, {'Function':'SCRIPTING:SAP.Session.Open', 'System':opts['System']})
#				workload[thread].insert (0, {'Function':'SCRIPTING:SAP.Session.Acquire', 'System':opts['System']})
				workload[thread].append ({'Function':'SCRIPTING:SAP.Session.Release'})
				workload[thread].append ({'Function':'SCRIPTING:SAP.Session.Close'})
#				for stepid in range (0, len (workload[thread])):
#					if 'Function' in workload[thread][stepid] and workload[thread][stepid]['Function'] != 'CORE:Break' and "'Function': 'CORE:Break'" in str (workload[thread][stepid]):
#						print ('\n\n\tADD_DISCONNECT_TO_BREAK\n')
#						self.internal_step_sap_process_transform_sub_break_add_disconnect (isolation, workload[thread])
			elif 'WEB:URL' in str (workload[thread]):
				wait = True
			if '%%OMOIKANE_URL%%' in str (workload[thread]):
				if 'OmoikaneV2.URL' not in opts or not isinstance (opts['OmoikaneV2.URL'], str):
					return False, {'Status':'WARNING', 'Title':'OMOIKANEV2:step_sap_process_transform: Aborted', 'Message':'The input OmoikaneV2.URL doesn\'t contain a string.'}
				workload[thread] = internal_zyd_arrayreplace (Array=workload[thread], ReplaceArray={'%%OMOIKANE_URL%%':'https://' + opts['OmoikaneV2.URL'] + '.emea.tdworldwide.com/'})
		
		if use_threading is False:
			workload_list = []
			for thread in workload.keys ():
				for step in workload[thread]:
					workload_list.append (step)
			workload = workload_list
		elif len (workload) > 1:
			for thread in workload.keys ():
				if wait is True and thread not in wait_threads:
					workload[thread].insert (0, {'Function':'LOGIC:Threading.Wait', 'Threads':wait_threads})
		
		if 'Debug.Console' in opts and opts['Debug.Console'] is True:
			print ('===[ step_sap_process_transform ]==========================================')
			if isinstance (workload, dict):
				for thread in workload.keys ():
					segment = ''
					print ('===[ ' + str (thread) + ' ]==========================================')
					for step in workload[thread]:
						prev_segment = copy.deepcopy (segment)
						segment = (step['Function.Segment'] if 'Function.Segment' in step else 'STD')
						if segment != prev_segment:
							print ('\t===[ ' + str (segment) + ' ]==========================================')
						print ('\t\t' + str (step))
			else:
				for step in workload:
					print ('\t' + str (step))
		
		if 'ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str):
			self.cls_steps.internal_value_set_value (isolation, 'Variable', workload, opts['ReturnVariable'])
		if 'ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str):
			self.cls_steps.internal_value_set_value (None, 'Variable', workload, opts['ReturnVariable.Global'])

		return True, {'Status':'OK'}
	
	
	def internal_step_sap_process_transform (self, step, omoikanev2url, omoikanev2urlverify, thread, use_threading = False):
		entry = None
		segment = (step['MetaSegment'] + ':' if use_threading is False and 'MetaSegment' in step else '') + (step['Segment'] if 'Segment' in step else '*')
		if 'Action' in step:
			if step['Action'] == 'SendText' and 'Field' in step and 'Value' in step:
				entry = {'Function':'SCRIPTING:SAP.Send.Text', 'Field':step['Field'], 'Text':step['Value']}
			elif step['Action'] == 'SendKey' and 'Field' in step and 'Value' in step:
				entry = {'Function':'SCRIPTING:SAP.Send.Key', 'Field':step['Field'], 'Key':step['Value']}
			elif step['Action'] == 'SendPress' and 'Field' in step:
				entry = {'Function':'SCRIPTING:SAP.Send.Press', 'Field':step['Field']}
			elif step['Action'] == 'SendSelect' and 'Field' in step:
				entry = {'Function':'SCRIPTING:SAP.Send.Select', 'Field':step['Field']}
			elif step['Action'] == 'SendFocus' and 'Field' in step:
				entry = {'Function':'SCRIPTING:SAP.Send.Focus', 'Field':step['Field']}
			elif step['Action'] == 'SendSelected' and 'Field' in step and 'Value' in step:
				entry = {'Function':'SCRIPTING:SAP.Send.Selected', 'Field':step['Field'], 'Selected':(True if step['Value'] == '1' else False)}
			elif step['Action'] == 'Return' and 'Status' in step and step['Status'] == 'OK':
				entry = [
					{'Function':'DATA:Variable.Set', 'ReturnVariable.Global':'SAPProcess:' + thread + ':' + segment + ':Status', 'Value':'OK'},
					{'Function':'CORE:Break', 'Segment':segment}
				]
			elif step['Action'] == 'Return' and 'Status' in step and step['Status'] in ['TERMINATED', 'WARNING', 'NOTICE']:
				entry = [
					{'Function':'DATA:Variable.Set', 'ReturnVariable.Global':'SAPProcess:' + thread + ':' + segment + ':Status', 'Value':step['Status']},
					{'Function':'CORE:Break'}
				]
			elif step['Action'] == 'CheckText' and 'Field' in step and 'Value' in step and 'Steps' in step and isinstance (step['Steps'], list) and 'Logic' in step and step['Logic'] == 'Contains':
				entry = {'Function':'SCRIPTING:SAP.Check.Text', 'Field':step['Field'], 'Text':step['Value'], 'OnTrue':[]}
				for substep in step['Steps']:
					subentry = self.internal_step_sap_process_transform (substep, omoikanev2url, omoikanev2urlverify, thread, use_threading)
					if isinstance (subentry, dict):
						entry['OnTrue'].append (subentry)
					elif isinstance (subentry, list):
						for subsubentry in subentry:
							if isinstance (subsubentry, dict):
								entry['OnTrue'].append (subsubentry)
							else:
								print ('ISSUE_CHECKTEXT_SUBSUB_STEP=' + str (subsubentry))
					else:
						print ('ISSUE_CHECKTEXT_SUB_STEP=' + str (substep))
			elif step['Action'] == 'LOCAL' and 'Function' in step and step['Function'] == 'RemoveFile' and 'File' in step:
				entry = {
					'Function':'IO:File.Remove',
					'File':step['File'],
					'Function.OnSuccess':[
						{'Function':'DATA:Variable.Set', 'ReturnVariable.Global':'SAPProcess:' + thread + ':' + segment + ':Text', 'Value':'File removed'},
						{'Function':'DATA:Variable.Set', 'ReturnVariable.Global':'SAPProcess:' + thread + ':' + segment + ':Status', 'Value':'OK' },
					],
					'Function.OnFailure':[
						{'Function':'DATA:Variable.Set', 'ReturnVariable.Global':'SAPProcess:' + thread + ':' + segment + ':Text', 'Value':'File removal failed'},
						{'Function':'DATA:Variable.Set', 'ReturnVariable.Global':'SAPProcess:' + thread + ':' + segment + ':Status', 'Value':'ERROR'},
					],
				}
			elif step['Action'] == 'OMOIKANE' and 'PageMethod' in step and step['PageMethod'] == 'PUT' and 'Page' in step and 'PageFile' in step and 'PageComp' in step:
				entry = [
					{
						'Function':'OMOIKANEV2:LoadToDB.Upload',
						'Compression':step['PageComp'],
						'OmoikaneV2.URL':omoikanev2url,
						'OmoikaneV2.URL.Verify':omoikanev2urlverify,
						'Page':step['Page'],
						'File':step['PageFile'],
						'ReturnVariable.Status.Global':'SAPProcess:' + thread + ':' + segment + ':Status',
						'ReturnVariable.Message.Global':'SAPProcess:' + thread + ':' + segment + ':Text',
					},
				]
				if '%%Session.FormatNumber%%' in entry[0]['Page'] or '%%Session.FormatDate%%' in entry[0]['Page']:
					entry[0]['Page'] = entry[0]['Page'].replace ('%%Session.FormatNumber%%', '<$INTERNAL:SAP:FormatNumber$>').replace ('%%Session.FormatDate%%', '<$INTERNAL:SAP:FormatDate$>')
					entry.insert (0, {'Function':'SCRIPTING:SAP.Capture', 'NumberFormat':True, 'ReturnVariable':'INTERNAL:SAP:FormatNumber'})
					entry.insert (0, {'Function':'SCRIPTING:SAP.Capture', 'DateFormat':True, 'ReturnVariable':'INTERNAL:SAP:FormatDate'})
			elif step['Action'] == 'OMOIKANE' and 'PageMethod' in step and step['PageMethod'] == 'GET' and 'Page' in step and 'PageFile' not in step:
				entry = {'Function':'WEB:URL', 'URL':'%%OMOIKANE_URL%%' + step['Page'], 'Method':'GET', 'Verify':False, 'Verify.DisableWarnings':True, 'Auth':True}
			elif step['Action'] == 'OMOIKANE':
				print ('UNKNOWN_OMOIKANE_STEP=' + str (step))
			elif step['Action'] == 'LOCAL':
				print ('UNKNOWN_LOCAL_STEP=' + str (step))
			else:
				print ('UNKNOWN_ACTION=' + str (step['Action']))
		else:
			print ('UNKNOWN_STEP=' + str (step))
		entries = []
		
		"""
		Not sure if it should be Function.Segment or Segment for the entry dicts...
		Function.Segment doesn't crash, but doesn't upload either...
		Function crashes whenever the file doesn't already exist...
		"""
		
		for entry in ([entry] if not isinstance (entry, list) else entry):
			if entry is not None:
				entry['Function.Segment'] = segment
				if entry['Function'] == 'CORE:Break':
					entry['Message'] = step['Message']
					for field in step.keys ():
						if field not in ['Action', 'Status', 'SubStatus', 'Segment', 'MetaSegment', 'Message']:
							if field == 'SubStatus' and step[field] is None:
								continue
							elif field == 'Special' and step[field] == 'MESSAGE_BAR_TEXT':
								if isinstance (entry, dict):
									entry = [entry]
								entry.insert (0, {'Function':'SCRIPTING:SAP.Capture', 'StatusBarText':True, 'ReturnVariable':'SAP:StatusBarText', 'Function.Segment':segment})
								for ientry in range (0, len (entry)):
									if 'Message' in entry[ientry]:
										entry[ientry]['Message'] += '<$SAP:StatusBarText$>'
							else:
								print ('UNKNOWN_BREAK_FIELD=' + str (field) + '::' + str (step))
					if isinstance (entry, dict):
						entry = [entry]
#					print (entry)
					for ientry in range (0, len (entry)):
						if 'Function' in entry[ientry] and entry[ientry]['Function'] == 'CORE:Break':
							entry.insert (ientry, {'Function':'DATA:Variable.Set', 'ReturnVariable.Global':'SAPProcess:' + thread + ':' + segment + ':Text', 'Value':copy.deepcopy (entry[ientry]['Message']), 'Function.Segment':segment})
							
			if '%%Session.TempPath%%' in str (entry):
				for key in entry.keys ():
					if isinstance (entry[key], str) and '%%Session.TempPath%%' in entry[key]:
						entry[key] = entry[key].replace ('%%Session.TempPath%%', tempfile.gettempdir () + '\\')
			if '%%Session.TempPath%%' in str (entry):
				print ('UNKNOWN_%%Session.TempPath%%==' + str (step))
				return None
			if '%%Session.FormatNumber%%' in str (entry):
				print ('UNKNOWN_%%Session.FormatNumber%%==' + str (step))
				return None
			if '%%Session.FormatDate%%' in str (entry):
				print ('UNKNOWN_%%Session.FormatDate%%==' + str (step))
				return None
			if isinstance (entry, list):
				for entryrow in entry:
					entries.append (entryrow)
			else:
				entries.append (entry)
			
		return (entries[0] if len (entries) == 1 else entries)
	
	
