# Copyright (c) 2025-2026 Erik Persson
# Licensed for free use only. Copying, modification, or redistribution prohibited.

import builtins
from Functions.Common import *
from Functions.DataHandling import *
for name in dir ():
    if not name.startswith ("_"):
        builtins.__dict__[name] = globals ()[name]
import tkinter
builtins.tkinter = tkinter
import tk
builtins.tk = tk
import customtkinter
builtins.customtkinter = customtkinter
import tksheet
builtins.tksheet = tksheet
import copy
builtins.copy = copy
import datetime
builtins.datetime = datetime
import calendar
builtins.calendar = calendar
import pathlib
builtins.pathlib = pathlib
import threading
builtins.threading = threading

class GUI:
	default_fields = {
		'Button':['fg_color', 'bg_color', 'border_color'],
		'Entry':['fg_color', 'bg_color', 'border_color'],
		'TextBox':['fg_color', 'bg_color', 'border_color'],
		'Label':['fg_color', 'bg_color'],
		'CheckBox':['fg_color', 'bg_color'],
		'ComboBox':['fg_color', 'bg_color'],
		'DatePicker':['fg_color'],
		'Frame':['fg_color'],
	}
	object_fields = {
		'Background':{
			'Entry':'fg_color',
			'DatePicker':'fg_color',
			'CheckBox':'bg_color',
		},
		'Background.Checkbox':{
			'CheckBox':'fg_color',
		},
		'Width':{
			'Entry':'width',
		},
		'Height':{
			'Entry':'height',
		},
		'Border.Color':{
			'Entry':'border_color',
		},
	}
	
	def __init__ (self, cls_steps):
		super ().__init__ ()
		self.startpos = None
		self.running = None			# Keeps track of if mainloop is running
		self.running_init = True	# True if mainloop hasn't been started
		self.cls_steps = cls_steps
		self.objects = {
			'Form':customtkinter.CTk (),
			'Button':{},
			'Entry':{},
			'Label':{},
			'CheckBox':{},
			'ComboBox':{},
			'DatePicker':{},
			'Frame':{},
			'TextBox':{},
			'Treeview':{},
			'Table':{},
			'WindowForm':{},
			'ProgressBar':{},
		}
		self.defaults = {
			'Form':None,
			'Positions':{},
		}
	
	
	def dynamic_function (self, function, to_class = True):
		if to_class is True:
			func = {}
			exec (function['Code'], func)
			setattr (GUI, function['Function'], func[function['Function']])
		else:
			exec (function['Code'], globals ())
			builtins.__dict__[function['Function']] = globals ()[function['Function']]
	
	
	def start (self):
		if self.running is not None:
			self.running = True
			self.running_init = False
			print ('MAIN_LOOP_START')
			self.objects['Form'].mainloop ()
			print ('MAIN_LOOP_END')
	
	
	def execute (self, isolation = None, **opts):
#		print (opts)
#		print ('Running=' + str (self.running) + '::' + str (self.running_init))
		try:
			if self.running is False and self.running_init is False:
				print ('SKIP_GUI')
				return False, {'Status':'WARNING', 'Title':'GUI:execute: Aborted', 'Message':'GUI shutdown, skipping step=' + str (opts)}
			
			if opts['Function'].endswith ('.Add') and not opts['Function'].endswith ('Form.Add'):
				for check_field in ['Placement.Row', 'Placement.Column']:
					if check_field not in opts:
						return False, {'Status':'WARNING', 'Title':'GUI:execute: Aborted', 'Message':'The function "' + str (opts['Function']) + '" requires a valid "' + str (check_field) + '" field.'}
					elif not isinstance (opts[check_field], int):
						valid = False
						if isinstance (opts[check_field], str):
							if opts[check_field].count ('%') >= 2:
								valid, value = self.internal_calculate_position (opts[check_field])
								if valid is False:
									return False, {'Status':'WARNING', 'Title':'GUI:execute: Aborted', 'Message':'The function "' + str (opts['Function']) + '" requires a valid "' + str (check_field) + '" value ("' + str (opts[check_field]) + '" returned "' + str (value) + '").'}
								else:
									opts[check_field] = value
							elif '+' in opts[check_field]:
								valid, value = zyd_calc (opts[check_field])
								if valid is False or not isinstance (value, int):
									return False, {'Status':'WARNING', 'Title':'GUI:execute: Aborted', 'Message':'The function "' + str (opts['Function']) + '" requires a valid "' + str (check_field) + '" calc value ("' + str (opts[check_field]) + '" returned "' + str (value) + '").'}
								else:
									opts[check_field] = value
						if valid is False:
							return False, {'Status':'WARNING', 'Title':'GUI:execute: Aborted', 'Message':'The function "' + str (opts['Function']) + '" requires a valid "' + str (check_field) + '" value.'}
				for check_field in ['Placement.Colspan', 'Placement.Rowspan']:
					if check_field in opts and not isinstance (opts[check_field], int):
						return False, {'Status':'WARNING', 'Title':'GUI:execute: Aborted', 'Message':'The function "' + str (opts['Function']) + '" requires a valid "' + str (check_field) + '" value.'}
				if 'Placement.Alignment' in opts and isinstance (opts['Placement.Alignment'], str) and opts['Placement.Alignment'] not in ['E', 'N', 'S', 'W', 'NW', 'NE', 'SE', 'SW']:
					return False, {'Status':'WARNING', 'Title':'GUI:execute: Aborted', 'Message':'The function "' + str (opts['Function']) + '" requires a valid "Placement.Alignment" value.'}
				
			if opts['Function'] == 'GUI:Form':
				return self.step_form (isolation, **opts)
			elif opts['Function'] == 'GUI:Exit':
				return self.step_exit (isolation, **opts)
			elif opts['Function'] == 'GUI:Button.Add':
				return self.step_button_add (isolation, **opts)
			elif opts['Function'] == 'GUI:Button.Change':
				return self.step_button_change (isolation, **opts)
			elif opts['Function'] == 'GUI:Entry.Add':
				return self.step_entry_add (isolation, **opts)
			elif opts['Function'] == 'GUI:Entry.Change':
				return self.step_entry_change (isolation, **opts)
			elif opts['Function'] == 'GUI:Label.Add':
				return self.step_label_add (isolation, **opts)
			elif opts['Function'] == 'GUI:Label.Change':
				return self.step_label_change (isolation, **opts)
			elif opts['Function'] == 'GUI:CheckBox.Add':
				return self.step_checkbox_add (isolation, **opts)
			elif opts['Function'] == 'GUI:CheckBox.Change':
				return self.step_checkbox_change (isolation, **opts)
			elif opts['Function'] == 'GUI:ComboBox.Add':
				return self.step_combobox_add (isolation, **opts)
			elif opts['Function'] == 'GUI:DatePicker.Add':
				return self.step_datepicker_add (isolation, **opts)
			elif opts['Function'] == 'GUI:DatePicker.Change':
				return self.step_datepicker_change (isolation, **opts)
			elif opts['Function'] == 'GUI:Frame.Add':
				return self.step_frame_add (isolation, **opts)
			elif opts['Function'] == 'GUI:Frame.Change':
				return self.step_frame_change (isolation, **opts)
			elif opts['Function'] == 'GUI:TextBox.Add':
				return self.step_textbox_add (isolation, **opts)
			elif opts['Function'] == 'GUI:TextBox.Change':
				return self.step_textbox_change (isolation, **opts)
			elif opts['Function'] == 'GUI:Treeview.Add':
				return self.step_treeview_add (isolation, **opts)
			elif opts['Function'] == 'GUI:Treeview.Change':
				return self.step_treeview_change (isolation, **opts)
			elif opts['Function'] == 'GUI:Table.Add':
				return self.step_table_add (isolation, **opts)
			elif opts['Function'] == 'GUI:Table.Change':
				return self.step_table_change (isolation, **opts)
			elif opts['Function'] == 'GUI:WindowForm.Add':
				return self.step_windowform_add (isolation, **opts)
			elif opts['Function'] == 'GUI:WindowForm.Change':
				return self.step_windowform_change (isolation, **opts)
			elif opts['Function'] == 'GUI:ProgressBar.Add':
				return self.step_progressbar_add (isolation, **opts)
			elif opts['Function'] == 'GUI:ProgressBar.Change':
				return self.step_progressbar_change (isolation, **opts)
			elif opts['Function'] == 'GUI:InputDialog.Action':
				return self.step_inputdialog_action (isolation, **opts)
			elif opts['Function'] == 'GUI:FileDialog.Action':
				return self.step_filedialog_action (isolation, **opts)
			elif opts['Function'] == 'GUI:Values.Export':
				return self.step_values_export (isolation, **opts)
			elif opts['Function'] == 'GUI:Values.Import':
				return self.step_values_import (isolation, **opts)
			elif opts['Function'] == 'GUI:Objects.Count':
				return self.step_objects_count (isolation, **opts)
			elif opts['Function'] == 'GUI:Defaults':
				return self.step_defaults (isolation, **opts)
			else:
				return False, {'Status':'WARNING', 'Title':'GUI:execute: Aborted', 'Message':'Unknown execute:' + str (opts)}
		except Exception as e:
			st = internal_zyd_stacktrace (e, FunctionOpts=opts)
			return False, {'Status':'CRASH', 'Title':'GUI:execute: Crashed', 'Message':'Crashed with the error: ' + str (e) + ' for step:\n' + str (opts), 'StackTrace':st}
	
	
	def step_values_export (self, isolation, **opts):
		data = []
		for objecttype in self.objects.keys ():
			if isinstance (self.objects[objecttype], dict):
				for object in self.objects[objecttype].keys ():
					if 'Value' in self.objects[objecttype][object]:
						data.append ({'Type':objecttype, 'ID':object, 'Value':copy.deepcopy (self.objects[objecttype][object]['Value'])})
		
		if 'ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str):
			self.cls_steps.internal_value_set_value (isolation, 'Variable', data, opts['ReturnVariable'])
		if 'ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str):
			self.cls_steps.internal_value_set_value (None, 'Variable', data, opts['ReturnVariable.Global'])
		return True, {'Status':'OK', 'Data':data}


	def step_values_import (self, isolation, **opts):
		if 'Data' not in opts:
			return False, {'Status':'WARNING', 'Title':'GUI:step_values_import: Aborted', 'Message':'No Data provided.'}
		elif not isinstance (opts['Data'], list):
			return False, {'Status':'WARNING', 'Title':'GUI:step_values_import: Aborted', 'Message':'Data needs to be a List.'}
		
		for entry in opts['Data']:
			self.internal_object_update (isolation, entry['Type'] + "##" + entry['ID'], **{"Value":(entry['Value'] if entry['Value'] is not None else ''), "Trigger":(True if 'Trigger' in opts and opts['Trigger'] is True else False)})
		
		return True, {'Status':'OK'}

	
	def step_form (self, isolation, **opts):
		if 'Geometry' in opts:
			self.objects['Form'].geometry (opts['Geometry'] + ('+' + self.startpos if self.startpos is not None else ''))
		elif self.startpos is not None:
			self.objects['Form'].geometry ('+' + self.startpos)
		if 'Title' in opts:
			self.objects['Form'].title (opts['Title'])
		if ('Resizable.Width' in opts and opts['Resizable.Width'] is False) or ('Resizable.Height' in opts and opts['Resizable.Height'] is False):
			self.objects['Form'].resizable ((False if 'Resizable.Width' in opts and opts['Resizable.Width'] is False else True), (False if 'Resizable.Height' in opts and opts['Resizable.Height'] is False else True))
		self.objects['Form'].protocol ("WM_DELETE_WINDOW", lambda: self.step_exit (isolation))
		self.running = False
		self.defaults['Form'] = ['Form']
		return True, {'Status':'OK'}
	
	
	def step_exit (self, isolation, **opts):
		self.cls_steps.stop ()
		if self.running is True:
