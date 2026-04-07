# Copyright (c) 2025-2026 Erik Persson
# Licensed for free use only. Copying, modification, or redistribution prohibited.

import builtins
from Functions.Common import *
from Functions.DataHandling import *
for name in dir ():
	if not name.startswith ("_"):
		builtins.__dict__[name] = globals ()[name]
import threading
builtins.threading = threading

class SQL:
	def __init__ (self, cls_steps):
		self.cls_steps = cls_steps
	
		
	def dynamic_function (self, function, to_class = True):
		if to_class is True:
			func = {}
			exec (function['Code'], func)
			setattr (SQL, function['Function'], func[function['Function']])
		else:
			exec (function['Code'], globals ())
			builtins.__dict__[function['Function']] = globals ()[function['Function']]
	
	
	def execute (self, isolation, **opts):
		try:
			if opts['Function'] == 'SQL:Table.Create':
				return self.step_table_create (isolation, **opts)
			elif opts['Function'] == 'SQL:Table.Drop':
				return self.step_table_drop (isolation, **opts)
			elif opts['Function'] == 'SQL:Table.DataColumnDetermination':
				return self.step_table_data_column_determination (isolation, **opts)
			elif opts['Function'] == 'SQL:Table.Insert':
				return self.step_table_insert (isolation, **opts)
			elif opts['Function'] == 'SQL:Query.Select':
				return self.step_query_select (isolation, **opts)
			elif opts['Function'] == 'SQL:Query.Select.Mass':
				return self.step_query_select_mass (isolation, **opts)
			elif opts['Function'] == 'SQL:Query.Select.Easy':
				return self.step_query_select_easy (isolation, **opts)
			else:
				return False, {'Status':'WARNING', 'Title':'SQL:execute: Aborted', 'Message':'Unknown execute:' + str (opts)}
		except Exception as e:
			st = internal_zyd_stacktrace (e, FunctionOpts=opts)
			return False, {'Status':'CRASH', 'Title':'SQL:execute: Crashed', 'Message':'Crashed with the error: ' + str (e) + ' for step:\n' + str (opts), 'StackTrace':st}

	
	def step_table_create (self, isolation = None, **opts):
		if 'Table' not in opts:
			return False, {'Status':'WARNING', 'Title':'SQL:step_table_create: Aborted', 'Message':'A "Table" variable is required for this function to work.'}
		if 'Columns' not in opts:
			return False, {'Status':'WARNING', 'Title':'SQL:step_table_create: Aborted', 'Message':'A "Columns" variable is required for this function to work.'}
		if not isinstance (opts['Columns'], dict):
			return False, {'Status':'WARNING', 'Title':'SQL:step_table_create: Aborted', 'Message':'The "Columns" variable is required to be a dict of columns and their format for this function to work.'}

		columns_raw = opts['Columns']
		query = "CREATE TABLE " + ("IF NOT EXISTS " if 'Create.IfNotExists' in opts and opts['Create.IfNotExists'] is True else '') + "`" + opts['Table'] + "` ("
		columns = []
		for field in columns_raw.keys ():
			columns.append ("`" + field + "` " + columns_raw[field])
		query += '\n,'.join (columns) + ')'
		
		if 'SQLite.File' in opts:
			status, result = self.internal_zyd_db_query (Query=query, DB='sqlite:///' + opts['SQLite.File'])
		else:
			status, result = self.internal_zyd_db_query (Query=query, InternalDB=True)
		if status is True:
			return True, {'Status':'OK', 'Message':'Table "' + str (opts['Table']) + '" created.'}
		return status, result
	
	
	def step_table_drop (self, isolation = None, **opts):
		if 'Table' not in opts:
			return False, {'Status':'WARNING', 'Title':'SQL:step_table_drop: Aborted', 'Message':'A "Table" variable is required for this function to work.'}
		
		query = "DROP TABLE " + ("IF EXISTS " if 'Drop.IfExists' in opts and opts['Drop.IfExists'] is True else '') + "`" + opts['Table'] + "`"
		if 'SQLite.File' in opts:
			status, result = self.internal_zyd_db_query (Query=query, DB='sqlite:///' + opts['SQLite.File'])
		else:
			status, result = self.internal_zyd_db_query (Query=query, InternalDB=True)
		if status is True:
			return True, {'Status':'OK', 'Message':'Table "' + str (opts['Table']) + '" dropped.'}
		return status, result
	
	
	def step_table_data_column_determination (self, isolation = None, **opts):
		columns = {}
		columns_list = []
		for column in opts['Columns']:
			columns[column] = 'INTEGER'
			columns_list.append (column)
		no_columns = len (columns)
		primary = {}
		for row in opts['Data']:
			if len (row) == no_columns:
				for column in range (0, no_columns):
					if 'ColumnPrimary' in opts and columns_list[column] == opts['ColumnPrimary']:
						if row[column] in primary:
							return False, {'Status':'ERROR', 'Title':'SQL.step_table_data_column_determination: Aborted', 'Message':'Duplicate values for the primary columns.'}
						else:
							primary[row[column]] = True
					if columns[columns_list[column]] == 'TEXT':
						continue
					elif columns[columns_list[column]] in ['INTEGER', 'REAL'] and isinstance (row[column], str):
						value = (row[column][1:] if len (row[column]) > 0 and row[column][0] in ['+', '-'] else row[column])
						if columns[columns_list[column]] == 'INTEGER' and not value.isdigit ():
							if '.' not in value:
								columns[columns_list[column]] = 'TEXT'
							elif value.count ('.') == 1 and value.replace ('.', '').isdigit ():
								columns[columns_list[column]] = 'REAL'
							else:
								cvalue = copy.deepcopy (value)
								for char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']:
									cvalue = cvalue.replace (char, '')
								if len (cvalue.strip ()) > 0:
									columns[columns_list[column]] = 'TEXT'
								else:
									return False, {'Status':'ERROR', 'Title':'SQL.step_table_data_column_determination: Aborted', 'Message':'Unknown INTEGER/REAL logic (value="' + str (value) + '")'}
						elif columns[columns_list[column]] == 'REAL':
							if value.count ('.') == 1 and value.replace ('.', '').isdigit ():
								continue
							else:
								return False, {'Status':'ERROR', 'Title':'SQL.step_table_data_column_determination: Aborted', 'Message':'Unknown REAL logic (value="' + str (value) + '")'}
		if 'ColumnPrimary' in opts:
			columns[opts['ColumnPrimary']] += " PRIMARY KEY"
		
		if 'ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str):
			self.cls_steps.internal_value_set_value (isolation, 'Variable', columns, opts['ReturnVariable'])
		if 'ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str):
			self.cls_steps.internal_value_set_value (None, 'Variable', columns, opts['ReturnVariable.Global'])
		return True, {'Status':'OK', 'Data':columns}
	
	
	def step_table_insert (self, isolation = None, **opts):
		query = "INSERT INTO `" + opts['Table'] + "` (`" + "`, `".join (opts['Columns']) + "`) VALUES "
		values = []
		for value in opts['Values']:
			for i in range (0, len (value)):
				value[i] = internal_zyd_db_value (value[i])
			values.append ("(" + ", ".join (value) + ")")
		query += "\n,".join (values)
		if 'SQLite.File' in opts:
			status, result = self.internal_zyd_db_query (Query=query, DB='sqlite:///' + opts['SQLite.File'])
		else:
			status, result = self.internal_zyd_db_query (Query=query, InternalDB=True)
		
		if status is True:
			return True, {'Status':'OK', 'Message':'Records created'}
		if 'Function.ErrorVariable' in opts and 'Error' in result and isinstance (opts['Function.ErrorVariable'], str):
			self.cls_steps.internal_value_set_value (isolation, 'Variable', result['Error'], opts['Function.ErrorVariable'])
		if 'Function.ErrorVariable.Global' in opts and 'Error' in result and isinstance (opts['Function.ErrorVariable.Global'], str):
			self.cls_steps.internal_value_set_value (None, 'Variable', result['Error'], opts['Function.ErrorVariable.Global'])
		
		return status, result
	
	
	def step_query_select_mass (self, isolation = None, **opts):
		if 'Queries' not in opts or not isinstance (opts['Queries'], dict):
			return True, {'Status':'WARNING', 'Title':'SQL:step_query_select_mass: Aborted', 'Message':'Queries needs to be a dict with queries to execute.'}
		for query in opts['Queries'].keys ():
			query_opts = {}
			for opts_key in opts.keys ():
				if opts_key not in ['Queries', 'ReturnVariable.Global']:
					query_opts[opts_key] = copy.deepcopy (opts[opts_key])
			query_opts['Query'] = opts['Queries'][query]
			query_opts[('ReturnVariable.Global' if 'ReturnVariables.Global' in opts and opts['ReturnVariables.Global'] is True else 'ReturnVariable')] = query
			status, result = self.step_query_select (**query_opts)
			if status is not True:
				return status, result
		return True, {'Status':'OK'}
		

	def step_query_select (self, isolation = None, **opts):
		if 'Query' not in opts or not isinstance (opts['Query'], str):
			return True, {'Status':'WARNING', 'Title':'SQL:step_query_select: Aborted', 'Message':'No valid Query was provided.'}
		if 'ReturnType' not in opts or not isinstance (opts['ReturnType'], str):
			return True, {'Status':'WARNING', 'Title':'SQL:step_query_select: Aborted', 'Message':'No valid ReturnType was provided.'}

		if 'SQLite.File' in opts:
			status, result = self.internal_zyd_db_query (Query=opts['Query'], DB='sqlite:///' + opts['SQLite.File'])
		else:
			status, result = self.internal_zyd_db_query (Query=opts['Query'], InternalDB=True)
		
		if status is True:
			status, result = zyd_db_fetch (result, All=True, Close=True)
			if status is True:
				if 'ReturnType' in opts:
					if opts['ReturnType'] in ['String', 'Integer', 'Decimal']:
						print (result)
						if result is None or result[0][list (result[0].keys ())[0]] is None:
							value = None
						elif len (result) == 1 and len (result[0]) == 1:
							if opts['ReturnType'] == 'String':
								value = str (result[0][list (result[0].keys ())[0]])
							elif opts['ReturnType'] == 'Integer':
								value = int (result[0][list (result[0].keys ())[0]])
							else:
								value = float (result[0][list (result[0].keys ())[0]])
						else:
							return True, {'Status':'WARNING', 'Title':'', 'Message':'Select query "' + str (opts['Query']) + '" did not generate a single value and can\'t use the ReturnType="' + str (opts['ReturnType']) + '".'}
					elif opts['ReturnType'] == 'List':
						value = list (result)
				if 'ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str):
					self.cls_steps.internal_value_set_value (isolation, 'Variable', value, opts['ReturnVariable'])
				if 'ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str):
					self.cls_steps.internal_value_set_value (None, 'Variable', value, opts['ReturnVariable.Global'])
				if 'UpdateGUI.Value' in opts and isinstance (opts['UpdateGUI.Value'], str):
					self.cls_steps.cls_gui.internal_object_update (isolation, opts['UpdateGUI.Value'], Value=value, Trigger=(True if 'UpdateGUI.Value.Trigger' in opts and opts['UpdateGUI.Value.Trigger'] is True else False))
				return True, {'Status':'OK', 'Data':value, 'Message':'Select query executed.'}
		return status, result
	
	
	def step_query_select_easy (self, isolation = None, **opts):
		status = False
		result = {'Status':'WARNING', 'Title':'SQL:step_query_select_easy: Aborted'}
		data = None
		if 'DB.Tables' in opts and opts['DB.Tables'] is True:
			data = []
			opts['Query'] = "SELECT name AS `Table` FROM sqlite_master WHERE type='table'"
			status, db_result = self.step_query_select (**opts)
			if status is not True:
				return status, db_result
			for row in db_result['Data']:
				data.append (str (row['Table']))
			result = {'Status':'OK'}
		elif 'DB.Table.Columns' in opts and opts['DB.Table.Columns'] is True:
			data = {}
			opts['Query'] = "SELECT p.name AS col_name, p.type AS col_type, p.pk AS col_is_pk, p.dflt_value AS col_default_val, p.[notnull] AS col_is_not_null FROM sqlite_master m LEFT OUTER JOIN pragma_table_info((m.name)) p ON m.name <> p.name WHERE m.type = 'table' ORDER BY table_name, col_id"
			opts['Query'] = "PRAGMA table_info(`" + str (opts['Table']) + "`)"
			status, db_result = self.step_query_select (**opts)
			if status is not True:
				return status, db_result
			for row in db_result['Data']:
				data[row['name']] = row['type']
			result = {'Status':'OK'}
		
		if 'ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str):
			self.cls_steps.internal_value_set_value (isolation, 'Variable', data, opts['ReturnVariable'])
		if 'ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str):
			self.cls_steps.internal_value_set_value (None, 'Variable', data, opts['ReturnVariable.Global'])
		return status, result


	def internal_zyd_db_query (self, **opts):
		if 'zyd_db_query' not in self.cls_steps.objects['Lock']:
			self.cls_steps.objects['Lock']['zyd_db_query'] = threading.RLock ()
		with self.cls_steps.objects['Lock']['zyd_db_query']:
			return zyd_db_query (**opts)