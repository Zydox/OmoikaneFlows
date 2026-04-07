# Copyright (c) 2025-2026 Erik Persson
# Licensed for free use only. Copying, modification, or redistribution prohibited.

# -*- coding: utf-8 -*-
import builtins
from Functions.Common import *
from Functions.DataHandling import *
for name in dir ():
    if not name.startswith ("_"):
        builtins.__dict__[name] = globals ()[name]
import pythoncom
builtins.pythoncom = pythoncom
import pywintypes
builtins.pywintypes = pywintypes
import win32com
builtins.win32com = win32com
import win32com.client
builtins.win32com.client = win32com.client
import subprocess
builtins.subprocess = subprocess
import copy
builtins.copy = copy
import threading
builtins.threading = threading
import time
builtins.time = time
import datetime
builtins.datetime = datetime

class Scripting:
	def __init__ (self, cls_steps = None):
		self.objects = {
			'SAP':{},
			'Excel':{},
			'Lock':{},
		}
		self.cls_steps = cls_steps
	
	
	def dynamic_function (self, function, to_class = True):
		if to_class is True:
			func = {}
			exec (function['Code'], func)
			setattr (Scripting, function['Function'], func[function['Function']])
		else:
			exec (function['Code'], globals ())
			builtins.__dict__[function['Function']] = globals ()[function['Function']]

	
	def execute (self, running_steps, isolation = None, **opts):
		try:
			opts = self.internal_date_number_format (opts, (isolation['Object.SAP'] if isinstance (isolation, dict) and 'Object.SAP' in isolation else str (isolation)))
			if opts['Function'] == 'SCRIPTING:SAP.Session.Open':
				return self.step_sap_session_open (running_steps, isolation, **opts)
			if opts['Function'] == 'SCRIPTING:SAP.Session.Acquire':
				return self.step_sap_session_acquire (running_steps, isolation, **opts)
			elif opts['Function'] == 'SCRIPTING:SAP.Session.Resize':
				return self.step_sap_session_resize (running_steps, isolation, **opts)
			elif opts['Function'] == 'SCRIPTING:SAP.Session.Formats':
				return self.step_sap_session_formats (running_steps, isolation, **opts)
			elif opts['Function'] == 'SCRIPTING:SAP.Session.Close':
				return self.step_sap_session_close (running_steps, isolation, **opts)
			elif opts['Function'] == 'SCRIPTING:SAP.Session.Release':
				return self.step_sap_session_release (running_steps, isolation, **opts)
			elif opts['Function'] == 'SCRIPTING:SAP.Send.Text':
				return self.step_sap_send_text (running_steps, isolation, **opts)
			elif opts['Function'] == 'SCRIPTING:SAP.Send.Key':
				return self.step_sap_send_key (running_steps, isolation, **opts)
			elif opts['Function'] == 'SCRIPTING:SAP.Send.Select':
				return self.step_sap_send_select (running_steps, isolation, **opts)
			elif opts['Function'] == 'SCRIPTING:SAP.Send.Selected':
				return self.step_sap_send_selected (running_steps, isolation, **opts)
			elif opts['Function'] == 'SCRIPTING:SAP.Send.Press':
				return self.step_sap_send_press (running_steps, isolation, **opts)
			elif opts['Function'] == 'SCRIPTING:SAP.Send.Focus':
				return self.step_sap_send_focus (running_steps, isolation, **opts)
			elif opts['Function'] == 'SCRIPTING:SAP.Send.NodeDoubleClick':
				return self.step_sap_send_nodedoubleclick (running_steps, isolation, **opts)
			elif opts['Function'] == 'SCRIPTING:SAP.Send.PressToolbarContextButton':
				return self.step_sap_send_presstoolbarcontextbutton (running_steps, isolation, **opts)
			elif opts['Function'] == 'SCRIPTING:SAP.Send.SelectContextMenuItem':
				return self.step_sap_send_selectcontextmenuitem (running_steps, isolation, **opts)
			elif opts['Function'] == 'SCRIPTING:SAP.Send.ContextMenu':
				return self.step_sap_send_contextmenu (running_steps, isolation, **opts)
			elif opts['Function'] == 'SCRIPTING:SAP.Send.SelectedRows':
				return self.step_sap_send_selectedrows (running_steps, isolation, **opts)
			elif opts['Function'] == 'SCRIPTING:SAP.Send.ClickCurrentCell':
				return self.step_sap_send_clickcurrentcell (running_steps, isolation, **opts)
			elif opts['Function'] == 'SCRIPTING:SAP.Send.PressToolbarButton':
				return self.step_sap_send_presstoolbarbutton (running_steps, isolation, **opts)
			elif opts['Function'] == 'SCRIPTING:SAP.Send.SelectedNode':
				return self.step_sap_send_selectednode (running_steps, isolation, **opts)
			elif opts['Function'] == 'SCRIPTING:SAP.Capture':
				return self.step_sap_capture (running_steps, isolation, **opts)
			elif opts['Function'] == 'SCRIPTING:SAP.LabelList.Search':
				return self.step_sap_labellist_search (running_steps, isolation, **opts)
			elif opts['Function'] == 'SCRIPTING:SAP.Screen.Capture':
				return self.step_sap_screen_capture (running_steps, isolation, **opts)
			elif opts['Function'] == 'SCRIPTING:SAP.Check.Text':
				return self.step_sap_check_text (running_steps, isolation, **opts)
			elif opts['Function'] == 'SCRIPTING:Excel.Open.List':
				return self.step_excel_open_list (running_steps, isolation, **opts)
			elif opts['Function'] == 'SCRIPTING:Excel.Read':
				return self.step_excel_read (running_steps, isolation, **opts)
			elif opts['Function'] == 'SCRIPTING:Excel.Write':
				return self.step_excel_write (running_steps, isolation, **opts)
		except Exception as e:
			st = internal_zyd_stacktrace (e, FunctionOpts=opts)
			return False, {'Status':'CRASH', 'Title':'SCRIPTING:execute: Crashed', 'Message':'Crashed with the error: ' + str (e) + ' for step:\n' + str (opts), 'StackTrace':st}
			
		return False, {'Status':'WARNING', 'Title':'', 'Message':'Unknown step=' + str (opts)}
	
	
	def step_excel_write (self, running_steps, isolation, **opts):
		if 'Workbook' not in opts or 'Sheet' not in opts:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_excel_write: Aborted', 'Message':'Workbook and Sheet needs to be provided for this function to work.'}
		result = (self.internal_excel_refresh (Refresh=True) if 'Refresh' in opts and opts['Refresh'] is True else self.internal_excel_refresh ())
		if result is not True:
			return False, result
		if opts['Workbook'] not in self.objects['Excel']['Index']:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_excel_write: Aborted', 'Message':'Workbook "' + str (opts['Workbook']) + '" not found.'}
		if opts['Workbook'] + ':' + opts['Sheet'] not in self.objects['Excel']['Index']:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_excel_write: Aborted', 'Message':'Workbook "' + str (opts['Workbook']) + '" does not contain the sheet "' + str (opts['Sheet']) + '".'}
		sheet_object = self.objects['Excel']['Application'].Workbooks (self.objects['Excel']['Index'][opts['Workbook']]).Worksheets (self.objects['Excel']['Index'][opts['Workbook'] + ':' + opts['Sheet']])
		
		if 'Cell' in opts and isinstance (opts['Cell'], str):
			self.internal_excel_write_cell (sheet_object.Range (opts['Cell']), **opts)
		else:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_excel_write: Aborted', 'Message':'No valid update input was provided.'}

		return True, {'Status':'OK'}
		
		
	def step_excel_read (self, running_steps, isolation, **opts):
		if 'Workbook' not in opts or 'Sheet' not in opts:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_excel_read: Aborted', 'Message':'Workbook and Sheet needs to be provided for this function to work.'}
		result = (self.internal_excel_refresh (Refresh=True) if 'Refresh' in opts and opts['Refresh'] is True else self.internal_excel_refresh ())
		if result is not True:
			return False, result
		if opts['Workbook'] not in self.objects['Excel']['Index']:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_excel_read: Aborted', 'Message':'Workbook "' + str (opts['Workbook']) + '" not found.'}
		if opts['Workbook'] + ':' + opts['Sheet'] not in self.objects['Excel']['Index']:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_excel_read: Aborted', 'Message':'Workbook "' + str (opts['Workbook']) + '" does not contain the sheet "' + str (opts['Sheet']) + '".'}
		sheet_object = self.objects['Excel']['Application'].Workbooks (self.objects['Excel']['Index'][opts['Workbook']]).Worksheets (self.objects['Excel']['Index'][opts['Workbook'] + ':' + opts['Sheet']])
		
		if 'Complete' in opts and opts['Complete'] is True:
			data = []
			if sheet_object.UsedRange.Value is not None:
				for irow in range (-sheet_object.UsedRange.Row + 2, sheet_object.UsedRange.Rows.Count + 1):
					row = []
					for icol in range (-sheet_object.UsedRange.Column + 2, sheet_object.UsedRange.Columns.Count + 1):
						row.append (self.internal_excel_read_cell (sheet_object.UsedRange.Cells (irow, icol), **opts))
					data.append (row)
		elif 'Row' in opts and isinstance (opts['Row'], int):
			if opts['Row'] < 1 or opts['Row'] > sheet_object.Rows.Count:
				return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_excel_read: Aborted', 'Message':'The row "' + str (opts['Row']) + '" is not active in the Excel sheet.'}
			data = []
			irow = opts['Row'] - sheet_object.UsedRange.Row + 1
			
			for icol in range (-sheet_object.UsedRange.Column + 2, sheet_object.UsedRange.Columns.Count + 1):
				data.append (self.internal_excel_read_cell (sheet_object.UsedRange.Cells (irow, icol), **opts))
		elif 'Cell' in opts:
			data = self.internal_excel_read_cell (sheet_object.Range (opts['Cell']), **opts)
		else:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_excel_read: Aborted', 'Message':'No valid selection input was provided.'}
			
		if 'ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str):
			self.cls_steps.internal_value_set_value (isolation, 'Variable', data, opts['ReturnVariable'])
		if 'ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str):
			self.cls_steps.internal_value_set_value (None, 'Variable', data, opts['ReturnVariable.Global'])
		return True, {'Status':'OK', 'Data':data}
	
	
	
	def step_excel_open_list (self, running_steps, isolation, **opts):
		result = (self.internal_excel_refresh (Refresh=True) if 'Refresh' in opts and opts['Refresh'] is True else self.internal_excel_refresh ())
		if result is not True:
			return False, result
		
		if 'Workbooks' in opts and opts['Workbooks'] is True:
			data = []
			for iworkbook in self.objects['Excel']['Workbooks'].keys ():
				data.append (self.objects['Excel']['Workbooks'][iworkbook]['Name'])
		elif 'Workbook' in opts and 'Sheets' in opts and opts['Sheets'] is True:
			if opts['Workbook'] not in self.objects['Excel']['Index']:
				return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_excel_open_list: Aborted', 'Message':'Workbook "' + str (opts['Workbook']) + '" not found.'}
			data = []
			iworkbook = self.objects['Excel']['Index'][opts['Workbook']]
			for isheet in self.objects['Excel']['Workbooks'][iworkbook]['Sheets'].keys ():
				data.append (self.objects['Excel']['Workbooks'][iworkbook]['Sheets'][isheet]['Name'])
		else:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_excel_open_list: Aborted', 'Message':'No valid selection logic was provided.'}
		
		if 'ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str):
			self.cls_steps.internal_value_set_value (isolation, 'Variable', data, opts['ReturnVariable'])
		if 'ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str):
			self.cls_steps.internal_value_set_value (None, 'Variable', data, opts['ReturnVariable.Global'])
		return True, {'Status':'OK', 'Data':data}
	
	
	def internal_excel_read_cell (self, cell_object, **opts):
		if 'CaptureValues' in opts and opts['CaptureValues'] is True:
			return cell_object.Value
		return cell_object.Text
	
	
	def internal_excel_write_cell (self, cell_object, **opts):
		if 'Cell.Value' in opts:
			cell_object.Value = opts['Cell.Value']
		if 'Cell.Background' in opts:
			if isinstance (opts['Cell.Background'], str) and len (opts['Cell.Background']) == 7 and opts['Cell.Background'][0] == '#':
				cell_object.Interior.Color = int (opts['Cell.Background'][5:7], 16) + int (opts['Cell.Background'][3:5], 16) * 256 + int (opts['Cell.Background'][1:3], 16) * 65536
		if 'Cell.Color' in opts:
			if isinstance (opts['Cell.Color'], str) and len (opts['Cell.Color']) == 7 and opts['Cell.Color'][0] == '#':
				cell_object.Font.Color = int (opts['Cell.Color'][5:7], 16) + int (opts['Cell.Color'][3:5], 16) * 256 + int (opts['Cell.Color'][1:3], 16) * 65536
	
	
	def internal_excel_refresh (self, **opts):
		if 'Refresh' in opts and opts['Refresh'] is True and 'Application' in self.objects['Excel']:
			self.objects['Excel']['Application'].Application.Quit ()
			self.objects['Excel']['Application'].Quit ()
			self.objects['Excel']['Application'] = None
			self.objects['Excel'] = {}
		
		if 'Application' not in self.objects['Excel']:
			self.objects['Excel'] = {
				'Application':win32com.client.dynamic.Dispatch ("Excel.Application"),
				'Workbooks':{},
				'Index':{},
			}
			for iworkbook in range (1, self.objects['Excel']['Application'].Workbooks.Count + 1):
				self.objects['Excel']['Workbooks'][iworkbook] = {
					'Name':self.objects['Excel']['Application'].Workbooks.Item (iworkbook).Name,
					'Sheets':{},
				}
				self.objects['Excel']['Index'][self.objects['Excel']['Application'].Workbooks.Item (iworkbook).Name] = iworkbook
				for isheet in range (1, len (self.objects['Excel']['Application'].Workbooks (iworkbook).Worksheets) + 1):
					self.objects['Excel']['Workbooks'][iworkbook]['Sheets'][isheet] = {
						'Name':self.objects['Excel']['Application'].Workbooks (iworkbook).Worksheets (isheet).Name
					}
					self.objects['Excel']['Index'][self.objects['Excel']['Application'].Workbooks.Item (iworkbook).Name + ':' + self.objects['Excel']['Application'].Workbooks (iworkbook).Worksheets (isheet).Name] = isheet
		return True
	
	
	
	def step_sap_session_open (self, running_steps, isolation, **opts):
		if 'System' not in opts:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_session_open: Aborted', 'Message':'No System was provided for the function.'}
		if 'SAPLogon' in opts and not isinstance (opts['SAPLogon'], list):
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_session_open: Aborted', 'Message':'SAPLogon was not a list.'}
		debug_console = (True if 'Debug.Console' in opts and opts['Debug.Console'] is True else False)
		
		key = (isolation['Object.SAP'] if isinstance (isolation, dict) and 'Object.SAP' in isolation else str (isolation))
		if 'SAP' not in self.objects['Lock']:
			self.objects['Lock']['SAP'] = threading.RLock ()