#			for job in self.objects['Form'].tk.call ("after", "info"):
#				print ('CANCEL_JOB=' + str (job))
#				try:
#					self.objects['Form'].after_cancel (job)
#				except Exception:
#					print ('FAILED')
#					pass
#			print ('MainForm.DESTROY')
			self.objects['Form'].quit ()
			self.objects['Form'].destroy ()
#			print ('MainForm.DESTROYED')
		self.running = False
		return True, {'Status':'OK'}
	
	
	
	def step_table_add (self, isolation, **opts):
		if 'ID' not in opts:
			return False, {'Status':'WARNING', 'Title':'GUI:step_table_add: Aborted', 'Message':'No ID provided.'}
		if opts['ID'] in self.objects['Table']:
			return False, {'Status':'WARNING', 'Title':'GUI:step_table_add: Aborted', 'Message':'The Table "' + str (opts['ID']) + '" already exists.'}
		if 'Table.Data' not in opts:
			return False, {'Status':'WARNING', 'Title':'GUI:step_table_add: Aborted', 'Message':'The table requires a Table.Data value.'}
		elif not isinstance (opts['Table.Data'], list):
			return False, {'Status':'WARNING', 'Title':'GUI:step_table_add: Aborted', 'Message':'The Table.Data input is requireing a list.'}
		else:
			for value in opts['Table.Data']:
				if not isinstance (value, list):
					return False, {'Status':'WARNING', 'Title':'GUI:step_table_add: Aborted', 'Message':'The Table.Data input is requireing a 2D list.'}
		
		data = copy.deepcopy (opts['Table.Data'])
		table_opts = {
			'data':data,
#			'theme':'dark',
		}
		if 'Table.Width' in opts and isinstance (opts['Table.Width'], int):
			table_opts['width'] = opts['Table.Width']
		if 'Table.Height' in opts and isinstance (opts['Table.Height'], int):
			table_opts['height'] = opts['Table.Height']
		table = tksheet.Sheet (self.internal_form ('Object', **opts), **table_opts)
		table.enable_bindings ("all", "edit_index", "edit_header")
		if 'Table.Opts' in opts and isinstance (opts['Table.Opts'], dict):
			for option in opts['Table.Opts'].keys ():
				if self.internal_step_table_valid_table_options (option) is False:
					return False, {'Status':'WARNING', 'Title':'GUI:step_table_change: Aborted', 'Message':'The Table.Opts key "' + str (option) + '" is not valid.'}
			table.set_options (**opts['Table.Opts'])
			table.refresh ()
		
		self.internal_grid (isolation, table, **opts)
		self.objects['Table'][opts['ID']] = {'Object':table, 'Value':data, 'Form':self.internal_form ('Form', **opts)}

		return True, {'Status':'OK'}


	def step_table_change (self, isolation, **opts):
		if 'ID' not in opts:
			return False, {'Status':'WARNING', 'Title':'GUI:step_table_change: Aborted', 'Message':'No ID provided.'}
		if opts['ID'] not in self.objects['Table']:
			return False, {'Status':'WARNING', 'Title':'GUI:step_table_change: Aborted', 'Message':'The Table "' + str (opts['ID']) + '" does not exist.'}
		if 'Table.Data' in opts:
			if not isinstance (opts['Table.Data'], list):
				return False, {'Status':'WARNING', 'Title':'GUI:step_table_change: Aborted', 'Message':'The Table.Data input is requireing a list.'}
			else:
				for value in opts['Table.Data']:
					if not isinstance (value, list):
						return False, {'Status':'WARNING', 'Title':'GUI:step_table_change: Aborted', 'Message':'The Table.Data input is requireing a 2D list.'}
			self.objects['Table'][opts['ID']]['Value'] = copy.deepcopy (opts['Table.Data'])
			self.objects['Table'][opts['ID']]['Object'].set_sheet_data (data=self.objects['Table'][opts['ID']]['Value'], reset_col_positions=True, reset_row_positions=True, redraw=True)
		if 'Table.Width' in opts and isinstance (opts['Table.Width'], int) and 'Table.Height' in opts and isinstance (opts['Table.Height'], int):
			self.objects['Table'][opts['ID']]['Object'].height_and_width (height=opts['Table.Height'], width=opts['Table.Width'])
		if 'Table.Opts' in opts and isinstance (opts['Table.Opts'], dict):
			for option in opts['Table.Opts'].keys ():
				if self.internal_step_table_valid_table_options (option) is False:
					return False, {'Status':'WARNING', 'Title':'GUI:step_table_change: Aborted', 'Message':'The Table.Opts key "' + str (option) + '" is not valid.'}
			self.objects['Table'][opts['ID']]['Object'].set_options (**opts['Table.Opts'])
			self.objects['Table'][opts['ID']]['Object'].refresh ()
		if 'Table.Debug.Set_Options' in opts and isinstance (opts['Table.Debug.Set_Options'], dict):
			self.objects['Table'][opts['ID']]['Object'].set_options (**opts['Table.Debug.Set_Options'])
			self.objects['Table'][opts['ID']]['Object'].refresh ()
			
		return True, {'Status':'OK'}
	
	
	def internal_step_table_valid_table_options (self, option):
		if option in ['top_left_bg', 'top_left_fg', 'header_bg', 'header_fg', 'index_bg', 'index_fg', 'table_bg', 'table_fg']:
			return True
		return False
	
	
	def step_treeview_add (self, isolation, **opts):
		if 'ID' not in opts:
			return False, {'Status':'WARNING', 'Title':'GUI:step_treeview_add: Aborted', 'Message':'No ID provided.'}
		if opts['ID'] in self.objects['Treeview']:
			return False, {'Status':'WARNING', 'Title':'GUI:step_treeview_add: Aborted', 'Message':'The Treeview "' + str (opts['ID']) + '" already exists.'}
		if 'Columns' not in opts:
			return False, {'Status':'WARNING', 'Title':'GUI:step_treeview_add: Aborted', 'Message':'No Columns provided.'}

		treeview = tkinter.ttk.Treeview (self.internal_form ('Object', **opts))
		self.objects['Treeview'][opts['ID']] = {'Object':treeview, 'Type':'2D', 'Tree':{}, 'Form':self.internal_form ('Form', **opts)}

		bg_color = self.internal_form ('Object', **opts)._apply_appearance_mode (customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"])
		text_color = self.internal_form ('Object', **opts)._apply_appearance_mode (customtkinter.ThemeManager.theme["CTkLabel"]["text_color"])
		selected_color = self.internal_form ('Object', **opts)._apply_appearance_mode (customtkinter.ThemeManager.theme["CTkButton"]["fg_color"])
		treestyle = tkinter.ttk.Style ()
		treestyle.theme_use ('default')
		treestyle.configure ("Treeview", background=bg_color, foreground=text_color, fieldbackground=bg_color, borderwidth=0)
		treestyle.map ('Treeview', background=[('selected', bg_color)], foreground=[('selected', selected_color)])
		
		treeview.configure (columns=list (range (1, len (opts['Columns']))))
		for columnid in range (0, len (opts['Columns'])):
			column = opts['Columns'][columnid]
			column_opts = {}
			heading_opts = {
				'text':column['Title']
			}
			if 'Alignment' in column:
				heading_opts['anchor'] = column['Alignment'].lower ()
			if 'Width' in column and isinstance (column['Width'], int):
				column_opts['width'] = column['Width']
			if 'Width.Min' in column and isinstance (column['Width.Min'], int):
				column_opts['minwidth'] = column['Width.Min']
			treeview.column ("#" + str (columnid), **column_opts)
			treeview.heading ("#" + str (columnid), **heading_opts)
		self.internal_object_configure (isolation, 'Treeview', self.objects['Treeview'][opts['ID']], 'Object', **opts)

		if 'Tree' in opts and isinstance (opts['Tree'], list):
			result = self.internal_treeview_configure (isolation, opts['ID'], opts['Tree'])
			if result is not None:
				return False, result
		
		self.internal_grid (isolation, treeview, **opts)
		return True, {'Status':'OK'}
	
	
	def step_treeview_change (self, isolation, **opts):
		if 'ID' not in opts:
			return False, {'Status':'WARNING', 'Title':'GUI:step_treeview_change: Aborted', 'Message':'No ID provided.'}
		elif opts['ID'] not in self.objects['Treeview']:
			return False, {'Status':'WARNING', 'Title':'GUI:step_treeview_change: Aborted', 'Message':'The Treeview "' + str (opts['ID']) + '" doesn\'t exist.'}

		if 'Tree' in opts:
			result = self.internal_treeview_configure (isolation, opts['ID'], opts['Tree'])
			if result is not None:
				return False, result
		return True, {'Status':'OK'}
	
	
	def internal_treeview_configure (self, isolation, object, changes, **opts):
		if object not in self.objects['Treeview']:
			return {'Status':'WARNING', 'Title':'GUI:internal_treeview_configure: Aborted', 'Message':'The Treeview "' + str (object) + '" does not exist.'}
		
		for change in changes:
			tree_opts = {}
			if change['Action'] == 'Add.1D':
				if self.objects['Treeview'][object]['Type'] == '2D':
					tree_opts['text'] = change['Key1D']
					if 'Values' in change and isinstance (change['Values'], list):
						tree_opts['values'] = change['Values']
					if 'Open' in change and isinstance (change['Open'], bool):
						tree_opts['open'] = change['Open']
					self.objects['Treeview'][object]['Tree'][change['Key1D']] = {'Key':self.objects['Treeview'][object]['Object'].insert ('', tkinter.END, **tree_opts), 'Tree':{}}
			elif change['Action'] == 'Change.1D':
				if self.objects['Treeview'][object]['Type'] == '2D':
					if 'Values' in change and isinstance (change['Values'], list):
						tree_opts['values'] = change['Values']
					if 'Open' in change and isinstance (change['Open'], bool):
						tree_opts['open'] = change['Open']
					self.objects['Treeview'][object]['Object'].item (self.objects['Treeview'][object]['Tree'][change['Key1D']]['Key'], **tree_opts)
			elif change['Action'] == 'Add.2D':
				if self.objects['Treeview'][object]['Type'] == '2D':
					tree_opts['text'] = change['Key2D']
					if 'Values' in change and isinstance (change['Values'], list):
						tree_opts['values'] = change['Values']
					self.objects['Treeview'][object]['Tree'][change['Key1D']]['Tree'][change['Key2D']] = {'Key':self.objects['Treeview'][object]['Object'].insert (self.objects['Treeview'][object]['Tree'][change['Key1D']]['Key'], tkinter.END, **tree_opts), 'Tree':{}}
			elif change['Action'] == 'Change.2D':
				if self.objects['Treeview'][object]['Type'] == '2D':
					if 'Values' in change and isinstance (change['Values'], list):
						tree_opts['values'] = change['Values']
					self.objects['Treeview'][object]['Object'].item (self.objects['Treeview'][object]['Tree'][change['Key1D']]['Tree'][change['Key2D']]['Key'], **tree_opts)
	
	
	def step_button_add (self, isolation, **opts):
		if 'ID' not in opts:
			return False, {'Status':'WARNING', 'Title':'GUI:step_button_add: Aborted', 'Message':'No ID provided.'}
		if opts['ID'] in self.objects['Button']:
			return False, {'Status':'WARNING', 'Title':'GUI:step_button_add: Aborted', 'Message':'The button "' + str (opts['ID']) + '" already exists.'}
		button = customtkinter.CTkButton (self.internal_form ('Object', **opts), command=lambda: self.internal_button_event (isolation, opts['ID']))
		self.internal_grid (isolation, button, **opts)
		defaults = {}
		for field in self.default_fields['Button']:
			defaults[field] = button.cget (field)
		self.objects['Button'][opts['ID']] = {'Object':button, 'Defaults':defaults, 'Form':self.internal_form ('Form', **opts)}
		if 'OnClick' in opts:
			self.objects['Button'][opts['ID']]['OnClick'] = opts['OnClick']
		self.internal_object_configure (isolation, 'Button', self.objects['Button'][opts['ID']], 'Object', **opts)
		return True, {'Status':'OK'}
	
	
	def step_button_change (self, isolation, **opts):
		if 'IDs' in opts and isinstance (opts['IDs'], list):
			for ID in opts['IDs']:
				if ID in self.objects['Button']:
					self.internal_object_configure (isolation, 'Button', self.objects['Button'][ID], 'Object', **opts)
				else:
					return False, {'Status':'WARNING', 'Title':'GUI:step_button_change: Aborted', 'Message':'No button ID named "' + str (ID) + '" exists.'}
			if 'Refresh' in opts and opts['Refresh'] is True:
				self.internal_form ('Object', **opts).update ()
			return True, {'Status':'OK'}
		elif 'ID' in opts and opts['ID'] in self.objects['Button']:
			self.internal_object_configure (isolation, 'Button', self.objects['Button'][opts['ID']], 'Object', **opts)
			if 'Refresh' in opts and opts['Refresh'] is True:
				self.internal_form ('Object', **opts).update ()
			return True, {'Status':'OK'}
		elif 'ID' in opts:
			return False, {'Status':'WARNING', 'Title':'GUI:step_button_change: Aborted', 'Message':'No button ID named "' + str (opts['ID']) + '" exists.'}
		else:
			return False, {'Status':'WARNING', 'Title':'GUI:step_button_change: Aborted', 'Message':'No button ID or IDs provided for the function.'}
	
	
	def step_entry_add (self, isolation, **opts):
		entry = customtkinter.CTkEntry (self.internal_form ('Object', **opts))
		self.internal_grid (isolation, entry, **opts)
		entry.bind ('<KeyRelease>', lambda event: self.internal_entry_event (isolation, opts['ID']), add='+')
		entry.bind ('<Tab>', lambda event: self.internal_entry_event (isolation, opts['ID']), add='+')
		entry.bind ('<Leave>', lambda event: self.internal_entry_event (isolation, opts['ID']), add='+')
		
		defaults = {}
		for field in self.default_fields['Entry']:
			defaults[field] = entry.cget (field)
		self.objects['Entry'][opts['ID']] = {'Object': entry, 'Value':(opts['Value'] if 'Value' in opts else ''), 'Defaults':defaults, 'Form':self.internal_form ('Form', **opts)}
		
		self.internal_object_configure (isolation, 'Entry', self.objects['Entry'][opts['ID']], 'Object', **opts)
		
		if 'OnChange' in opts:
			self.objects['Entry'][opts['ID']]['OnChange'] = opts['OnChange']
		return True, {'Status':'OK'}


	def step_entry_change (self, isolation, **opts):
		if 'IDs' in opts and isinstance (opts['IDs'], list):
			for ID in opts['IDs']:
				if ID in self.objects['Entry']:
					if 'Value' in opts and 'OnChange.Trigger' in opts and opts['OnChange.Trigger'] is True:
						value = copy.deepcopy (self.objects['Entry'][ID]['Value'])
					self.internal_object_configure (isolation, 'Entry', self.objects['Entry'][ID], 'Object', **opts)
					if 'Value' in opts and 'OnChange.Trigger' in opts and opts['OnChange.Trigger'] is True:
						self.internal_entry_event (isolation, ID, (True if value != opts['Value'] else False))
				else:
					return False, {'Status':'WARNING', 'Title':'GUI:step_entry_change: Aborted', 'Message':'No entry ID named "' + str (ID) + '" exists.'}
			return True, {'Status':'OK'}
		elif 'ID' in opts and opts['ID'] in self.objects['Entry']:
			if 'Value' in opts and 'OnChange.Trigger' in opts and opts['OnChange.Trigger'] is True:
				value = copy.deepcopy (self.objects['Entry'][opts['ID']]['Value'])
			self.internal_object_configure (isolation, 'Entry', self.objects['Entry'][opts['ID']], 'Object', **opts)
			if 'Value' in opts and 'OnChange.Trigger' in opts and opts['OnChange.Trigger'] is True:
				self.internal_entry_event (isolation, opts['ID'], (True if value != opts['Value'] else False))
			return True, {'Status':'OK'}
		elif 'ID' in opts:
			return False, {'Status':'WARNING', 'Title':'GUI:step_entry_change: Aborted', 'Message':'No entry ID named "' + str (opts['ID']) + '" exists.'}
		else:
			return False, {'Status':'WARNING', 'Title':'GUI:step_entry_change: Aborted', 'Message':'No entry ID or IDs provided for the function.'}
	
	
	def step_textbox_add (self, isolation, **opts):
		textbox = customtkinter.CTkTextbox (self.internal_form ('Object', **opts))
		self.internal_grid (isolation, textbox, **opts)
		textbox.bind ('<KeyRelease>', lambda event: self.internal_textbox_event (isolation, opts['ID']), add='+')
		textbox.bind ('<Tab>', lambda event: self.internal_textbox_event (isolation, opts['ID']), add='+')
		textbox.bind ('<Leave>', lambda event: self.internal_textbox_event (isolation, opts['ID']), add='+')
		if 'Value' in opts:
			if isinstance (opts['Value'], str):
				textbox.insert ("0.0", opts['Value'])
			else:
				return False, {'Status':'WARNING', 'Title':'GUI:step_textbox_add: Aborted', 'Message':'Value has to be a string (not "' + str (type (opts['Value'])) + '").'}
		
		defaults = {}
		for field in self.default_fields['TextBox']:
			defaults[field] = textbox.cget (field)
		self.objects['TextBox'][opts['ID']] = {'Object': textbox, 'Value':(opts['Value'] if 'Value' in opts else ''), 'Defaults':defaults, 'Form':self.internal_form ('Form', **opts)}
		
		self.internal_object_configure (isolation, 'TextBox', self.objects['TextBox'][opts['ID']], 'Object', **opts)
		
		if 'OnChange' in opts:
			self.objects['TextBox'][opts['ID']]['OnChange'] = opts['OnChange']
		return True, {'Status':'OK'}


	def step_textbox_change (self, isolation, **opts):
		if 'IDs' in opts and isinstance (opts['IDs'], list):
			for ID in opts['IDs']:
				if ID in self.objects['TextBox']:
					if 'Value' in opts and 'OnChange.Trigger' in opts and opts['OnChange.Trigger'] is True:
						value = copy.deepcopy (self.objects['TextBox'][ID]['Value'])
					self.internal_object_configure (isolation, 'TextBox', self.objects['TextBox'][ID], 'Object', **opts)
					if 'Value' in opts and 'OnChange.Trigger' in opts and opts['OnChange.Trigger'] is True:
						self.internal_textbox_event (isolation, ID, (True if value != opts['Value'] else False))
				else:
					return False, {'Status':'WARNING', 'Title':'GUI:step_textbox_change: Aborted', 'Message':'No TextBox ID named "' + str (ID) + '" exists.'}
			return True, {'Status':'OK'}
		elif 'ID' in opts and opts['ID'] in self.objects['TextBox']:
			if 'Value' in opts and 'OnChange.Trigger' in opts and opts['OnChange.Trigger'] is True:
				value = copy.deepcopy (self.objects['TextBox'][opts['ID']]['Value'])
			self.internal_object_configure (isolation, 'TextBox', self.objects['TextBox'][opts['ID']], 'Object', **opts)
			if 'Value' in opts and 'OnChange.Trigger' in opts and opts['OnChange.Trigger'] is True:
				self.internal_textbox_event (isolation, opts['ID'], (True if value != opts['Value'] else False))
			return True, {'Status':'OK'}
		elif 'ID' in opts:
			return False, {'Status':'WARNING', 'Title':'GUI:step_textbox_change: Aborted', 'Message':'No TextBox ID named "' + str (opts['ID']) + '" exists.'}
		else:
			return False, {'Status':'WARNING', 'Title':'GUI:step_textbox_change: Aborted', 'Message':'No TextBox ID or IDs provided for the function.'}

	
	def step_checkbox_add (self, isolation, **opts):
		checkbox = customtkinter.CTkCheckBox (self.internal_form ('Object', **opts), command=lambda: self.internal_checkbox_event (isolation, opts['ID']))
		self.internal_grid (isolation, checkbox, **opts)
#		entry.bind ('<KeyRelease>', lambda event: self.internal_checkbox_event (opts['ID']), add='+')
#		entry.bind ('<Tab>', lambda event: self.internal_checkbox_event (opts['ID']), add='+')
#		entry.bind ('<Leave>', lambda event: self.internal_checkbox_event (opts['ID']), add='+')
		
		defaults = {}
		for field in self.default_fields['CheckBox']:
			defaults[field] = checkbox.cget (field)
		self.objects['CheckBox'][opts['ID']] = {'Object': checkbox, 'Value':False, 'Defaults':defaults, 'Form':self.internal_form ('Form', **opts)}
		
		self.internal_object_configure (isolation, 'CheckBox', self.objects['CheckBox'][opts['ID']], 'Object', **opts)
		
		if 'OnChange' in opts:
			self.objects['CheckBox'][opts['ID']]['OnChange'] = opts['OnChange']
		if 'OnChange.Checked' in opts:
			self.objects['CheckBox'][opts['ID']]['OnChange.Checked'] = opts['OnChange.Checked']
		if 'OnChange.Unchecked' in opts:
			self.objects['CheckBox'][opts['ID']]['OnChange.Unchecked'] = opts['OnChange.Unchecked']
		return True, {'Status':'OK'}


	def step_checkbox_change (self, isolation, **opts):
		if opts['ID'] in self.objects['CheckBox']:
			self.internal_object_configure (isolation, 'CheckBox', self.objects['CheckBox'][opts['ID']], 'Object', **opts)
			return True, {'Status':'OK'}
		else:
			return False, {'Status':'WARNING', 'Title':'GUI:step_checkbox_change: Aborted', 'Message':'No checkbox ID named "' + str (opts['ID']) + '" exists.'}
	
	
	def step_label_add (self, isolation, **opts):
		if 'ID' not in opts:
			return False, {'Status':'WARNING'}
		label = customtkinter.CTkLabel (self.internal_form ('Object', **opts))
		self.internal_grid (isolation, label, **opts)
		defaults = {}
		for field in self.default_fields['Label']:
			defaults[field] = label.cget (field)
		self.objects['Label'][opts['ID']] = {'Object':label, 'Defaults':defaults, 'Form':self.internal_form ('Form', **opts)}
		self.internal_object_configure (isolation, 'Label', self.objects['Label'][opts['ID']], 'Object', **opts)
		return True, {'Status':'OK'}
	
	
	def step_label_change (self, isolation, **opts):
		if 'IDs' in opts and isinstance (opts['IDs'], list):
			for ID in opts['IDs']:
				if ID in self.objects['Label']:
					self.internal_object_configure (isolation, 'Label', self.objects['Label'][ID], 'Object', **opts)
				else:
					return False, {'Status':'WARNING', 'Title':'GUI:step_label_change: Aborted', 'Message':'No label ID named "' + str (ID) + '" exists.'}
			return True, {'Status':'OK'}
		elif 'ID' in opts and opts['ID'] in self.objects['Label']:
			self.internal_object_configure (isolation, 'Label', self.objects['Label'][opts['ID']], 'Object', **opts)
			return True, {'Status':'OK'}
		elif 'ID' in opts:
			return False, {'Status':'WARNING', 'Title':'GUI:step_label_change: Aborted', 'Message':'No label ID named "' + str (opts['ID']) + '" exists.'}
		else:
			return False, {'Status':'WARNING', 'Title':'GUI:step_label_change: Aborted', 'Message':'No label ID or IDs provided for the function.'}

	
	def step_combobox_add (self, isolation, **opts):
		key = opts['ID']
		combobox = customtkinter.CTkComboBox (self.internal_form ('Object', **opts), command=lambda event: self.internal_combobox_event (isolation, key, event))
		self.internal_grid (isolation, combobox, **opts)
		values = (opts['Values'] if 'Values' in opts else [])
		self.objects['ComboBox'][key] = {'Object':combobox, 'Form':self.internal_form ('Form', **opts)}
		if isinstance (values, dict):
			combobox.configure (values=values.values ())
			combobox.set (list (values.values ())[0])
			self.objects['ComboBox'][key]['Values'] = values
			self.objects['ComboBox'][key]['Value'] = list (values.keys ())[0]
		else:
			combobox.configure (values=values)
			combobox.set (values[0])
			self.objects['ComboBox'][key]['Value'] = values[0]
		if 'OnChange' in opts:
			self.objects['ComboBox'][key]['OnChange'] = opts['OnChange']
		return True, {'Status':'OK'}
	
	
	def step_datepicker_add (self, isolation, **opts):
		key = opts['ID']
		
		frame = customtkinter.CTkFrame (self.internal_form ('Object', **opts), width=100, height=20)
		
		entry = customtkinter.CTkEntry (frame)
		entry.grid (row=1, column=1)
		entry.bind ('<KeyRelease>', lambda event: self.internal_step_datepicker_entry (isolation, key), add='+')
		entry.bind ('<Tab>', lambda event: self.internal_step_datepicker_entry (isolation, key), add='+')
		entry.bind ('<Leave>', lambda event: self.internal_step_datepicker_entry (isolation, key), add='+')
		if 'Value' in opts:
			entry.insert (-1, opts['Value'])
		elif 'Value.Placeholder' in opts:
			entry.configure (placeholder_text=opts['Value.Placeholder'])
		if 'Width' in opts and isinstance (opts['Width'], int):
			entry.configure (width=opts['Width'])
		button = customtkinter.CTkButton (frame, text="▼", width=20, command=lambda: self.internal_step_datepicker_calendar (isolation, key))
		button.grid (row=1, column=2, sticky="ew", padx=5, pady=5)
		self.internal_grid (isolation, frame, **opts)
		
		defaults = {}
		for field in self.default_fields['DatePicker']:
			defaults[field] = entry.cget (field)
		self.objects['DatePicker'][key] = {'Object':frame, 'ObjectEntry':entry, 'ObjectButton':button, 'ObjectCalendar':None, 'ObjectCalendarFrame':None, 'Value':copy.deepcopy (entry.get ()), 'Defaults':defaults, 'Form':self.internal_form ('Form', **opts)}
		if 'OnChange' in opts:
			self.objects['DatePicker'][key]['OnChange'] = opts['OnChange']
		
		return True, {'Status':'OK'}
	
	
	def step_datepicker_change (self, isolation, **opts):
		if opts['ID'] in self.objects['DatePicker']:
			value = copy.deepcopy (self.objects['DatePicker'][opts['ID']]['Value'])
			self.internal_object_configure (isolation, 'DatePicker', self.objects['DatePicker'][opts['ID']], 'ObjectEntry', **opts)
			if 'Value' in opts and 'OnChange.Trigger' in opts and opts['OnChange.Trigger'] is True:
				self.internal_step_datepicker_entry (isolation, opts['ID'], (True if value != opts['Value'] else False))
			return True, {'Status':'OK'}
		else:
			return False, {'Status':'WARNING', 'Title':'GUI:step_datepicker_change: Aborted', 'Message':'No datepicker ID named "' + str (opts['ID']) + '" exists.'}
	
	
	def step_inputdialog_action (self, isolation, **opts):
		inputdialog = customtkinter.CTkInputDialog (title=(str (opts['Title']) if 'Title' in opts else ''), text=(str (opts['Text']) if 'Text' in opts else ''))
		input = inputdialog.get_input ()
		
		if 'ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str):
			self.cls_steps.internal_value_set_value (isolation, 'Variable', input, opts['ReturnVariable'])
		if 'ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str):
			self.cls_steps.internal_value_set_value (None, 'Variable', input, opts['ReturnVariable.Global'])
		if 'UpdateGUI.Value' in opts and isinstance (opts['UpdateGUI.Value'], str):
			self.cls_steps.cls_gui.internal_object_update (isolation, opts['UpdateGUI.Value'], Value=input, Trigger=(True if 'UpdateGUI.Value.Trigger' in opts and opts ['UpdateGUI.Value.Trigger'] is True else False))
		
		if input is None:
			if 'OnCancel' in opts and isinstance (opts['OnCancel'], list):
				status, result = self.cls_steps.execute_steps (copy.deepcopy (opts['OnCancel']), isolation)
		else:
			if 'OnOK' in opts and isinstance (opts['OnOK'], list):
				status, result = self.cls_steps.execute_steps (copy.deepcopy (opts['OnOK']), isolation)
		return True, {'Status':'OK'}
	
	
	def step_frame_add (self, isolation, **opts):
		frame = customtkinter.CTkFrame (self.internal_form ('Object', **opts), width=500)
		self.internal_grid (isolation, frame, **opts)

		defaults = {}
		for field in self.default_fields['Frame']:
			defaults[field] = frame.cget (field)
		self.objects['Frame'][opts['ID']] = {'Object':frame, 'Defaults':defaults, 'Form':self.internal_form ('Form', **opts)}

		self.internal_object_configure (isolation, 'Frame', self.objects['Frame'][opts['ID']], 'Object', **opts)

		return True, {'Status':'OK'}
	

	def step_frame_change (self, isolation, **opts):
		if 'IDs' in opts and isinstance (opts['IDs'], list):
			for ID in opts['IDs']:
				if ID in self.objects['Label']:
					self.internal_object_configure (isolation, 'Frame', self.objects['Frame'][ID], 'Object', **opts)
				else:
					return False, {'Status':'WARNING', 'Title':'GUI:step_frame_change: Aborted', 'Message':'No frame ID named "' + str (ID) + '" exists.'}
			return True, {'Status':'OK'}
		elif 'ID' in opts and opts['ID'] in self.objects['Frame']:
			self.internal_object_configure (isolation, 'Frame', self.objects['Frame'][opts['ID']], 'Object', **opts)
			return True, {'Status':'OK'}
		elif 'ID' in opts:
			return False, {'Status':'WARNING', 'Title':'GUI:step_frame_change: Aborted', 'Message':'No frame ID named "' + str (opts['ID']) + '" exists.'}
		else:
			return False, {'Status':'WARNING', 'Title':'GUI:step_frame_change: Aborted', 'Message':'No frame ID or IDs provided for the function.'}
	
	
	def step_windowform_add (self, isolation, **opts):
		if 'WindowForm' not in self.objects:
			self.objects['WindowForm'] = {}
		if 'ID' not in opts:
			return False, {'Status':'WARNING', 'Title':'GUI:step_windowform_add: Aborted', 'Message':'No window ID provided.'}
		if opts['ID'] in self.objects['WindowForm']:
			return False, {'Status':'WARNING', 'Title':'GUI:step_windowform_add: Aborted', 'Message':'Window ID "' + str (opts['ID']) + '" already exists.'}
		
		self.objects['WindowForm'][opts['ID']] = customtkinter.CTkToplevel (self.objects['Form'])
		self.objects['WindowForm'][opts['ID']].protocol ("WM_DELETE_WINDOW", lambda: self.internal_step_windowform_event (isolation, opts['ID'], 'Destroy'))
		if 'Geometry' in opts:
			startpos = [self.objects['Form'].winfo_x (), self.objects['Form'].winfo_y ()]
			if 'StartPos.Width' in opts and isinstance (opts['StartPos.Width'], str) and opts['StartPos.Width'][0] in ['+', '-']:
				startpos[0] = startpos[0] + (-int (opts['StartPos.Width'][1:]) if opts['StartPos.Width'][0] == '-' else int (opts['StartPos.Width'][1:]))
			if 'StartPos.Height' in opts and isinstance (opts['StartPos.Height'], str) and opts['StartPos.Height'][0] in ['+', '-']:
				startpos[1] = startpos[1] + (-int (opts['StartPos.Height'][1:]) if opts['StartPos.Height'][0] == '-' else int (opts['StartPos.Height'][1:]))
			self.objects['WindowForm'][opts['ID']].geometry (opts['Geometry'] + '+' + str (startpos[0]) + '+' + str (startpos[1]))
		if 'Title' in opts:
			self.objects['WindowForm'][opts['ID']].title (opts['Title'])
		if ('Resizable.Width' in opts and opts['Resizable.Width'] is False) or ('Resizable.Height' in opts and opts['Resizable.Height'] is False):
			self.objects['WindowForm'][opts['ID']].resizable ((False if 'Resizable.Width' in opts and opts['Resizable.Width'] is False else True), (False if 'Resizable.Height' in opts and opts['Resizable.Height'] is False else True))
		return True, {'Status':'OK'}
	
	
	def step_windowform_change (self, isolation, **opts):
		if 'ID' not in opts:
			return False, {'Status':'WARNING', 'Title':'GUI:step_windowform_change: Aborted', 'Message':'No window ID provided.'}
		if opts['ID'] not in self.objects['WindowForm']:
			return False, {'Status':'WARNING', 'Title':'GUI:step_windowform_change: Aborted', 'Message':'No window ID named "' + str (opts['ID']) + '" exists.'}
		if 'Focus' in opts and opts['Focus'] is True:
			self.objects['WindowForm'][opts['ID']].focus ()
		if 'Destroy' in opts and opts['Destroy'] is True:
			result = self.internal_step_windowform_event (isolation, opts['ID'], 'Destroy')
			if result is not None:
				return False, result
		return True, {'Status':'OK'}
	
	
	def internal_step_windowform_event (self, isolation, key, action):
		if key not in self.objects['WindowForm']:
			return {'Status':'ERROR', 'Title':'', 'Message':'The window key "' + str (key) + '" was not found.'}
		if action == 'Destroy':
			self.internal_object_destroy ('WindowForm', key)
	
	
	def internal_object_destroy (self, type, key):
		if type == 'WindowForm' and key in self.objects['WindowForm']:
			self.objects['WindowForm'][key].destroy ()
			del (self.objects['WindowForm'][key])
			for object_type in self.objects.keys ():
				if isinstance (self.objects[object_type], dict):
					for object_id in list (self.objects[object_type].keys ()):
						if isinstance (self.objects[object_type][object_id], dict) and 'Form' in self.objects[object_type][object_id] and isinstance (self.objects[object_type][object_id]['Form'], list) and len (self.objects[object_type][object_id]['Form']) > 1 and self.objects[object_type][object_id]['Form'][0] == 'WindowID' and self.objects[object_type][object_id]['Form'][1] == key:
							if 'Object' in self.objects[object_type][object_id]:
								self.objects[object_type][object_id]['Object'].destroy ()
							if object_type == 'DatePicker':
								print ('MISSING_LOGIC_DATEPICKER_DELETE')
							del (self.objects[object_type][object_id])
							print ('DELETE_OBJECT::' + str (object_type) + '::' + str (object_id))
	
	
	def step_filedialog_action (self, isolation, **opts):
		ask_opts = {}
		if 'Title' in opts:
			ask_opts['title'] = opts['Title']
		if 'Directory' in opts:
			ask_opts['initialdir'] = opts['Directory']
		elif 'Directory.Downloads' in opts and opts['Directory.Downloads'] is True:
			ask_opts['initialdir'] = str (pathlib.Path.home ()) + '\\Downloads\\'
			
		if 'File' in opts:
			ask_opts['initialfile'] = opts['File']
		if 'FileTypes' in opts:
			ask_opts['filetypes'] = opts['FileTypes']
		if 'Multiple' in opts and opts['Multiple'] is True:
			ask_opts['multiple'] = True
		
		value = (list (tkinter.filedialog.askopenfilename (**ask_opts)) if 'multiple' in ask_opts else tkinter.filedialog.askopenfilename (**ask_opts))
		
		if 'ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str):
			self.cls_steps.internal_value_set_value (isolation, 'Variable', value, opts['ReturnVariable'])
		if 'ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str):
			self.cls_steps.internal_value_set_value (None, 'Variable', value, opts['ReturnVariable.Global'])
		if 'UpdateGUI.Value' in opts and isinstance (opts['UpdateGUI.Value'], str):
			self.cls_steps.cls_gui.internal_object_update (isolation, opts['UpdateGUI.Value'], Value=value, Trigger=(True if 'UpdateGUI.Value.Trigger' in opts and opts ['UpdateGUI.Value.Trigger'] is True else False))
		return True, {'Status':'OK', 'Data':value}
		
	
	def step_defaults (self, isolation, **opts):
		if 'Type' not in opts:
			return False, {'Status':'WARNING', 'Title':'GUI:step_defaults: Aborted', 'Message':'No Type provided.'}
		
		if opts['Type'] == 'Window':
			if 'Window.Type' not in opts or opts['Window.Type'] not in ['Form', 'FrameID', 'WindowID']:
				return False, {'Status':'WARNING', 'Title':'GUI:step_defaults: Aborted', 'Message':'The Type "Window" requires a valid Window.Type value.'}
			if opts['Window.Type'] == 'Form':
				self.defaults['Form'] = ['Form']
			elif 'Window.ID' not in opts or not isinstance (opts['Window.ID'], str):
				return False, {'Status':'WARNING', 'Title':'GUI:step_defaults: Aborted', 'Message':'The Type "Window" requires a valid Window.ID value.'}
			elif opts['Window.Type'] == 'FrameID':
				if opts['Window.ID'] not in self.objects['Frame']:
					return False, {'Status':'WARNING', 'Title':'GUI:step_defaults: Aborted', 'Message':'The FrameID "' + str (opts['Window.ID']) + '" does not exist.'}
				self.defaults['Form'] = ['FrameID', str (opts['Window.ID'])]
			elif opts['Window.Type'] == 'WindowID':
				if opts['Window.ID'] not in self.objects['WindowForm']:
					return False, {'Status':'WARNING', 'Title':'GUI:step_defaults: Aborted', 'Message':'The WindowID "' + str (opts['Window.ID']) + '" does not exist.'}
				self.defaults['Form'] = ['WindowID', str (opts['Window.ID'])]
		elif opts['Type'] == 'Position':
			if 'Positions.Dict' in opts:
				if not isinstance (opts['Positions.Dict'], dict):
					return False, {'Status':'WARNING', 'Title':'GUI:step_defaults: Aborted', 'Message':'The "Positions.Dict" requires a dict.'}
				for position in opts['Positions.Dict'].keys ():
					if not isinstance (position, str) or not isinstance (opts['Positions.Dict'][position], int):
						return False, {'Status':'WARNING', 'Title':'GUI:step_defaults: Aborted', 'Message':'The "Positions.Dict" key "' + str (position) + '" (' + str (type (position)) + ') with the value "' + str (opts['Positions.Dict'][position]) + '" (' + str (type (opts['Positions.Dict'][position])) + ') is not valid.'}
					self.defaults['Positions'][position] = opts['Positions.Dict'][position]
			else:
				if 'Position.ID' not in opts:
					return False, {'Status':'WARNING', 'Title':'GUI:step_defaults: Aborted', 'Message':'The Type "Position" requires a valid Position.ID value.'}
				elif not isinstance (opts['Position.ID'], str):
					return False, {'Status':'WARNING', 'Title':'GUI:step_defaults: Aborted', 'Message':'The "Position.ID" requires a string value.'}
				if 'Position.Value' not in opts:
					return False, {'Status':'WARNING', 'Title':'GUI:step_defaults: Aborted', 'Message':'The Type "Position" requires a valid Position.Value value.'}
				elif not isinstance (opts['Position.Value'], int):
					return False, {'Status':'WARNING', 'Title':'GUI:step_defaults: Aborted', 'Message':'The "Position.ID" requires a integer value.'}
				self.defaults['Positions'][opts['Position.ID']] = opts['Position.Value']
		else:
			return False, {'Status':'WARNING', 'Title':'GUI:step_defaults: Aborted', 'Message':'The Type "' + str (opts['Type']) + '" is not known.'}
		
		return True, {'Status':'OK'}
	
	
	def step_progressbar_add (self, isolation, **opts):
		if 'ID' not in opts:
			return False, {'Status':'WARNING', 'Title':'GUI:step_progressbar_add: Aborted', 'Message':'No ID provided.'}
		if opts['ID'] in self.objects['ProgressBar']:
			return False, {'Status':'WARNING', 'Title':'GUI:step_progressbar_add: Aborted', 'Message':'The ID "' + str (opts['ID']) + '" already exists.'}
		pb_opts = {}
		for field in [['Width', 'width'], ['Height', 'height']]:
			if field[0] in opts:
				if not isinstance (opts[field[0]], int):
					return False, {'Status':'WARNING', 'Title':'GUI:step_progressbar_add: Aborted', 'Message':'The ' + field[0] + ' needs to be an integer.'}
				pb_opts[field[1]] = opts[field[0]]
		if 'Vertical' in opts and opts['Vertical'] is True:
			pb_opts['orientation'] = 'vertical'

		progressbar = customtkinter.CTkProgressBar (master=self.internal_form ('Object', **opts), **pb_opts)
		self.internal_grid (isolation, progressbar, **opts)
		self.objects['ProgressBar'][opts['ID']] = {'Object':progressbar, 'Value':0, 'Form':self.internal_form ('Form', **opts), 'ProgressColorRange':[], 'Scale':(opts['ProgressScale'] if 'ProgressScale' in opts and isinstance (opts['ProgressScale'], int) and opts['ProgressScale'] != 0 else 100)}
		if 'ProgressColor.Range' in opts and isinstance (opts['ProgressColor.Range'], list):
			if len (opts['ProgressColor.Range']) > 100:
				return False, {'Status':'WARNING', 'Title':'GUI:step_progressbar_add: Aborted', 'Message':'Only 100 entries are allowed for "ProgressColor.Range" (' + str (len (opts['ProgressColor.Range'])) + ' provided.).'}
			self.objects['ProgressBar'][opts['ID']]['ProgressColorRange'] = opts['ProgressColor.Range']
			if 'Progress' not in opts:
				self.internal_progressbar_update (opts['ID'], Progress=self.objects['ProgressBar'][opts['ID']]['Value'])
		elif 'ProgressColor.RangePreset' in opts and isinstance (opts['ProgressColor.RangePreset'], str):
			values = self.internal_color_ranges (opts['ProgressColor.RangePreset'])
			if values is None:
				return False, {'Status':'WARNING', 'Title':'GUI:step_progressbar_add: Aborted', 'Message':'The "ProgressColor.RangePreset" named "' + opts['ProgressColor.RangePreset'] + '" does not exist.'}
			self.objects['ProgressBar'][opts['ID']]['ProgressColorRange'] = values
			if 'Progress' not in opts:
				self.internal_progressbar_update (opts['ID'], Progress=self.objects['ProgressBar'][opts['ID']]['Value'])
		if ('Progress' in opts and isinstance (opts['Progress'], int)) or ('ProgressColor' in opts and isinstance (opts['ProgressColor'], str)):
			result = self.internal_progressbar_update (opts['ID'], **opts)
			if result is not True:
				return False, {'Status':'ERROR', 'Title':'GUI:step_progressbar_add: Error', 'Message':'The ProgressBar ' + opts['ID'] + ' failed to update the progress bar.'}
		else:
			self.objects['ProgressBar'][opts['ID']]['Object'].set (0)
		return True, {'Status':'OK'}

	
	def step_progressbar_change (self, isolation, **opts):
		if 'ID' not in opts:
			return False, {'Status':'WARNING', 'Title':'GUI:step_progressbar_change: Aborted', 'Message':'No ID provided.'}
		if opts['ID'] not in self.objects['ProgressBar']:
			return False, {'Status':'WARNING', 'Title':'GUI:step_progressbar_change: Aborted', 'Message':'No progress bar with the ID "' + str (opts['ID']) + '" exists.'}
		if 'ProgressScale' in opts and isinstance (opts['ProgressScale'], int) and opts['ProgressScale'] != 0:
			self.objects['ProgressBar'][opts['ID']]['Scale'] = opts['ProgressScale']
		if 'ProgressColor.Range' in opts and isinstance (opts['ProgressColor.Range'], list):
			if len (opts['ProgressColor.Range']) > 100:
				return False, {'Status':'WARNING', 'Title':'GUI:step_progressbar_change: Aborted', 'Message':'Only 100 entries are allowed for "ProgressColor.Range" (' + str (len (opts['ProgressColor.Range'])) + ' provided.).'}
			self.objects['ProgressBar'][opts['ID']]['ProgressColorRange'] = opts['ProgressColor.Range']
			if 'Progress' not in opts:
				self.internal_progressbar_update (opts['ID'], Progress=self.objects['ProgressBar'][opts['ID']]['Value'])
		elif 'ProgressColor.RangePreset' in opts and isinstance (opts['ProgressColor.RangePreset'], str):
			values = self.internal_color_ranges (opts['ProgressColor.RangePreset'])
			if values is None:
				return False, {'Status':'WARNING', 'Title':'GUI:step_progressbar_change: Aborted', 'Message':'The "ProgressColor.RangePreset" named "' + opts['ProgressColor.RangePreset'] + '" does not exist.'}
			self.objects['ProgressBar'][opts['ID']]['ProgressColorRange'] = values
			if 'Progress' not in opts:
				self.internal_progressbar_update (opts['ID'], Progress=self.objects['ProgressBar'][opts['ID']]['Value'])
		if ('Progress' in opts and isinstance (opts['Progress'], int)) or ('ProgressColor' in opts and isinstance (opts['ProgressColor'], str)):
			result = self.internal_progressbar_update (opts['ID'], **opts)
			if result is not True:
				return False, {'Status':'ERROR', 'Title':'GUI:step_progressbar_change: Error', 'Message':'The ProgressBar ' + opts['ID'] + ' failed to update the progress bar.'}
		return True, {'Status':'OK'}
	
	
	def internal_progressbar_update (self, object_or_id, **opts):
		if isinstance (object_or_id, str):
			if object_or_id in self.objects['ProgressBar']:
				object_or_id = self.objects['ProgressBar'][object_or_id]
			else:
				return False
		if 'Progress' in opts and isinstance (opts['Progress'], int):
			progress = internal_zyd_floor ((opts['Progress'] / object_or_id['Scale']) * 100, Decimals=0, Internal=True)
			object_or_id['Object'].set (min (progress, 100) / 100)
			object_or_id['Value'] = opts['Progress']
		if 'ProgressColor' in opts and isinstance (opts['ProgressColor'], str):
			object_or_id['Object'].configure (progress_color=opts['ProgressColor'])
		elif 'Progress' in opts and isinstance (opts['Progress'], int) and 'ProgressColorRange' in object_or_id and len (object_or_id['ProgressColorRange']) > 0:
			if len (object_or_id['ProgressColorRange']) == 100:
				object_or_id['Object'].configure (progress_color=object_or_id['ProgressColorRange'][min (progress, 100) - 1])
		return True
	
	
	def step_objects_count (self, isolation, **opts):
		count = 0
		for object_type in self.objects.keys ():
			if object_type not in ['Form']:
				valid = True
				if 'Filter.Type' in opts and isinstance (opts['Filter.Type'], list):
					for filter in opts['Filter.Type']:
						if not self.internal_step_objects_count_match_filter (object_type, filter):
							valid = False
				if valid is True:
					object_field = ('ObjectEntry' if object_type in ['DatePicker'] else 'Object')
					for object_id in self.objects[object_type].keys ():
						valid = True
						if 'Filter.ID' in opts and isinstance (opts['Filter.ID'], list):
							for filter in opts['Filter.ID']:
								if not self.internal_step_objects_count_match_filter (object_id, filter):
									valid = False
						if valid is True and isinstance (self.objects[object_type][object_id], dict) and object_field in self.objects[object_type][object_id]:
							for field in self.object_fields.keys ():
								if 'Filter.' + field in opts and isinstance (opts['Filter.' + field], list):
									if object_type not in self.object_fields[field]:
										return False, {'Status':'WARNING', 'Title':'GUI:step_objects_count: Aborted', 'Message':'The filter "' + str (field) + '" is not valid for the object type "' + str (object_type) + '".'}
									else:
										filter_valid = True
										for filter in opts['Filter.' + field]:
											if not self.internal_step_objects_count_match_filter (str (self.objects[object_type][object_id][object_field].cget (self.object_fields[field][object_type])), filter):
												filter_valid = False
												break
										if filter_valid is False:
											valid = False
											break
							if 'Filter.Readonly' in opts and isinstance (opts['Filter.Readonly'], list):
								for filter in opts['Filter.Readonly']:
									if not self.internal_step_objects_count_match_filter ((True if 'readonly' in self.objects[object_type][object_id][object_field].cget ('state') else False), filter):
										valid = False
										break
							if valid is True:
								count += 1
		if 'ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str):
			self.cls_steps.internal_value_set_value (isolation, 'Variable', count, opts['ReturnVariable'])
		if 'ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str):
			self.cls_steps.internal_value_set_value (None, 'Variable', count, opts['ReturnVariable.Global'])
		if 'UpdateGUI.Value' in opts and isinstance (opts['UpdateGUI.Value'], str):
			self.cls_steps.cls_gui.internal_object_update (isolation, opts['UpdateGUI.Value'], Value=count, Trigger=(True if 'UpdateGUI.Value.Trigger' in opts and opts ['UpdateGUI.Value.Trigger'] is True else False))
		return True, {'Status':'OK', 'Data':count}
		
		
	def internal_step_objects_count_match_filter (self, value, filter):
		if not isinstance (filter, dict) or 'Logic' not in filter or 'Values' not in filter:
			return False
		elif filter['Logic'] == '=' and value in filter['Values']:
			return True
		elif filter['Logic'] == '!=' and value not in filter['Values']:
			return True
		return False
	
	
	# Used to update an object by step functions...
	def internal_object_update (self, isolation, object, **opts):
		if isinstance (object, str) and len (object) > 4 and '##' in object:
			gui = object.split ('##')
			if gui[0] in self.objects and gui[1] in self.objects[gui[0]]:
				objectname = 'Object'
				if gui[0] == 'DatePicker':
					objectname = 'ObjectEntry'
				self.internal_object_configure (isolation, gui[0], self.objects[gui[0]][gui[1]], objectname, **opts)
				if 'Trigger' in opts and opts['Trigger'] is True:
					if gui[0] == 'Entry':
						self.internal_entry_event (isolation, gui[1], True)
					elif gui[0] == 'DatePicker':
						self.internal_step_datepicker_entry (isolation, gui[1], True)
					elif gui[0] in ['ProgressBar', 'Label']:
						pass
					else:
						print ('ERROR::GUI::internal_object_update::TRIGGER_LOGIC=' + str (object) + '::' + str (opts))
	
	
	def internal_form (self, type, **opts):
		if 'WindowID' in opts and isinstance (opts['WindowID'], str) and opts['WindowID'] in self.objects['WindowForm']:
			if type == 'Object':
				return self.objects['WindowForm'][opts['WindowID']]
			elif type == 'Form':
				return ['WindowID', opts['WindowID']]
		elif 'FrameID' in opts and isinstance (opts['FrameID'], str) and opts['FrameID'] in self.objects['Frame'] and 'Object' in self.objects['Frame'][opts['FrameID']]:
			if type == 'Object':
				return self.objects['Frame'][opts['FrameID']]['Object']
			elif type == 'Form':
				return ['FrameID', opts['FrameID']]
		if self.defaults['Form'][0] == 'Form':
			if type == 'Object':
				return self.objects['Form']
			elif type == 'Form':
				return ['Form']
		elif self.defaults['Form'][0] == 'FrameID':
			return self.internal_form (type, FrameID=self.defaults['Form'][1])
		elif self.defaults['Form'][0] == 'WindowID':
			return self.internal_form (type, WindowID=self.defaults['Form'][1])
	
	
	def internal_grid (self, isolation, object, **opts):
		grid = {
			'row':opts['Placement.Row'],
			'column':opts['Placement.Column']
		}
		if 'Placement.Colspan' in opts and isinstance (opts['Placement.Colspan'], int):
			grid['columnspan'] = opts['Placement.Colspan']
		if 'Placement.Rowspan' in opts and isinstance (opts['Placement.Rowspan'], int):
			grid['rowspan'] = opts['Placement.Rowspan']
		if 'Placement.Alignment' in opts and isinstance (opts['Placement.Alignment'], str):
			grid['sticky'] = opts['Placement.Alignment']
		object.grid (**grid)
	
	
	# Calculates the numeric position and if the postion contans something like %Pos1%=%Pos1%+1, the Pos1 value is updated with the new value
	def internal_calculate_position (self, position):
		field = copy.deepcopy (position)
		if len (self.defaults['Positions']) > 0:
			save = None
			for placement in self.defaults['Positions'].keys ():
				if field.startswith ('%' + placement + '%='):
					save = copy.deepcopy (placement)
					field = field[len (placement) + 3:]
				field = field.replace ('%' + placement + '%', str (self.defaults['Positions'][placement]))
			if field != position:
				status, value = zyd_calc (field)
				if status is True and save is not None:
					print ('DEBUG.UPDATE_POSITION::' + save + '::' + str (self.defaults['Positions'][save]) + '=>' + str (value))
					self.defaults['Positions'][save] = value
				return status, value
		return False, {'Status':'WARNING', 'Title':'GUI:internal_calculate_position: Aborted', 'Message':'Not a valid dynamic position ("' + str (position) + '").'}
	
	
	def internal_step_datepicker_calendar (self, isolation, key):
		if self.objects['DatePicker'][key]['ObjectCalendar'] is not None:
			self.objects['DatePicker'][key]['ObjectCalendar'].destroy ()
		self.objects['DatePicker'][key]['ObjectCalendar'] = customtkinter.CTkToplevel (self.objects['DatePicker'][key]['Object'])
		self.objects['DatePicker'][key]['ObjectCalendar'].title ("Select Date")
		self.objects['DatePicker'][key]['ObjectCalendar'].wm_attributes("-toolwindow", True)
		self.objects['DatePicker'][key]['ObjectCalendar'].geometry ("+%d+%d" % (self.objects['DatePicker'][key]['Object'].winfo_rootx (), self.objects['DatePicker'][key]['Object'].winfo_rooty () + self.objects['DatePicker'][key]['Object'].winfo_height ()))
		self.objects['DatePicker'][key]['ObjectCalendar'].resizable (False, False)

		if len (self.objects['DatePicker'][key]['Value']) == 10 and internal_datahandling_verify (self.objects['DatePicker'][key]['Value'], Type='Date') is None:
			self.objects['DatePicker'][key]['Year'] = int (self.objects['DatePicker'][key]['Value'][:4])
			self.objects['DatePicker'][key]['Month'] = int (self.objects['DatePicker'][key]['Value'][5:7])
			self.objects['DatePicker'][key]['Day'] = int (self.objects['DatePicker'][key]['Value'][-2:])
		else:
			self.objects['DatePicker'][key]['Year'] = datetime.datetime.now ().year
			self.objects['DatePicker'][key]['Month'] = datetime.datetime.now ().month
			self.objects['DatePicker'][key]['Day'] = datetime.datetime.now ().day
		self.objects['DatePicker'][key]['Selected'] = str (self.objects['DatePicker'][key]['Year']) + '.' + str (self.objects['DatePicker'][key]['Month']) + '.' + str (self.objects['DatePicker'][key]['Day'])
		self.internal_step_datepicker_calendar_build (isolation, key)
		self.objects['DatePicker'][key]['ObjectCalendar'].after (150, lambda:self.internal_step_datepicker_calendar_build (isolation, key, 'Focus'))
		self.objects['DatePicker'][key]['ObjectCalendar'].after (500, lambda:self.internal_step_datepicker_calendar_build (isolation, key, 'Focus'))
		self.objects['DatePicker'][key]['ObjectCalendar'].after (250, lambda:self.internal_step_datepicker_calendar_build (isolation, key, 'BindDestroy'))

	
	def internal_step_datepicker_calendar_build (self, isolation, key, part = 'Frame'):
		if part == 'Frame':
			if self.objects['DatePicker'][key]['ObjectCalendarFrame'] is not None:
				self.objects['DatePicker'][key]['ObjectCalendarFrame'].destroy ()
			self.objects['DatePicker'][key]['ObjectCalendarFrame'] = customtkinter.CTkFrame (self.objects['DatePicker'][key]['ObjectCalendar'])
			self.objects['DatePicker'][key]['ObjectCalendarFrame'].grid (row=0, column=0)
			
			monthyear = customtkinter.CTkLabel (self.objects['DatePicker'][key]['ObjectCalendarFrame'], text=calendar.month_name[self.objects['DatePicker'][key]['Month']].capitalize() + ', ' + str (self.objects['DatePicker'][key]['Year']))
			monthyear.grid (row=0, column=1, columnspan=5)
			
			button_prev = customtkinter.CTkButton (self.objects['DatePicker'][key]['ObjectCalendarFrame'], text="<", width=5, command=lambda: self.internal_step_datepicker_calendar_build (isolation, key, 'Month-'))
			button_prev.grid (row=0, column=0)
			button_next = customtkinter.CTkButton (self.objects['DatePicker'][key]['ObjectCalendarFrame'], text=">", width=5, command=lambda: self.internal_step_datepicker_calendar_build (isolation, key, 'Month+'))
			button_next.grid (row=0, column=6)
			
			days = [calendar.day_name[i][:3].capitalize () for i in range (7)]
			for i, day in enumerate (days):
				lbl = customtkinter.CTkLabel (self.objects['DatePicker'][key]['ObjectCalendarFrame'], text=day)
				lbl.grid (row=1, column=i)
			
			# Days in month
			month_days = calendar.monthrange (self.objects['DatePicker'][key]['Year'], self.objects['DatePicker'][key]['Month'])[1]
			start_day = calendar.monthrange (self.objects['DatePicker'][key]['Year'], self.objects['DatePicker'][key]['Month'])[0]
			day = 1
			for week in range (2, 8):
				for day_col in range (7):
					if week == 2 and day_col < start_day:
						lbl = customtkinter.CTkLabel (self.objects['DatePicker'][key]['ObjectCalendarFrame'], text="")
						lbl.grid (row=week, column=day_col)
					elif day > month_days:
						lbl = customtkinter.CTkLabel (self.objects['DatePicker'][key]['ObjectCalendarFrame'], text="")
						lbl.grid (row=week, column=day_col)
					else:
						if customtkinter.get_appearance_mode () == "Light":
							btn = customtkinter.CTkButton (self.objects['DatePicker'][key]['ObjectCalendarFrame'], text=str (day), width=3, command=lambda day=day:self.internal_step_datepicker_calendar_build (isolation, key, day), fg_color="transparent", text_color="black", hover_color="#3b8ed0")
						else:
							btn = customtkinter.CTkButton (self.objects['DatePicker'][key]['ObjectCalendarFrame'], text=str (day), width=3, command=lambda day=day:self.internal_step_datepicker_calendar_build (isolation, key, day), fg_color="transparent")
						if str (self.objects['DatePicker'][key]['Year']) + '.' + str (self.objects['DatePicker'][key]['Month']) + '.' + str (day) == self.objects['DatePicker'][key]['Selected']:
							btn.configure (fg_color="Red")
						btn.grid (row=week, column=day_col)
						day += 1
		elif part == 'Month+':
			self.objects['DatePicker'][key]['Month'] += 1
			self.objects['DatePicker'][key]['Day'] = 0
			if self.objects['DatePicker'][key]['Month'] > 12:
				self.objects['DatePicker'][key]['Month'] = 1
				self.objects['DatePicker'][key]['Year'] += 1
			self.internal_step_datepicker_calendar_build (isolation, key, 'Frame')
		elif part == 'Month-':
			self.objects['DatePicker'][key]['Month'] -= 1
			self.objects['DatePicker'][key]['Day'] = 0
			if self.objects['DatePicker'][key]['Month'] < 1:
				self.objects['DatePicker'][key]['Month'] = 12
				self.objects['DatePicker'][key]['Year'] -= 1
			self.internal_step_datepicker_calendar_build (isolation, key, 'Frame')
		elif part == 'BindDestroy':
			if key in self.objects['DatePicker'] and 'ObjectCalendar' in self.objects['DatePicker'][key] and self.objects['DatePicker'][key]['ObjectCalendar'] is not None:
				self.objects['DatePicker'][key]['ObjectCalendar'].bind ('<FocusOut>', lambda event:self.internal_step_datepicker_calendar_build (isolation, key, 'Destroy'))
			else:
				print ('\t\tBindDestroy::SKIPPED')
		elif part == 'Destroy':
			if str (self.objects['DatePicker'][key]['ObjectCalendar'].focus_get ()) + str (self.objects['Form'].focus_get ()) != '..':
				self.objects['DatePicker'][key]['ObjectCalendar'].destroy ()
		elif part == 'Focus':
			self.objects['DatePicker'][key]['ObjectCalendar'].focus ()
		else:
			self.objects['DatePicker'][key]['ObjectEntry'].configure (state='normal')
			self.objects['DatePicker'][key]['ObjectEntry'].delete (0, customtkinter.END)
			self.objects['DatePicker'][key]['ObjectEntry'].insert (0, str (self.objects['DatePicker'][key]['Year']) + '-' + ('0' if self.objects['DatePicker'][key]['Month'] < 10 else '') + str (self.objects['DatePicker'][key]['Month']) + '-' + ('0' if part < 10 else '') + str (part))
			self.internal_step_datepicker_entry (isolation, key)
			self.objects['DatePicker'][key]['ObjectCalendarFrame'].destroy ()
			self.objects['DatePicker'][key]['ObjectCalendarFrame'] = None
			self.objects['DatePicker'][key]['ObjectCalendar'].destroy ()
			self.objects['DatePicker'][key]['ObjectCalendar'] = None
		

	def internal_step_datepicker_entry (self, isolation, key, force = False):
		if key in self.objects['DatePicker']:
			if force or str (self.objects['DatePicker'][key]['Value']) != str (self.objects['DatePicker'][key]['ObjectEntry'].get ()):
				self.objects['DatePicker'][key]['Value'] = copy.deepcopy (self.objects['DatePicker'][key]['ObjectEntry'].get ())
				if 'OnChange' in self.objects['DatePicker'][key]:
					self.cls_steps.execute_steps (copy.deepcopy (self.objects['DatePicker'][key]['OnChange']), isolation)
	
	
	def internal_button_event (self, isolation, key):
		if 'OnClick' in self.objects['Button'][key]:
			status, result = self.cls_steps.execute_steps (copy.deepcopy (self.objects['Button'][key]['OnClick']), isolation)
	
	
	def internal_entry_event (self, isolation, key, force = False):
		if key in self.objects['Entry']:
			if (force or str (self.objects['Entry'][key]['Value']) != str (self.objects['Entry'][key]['Object'].get ())):
				self.objects['Entry'][key]['Value'] = copy.deepcopy (self.objects['Entry'][key]['Object'].get ())
				if 'OnChange' in self.objects['Entry'][key]:
					self.cls_steps.execute_steps (copy.deepcopy (self.objects['Entry'][key]['OnChange']), isolation)
		else:
			print ('ERROR::GUI::internal_entry_event::UNKNOWN_ID::' + str (key))
	
	
	def internal_textbox_event (self, isolation, key, force = False):
		if force or (key in self.objects['TextBox'] and str (self.objects['TextBox'][key]['Value']) != str (self.objects['TextBox'][key]['Object'].get ("0.0", "end"))):
			self.objects['TextBox'][key]['Value'] = copy.deepcopy (self.objects['TextBox'][key]['Object'].get ("0.0", "end"))
			if 'OnChange' in self.objects['TextBox'][key]:
				self.cls_steps.execute_steps (copy.deepcopy (self.objects['TextBox'][key]['OnChange']), isolation)
	
	
	def internal_checkbox_event (self, isolation, key):
		if key in self.objects['CheckBox'] and self.objects['CheckBox'][key]['Value'] != (True if self.objects['CheckBox'][key]['Object'].get() == 1 else False):
			self.objects['CheckBox'][key]['Value'] = (True if self.objects['CheckBox'][key]['Object'].get() == 1 else False)
			if 'OnChange' in self.objects['CheckBox'][key]:
				self.cls_steps.execute_steps (copy.deepcopy (self.objects['CheckBox'][key]['OnChange']), isolation)
			if 'OnChange.Checked' in self.objects['CheckBox'][key] and self.objects['CheckBox'][key]['Value'] is True:
				self.cls_steps.execute_steps (copy.deepcopy (self.objects['CheckBox'][key]['OnChange.Checked']), isolation)
			if 'OnChange.Unchecked' in self.objects['CheckBox'][key] and self.objects['CheckBox'][key]['Value'] is False:
				self.cls_steps.execute_steps (copy.deepcopy (self.objects['CheckBox'][key]['OnChange.Unchecked']), isolation)
	
	
	def internal_combobox_event (self, isolation, key, event_value):
		if key in self.objects['ComboBox']:
			if 'Values' in self.objects['ComboBox'][key]:
				for value_key in self.objects['ComboBox'][key]['Values'].keys ():
					if self.objects['ComboBox'][key]['Values'][value_key] == event_value:
						if value_key != self.objects['ComboBox'][key]['Value']:
							print (str (key) + '=>' + str (value_key) + '::' + str (event_value))
							self.objects['ComboBox'][key]['Value'] = copy.deepcopy (value_key)
							if 'OnChange' in self.objects['ComboBox'][key]:
								self.cls_steps.execute_steps (copy.deepcopy (self.objects['ComboBox'][key]['OnChange']), isolation)
						break
	
	
	def internal_color_ranges (self, name):
		ranges = {
			'Traffic Flow':['#FF0000', '#FC0200', '#F90500', '#F70700', '#F40A00', '#F20C00', '#EF0F00', '#EC1200', '#EA1400', '#E71700', '#E51900', '#E21C00', '#E01E00', '#DD2100', '#DA2400', '#D82600', '#D52900', '#D32B00', '#D02E00', '#CE3000', '#CB3300', '#C83600', '#C63800', '#C33B00', '#C13D00', '#BE4000', '#BC4200', '#B94500', '#B64800', '#B44A00', '#B14D00', '#AF4F00', '#AC5200', '#AA5500', '#A75700', '#A45A00', '#A25C00', '#9F5F00', '#9D6100', '#9A6400', '#976700', '#956900', '#926C00', '#906E00', '#8D7100', '#8B7300', '#887600', '#857900', '#837B00', '#807E00', '#7E8000', '#7B8300', '#798500', '#768800', '#738B00', '#718D00', '#6E9000', '#6C9200', '#699500', '#679700', '#649A00', '#619D00', '#5F9F00', '#5CA200', '#5AA400', '#57A700', '#55AA00', '#52AC00', '#4FAF00', '#4DB100', '#4AB400', '#48B600', '#45B900', '#42BC00', '#40BE00', '#3DC100', '#3BC300', '#38C600', '#36C800', '#33CB00', '#30CE00', '#2ED000', '#2BD300', '#29D500', '#26D800', '#24DA00', '#21DD00', '#1EE000', '#1CE200', '#19E500', '#17E700', '#14EA00', '#12EC00', '#0FEF00', '#0CF200', '#0AF400', '#07F700', '#05F900', '#02FC00', '#00FF00'],
			'Status Spectrum':['#FF0000', '#FF0500', '#FF0A00', '#FF0F00', '#FF1400', '#FF1A00', '#FF1F00', '#FF2400', '#FF2900', '#FF2E00', '#FF3400', '#FF3900', '#FF3E00', '#FF4300', '#FF4800', '#FF4E00', '#FF5300', '#FF5800', '#FF5D00', '#FF6200', '#FF6800', '#FF6D00', '#FF7200', '#FF7700', '#FF7C00', '#FF8200', '#FF8700', '#FF8C00', '#FF9100', '#FF9600', '#FF9C00', '#FFA100', '#FFA600', '#FFAB00', '#FFB000', '#FFB600', '#FFBB00', '#FFC000', '#FFC500', '#FFCA00', '#FFD000', '#FFD500', '#FFDA00', '#FFDF00', '#FFE400', '#FFEA00', '#FFEF00', '#FFF400', '#FFF900', '#FFFF00', '#FFFF00', '#F9FF00', '#F4FF00', '#EFFF00', '#EAFF00', '#E4FF00', '#DFFF00', '#DAFF00', '#D5FF00', '#D0FF00', '#CAFF00', '#C5FF00', '#C0FF00', '#BBFF00', '#B6FF00', '#B0FF00', '#ABFF00', '#A6FF00', '#A1FF00', '#9CFF00', '#96FF00', '#91FF00', '#8CFF00', '#87FF00', '#82FF00', '#7CFF00', '#77FF00', '#72FF00', '#6DFF00', '#68FF00', '#62FF00', '#5DFF00', '#58FF00', '#53FF00', '#4EFF00', '#48FF00', '#43FF00', '#3EFF00', '#39FF00', '#34FF00', '#2EFF00', '#29FF00', '#24FF00', '#1FFF00', '#1AFF00', '#14FF00', '#0FFF00', '#0AFF00', '#05FF00', '#00FF00'],
			'Twilight Drift':['#0000FF', '#0200FE', '#0400FD', '#0600FC', '#0800FB', '#0A00FA', '#0C00F9', '#0E00F8', '#1000F7', '#1200F6', '#1400F5', '#1600F4', '#1800F3', '#1A00F2', '#1C00F1', '#1E00F0', '#2000EF', '#2200EE', '#2400ED', '#2600EC', '#2800EB', '#2A00EA', '#2C00E9', '#2E00E8', '#3000E7', '#3200E6', '#3400E5', '#3600E4', '#3800E3', '#3A00E2', '#3C00E1', '#3E00E0', '#4000DF', '#4200DE', '#4400DD', '#4600DC', '#4800DB', '#4A00DA', '#4C00D9', '#4E00D8', '#5000D7', '#5200D6', '#5400D5', '#5600D4', '#5800D3', '#5A00D2', '#5C00D1', '#5E00D0', '#6000CF', '#6200CE', '#6400CD', '#6600CC', '#6800CB', '#6A00CA', '#6C00C9', '#6E00C8', '#7000C7', '#7200C6', '#7400C5', '#7600C4', '#7800C3', '#7A00C2', '#7C00C1', '#7E00C0', '#8000BF', '#8200BE', '#8400BD', '#8600BC', '#8800BB', '#8A00BA', '#8C00B9', '#8E00B8', '#9000B7', '#9200B6', '#9400B5', '#9600B4', '#9800B3', '#9A00B2', '#9C00B1', '#9E00B0', '#A000AF', '#A200AE', '#A400AD', '#A600AC', '#A800AB', '#AA00AA', '#AC00A9', '#AE00A8', '#B000A7', '#B200A6', '#B400A5', '#B600A4', '#B800A3', '#BA00A2', '#BC00A1', '#BE00A0', '#C0009F', '#C2009E', '#C4009D', '#C6009C'],
			'Sunset':['#FFA500', '#FFA407', '#FFA30E', '#FFA215', '#FFA11C', '#FFA023', '#FF9F2A', '#FF9E31', '#FF9D38', '#FF9C3F', '#FF9B46', '#FF9A4D', '#FF9954', '#FF985B', '#FF9762', '#FF9669', '#FF9570', '#FF9477', '#FF937E', '#FF9285', '#FF918C', '#FF9093', '#FF8F9A', '#FF8EA1', '#FF8DA8', '#FF8CAF', '#FF8BB6', '#FF8ABD', '#FF89C4', '#FF88CB', '#FF87D2', '#FF86D9', '#FF85E0', '#FF84E7', '#FF83EE', '#FF82F5', '#FF81FC', '#FF80FF', '#FF7EFF', '#FF7CFF', '#FF7AFF', '#FF78FF', '#FF76FF', '#FF74FF', '#FF72FF', '#FF70FF', '#FF6EFF', '#FF6CFF', '#FF6AFF', '#FF69FF', '#FF69FF', '#F968F6', '#F367ED', '#ED66E4', '#E765DB', '#E164D2', '#DB63C9', '#D562C0', '#CF61B7', '#C960AE', '#C35FA5', '#BD5E9C', '#B75D93', '#B15C8A', '#AB5B81', '#A55A78', '#9F596F', '#995866', '#93575D', '#8D5654', '#87554B', '#815442', '#7B5339', '#755230', '#6F5127', '#69401E', '#633F15', '#5D3E0C', '#573D03', '#513C00', '#4B3B00', '#453A00', '#3F3900', '#393800', '#333700', '#2D3600', '#273500', '#213400', '#1B3300', '#153200', '#0F3100', '#093000', '#032F00', '#002E00', '#002D00', '#002C00', '#002B00', '#002A00', '#002900', '#002800'],
			'Ocean':['#008080', '#007D82', '#007A85', '#007887', '#00758A', '#00728C', '#00708F', '#006D92', '#006B94', '#006897', '#006599', '#00639C', '#00609F', '#005EA1', '#005BA4', '#0058A6', '#0056A9', '#0053AC', '#0050AE', '#004EB1', '#004BB3', '#0049B6', '#0046B9', '#0043BB', '#0041BE', '#003EC0', '#003CC3', '#0039C5', '#0036C8', '#0034CB', '#0031CD', '#002FD0', '#002CD2', '#0029D5', '#0027D8', '#0024DA', '#0021DD', '#001FDF', '#001CE2', '#001AE5', '#0017E7', '#0014EA', '#0012EC', '#000FEF', '#000DF2', '#000AF4', '#0007F7', '#0005F9', '#0002FC', '#0000FF', '#0000FF', '#0000FC', '#0000F9', '#0000F7', '#0000F4', '#0000F2', '#0000EF', '#0000EC', '#0000EA', '#0000E7', '#0000E5', '#0000E2', '#0000DF', '#0000DD', '#0000DA', '#0000D8', '#0000D5', '#0000D2', '#0000D0', '#0000CD', '#0000CB', '#0000C8', '#0000C5', '#0000C3', '#0000C0', '#0000BE', '#0000BB', '#0000B9', '#0000B6', '#0000B3', '#0000B1', '#0000AE', '#0000AC', '#0000A9', '#0000A6', '#0000A4', '#0000A1', '#00009F', '#00009C', '#000099', '#000097', '#000094', '#000092', '#00008F', '#00008C', '#00008A', '#000087', '#000085', '#000082', '#000080'],
			'Cool Ice':['#FFFFFF', '#FDFEFE', '#FBFDFD', '#F9FCFD', '#F8FBFC', '#F6FBFC', '#F4FAFB', '#F3F9FB', '#F1F8FA', '#EFF7FA', '#EEF7F9', '#ECF6F9', '#EAF5F8', '#E9F4F8', '#E7F3F7', '#E5F3F7', '#E4F2F6', '#E2F1F6', '#E0F0F5', '#DFEFF5', '#DDEFF4', '#DBEEF4', '#DAEDF3', '#D8ECF3', '#D6EBF2', '#D5EBF2', '#D3EAF1', '#D1E9F1', '#D0E8F0', '#CEE7F0', '#CCE7EF', '#CBE6EF', '#C9E5EE', '#C7E4EE', '#C6E3ED', '#C4E3ED', '#C2E2EC', '#C1E1EC', '#BFE0EB', '#BDDFEB', '#BCDFEA', '#BADEEA', '#B8DDE9', '#B7DCE9', '#B5DBE8', '#B3DBE8', '#B2DAE7', '#B0D9E7', '#AED8E6', '#ADD8E6', '#ADD8E6', '#A9D8E6', '#A5D9E7', '#A2DAE7', '#9EDBE8', '#9BDBE8', '#97DCE9', '#94DDE9', '#90DEEA', '#8DDFEA', '#89DFEB', '#86E0EB', '#82E1EC', '#7FE2EC', '#7BE3ED', '#78E3ED', '#74E4EE', '#70E5EE', '#6DE6EF', '#69E7EF', '#66E7F0', '#62E8F0', '#5FE9F1', '#5BEAF1', '#58EBF2', '#54EBF2', '#51ECF3', '#4DEDF3', '#4AEEF4', '#46EFF4', '#43EFF5', '#3FF0F5', '#3CF1F6', '#38F2F6', '#34F3F7', '#31F3F7', '#2DF4F8', '#2AF5F8', '#26F6F9', '#23F7F9', '#1FF7FA', '#1CF8FA', '#18F9FB', '#15FAFB', '#11FBFC', '#0EFBFC', '#0AFCFD', '#07FDFD', '#03FEFE', '#00FFFF'],
			'Rainbow':['#FF0000', '#FF0F00', '#FF1E00', '#FF2D00', '#FF3D00', '#FF4C00', '#FF5B00', '#FF6B00', '#FF7A00', '#FF8900', '#FF9900', '#FFA800', '#FFB700', '#FFC600', '#FFD600', '#FFE500', '#FFF400', '#F9FF00', '#EAFF00', '#DBFF00', '#CBFF00', '#BCFF00', '#ADFF00', '#9EFF00', '#8EFF00', '#7FFF00', '#70FF00', '#60FF00', '#51FF00', '#42FF00', '#33FF00', '#23FF00', '#14FF00', '#05FF00', '#00FF0A', '#00FF19', '#00FF28', '#00FF38', '#00FF47', '#00FF56', '#00FF66', '#00FF75', '#00FF84', '#00FF93', '#00FFA3', '#00FFB2', '#00FFC1', '#00FFD1', '#00FFE0', '#00FFEF', '#00FFFF', '#00EFFF', '#00E0FF', '#00D1FF', '#00C1FF', '#00B2FF', '#00A3FF', '#0093FF', '#0084FF', '#0075FF', '#0066FF', '#0056FF', '#0047FF', '#0038FF', '#0028FF', '#0019FF', '#000AFF', '#0500FF', '#1400FF', '#2300FF', '#3200FF', '#4200FF', '#5100FF', '#6000FF', '#7000FF', '#7F00FF', '#8E00FF', '#9E00FF', '#AD00FF', '#BC00FF', '#CC00FF', '#DB00FF', '#EA00FF', '#F900FF', '#FF00F4', '#FF00E5', '#FF00D6', '#FF00C6', '#FF00B7', '#FF00A8', '#FF0098', '#FF0089', '#FF007A', '#FF006B', '#FF005B', '#FF004C', '#FF003D', '#FF002D', '#FF001E', '#FF000F'],
		}
		if name in ranges:
			return ranges[name]
		return None
		
	
	def internal_object_configure (self, isolation, type, object, objectname, **opts):
		config = {}
		if 'Width' in opts and isinstance (opts['Width'], int):
			config['width'] = opts['Width']
		if 'Width.Checkbox' in opts and isinstance (opts['Width.Checkbox'], int):
			if type == 'CheckBox':
				config['checkbox_width'] = opts['Width.Checkbox']
		if 'Checked' in opts:
			if type == 'CheckBox':
				if opts['Checked'] is True:
					object['Value'] = True
					object[objectname].select ()
				elif opts['Checked'] is False:
					object['Value'] = False
					object[objectname].deselect ()
		if 'Height' in opts and isinstance (opts['Height'], int):
			config['height'] = opts['Height']
		if 'Height.Checkbox' in opts and isinstance (opts['Height.Checkbox'], int):
			if type == 'CheckBox':
				config['checkbox_height'] = opts['Height.Checkbox']
		if 'Readonly' in opts and type == 'Entry':
			config['state'] = ('readonly' if opts['Readonly'] is True else 'normal')
		if 'Disabled' in opts:
			config['state'] = ('disabled' if opts['Disabled'] is True else (config['state'] if 'state' in config else 'normal'))
		if 'Value' in opts:
			if type in ['Entry', 'DatePicker']:
				object[objectname].delete (-1, customtkinter.END)
				object[objectname].insert (-1, ('' if opts['Value'] is None else opts['Value']))
				object['Value'] = ('' if opts['Value'] is None else copy.deepcopy (opts['Value']))
			elif type in ['ProgressBar']:
				self.internal_progressbar_update (object, Progress=opts['Value'])
		if 'Value.Placeholder' in opts:
			config['placeholder_text'] = opts['Value.Placeholder']
		if 'Progress' in opts and isinstance (opts['Process'], int) and type in ['ProgressBar']:
			self.internal_progressbar_update (object, Progress=opts['Progress'])
		if 'ProgressColor' in opts and isinstance (opts['ProgressColor'], str) and type in ['ProgressBar']:
			self.internal_progressbar_update (object, ProgressColor=opts['ProgressColor'])
		if 'Background.Checkbox' in opts:
			if type == 'CheckBox':
				config['fg_color'] = (object['Defaults']['fg_color'] if opts['Background.Checkbox'] is None else opts['Background.Checkbox'])
		if 'Background' in opts:
			if type == 'CheckBox':
				config['bg_color'] = (object['Defaults']['bg_color'] if opts['Background'] is None else opts['Background'])
			else:
				config['fg_color'] = (object['Defaults']['fg_color'] if opts['Background'] is None else opts['Background'])
		if 'Text' in opts:
			config['text'] = opts['Text']
		if 'Border' in opts and isinstance (opts['Border'], int):
			config['border_width'] = opts['Border']
		if 'Border.Color' in opts:
			config['border_color'] = opts['Border.Color']

		if len (config) > 0:
			object[objectname].configure (**config)
		
		return config
	