# Copyright (c) 2025-2026 Erik Persson
# Licensed for free use only. Copying, modification, or redistribution prohibited.

import builtins
from logging import exception, error
from Functions.Common import *
from Functions.DataHandling import *
for name in dir ():
	if not name.startswith ("_"):
		builtins.__dict__[name] = globals ()[name]
import hashlib
builtins.hashlib = hashlib
import os
builtins.os = os
import shutil
builtins.shutil = shutil
import tempfile
builtins.tempfile = tempfile
import pathlib
builtins.pathlib = pathlib
import filecmp
builtins.filecmp = filecmp

class IO:
	def __init__ (self, cls_steps):
		self.cls_steps = cls_steps
	
	
	def dynamic_function (self, function, to_class = True):
		if to_class is True:
			func = {}
			exec (function['Code'], func)
			setattr (IO, function['Function'], func[function['Function']])
		else:
			exec (function['Code'], globals ())
			builtins.__dict__[function['Function']] = globals ()[function['Function']]
	
	
	def execute (self, isolation = None, **opts):
		try:
			if opts['Function'] == 'IO:File.Exists':
				return self.step_file_exists (isolation, **opts)
			elif opts['Function'] == 'IO:File.MD5':
				return self.step_file_md5 (isolation, **opts)
			elif opts['Function'] == 'IO:File.Copy':
				return self.step_file_copy (isolation, **opts)
			elif opts['Function'] == 'IO:File.Remove':
				return self.step_file_remove (isolation, **opts)
			elif opts['Function'] == 'IO:File.Info':
				return self.step_file_info (isolation, **opts)
			elif opts['Function'] == 'IO:Files.Compare':
				return self.step_files_compare (isolation, **opts)
			elif opts['Function'] == 'IO:Path.Exists':
				return self.step_path_exists (isolation, **opts)
			elif opts['Function'] == 'IO:Path.Transform':
				return self.step_path_transform (isolation, **opts)
			elif opts['Function'] == 'IO:Path.List':
				return self.step_path_list (isolation, **opts)
			elif opts['Function'] == 'IO:Folder.Create':
				return self.step_folder_create (isolation, **opts)
			elif opts['Function'] == 'IO:Flow':
				return self.step_flow (isolation, **opts)
			else:
				return False, {'Status':'WARNING', 'Title':'IO:execute: Aborted', 'Message':'Unknown execute:' + str (opts)}
		except Exception as e:
			st = internal_zyd_stacktrace (e, FunctionOpts=opts)
			return False, {'Status':'CRASH', 'Title':'IO:execute: Crashed', 'Message':'Crashed with the error: ' + str (e) + ' for step:\n' + str (opts), 'StackTrace':st}

	
	def step_file_exists (self, isolation, **opts):
		if 'File' not in opts:
			return False, {'Status':'WARNING', 'Title':'IO:step_file_exists: Aborted', 'Message':'No File was provided.'}
		result = os.path.exists (opts['File'])
		if 'ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str):
			self.cls_steps.internal_value_set_value (isolation, 'Variable', result, opts['ReturnVariable'])
		if 'ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str):
			self.cls_steps.internal_value_set_value (None, 'Variable', result, opts['ReturnVariable.Global'])
		return True, {'Status':'OK', 'Data':result}
	
	
	def step_file_info (self, isolation, **opts):
		if 'File' not in opts:
			return False, {'Status':'WARNING', 'Title':'IO:step_file_info: Aborted', 'Message':'No File was provided.'}
		if not os.path.exists (opts['File']):
			return False, {'Status':'WARNING', 'Title':'IO:step_file_info: Aborted', 'Message':'The File "' + str (opts['File']) + '" does not exist.'}
		if 'Logic' not in opts:
			return False, {'Status':'WARNING', 'Title':'IO:step_file_info: Aborted', 'Message':'No Logic was provided.'}

		if opts['Logic'] == 'Size':
			result = os.path.getsize (opts['File'])
		else:
			return False, {'Status':'WARNING', 'Title':'IO:step_file_info: Aborted', 'Message':'The Logic "' + str (opts['Logic']) + '" is unsupported.'}
		
		if 'ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str):
			self.cls_steps.internal_value_set_value (isolation, 'Variable', result, opts['ReturnVariable'])
		if 'ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str):
			self.cls_steps.internal_value_set_value (None, 'Variable', result, opts['ReturnVariable.Global'])
		if 'UpdateGUI.Value' in opts and isinstance (opts['UpdateGUI.Value'], str):
			self.cls_steps.cls_gui.internal_object_update (isolation, opts['UpdateGUI.Value'], Value=result, Trigger=(True if 'UpdateGUI.Value.Trigger' in opts and opts['UpdateGUI.Value.Trigger'] is True else False))
		return True, {'Status':'OK'}
	
	
	def step_file_remove (self, isolation, **opts):
		if 'File' not in opts:
			return False, {'Status':'WARNING', 'Title':'IO:step_file_remove: Aborted', 'Message':'No File was provided.'}
		if tempfile.gettempdir () + '\\' not in opts['File']:
			return False, {'Status':'WARNING', 'Title':'IO:step_file_remove: Aborted', 'Message':'The file "' + str (opts['File']) + '" is not in the path "' + str (tempfile.gettempdir () + '\\') + '" and can\'t be deleted.'}
		if not os.path.exists (opts['File']):
			return False, {'Status':'WARNING', 'Title':'IO:step_file_remove: Aborted', 'Message':'The file "' + str (opts['File']) + '" does not exist.'}
		
		os.remove (opts['File'])
		return True, {'Status':'OK'}
	
	
	def step_file_md5 (self, isolation, **opts):
		if 'File' not in opts:
			return False, {'Status':'WARNING', 'Title':'IO:step_file_md5: Aborted', 'Message':'No File was provided.'}
		
		with open (opts['File'], "rb") as fp:
			md5 = hashlib.md5 ()
			while chunk := fp.read (8192):
				md5.update (chunk)
		result = md5.hexdigest ()
		del md5

		if 'ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str):
			self.cls_steps.internal_value_set_value (isolation, 'Variable', result, opts['ReturnVariable'])
		if 'ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str):
			self.cls_steps.internal_value_set_value (None, 'Variable', result, opts['ReturnVariable.Global'])
		return True, {'Status':'OK', 'Data':result}

	
	def step_file_copy (self, isolation, **opts):
		if 'File.Source' not in opts:
			return False, {'Status':'WARNING', 'Title':'IO:step_file_copy: Aborted', 'Message':'No File.Source was provided.'}
		if 'File.Destination' not in opts:
			return False, {'Status':'WARNING', 'Title':'IO:step_file_copy: Aborted', 'Message':'No File.Destination was provided.'}
		if not os.path.exists (opts['File.Source']):
			return False, {'Status':'WARNING', 'Title':'IO:step_file_copy: Aborted', 'Message':'No source file was found.'}
		if os.path.exists (opts['File.Destination']) and ('Overwrite' not in opts or opts['Overwrite'] is not True):
			return False, {'Status':'WARNING', 'Title':'IO:step_file_copy: Aborted', 'Message':'Destination file already exists and overwrite is not allowed.'}
		try:
			result = shutil.copy2 (opts['File.Source'], opts['File.Destination'])
		except Exception as e:
			return False, {'Status': 'CRASH', 'Title':'IO:step_file_copy: Crashed', 'Message':'Copying the file crashed with the following error: ' + str (e), 'Error':str (e)}
		
		if 'ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str):
			self.cls_steps.internal_value_set_value (isolation, 'Variable', result, opts['ReturnVariable'])
		if 'ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str):
			self.cls_steps.internal_value_set_value (None, 'Variable', result, opts['ReturnVariable.Global'])
		return True, {'Status':'OK', 'Data':result}
	
	
	def step_path_transform (self, isolation, **opts):
		if 'Path' in opts and isinstance (opts['Path'], str):
			path = os.path.expandvars (opts['Path'])
		elif 'Paths.Exist' in opts and isinstance (opts['Paths.Exist'], list):
			path = None
			for opath in opts['Paths.Exist']:
				opath = os.path.expandvars (opath)
				if pathlib.Path (opath).is_dir () is True:
					path = opath
					break
			if path is None:
				return False, {'Status':'WARNING', 'Title':'IO:step_path_transform: Aborted', 'Message':'No value path was found from the Paths.Exists variable.'}
		else:
			return False, {'Status':'WARNING', 'Title':'IO:step_path_transform: Aborted', 'Message':'No valid input was provided.'}
		
		if 'Path.Suffix' in opts and isinstance (opts['Path.Suffix'], str):
			path += opts['Path.Suffix']
		
		if 'ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str):
			self.cls_steps.internal_value_set_value (isolation, 'Variable', path, opts['ReturnVariable'])
		if 'ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str):
			self.cls_steps.internal_value_set_value (None, 'Variable', path, opts['ReturnVariable.Global'])
		return True, {'Status':'OK', 'Data':path}
	
	
	def step_path_exists (self, isolation, **opts):
		data = False
		if 'Path' in opts and pathlib.Path (opts['Path']).is_dir () is True:
			data = True
		
		if 'ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str):
			self.cls_steps.internal_value_set_value (isolation, 'Variable', data, opts['ReturnVariable'])
		if 'ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str):
			self.cls_steps.internal_value_set_value (None, 'Variable', data, opts['ReturnVariable.Global'])
		return True, {'Status':'OK', 'Data':data}
	
	
	def step_flow (self, isolation, **opts):
		if 'File' not in opts:
			return False, {'Status':'WARNING', 'Title':'IO:step_flow: Aborted', 'Message':'No File was provided.'}
		if 'Format' not in opts:
			return False, {'Status':'WARNING', 'Title':'IO:step_flow: Aborted', 'Message':'No Format was provided.'}
		if opts['Format'] not in ['JSON']:
			return False, {'Status':'WARNING', 'Title':'IO:step_flow: Aborted', 'Message':'The format "' + str (opts['Format']) + '" is not valid.'}
		if not os.path.exists (opts['File']):
			return False, {'Status':'WARNING', 'Title':'IO:step_flow: Aborted', 'Message':'The file "' + str (opts['File']) + '" does not exist.'}
		steps = None
		with (open (opts['File'], 'r') as file):
			content = file.read ().replace ('\r', '')
			if len (content) == 0:
				return False, {'Status':'WARNING', 'Title':'IO:step_flow: Aborted', 'Message':'The file "' + str (opts['File']) + '" was empty.'}
			if opts['Format'] == 'JSON':
				status, steps = zyd_json (content, Decode=True)
				if status is not True:
					return False, {'Status':'WARNING', 'Title':'IO:step_flow: Aborted', 'Message':'The file "' + str (opts['File']) + '" failed to open with the following error:\n' + str (steps)}
		
		if not isinstance (steps, list):
			return False, {'Status':'WARNING', 'Title':'IO:step_flow: Aborted', 'Message':'The file did not contain a list of steps.'}
		elif len (steps) == 0:
			return False, {'Status':'WARNING', 'Title':'IO:step_flow: Aborted', 'Message':'The file contained an empty list.'}
		count = len (steps)
		status, result = self.cls_steps.execute_steps (steps, isolation)
		if status is True:
			return True, {'Status':'OK', 'Message':str (count) + ' step' + ('s' if count != 1 else '') + ' executed successfully.'}
		return status, result
	
	
	def step_path_list (self, isolation, **opts):
		if 'Path' not in opts:
			return False, {'Status':'WARNING', 'Title':'IO:step_path_list: Aborted', 'Message':'No Path provided.'}
		elif pathlib.Path (opts['Path']).is_dir () is False:
			return False, {'Status':'WARNING', 'Title':'IO:step_path_list: Aborted', 'Message':'The Path "' + str (opts['Path']) + '" is not a directory.'}
		if 'Files' not in opts and 'Folders' not in opts:
			return False, {'Status':'WARNING', 'Title':'IO:step_path_list: Aborted', 'Message':'Neither Files or Folders were specified as the return type.'}
		path = pathlib.Path (opts['Path'])
		value = []
		if 'Size' in opts and opts['Size'] is True:
			size = 0
		if 'Count' in opts and opts['Count'] is True:
			count = 0
		for file in (path.rglob ('*') if 'Recursive' in opts and opts['Recursive'] is True else path.iterdir ()):
			if 'Files' in opts and opts['Files'] is True and file.is_file ():
				value.append (str (file))
				if 'Count' in opts and opts['Count'] is True:
					count += 1
				if 'Size' in opts and opts['Size'] is True:
					size += file.stat ().st_size
			if 'Folders' in opts and opts['Folders'] is True and file.is_dir ():
				value.append (str (file))
				if 'Count' in opts and opts['Count'] is True:
					count += 1

		if 'Path.Remove' in opts and opts['Path.Remove'] is True:
			length = len (opts['Path'])
			for key in range (0, len (value)):
				if value[key][0:length] == opts['Path']:
					value[key] = value[key][length:]
		
		if 'ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str):
			self.cls_steps.internal_value_set_value (isolation, 'Variable', value, opts['ReturnVariable'])
		if 'ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str):
			self.cls_steps.internal_value_set_value (None, 'Variable', value, opts['ReturnVariable.Global'])
		if 'Size' in opts and opts['Size'] is True:
			if 'ReturnVariable.Size' in opts and isinstance (opts['ReturnVariable.Size'], str):
				self.cls_steps.internal_value_set_value (isolation, 'Variable', size, opts['ReturnVariable.Size'])
			if 'ReturnVariable.Size.Global' in opts and isinstance (opts['ReturnVariable.Size.Global'], str):
				self.cls_steps.internal_value_set_value (None, 'Variable', size, opts['ReturnVariable.Size.Global'])
			if 'UpdateGUI.Size.Value' in opts and isinstance (opts['UpdateGUI.Size.Value'], str):
				self.cls_steps.cls_gui.internal_object_update (isolation, opts['UpdateGUI.Size.Value'], Value=size, Trigger=(True if 'UpdateGUI.Size.Value.Trigger' in opts and opts['UpdateGUI.Size.Value.Trigger'] is True else False))
		if 'Count' in opts and opts['Count'] is True:
			if 'ReturnVariable.Count' in opts and isinstance (opts['ReturnVariable.Count'], str):
				self.cls_steps.internal_value_set_value (isolation, 'Variable', count, opts['ReturnVariable.Count'])
			if 'ReturnVariable.Count.Global' in opts and isinstance (opts['ReturnVariable.Count.Global'], str):
				self.cls_steps.internal_value_set_value (None, 'Variable', count, opts['ReturnVariable.Count.Global'])
			if 'UpdateGUI.Count.Value' in opts and isinstance (opts['UpdateGUI.Count.Value'], str):
				self.cls_steps.cls_gui.internal_object_update (isolation, opts['UpdateGUI.Count.Value'], Value=count, Trigger=(True if 'UpdateGUI.Count.Value.Trigger' in opts and opts['UpdateGUI.Count.Value.Trigger'] is True else False))
		return True, {'Status':'OK', 'Message':str (len (value)) + ' values entries captured.'}
	
	
	def step_files_compare (self, isolation, **opts):
		if 'File1' not in opts:
			return False, {'Status':'WARNING', 'Title':'IO:step_files_compare: Aborted', 'Message':'No File1 provided.'}
		if 'File2' not in opts:
			return False, {'Status':'WARNING', 'Title':'IO:step_files_compare: Aborted', 'Message':'No File2 provided.'}
		if os.path.exists (opts['File1']) is False or os.path.exists (opts['File2']) is False:
			value = False
			reason = ''
			if os.path.exists (opts['File1']) is False:
				reason = 'File1 does not exist'
			if os.path.exists (opts['File2']) is False:
				reason = (reason + ' and ' if len (reason) > 0 else '') + 'File2 does not exist'
			reason += '.'
		else:
			matchrules = (opts['MatchRules'] if 'MatchRules' in opts and isinstance (opts['MatchRules'], list) else self.cls_steps.cls_flows.functions['IO:Files.Compare']['Input']['MatchRules']['Default'])
			size = os.path.getsize (opts['File1'])
			if 'Size' in matchrules and size != os.path.getsize (opts['File2']):
				value = False
				reason = 'File sizes mismatch (' + str (size) + ' vs. ' + str (os.path.getsize (opts['File2'])) + ').'
			elif 'Metadata' in matchrules and filecmp.cmp (opts['File1'], opts['File2'], shallow=True) is False:
				value = False
				reason = 'File metadata mismatches.'
			else:
				value = True
				reason = 'OK'
				if 'MD5.Minimal' in matchrules:
					if size <= 49152:
						if self.internal_files_compare_md5 (opts['File1']) != self.internal_files_compare_md5 (opts['File2']):
							value = False
							reason = 'MD5.Minimal mismatches (full).'
					elif self.internal_files_compare_md5 (opts['File1'], 0, 16384) != self.internal_files_compare_md5 (opts['File2'], 0, 16384):
						value = False
						reason = 'MD5.Minimal mismatches (start).'
					elif self.internal_files_compare_md5 (opts['File1'], int (size/2) - 8192, 16384) != self.internal_files_compare_md5 (opts['File2'], int (size/2) - 8192, 16384):
						value = False
						reason = 'MD5.Minimal mismatches (middle).'
					elif self.internal_files_compare_md5 (opts['File1'], size - 16384, 16384) != self.internal_files_compare_md5 (opts['File2'], size - 16384, 16384):
						value = False
						reason = 'MD5.Minimal mismatches (end).'
				if value is True and 'MD5.Full' in matchrules and ('MD5.Minimal' not in matchrules or size > 49152):
					if self.internal_files_compare_md5 (opts['File1']) != self.internal_files_compare_md5 (opts['File2']):
						value = False
						reason = 'MD5.Full mismatches.'
		
		if 'ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str):
			self.cls_steps.internal_value_set_value (isolation, 'Variable', value, opts['ReturnVariable'])
		if 'ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str):
			self.cls_steps.internal_value_set_value (None, 'Variable', value, opts['ReturnVariable.Global'])
		if 'ReturnVariable.Reason' in opts and isinstance (opts['ReturnVariable.Reason'], str):
			self.cls_steps.internal_value_set_value (isolation, 'Variable', reason, opts['ReturnVariable.Reason'])
		if 'ReturnVariable.Reason.Global' in opts and isinstance (opts['ReturnVariable.Reason.Global'], str):
			self.cls_steps.internal_value_set_value (None, 'Variable', reason, opts['ReturnVariable.Reason.Global'])
		return True, {'Status':'OK', 'Data':value, 'Message':reason}
	
	
	def step_folder_create (self, isolation, **opts):
		if 'Folder' not in opts:
			return False, {'Status':'WARNING', 'Title':'IO:step_folder_create: Aborted', 'Message':'No Folder provided.'}
		path = pathlib.Path (opts['Folder'])
		if path.is_dir () is True:
			return False, {'Status':'WARNING', 'Title':'IO:step_folder_create: Aborted', 'Message':'The Folder "' + str (opts['Folder']) + '" already exists.'}
		try:
			path.mkdir (exist_ok=False)
			return True, {'Status':'OK', 'Data':True}
		except Exception as e:
			st = internal_zyd_stacktrace (e, FunctionOpts=opts)
			return False, {'Status':'CRASH', 'Title':'IO:step_folder_create: Crashed', 'Message':'Crashed with the error: ' + str (e) + ' for folder "' + str (opts['Folder']) + '".', 'StackTrace':st}
	
	
	def internal_files_compare_md5 (self, file, offset = None, size = None):
		md5 = hashlib.md5 ()
		with open (file, "rb") as fp:
			if offset is None:
				for data in iter (lambda:fp.read (8192), b""):
					md5.update (data)
			else:
				fp.seek (offset)
				md5.update (fp.read (size))
			return md5.hexdigest ()