#		self.objects['Lock']['SAP'].acquire ()
		
		with self.objects['Lock']['SAP']:
			try:
				pythoncom.CoInitialize ()
				try:
					self.winapp_sapgui = win32com.client.GetObject ("SAPGUI")
				except pywintypes.com_error as e:
					self.winapp_sapgui = None
					if 'SAPLogon' in opts:
						for path in opts['SAPLogon']:
							if os.path.exists (path):
								subprocess.Popen (path)
								time.sleep (5)
								self.winapp_sapgui = win32com.client.GetObject ("SAPGUI")
								break
						if self.winapp_sapgui is None:
							return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_session_open: Aborted', 'Message':'No SAPlogon was found running and it failed to be started from any of the following locations:\n* ' + '\n* '.join (opts['SAPLogon'])}
					if self.winapp_sapgui is None:
						return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_session_open: Aborted', 'Message':'No SAPlogon was found running.'}
				
				self.winapp_engine = self.winapp_sapgui.GetScriptingEngine
				self.cls_steps.internal_value_set_value (isolation, 'InternalVariable', key, 'Thread.CurrentID')
				connection = self.winapp_engine.OpenConnection (opts['System'], True)
				window = connection.Children(0)
				self.objects['SAP'][key] = {
					'System':copy.deepcopy (opts['System']),
					'Connection':connection,
					'Window':window,
					'NumberFormat':None,
					'DateFormat':None,
					'Active':True,
					'Processing':False,
					'LastAction':round (datetime.datetime.now ().timestamp (), 3),
				}
			except Exception as e:
				st = internal_zyd_stacktrace (e, FunctionOpts=opts)
				return False, {'Status':'CRASH', 'Title':'SCRIPTING:step_sap_session_open: Crashed', 'Message':'Crashed with the errro: ' + str (e), 'StackTrace':st}
		self.internal_sap_object_processing (key, False)
		
		if window.Info.Transaction == 'S000':
			status, result = self.cls_steps.execute_steps ([
				{'Function':'SCRIPTING:SAP.Session.Resize', 'Object.SAP':key, 'Minimize':True},
				{'Function':'SCRIPTING:SAP.Send.Select', 'Object.SAP':key, 'Field':'wnd[1]/usr/radMULTI_LOGON_OPT2'},
				{'Function':'SCRIPTING:SAP.Send.Press', 'Object.SAP':key, 'Field':'wnd[1]/tbar[0]/btn[0]'},
				{'Function':'SCRIPTING:SAP.Capture', 'Object.SAP':key, 'Transaction':True, 'ReturnVariable':'SAP:Transaction'},
			], isolation)
		
		status, result = self.cls_steps.execute_steps ([
			{'Function':'SCRIPTING:SAP.Session.Resize', 'Object.SAP':key, 'Minimize':True},
			{'Function':'SCRIPTING:SAP.Send.Text', 'Object.SAP':key, 'Field':'wnd[0]/tbar[0]/okcd', 'Text':'/NSU3'},
			{'Function':'SCRIPTING:SAP.Send.Key', 'Object.SAP':key, 'Field':'wnd[0]', 'Key':0},
			{'Function':'SCRIPTING:SAP.Check.Text', 'Object.SAP':key, 'Field':'wnd[0]/sbar', 'Text':'locked by', 'WhileTrue.Loops':50, 'WhileTrue.Wait':0.1, 'WhileTrue.Wait.Multiplier':1.1, 'WhileTrue.Wait.Max':1,
				'WhileTrue.Steps':[
					{'Function':'SCRIPTING:SAP.Send.Text', 'Object.SAP':key, 'Field':'wnd[0]/tbar[0]/okcd', 'Text':'/NSU3'},
					{'Function':'SCRIPTING:SAP.Send.Key', 'Object.SAP':key, 'Field':'wnd[0]', 'Key':0},
				],
				'OnTrue':[
					{'Function':'EXTERNAL:Break', 'Object.SAP':key, 'Message':'Aborting: Users SU3 is locked.'}
				]
			},
			{'Function':'SCRIPTING:SAP.Send.Select', 'Object.SAP':key, 'Field':'wnd[0]/usr/tabsTABSTRIP1/tabpDEFA'},
			{'Function':'SCRIPTING:SAP.Check.Text', 'Object.SAP':key, 'Field':'wnd[0]/usr/tabsTABSTRIP1/tabpDEFA/ssubMAINAREA:SAPLSUID_MAINTENANCE:1105/cmbSUID_ST_NODE_DEFAULTS-DCPFM', 'Verify':{'Type':'String', 'Contains':'1,234,567.89'}, 'Debug.Console':debug_console,
				'OnTrue':[{'Function':'SCRIPTING:SAP.Session.Formats', 'Object.SAP':key, 'NumberFormat.Set':'X,XXX,XXX.XX'}],
				'OnFalse':[
					{'Function':'SCRIPTING:SAP.Check.Text', 'Object.SAP':key, 'Field':'wnd[0]/usr/tabsTABSTRIP1/tabpDEFA/ssubMAINAREA:SAPLSUID_MAINTENANCE:1105/cmbSUID_ST_NODE_DEFAULTS-DCPFM', 'Verify':{'Type':'String', 'Contains':'1.234.567,89'}, 'Debug.Console':debug_console,
						'OnTrue':[{'Function':'SCRIPTING:SAP.Session.Formats', 'Object.SAP':key, 'NumberFormat.Set':'X.XXX.XXX,XX'}],
						'OnFalse':[
							{'Function':'SCRIPTING:SAP.Check.Text', 'Object.SAP':key, 'Field':'wnd[0]/usr/tabsTABSTRIP1/tabpDEFA/ssubMAINAREA:SAPLSUID_MAINTENANCE:1105/cmbSUID_ST_NODE_DEFAULTS-DCPFM', 'Verify':{'Type':'String', 'Contains':'1 234 567,89'}, 'Debug.Console':debug_console,
								'OnTrue':[{'Function':'SCRIPTING:SAP.Session.Formats', 'Object.SAP':key, 'NumberFormat.Set':'X XXX XXX,XX'}],
								'OnFalse':[{'Function':'SCRIPTING:SAP.Session.Formats', 'Object.SAP':key, 'NumberFormat.Set':None}]
					}]
				}]
			},
			{'Function':'SCRIPTING:SAP.Check.Text', 'Object.SAP':key, 'Field':'wnd[0]/usr/tabsTABSTRIP1/tabpDEFA/ssubMAINAREA:SAPLSUID_MAINTENANCE:1105/cmbSUID_ST_NODE_DEFAULTS-DATFM', 'Verify':{'Type':'String', 'Contains':'YYYY-MM-DD'}, 'Debug.Console':debug_console,
				'OnTrue':[{'Function':'SCRIPTING:SAP.Session.Formats', 'Object.SAP':key, 'DateFormat.Set':'YYYY-MM-DD'}],
				'OnFalse':[
					{'Function':'SCRIPTING:SAP.Check.Text', 'Object.SAP':key, 'Field':'wnd[0]/usr/tabsTABSTRIP1/tabpDEFA/ssubMAINAREA:SAPLSUID_MAINTENANCE:1105/cmbSUID_ST_NODE_DEFAULTS-DATFM', 'Verify':{'Type':'String', 'Contains':'DD.MM.YYYY'}, 'Debug.Console':debug_console,
						'OnTrue':[{'Function':'SCRIPTING:SAP.Session.Formats', 'Object.SAP':key, 'DateFormat.Set':'DD.MM.YYYY'}],
						'OnFalse':[
							{'Function':'SCRIPTING:SAP.Check.Text', 'Object.SAP':key, 'Field':'wnd[0]/usr/tabsTABSTRIP1/tabpDEFA/ssubMAINAREA:SAPLSUID_MAINTENANCE:1105/cmbSUID_ST_NODE_DEFAULTS-DATFM', 'Verify':{'Type':'String', 'Contains':'MM-DD-YYYY'}, 'Debug.Console':debug_console,
								'OnTrue':[{'Function':'SCRIPTING:SAP.Session.Formats', 'Object.SAP':key, 'DateFormat.Set':'MM-DD-YYYY'}],
								'OnFalse':[
									{'Function':'SCRIPTING:SAP.Check.Text', 'Object.SAP':key, 'Field':'wnd[0]/usr/tabsTABSTRIP1/tabpDEFA/ssubMAINAREA:SAPLSUID_MAINTENANCE:1105/cmbSUID_ST_NODE_DEFAULTS-DATFM', 'Verify':{'Type':'String', 'Contains':'YYYY.MM.DD'}, 'Debug.Console':debug_console,
										'OnTrue':[{'Function':'SCRIPTING:SAP.Session.Formats', 'Object.SAP':key, 'DateFormat.Set':'YYYY.MM.DD'}],
										'OnFalse':[
											{'Function':'SCRIPTING:SAP.Check.Text', 'Object.SAP':key, 'Field':'wnd[0]/usr/tabsTABSTRIP1/tabpDEFA/ssubMAINAREA:SAPLSUID_MAINTENANCE:1105/cmbSUID_ST_NODE_DEFAULTS-DATFM', 'Verify':{'Type':'String', 'Contains':'YYYY/MM/DD'}, 'Debug.Console':debug_console,
												'OnTrue':[{'Function':'SCRIPTING:SAP.Session.Formats', 'Object.SAP':key, 'DateFormat.Set':'YYYY/MM/DD'}],
												'OnFalse':[
													{'Function':'SCRIPTING:SAP.Check.Text', 'Object.SAP':key, 'Field':'wnd[0]/usr/tabsTABSTRIP1/tabpDEFA/ssubMAINAREA:SAPLSUID_MAINTENANCE:1105/cmbSUID_ST_NODE_DEFAULTS-DATFM', 'Verify':{'Type':'String', 'Contains':'MM/DD/YYYY'}, 'Debug.Console':debug_console,
														'OnTrue':[{'Function':'SCRIPTING:SAP.Session.Formats', 'Object.SAP':key, 'DateFormat.Set':'MM/DD/YYYY'}],
														'OnFalse':[{'Function':'SCRIPTING:SAP.Session.Formats', 'Object.SAP':key, 'DateFormat.Set':None}]
												}]
										}]
								}]
						}]
				}]
			},
			{'Function':'SCRIPTING:SAP.Send.Text', 'Object.SAP':key, 'Field':'wnd[0]/tbar[0]/okcd', 'Text':'/N'},
			{'Function':'SCRIPTING:SAP.Send.Key', 'Object.SAP':key, 'Field':'wnd[0]', 'Key':0},
			{'Function':'SCRIPTING:SAP.Session.Resize', 'Object.SAP':key, 'Restore':True},
		], isolation)
		
		if 'ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str):
			self.cls_steps.internal_value_set_value (isolation, 'Variable', key, opts['ReturnVariable'])
		if 'ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str):
			self.cls_steps.internal_value_set_value (None, 'Variable', key, opts['ReturnVariable.Global'])
		
		return status, result
	
	
	def step_sap_session_resize (self, running_steps, isolation, **opts):
		key = (isolation['Object.SAP'] if isinstance (isolation, dict) and 'Object.SAP' in isolation else str (isolation))
		self.internal_sap_object_processing (key, True)
		object = self.objects['SAP'][key]['Window'].findById (("wnd[0]" if 'Window' not in opts else opts['Window']))
		if 'Minimize' in opts and opts['Minimize'] is True:
			object.iconify ()
		elif 'Maximize' in opts and opts['Maximize'] is True:
			object.maximize ()
		elif 'Restore' in opts and opts['Restore'] is True:
			object.restore ()
		elif 'Width' in opts and isinstance (opts['Width'], int) and 'Height' in opts and isinstance (opts['Height'], int):
			object.ResizeWorkingPaneEx (opts['Width'], opts['Height'], False)
		else:
			self.internal_sap_object_processing (key, False)
			return True, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_session_resize: Aborted', 'Message':'Unknown opts=' + str (opts)}
		self.internal_sap_object_processing (key, False)
		return True, {'Status':'OK'}
	
	
	def step_sap_session_formats (self, running_steps, isolation, **opts):
		key = (isolation['Object.SAP'] if isinstance (isolation, dict) and 'Object.SAP' in isolation else str (isolation))
		self.internal_sap_object_processing (key, True)
		if 'NumberFormat.Set' in opts:
			if opts['NumberFormat.Set'] in [None, 'X,XXX,XXX.XX', 'X.XXX.XXX,XX', 'X XXX XXX,XX']:
				self.objects['SAP'][key]['NumberFormat'] = copy.deepcopy (opts['NumberFormat.Set'])
			else:
				self.internal_sap_object_processing (key, False)
				return True, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_session_formats: Aborted', 'Message':'Invalid NumberFormat: "' + str (opts['NumberFormat.Set']) + '".'}
		if 'DateFormat.Set' in opts:
			if opts['DateFormat.Set'] in [None, 'YYYY-MM-DD', 'DD.MM.YYYY', 'MM-DD-YYYY', 'YYYY.MM.DD', 'YYYY/MM/DD', 'MM/DD/YYYY']:
				self.objects['SAP'][key]['DateFormat'] = copy.deepcopy (opts['DateFormat.Set'])
			else:
				self.internal_sap_object_processing (key, False)
				return True, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_session_formats: Aborted', 'Message':'Invalid DateFormat: "' + str (opts['DateFormat.Set']) + '".'}
			
		self.internal_sap_object_processing (key, False)
		return True, {'Status':'OK'}
	
	
	def step_sap_session_close (self, running_steps, isolation, **opts):
		key = (opts['Isolation'] if 'Isolation' in opts and isinstnace (opts['Isolation'], str) else (isolation['Object.SAP'] if isinstance (isolation, dict) and 'Object.SAP' in isolation else str (isolation)))
		if key in self.objects['SAP']:
			self.internal_sap_object_processing (key, True)
			self.objects['SAP'][key]['Connection'].CloseConnection ()
			del (self.objects['SAP'][key])
			return True, {'Status':'OK'}
		elif 'IfExists' in opts and opts['IfExists'] is True:
			return True, {'Status':'OK', 'Message':'Connection doesn\'t exist'}
		else:
			return True, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_session_close: Aborted', 'Message':'Session "' + str (key) + '" does not exist.'}
		
	
	def step_sap_session_release (self, running_steps, isolation, **opts):
		key = (isolation['Object.SAP'] if isinstance (isolation, dict) and 'Object.SAP' in isolation else str (isolation))
		self.objects['SAP'][isolation]['Active'] = False
		return True, {'Status':'OK'}
	
	
	def step_sap_session_acquire (self, running_steps, isolation, **opts):
		if 'System' not in opts:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_session_acquire: Aborted', 'Message':'No System was provided for the function.'}
		key = (isolation['Object.SAP'] if isinstance (isolation, dict) and 'Object.SAP' in isolation else str (isolation))
		if key in self.objects['SAP'] and self.objects['SAP'][key]['System'] == opts['System'] and self.objects['SAP'][key]['Active'] is False:
			self.objects['SAP'][key]['Active'] = True
		else:
			key = internal_zyd_uniqueid ()
			status, result = self.step_sap_session_open (running_steps, {'Isolation':isolation, 'Object.SAP':key}, **opts)
			
		if 'ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str):
			self.cls_steps.internal_value_set_value (isolation, 'Variable', key, opts['ReturnVariable'])
		if 'ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str):
			self.cls_steps.internal_value_set_value (None, 'Variable', key, opts['ReturnVariable.Global'])
		return True, {'Status':'OK', 'Data':key}
	
	
	def step_sap_send_text (self, running_steps, isolation, **opts):
		if 'Field' not in opts:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_send_text: Aborted', 'Message':'No Field was provided for the function.'}
		if 'Text' not in opts:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_send_text: Aborted', 'Message':'No Text was provided for the function.'}
		key = (isolation['Object.SAP'] if isinstance (isolation, dict) and 'Object.SAP' in isolation else str (isolation))
		self.internal_sap_object_processing (key, True)
		self.objects['SAP'][key]['Window'].findById (opts['Field']).text = opts['Text']
		self.internal_sap_object_processing (key, False)
		return True, {'Status':'OK'}
	
	
	def step_sap_send_key (self, running_steps, isolation, **opts):
		if 'Field' not in opts:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_send_key: Aborted', 'Message':'No Field was provided for the function.'}
		if 'Key' not in opts:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_send_key: Aborted', 'Message':'No Key was provided for the function.'}
		key = (isolation['Object.SAP'] if isinstance (isolation, dict) and 'Object.SAP' in isolation else str (isolation))
		self.internal_sap_object_processing (key, True)
		self.objects['SAP'][key]['Window'].findById (opts['Field']).sendVKey (opts['Key'])
		self.internal_sap_object_processing (key, False)
		return True, {'Status':'OK'}
	
	
	def step_sap_send_select (self, running_steps, isolation, **opts):
		if 'Field' not in opts:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_send_select: Aborted', 'Message':'No Field was provided for the function.'}
		key = (isolation['Object.SAP'] if isinstance (isolation, dict) and 'Object.SAP' in isolation else str (isolation))
		self.internal_sap_object_processing (key, True)
		self.objects['SAP'][key]['Window'].findById (opts['Field']).Select ()
		self.internal_sap_object_processing (key, False)
		return True, {'Status':'OK'}
	
	
	def step_sap_send_selected (self, running_steps, isolation, **opts):
		if 'Field' not in opts:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_send_selected: Aborted', 'Message':'No Field was provided for the function.'}
		if 'Selected' not in opts or not isinstance (opts['Selected'], bool):
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_send_selected: Aborted', 'Message':'Selected wasn\'t provided or didn\'t contain True or False.'}
		key = (isolation['Object.SAP'] if isinstance (isolation, dict) and 'Object.SAP' in isolation else str (isolation))
		self.internal_sap_object_processing (key, True)
		self.objects['SAP'][key]['Window'].findById (opts['Field']).selected = opts['Selected']
		self.internal_sap_object_processing (key, False)
		return True, {'Status':'OK'}
	
	
	def step_sap_send_press (self, running_steps, isolation, **opts):
		if 'Field' not in opts:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_send_press: Aborted', 'Message':'No Field was provided for the function.'}
		key = (isolation['Object.SAP'] if isinstance (isolation, dict) and 'Object.SAP' in isolation else str (isolation))
		self.internal_sap_object_processing (key, True)
		self.objects['SAP'][key]['Window'].findById (opts['Field']).press ()
		self.internal_sap_object_processing (key, False)
		return True, {'Status':'OK'}
	
	
	def step_sap_send_focus (self, running_steps, isolation, **opts):
		if 'Field' not in opts:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_send_focus: Aborted', 'Message':'No Field was provided for the function.'}
		key = (isolation['Object.SAP'] if isinstance (isolation, dict) and 'Object.SAP' in isolation else str (isolation))
		self.internal_sap_object_processing (key, True)
		self.objects['SAP'][key]['Window'].findById (opts['Field']).SetFocus ()
		self.internal_sap_object_processing (key, False)
		return True, {'Status':'OK'}
	
	
	def step_sap_send_nodedoubleclick (self, running_steps, isolation, **opts):
		if 'Field' not in opts:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_send_nodedoubleclick: Aborted', 'Message':'No Field was provided for the function.'}
		if 'Node' not in opts:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_send_nodedoubleclick: Aborted', 'Message':'No Node was provided for the function.'}
		key = (isolation['Object.SAP'] if isinstance (isolation, dict) and 'Object.SAP' in isolation else str (isolation))
		self.internal_sap_object_processing (key, True)
		self.objects['SAP'][key]['Window'].findById (opts['Field']).doubleClickNode (opts['Node'])
		self.internal_sap_object_processing (key, False)
		return True, {'Status':'OK'}
	
	
	def step_sap_send_selectcontextmenuitem (self, running_steps, isolation, **opts):
		if 'Field' not in opts:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_send_selectcontextmenuitem: Aborted', 'Message':'No Field was provided for the function.'}
		if 'Item' not in opts:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_send_selectcontextmenuitem: Aborted', 'Message':'No Item was provided for the function.'}
		key = (isolation['Object.SAP'] if isinstance (isolation, dict) and 'Object.SAP' in isolation else str (isolation))
		self.internal_sap_object_processing (key, True)
		self.objects['SAP'][key]['Window'].findById (opts['Field']).selectContextMenuItem (opts['Item'])
		self.internal_sap_object_processing (key, False)
		return True, {'Status':'OK'}
	
	
	def step_sap_send_presstoolbarcontextbutton (self, running_steps, isolation, **opts):
		if 'Field' not in opts:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_send_presstoolbarcontextbutton: Aborted', 'Message':'No Field was provided for the function.'}
		if 'Toolbar' not in opts:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_send_presstoolbarcontextbutton: Aborted', 'Message':'No Toolbar was provided for the function.'}
		key = (isolation['Object.SAP'] if isinstance (isolation, dict) and 'Object.SAP' in isolation else str (isolation))
		self.internal_sap_object_processing (key, True)
		self.objects['SAP'][key]['Window'].findById (opts['Field']).pressToolbarContextButton (opts['Toolbar'])
		self.internal_sap_object_processing (key, False)
		return True, {'Status':'OK'}
	
	
	def step_sap_send_selectedrows (self, running_steps, isolation, **opts):
		if 'Field' not in opts:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_send_selectedrows: Aborted', 'Message':'No Field was provided for the function.'}
		if 'Rows' not in opts:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_send_selectedrows: Aborted', 'Message':'No Rows was provided for the function.'}
		key = (isolation['Object.SAP'] if isinstance (isolation, dict) and 'Object.SAP' in isolation else str (isolation))
		self.internal_sap_object_processing (key, True)
		self.objects['SAP'][key]['Window'].findById (opts['Field']).selectedRows = opts['Rows']
		self.internal_sap_object_processing (key, False)
		return True, {'Status':'OK'}
	
	
	def step_sap_send_clickcurrentcell (self, running_steps, isolation, **opts):
		if 'Field' not in opts:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_send_clickcurrentcell: Aborted', 'Message':'No Field was provided for the function.'}
		key = (isolation['Object.SAP'] if isinstance (isolation, dict) and 'Object.SAP' in isolation else str (isolation))
		self.internal_sap_object_processing (key, True)
		self.objects['SAP'][key]['Window'].findById (opts['Field']).clickCurrentCell ()
		self.internal_sap_object_processing (key, False)
		return True, {'Status':'OK'}
	
	
	def step_sap_send_contextmenu (self, running_steps, isolation, **opts):
		if 'Field' not in opts:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_send_contextmenu: Aborted', 'Message':'No Field was provided for the function.'}
		key = (isolation['Object.SAP'] if isinstance (isolation, dict) and 'Object.SAP' in isolation else str (isolation))
		self.internal_sap_object_processing (key, True)
		self.objects['SAP'][key]['Window'].findById (opts['Field']).contextMenu ()
		self.internal_sap_object_processing (key, False)
		return True, {'Status':'OK'}
	
	
	def step_sap_send_presstoolbarbutton (self, running_steps, isolation, **opts):
		if 'Field' not in opts:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_send_presstoolbarbutton: Aborted', 'Message':'No Field was provided for the function.'}
		if 'Button' not in opts:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_send_presstoolbarbutton: Aborted', 'Message':'No Button was provided for the function.'}
		key = (isolation['Object.SAP'] if isinstance (isolation, dict) and 'Object.SAP' in isolation else str (isolation))
		self.internal_sap_object_processing (key, True)
		self.objects['SAP'][key]['Window'].findById (opts['Field']).pressToolbarButton (opts['Button'])
		self.internal_sap_object_processing (key, False)
		return True, {'Status':'OK'}
	
	
	def step_sap_send_selectednode (self, running_steps, isolation, **opts):
		if 'Field' not in opts:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_send_selectednode: Aborted', 'Message':'No Field was provided for the function.'}
		if 'Node' not in opts:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_send_selectednode: Aborted', 'Message':'No Node was provided for the function.'}
		key = (isolation['Object.SAP'] if isinstance (isolation, dict) and 'Object.SAP' in isolation else str (isolation))
		self.internal_sap_object_processing (key, True)
		self.objects['SAP'][key]['Window'].findById (opts['Field']).selectedNode = opts['Node']
		self.internal_sap_object_processing (key, False)
		return True, {'Status':'OK'}
	
	
	def step_sap_capture (self, running_steps, isolation, **opts):
		key = (isolation['Object.SAP'] if isinstance (isolation, dict) and 'Object.SAP' in isolation else str (isolation))
		self.internal_sap_object_processing (key, True)
		if 'Transaction' in opts and opts['Transaction'] is True:
			value = self.objects['SAP'][key]['Window'].Info.Transaction
		elif 'StatusBarText' in opts and opts['StatusBarText'] is True:
			value = self.objects['SAP'][key]['Window'].findById ("wnd[0]/sbar").text
		elif 'NumberFormat' in opts and opts['NumberFormat'] is True:
			value = self.objects['SAP'][key]['NumberFormat']
		elif 'DateFormat' in opts and opts['DateFormat'] is True:
			value = self.objects['SAP'][key]['DateFormat']
		elif 'Field.Text' in opts:
			value = self.objects['SAP'][key]['Window'].findById (opts['Field.Text']).text
		else:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_capture: Aborted', 'Message':'No capture logic was provided for the function.'}
			
		self.internal_sap_object_processing (key, False)
	
		if 'ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str):
			self.cls_steps.internal_value_set_value (isolation, 'Variable', value, opts['ReturnVariable'])
		if 'ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str):
			self.cls_steps.internal_value_set_value (None, 'Variable', value, opts['ReturnVariable.Global'])
		return True, {'Status':'OK', 'Data':value}
		
	
	def step_sap_check_text (self, running_steps, isolation, **opts):
		key = (isolation['Object.SAP'] if isinstance (isolation, dict) and 'Object.SAP' in isolation else str (isolation))
		valid = self.internal_step_sap_check_text (isolation, **opts)
		
		if valid is False and 'WhileFalse.Wait' in opts and isinstance (opts['WhileFalse.Wait'], (int, float)) and 'WhileFalse.Loops' in opts and isinstance (opts['WhileFalse.Loops'], int):
			loops = 1
			print ('WAIT_FALSE')
			wait = copy.deepcopy (opts['WhileFalse.Wait'])
			while valid is False and loops <= opts['WhileFalse.Loops']:
				print ('SLEEP_FALSE.' + str (loops) + '=' + str (wait))
				time.sleep (wait)
				loops += 1
				if 'WhileFalse.Steps' in opts and isinstance (opts['WhileFalse.Steps'], list):
					status, result = self.cls_steps.execute_steps (opts['WhileFalse.Steps'], isolation)
				if 'WhileFalse.Wait.Max' in opts and isinstance (opts['WhileFalse.Wait.Max'], (int, float)) and wait < opts['WhileFalse.Wait.Max'] and 'WhileFalse.Wait.Multiplier' in opts and isinstance (opts['WhileFalse.Wait.Multiplier'], (int, float)):
					wait *= opts['WhileFalse.Wait.Multiplier']
					if wait > opts['WhileFalse.Wait.Max']:
						wait = copy.deepcopy (opts['WhileFalse.Wait.Max'])
				valid = self.internal_step_sap_check_text (isolation, **opts)
		if valid is True and 'WhileTrue.Wait' in opts and isinstance (opts['WhileTrue.Wait'], (int, float)) and 'WhileTrue.Loops' in opts and isinstance (opts['WhileTrue.Loops'], int):
			loops = 1
			print ('WAIT_TRUE')
			wait = copy.deepcopy (opts['WhileTrue.Wait'])
			while valid is True and loops <= opts['WhileTrue.Loops']:
				print ('SLEEP_TRUE.' + str (loops) + '=' + str (wait))
				time.sleep (wait)
				loops += 1
				if 'WhileTrue.Steps' in opts and isinstance (opts['WhileTrue.Steps'], list):
					status, result = self.cls_steps.execute_steps (opts['WhileTrue.Steps'], isolation)
				if 'WhileTrue.Wait.Max' in opts and isinstance (opts['WhileTrue.Wait.Max'], (int, float)) and wait < opts['WhileTrue.Wait.Max'] and 'WhileTrue.Wait.Multiplier' in opts and isinstance (opts['WhileTrue.Wait.Multiplier'], (int, float)):
					wait *= opts['WhileTrue.Wait.Multiplier']
					if wait > opts['WhileTrue.Wait.Max']:
						wait = copy.deepcopy (opts['WhileTrue.Wait.Max'])
				valid = self.internal_step_sap_check_text (isolation, **opts)
		
		if valid is None:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_check_text: Aborted', 'Message':'No valid check was found with the opts=\n' + str (opts)}
		if valid is True and 'OnTrue' in opts and isinstance (opts['OnTrue'], list):
			for step in reversed (opts['OnTrue']):
				running_steps.insert (0, step)
		elif valid is False and 'OnFalse' in opts and isinstance (opts['OnFalse'], list):
			for step in reversed (opts['OnFalse']):
				running_steps.insert (0, step)
		return True, {'Status':'OK', 'Data':valid}
		
	
	def step_sap_labellist_search (self, running_steps, isolation, **opts):
		key = (isolation['Object.SAP'] if isinstance (isolation, dict) and 'Object.SAP' in isolation else str (isolation))
		self.internal_sap_object_processing (key, True)
		try:
			for irow in range (opts['Label.RowStart'], 9999):
				if self.objects['SAP'][key]['Window'].findById (opts['Label'] + '[' + str (opts['Label.Column']) + ',' + str (irow) + ']').Text == opts['Search.Value']:
					if 'ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str):
						self.cls_steps.internal_value_set_value (isolation, 'Variable', irow, opts['ReturnVariable'])
					if 'ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str):
						self.cls_steps.internal_value_set_value (None, 'Variable', irow, opts['ReturnVariable.Global'])
					self.internal_sap_object_processing (key, False)
					return True, {'Status':'OK', 'Data':irow}
		except:
			self.internal_sap_object_processing (key, False)
			if irow == opts['Label.RowStart']:
				return False, {'Status':'CRASH', 'Title':'SCRIPTING:step_sap_labellist_search: Crashed', 'Message':'The label list "' + opts['Label'] + '[' + str (opts['Label.Column']) + ',' + str (irow) + ']" couldn\'t be found.'}
			print ('CRASH=' + str (irow))
			return False, False
	
	
	def step_sap_screen_capture (self, running_steps, isolation, **opts):
		key = (isolation['Object.SAP'] if isinstance (isolation, dict) and 'Object.SAP' in isolation else str (isolation))
		if 'Window' in opts:
			if not isinstance (opts['Window'], int):
				return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_screen_capture: Aborted', 'Message':'Window needs to be an integer value.'}
			windows = [opts['Window']]
		elif 'Windows' in opts:
			if not isinstance (opts['Windows'], list):
				return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_screen_capture: Aborted', 'Message':'Windows needs to be a list of integer values.'}
			for window in opts['Windows']:
				if not isinstance (window, int):
					return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_screen_capture: Aborted', 'Message':'Windows needs to be a list of integer values.'}
			windows = opts['Windows']
		elif 'Windows.All' in opts and opts['Windows.All'] is True:
			windows = []
			for window in range (0, 999):
				if self.objects['SAP'][key]['Window'].findByID ('wnd[' + str (window) + ']'):
					windows.append (window)
			if len (windows) == 0:
				return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_screen_capture: Aborted', 'Message':'No active windows found.'}
		else:
			return False, {'Status':'WARNING', 'Title':'SCRIPTING:step_sap_screen_capture: Aborted', 'Message':'No source Window or Windows was provided.'}
		
		images = {}
		for window in windows:
			self.internal_sap_object_processing (key, True)
			images[window] = self.objects['SAP'][key]['Window'].findByID ('wnd[' + str (window) + ']').HardCopyToMemory (2)
			self.internal_sap_object_processing (key, False)
		if 'File' in opts:
			files = []
			for window in images.keys ():
				file = opts['File'].replace ('%Window%', str (window))
				fp = open (file, "wb")
				fp.write (images[window])
				fp.close ()
				files.append (file)
		if 'ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str):
			self.cls_steps.internal_value_set_value (isolation, 'Variable', (images[opts['Window']] if 'Window' in opts else images), opts['ReturnVariable'])
		if 'ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str):
			self.cls_steps.internal_value_set_value (None, 'Variable', (images[opts['Window']] if 'Window' in opts else images), opts['ReturnVariable.Global'])
		
		if 'File' in opts:
			return True, {'Status':'OK', 'Data':files}
		else:
			return True, {'Status':'OK'}
			
	
	def internal_step_sap_check_text (self, isolation, **opts):
		key = (isolation['Object.SAP'] if isinstance (isolation, dict) and 'Object.SAP' in isolation else str (isolation))
		debug_console = (True if 'Debug.Console' in opts and opts['Debug.Console'] is True else False)
		if debug_console is True:
			print ('\t===[ Console debug.init: internal_step_sap_check_text ]=========================')
			for field in ['Field', 'Text', 'Verify']:
				if field in opts:
					print ('\tOPTS.' + str (field) + '=' + str (opts[field]))
		self.internal_sap_object_processing (key, True)
		text = self.objects['SAP'][key]['Window'].findById (opts['Field']).text
		self.internal_sap_object_processing (key, False)
		valid = None
		if 'Verify' in opts and isinstance (opts['Verify'], dict):
			valid, result = datahandling_verify (text, **opts['Verify'])
			if debug_console is True:
				print ('\tVERIFY_VALID=' + str (valid))
				print ('\tVERIFY_RESULT=' + str (result))
		elif 'Text' in opts:
			if opts['Text'] in text:
				valid = True
			else:
				valid = False
		if debug_console is True:
			print ('\tTEXT=' + str (text))
			print ('\tVALID=' + str (valid))
			print ('\t===[ Console debug.end: internal_step_sap_check_text ]==========================')
		return valid
	
	
	def internal_date_number_format (self, data, sapkey):
		if isinstance (data, dict):
			for key in data.keys ():
				data[key] = self.internal_date_number_format (data[key], sapkey)
		elif isinstance (data, list):
			for key in range (0, len (data)):
				data[key] = self.internal_date_number_format (data[key], sapkey)
		elif isinstance (data, str) and len (data) > 1 and data[0] == '<' and '>' in data:
			if data.startswith ('<DATETIME>'):
				if len (data) == 29 and data[14] + data[17] + data[20] + data[23] + data[26] == '-- ::':
					date = data[10:20].split ('-')
					data = self.objects['SAP'][sapkey]['DateFormat'].replace ('YYYY', date[0]).replace ('MM', date[1]).replace ('DD', date[2]) + data[20:]
				else:
					print ('UNKNOWN_DATE_FORMAT::' + str (self.objects['SAP'][sapkey]['DateFormat']) + '::' + str (data))
					data = data[10:]
			elif data.startswith ('<DATE>'):
				if len (data) == 16 and data[10] + data[13] == '--':
					date = data[6:].split ('-')
					data = self.objects['SAP'][sapkey]['DateFormat'].replace ('YYYY', date[0]).replace ('MM', date[1]).replace ('DD', date[2])
				else:
					print ('UNKNOWN_DATE_FORMAT::' + str (self.objects['SAP'][sapkey]['DateFormat']) + '::' + str (data))
					data = data[6:]
			elif data.startswith ('<NUMERIC>'):
				number = (float (data[9:]) if '.' in data else int (data[9:]))
				if self.objects['SAP'][sapkey]['NumberFormat'] == 'X,XXX,XXX.XX':
					data = str ('{:,}'.format (number))
				elif self.objects['SAP'][sapkey]['NumberFormat'] == 'X.XXX.XXX,XX':
					data = str ('{:,}'.format (number)).replace ('.', '#').replace (',', '.').replace ('#', ',')
				elif self.objects['SAP'][sapkey]['NumberFormat'] == 'X XXX XXX,XX':
					data = str ('{:,}'.format (number)).replace(',', ' ').replace ('.', ',')
				else:
					print ('UNKNOWN_NUMBER_FORMAT::' + str (self.objects['SAP'][sapkey]['NumberFormat']) + '::' + str (data))
					data = data[9:]
			else:
				print ('UNKNOWN_REPLACE?=' + str (data))
		return data
	
	
	def internal_sap_object_processing (self, key, processing):
		if key in self.objects['SAP']:
			self.objects['SAP']['Processing'] = processing
			self.objects['SAP']['LastAction'] = round (datetime.datetime.now ().timestamp (), 3)
		