# Copyright (c) 2025-2026 Erik Persson
# Licensed for free use only. Copying, modification, or redistribution prohibited.

class Flows:
	help = {
		'Variables':{
			'Variable.Isolated':{'Syntax':'<$VARIABLE$>', 'Help':'Variables that are separated into different isolated area (if isolation is used, if not, uses the same area as global variables).\nWriting something like "Hello <$USER$>" will replace the <$USER$> part with the USER variable if it is used.'},
			'Variable.Global':{'Syntax':'<#VARIABLE#>', 'Help':'Global variables that are shared with non isolated areas or when a variable was specified to be global.\nWriting something like "Hello <#USER#>" will replace the <#USER#> part with the USER global variable if it is used.'},
			'InternalVariable':{'Syntax':'<@VARIABLE@>', 'Help':'This is used to look at internal variables.\n<@Steps@> contains how many steps that has been executed since the program was started.'},
			'GUI':{'Syntax':'<$#TYPE##ID#$>', 'Help':'Gets or sets the GUI variable for the specified type.\n<$#Entry##Name#$> would look for the GUI entry field with the ID Name and used that value.'},
		},
		'Convert':{
			'Type':{
				'String':'Converts the value into a string.',
				'Integer':'Converts the value into an integer if possible.',
				'Decimal':'Converts the value into an decimal if possible.',
				'Numeric':'Converts the value into an decimal or integer if possible.',
				'Date':'Converts the value into a string date, most usefull in combination with "DateFormat.To".',
				'Datetime':'',
				'DBDatetime':'',
				'Enum':'',
				'JSON':'Decodes the JSON string',
				'Boolean':'Convert he value into a Boolean (None, 0 and "" becomes False, anything else True.',
				'Array':'',
			},
			'Trim':{
				True:'If the converstion type is "String", this will strip leading and tailing spaces and newlines from the value.',
			},
			'Trim.Left':{
				True:'If the converstion type is "String", this will strip leading spaces and newlines from the value.',
				'String':'If the converstion type is "String", this will strip leading characters provided from the value.',
			},
			'Trim.Right':{
				True:'If the converstion type is "String", this will strip tailing spaces and newlines from the value.',
				'String':'If the converstion type is "String", this will strip tailing characters provided from the value.',
			},
			'Replace.Empty':{
				'Value':'If the value is an empty string, replace it with this value.'
			},
			'Replace.NULL':{
				'Value':'If the value is a NULL value, replace it with this value.'
			},
			'Canonicalize.Negative':{
				True:'If the converstion type is "String" and the string ends with a -, it will be moved to the front (so 128,23- would become -128,23).',
			},
			'Canonicalize.Positive':{
				True:'If the converstion type is "String" and the string starts or ends with a +, it will be removed (so 128,23+ or +128,23 would become 128,23).',
			},
			'NumberFormat.From':{
				'X,XXX,XXX.XX':'If the value is a string it will be transformed based on the specified number format (so 123,128.12 would become 123128.12).',
				'X XXX XXX,XX':'If the value is a string it will be transformed based on the specified number format (so 123 128,12 would become 123128.12).',
				'X.XXX.XXX,XX':'If the value is a string it will be transformed based on the specified number format (so 123.128,12 would become 123128.12).',
			},
			'NumberFormat.To':{
				'X,XXX,XXX.XX':'If the converstion type is "Number" it will be transformed based on the specified number format (so 123128.12 would become 123,128.12).',
				'X XXX XXX,XX':'If the converstion type is "Number" it will be transformed based on the specified number format (so 123128.12 would become 123 128,12).',
				'X.XXX.XXX,XX':'If the converstion type is "Number" it will be transformed based on the specified number format (so 123128.12 would become 123 128,12).',
			},
			'Encode':{
				'Charset':'If the converstion type is "String", encodes the string with the provided charset',
			},
			'Decode':{
				'Charset':'If the converstion type is "String", decodes the string with the provided charset',
			},
			'Decimals':{
				'Integer':'If the converstion type is "Number", "Decimal" or "Numeric" the value will be converted to this amount of decimals.',
			},
			'DateFormat.From':{
				'DD.MM.YYYY':'If the value is a string and at least 8 characters and had . on the right positions it will be converted to an ISO date (so 20.04.2025 would become 2025-04-20).',
				'MM/DD/YYYY':'If the value is a string and at least 8 characters and had / on the right positions it will be converted to an ISO date (so 04/20/2025 would become 2025-04-20).',
				'MM-DD-YYYY':'If the value is a string and at least 8 characters and had - on the right positions it will be converted to an ISO date (so 04-20-2025 would become 2025-04-20).',
				'YYYY.MM.DD':'If the value is a string and at least 8 characters and had . on the right positions it will be converted to an ISO date (so 2025.04.20 would become 2025-04-20).',
				'YYYY/MM/DD':'If the value is a string and at least 8 characters and had / on the right positions it will be converted to an ISO date (so 2025/04/20 would become 2025-04-20).',
				'YYYY-MM-DD':'Nothing will be done as it is the correct format.',
			},
			'DateFormat.To':{
				'DD.MM.YYYY':'If the conversion type is Date, this will convert the value from an ISO date to the specified format (so 2025-04-20 would become 20.04.2025).',
				'MM/DD/YYYY':'If the conversion type is Date, this will convert the value from an ISO date to the specified format (so 2025-04-20 would become 04/20/2025).',
				'MM-DD-YYYY':'If the conversion type is Date, this will convert the value from an ISO date to the specified format (so 2025-04-20 would become 04-20-2025).',
				'YYYY.MM.DD':'If the conversion type is Date, this will convert the value from an ISO date to the specified format (so 2025-04-20 would become 2025.04.20).',
				'YYYY/MM/DD':'If the conversion type is Date, this will convert the value from an ISO date to the specified format (so 2025-04-20 would become 2025/04/20).',
				'YYYY-MM-DD':'Nothing will be done as it is the correct format.',
			},
			'Replace':{
				'Dict':'If the converstion type is "String" and contains a dict, it will search for the keys and replace with the matching value.',
			},
			'NULL':{
				True:'If the converstion type is "String" and the value is empty, it will return NULL/None value instead.',
			},
			'JSON':{
				True:'If the converstion type is "String", returns a JSON string based on the value.',
			},
			'Glue':{
				'String':'If the converstion type is "String" and the input value is a list or dict, returns a string with this glue.',
			},
			'Path.Basename':{
				True:'If the converstion type is "String", returns the filename part of a path with filename.',
			},
			'Path.Dirname':{
				True:'If the converstion type is "String", returns the path part of a path with filename.',
			},
			'Array.Convert':{
				'Dict':'If the converstion type is "Array", this dict of convert types and a list of the convert rules will be executed for each value in the array. Works for the types String, Integer, Float & Decimal'
			},
		},
		'Verify':{
			'Type':{
				'Integer':'Verifies that the type is an Integer value.',
				'Decimal':'Verifies that the type is an Float value.',
				'Numeric':'Verifies that the type is an Integer or Float value.',
				'Datetime':'Verifies that the type is an Datetime value.',
				'List':'Verifies that the type is a list.',
				'Dict':'Verifies that the type is a dict.',
				'Enum':'Verifies that the value is in the list of Values.',
				'!Enum':'Verifies that the value is not in the list of Values.',
				'String':'Verifies that the type is an String value.',
				'Date':'Verifies that the type is an Date value.',
				'Boolean':'Verifies that the type is an Boolean value.',
				'Value':'Verifies that the value matches the value in Value.',
				'NULL':'Verifies that the value is NULL.',
				'!NULL':'Verifies that the value is not NULL.',
				'Array=Array':'Verifies that the input value is the same as what\'s in Values (list or dict).',
			},
			'Min':{
				'Value':'If the verify type is "Integer", "Decimal" or "Numeric", will check that the value isn\'t less than this value.',
			},
			'Max':{
				'Value':'If the verify type is "Integer", "Decimal" or "Numeric", will check that the value isn\'t greater than this value.',
			},
			'Greater':{
				'Value':'If the verify type is "Integer", "Decimal" or "Numeric", will check that the value isn\'t greater than this value.',
			},
			'Less':{
				'Value':'If the verify type is "Integer", "Decimal" or "Numeric", will check that the value isn\'t greater than this value.',
			},
			'Equal':{
				'Value':'If the verify type is "Integer", "Decimal" or "Numeric", will check that the value is equal to this value.',
			},
			'NotEqual':{
				'Value':'If the verify type is "Integer", "Decimal" or "Numeric", will check that the value isn\'t rqual to this value.',
			},
			'LengthMin':{
				'Value':'If the verify type is "String", will check that the value length isn\'t less than this value.',
			},
			'LengthMax':{
				'Value':'If the verify type is "String", will check that the value length isn\'t greater than this value.',
			},
			'Contains':{
				'String':'If the verify type is "String", will check that the value contains the specified string.',
			},
			'NotContains':{
				'String':'If the verify type is "String", will check that the value doesn\'t contain the specified string.',
			},
			'StartWith':{
				'String':'If the verify type is "String", will check that the value starts with the specified string.',
			},
			'NotStartWith':{
				'String':'If the verify type is "String", will check that the value doesn\'t start with the specified string.',
			},
			'EndWith':{
				'String':'If the verify type is "String", will check that the value ends with the specified string.',
			},
			'NotEndWith':{
				'String':'If the verify type is "String", will check that the value doesn\'t end with the specified string.',
			},
			'Value':{
				'Value':'If the verify type is "Value", "Boolean" or "String", will check that the value matches this value and type.',
			},
			'Values':{
				'List or Dict':'If the verify type is "Enum", "Value" or "String", will check that the value is in the specified list or dict.',
			},
			'EntriesMin':{
				'Value':'If the verify type is "List", will check that the number of entries are this number or more.',
			},
			'EntriesMax':{
				'Value':'If the verify type is "List", will check that the number of entries are this number or lower.',
			},
			'Key':{
				'Value':'If the verify type is "Dict", will check if the key is in the dict.',
				'List':'If the verify type is "Dict", will check if any of the keys are in the dict.',
			},
			'Keys':{
				'List':'If the verify type is "Dict", will check that all the keys are in the dict.',
			},
		},
		'Function':{
			'Function':'Specifies which function that should be executed in the step.',
			'_Function':'If this exists and Function is not used, then the step is skipped (used to temporarily disable a step).',
			'Function.Segment':'Decides which segment a step belongs to, used by the CORE:Break function to decide which steps to skip (if not segment is specified, * is used).',
			'Function.FullResult':'If True, doesn\'t compress the output result variable.',
			'Function.OnFailure':'A list of steps which are executed if the function fails.',
			'Function.OnSuccess':'A list of steps which are executed if the function succeeds.',
			'Function.OnSuccess.DataTrue':'',
			'Function.OnSuccess.DataFalse':'',
		},
		'Functions':{
			'Functions.OnFailure':'A list of steps which are executed if the function fails.',
			'Functions.OnError':'A list of steps which are executed if the function returns the status ERROR.',
			'Functions.OnWarning':'A list of steps which are executed if the function returns the status WARNING.',
			'Functions.OnCrash':'A list of steps which are executed if the function returns the status CRASH.',
			'Functions.OnSuccess':'A list of steps which are executed if the function succeeds.',
			'Functions.OnOK':'A list of steps which are executed if the function returns the status OK.',
			'Functions.Opts.Steps':'A list of opts keys which will be handled as Steps (adding to what comes from the base function setup).',
		},
	}
	version_core = 9
	version_build = {
		'Core':8,
		'Functions':122,
		'Versions':188,
		'InternalFunctions':19,
		'InternalVersions':34
	}
	versions = {
		'Common:internal_zyd_uniqueid':1,
		'Common:internal_zyd_date':2,
		'Common:internal_zyd_time':1,
		'Common:internal_zyd_ucfirst':1,
		'Common:internal_zyd_arrayreplace':1,
		'Common:internal_zyd_ceil':1,
		'Common:internal_zyd_floor':1,
		'Common:internal_zyd_db_value':1,
		'Common:internal_zyd_stacktrace':1,
		'Common:internal_zyd_shorten':1,
		'Common:internal_zyd_session_key':1,
		'Common:zyd_json':3,
		'Common:zyd_passwords':1,
		'Common:zyd_db_query':2,
		'Common:zyd_db_fetch':1,
		'Common:zyd_return':1,
		'Common:zyd_calc':2,
		'DataHandling:datahandling_convert':7,
		'DataHandling:datahandling_verify':7,
		'DataHandling:datahandling_verify_entry':1,
		'DataHandling:internal_datahandling_verify':1,
		'DataHandling:internal_datahandling_convert_array_convert':1,
	}
	functions = {
		'CORE:Break':{
			'Version':1,
			'Title':'Break',
			'Description':'Breaks the current chain of steps.',
			'Input':{
				'Segment':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':32}, 'Default':'*', 'Help':'Breaks the current chain of steps in the specified segment.'},
			},
		},
		'CORE:Function.Defaults':{
			'Title':'Sets global defaults for Function args',
			'Description':'',
			'Version':1,
			'Input':{
				'Defaults':{'Type':{'Type':'Dict'}, 'Default':{}, 'Help':'Sets the global defaults for Function arguments as listed below:\n* ' + '\n* '.join (func for func in help['Functions'] if func not in ['Function', 'Function.Segment'])},
			},
		},
		'CORE:Debug.Variables.Print':{
			'Version':3,
			'Title':'Prints debug for the content of variables',
			'Description':'',
			'Input':{
				'Output':{'Type':{'Type':'Enum', 'Values':['CONSOLE', 'LOG']}, 'Mandatory':'*', 'Default':'CONSOLE', 'Example':'LOG', 'Help':"""Controls to where the output will be sent:
* CONSOLE - prints the output to console
* LOG - outputs the debug to the log file if activated"""},
				'Variables':{'Type':{'Type':'List'}, 'Example':['TempVar', 'TempStr'], 'Help':'If used, will only print variables in this list.'},
				'Split':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'Controls if the output should be split by variable or just 3 complete dumps.'},
				'Print.Variable.MaxLength':{'Type':{'Type':'Integer'}, 'Example':100, 'Help':'Control the max length of a displayed variable.'},
				'Print.Variable.Full':{'Type':{'Type':'List'}, 'Example':['WEB:Debug', 'INT:Help'], 'Help':'A list of variables which will not displayed in full length.'},
			},
		},
		'CORE:Debug.Variable.Print':{
			'Version':2,
			'Title':'Prints debug for the content of a variable.',
			'Description':'',
			'Input':{
				'Variable':{'Type':{'Type':'String'}, 'Example':'TempVar', 'Help':'Prints the variable to console.'},
			},
		},
		'CORE:Debug.Print':{
			'Version':1,
			'Title':'Prints debug',
			'Description':'',
			'Input':{
				'Output':{'Type':{'Type':'Enum', 'Values':['CONSOLE']}, 'Mandatory':'*', 'Default':'CONSOLE', 'Example':'CONSOLE', 'Help':"""Controls to where the output will be sent:
* CONSOLE - prints the output to console"""},
				'Text':{'Type':{'Type':'String'}, 'Example':'Debug text: <$ID$>', 'Help':'Prints the text provided.'},
				'CONSOLE.Containment':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'Controls if the output for console should incluse containment output to make it easier to read.'},
			}
		},
		'GUI:Form':{
			'Version':3,
			'Title':'Creates a GUI form',
			'Description':'',
			'Input':{
				'Geometry':{'Type':{'Type':'String', 'LengthMin':3, 'LengthMax':32}, 'Default':'400x200', 'Example':'400x200', 'Help':'The input "400x200" creates a GUI form with the size of 400px wide and 200px high.'},
				'Title':{'Type':{'Type':'String', 'LengthMax':128}, 'Default':'Omoikane windows', 'Example':'Omoikane', 'Help':'The input "Omoikane" sets the title of the GUI form.'},
				'Resizable.Width':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'Controls if the forms width is resizable or not.'},
				'Resizable.Height':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'Controls if the forms height is resizable or not.'},
			},
		},
		'GUI:Exit':{
			'Version':2,
			'Title':'Exists the program',
			'Input':{},
		},
		'GUI:Button.Add':{
			'Version':2,
			'Title':'Creates a GUI button',
			'Description':'',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Mandatory':'*', 'Default':'ButtonID', 'Example':'Temp', 'Help':'The input "Temp" creates a GUI button with the ID of "Temp".\nThis is later used to identify the button.'},
				'FrameID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Example':'Frame1', 'Help':'Specifies into which frame the object should be placed if not the main one.'},
				'WindowID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Example':'Window1', 'Help':'Specifies into which window the object should be placed if not the main one.'},
				'Text':{'Type':{'Type':'String', 'LengthMax':128}, 'Example':'Exit', 'Help':'The input "Exit" displays the text as the button.'},
				'Width':{'Type':{'Type':'Integer', 'Min':1, 'Max':1024}, 'Example':'80', 'Help':'Sets the width of the object to 80.'},
				'Background':{'Type':{'Type':'String', 'LengthMax':32}, 'Example':'Blue', 'Help':'Sets the background of the object.'},
				'OnClick':{'Type':{'Type':'List'}, 'Steps':True},
				'Disabled':{'Type':{'Type':'Boolean'}, 'Example':'true', 'Help':'Controls if the button is disabled or not.'},
				'Placement.Row':{'Type':{'Type':'Integer'}, 'Mandatory':'*', 'Example':'1', 'Help':'The input "1" would place the object on the first row in the layout grid.'},
				'Placement.Column':{'Type':{'Type':'Integer'}, 'Mandatory':'*', 'Example':'1', 'Help':'The input "1" would place the object on the first column in the layout grid.'},
				'Placement.Colspan':{'Type':{'Type':'Integer'}, 'Example':'2', 'Help':'Control how many columns this object would occupy.'},
				'Placement.Rowspan':{'Type':{'Type':'Integer'}, 'Example':'2', 'Help':'Control how many rows this object would occupy.'},
				'Placement.Alignment':{'Type':{'Type':'Enum', 'Values':['E', 'N', 'S', 'W', 'NW', 'NE', 'SE', 'SW']}, 'Example':'SE', 'Help':'Controls the alignment of the object.\nE = East, N = North, W = West & S = South.\nCan be combined to SE, NW, NE, SW.'},
			},
		},
		'GUI:Button.Change':{
			'Version':1,
			'Title':'Changes a button',
			'Description':'',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Mandatory':'ID', 'Default':'ButtonID', 'Example':'Temp', 'Help':'The input "Temp" identifies which button to change.'},
				'IDs':{'Type':{'Type':'List'}, 'Mandatory':'ID', 'Default':['ID1', 'ID2'], 'Example':['Temp1', 'Temp2'], 'Help':'The input "Temp1", "Temp2" changes a GUI button with the ID of "Temp1" and "Temp2".'},
				'Text':{'Type':{'Type':'String', 'LengthMax':128}, 'Example':'50', 'Help':'The input "50" displays the text as the button.'},
				'Disabled':{'Type':{'Type':'Boolean'}, 'Example':'true', 'Help':'Controls if the button is disabled or not.'},
			},
		},
		'GUI:Entry.Add':{
			'Version':2,
			'Title':'Creates a GUI entry',
			'Description':'',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Mandatory':'*', 'Default':'EntryID', 'Example':'Temp', 'Help':'The input "Temp" creates a GUI input entry with the ID of "Temp".\nThis is later used to identify the entry object.'},
				'FrameID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Example':'Frame1', 'Help':'Specifies into which frame the object should be placed if not the main one.'},
				'WindowID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Example':'Window1', 'Help':'Specifies into which window the object should be placed if not the main one.'},
				'Value':{'Type':{'Type':'String', 'LengthMax':128}, 'Example':'50', 'Help':'The input "50" displays the text as the pre filled value of the entry.'},
				'Value.Placeholder':{'Type':{'Type':'String', 'LengthMax':128}, 'Example':'50', 'Help':'The input "50" displays the placeholder text for the entry.\nIf a Value has been specified, the placeholder will be ignored'},
				'Width':{'Type':{'Type':'Integer', 'Min':1, 'Max':1024}, 'Example':'80', 'Help':'Sets the width of the object to 80.'},
				'Background':{'Type':{'Type':'String', 'LengthMax':32}, 'Example':'Blue', 'Help':'Sets the background of the object.'},
				'OnChange':{'Type':{'Type':'List'}, 'Steps':True},
				'Disabled':{'Type':{'Type':'Boolean'}, 'Example':'true', 'Help':'Controls if the input field is disabled or not.'},
				'Readonly':{'Type':{'Type':'Boolean'}, 'Example':'false', 'Help':'Controls if the input field is readonly or not.'},
				'Placement.Row':{'Type':{'Type':'Integer'}, 'Mandatory':'*', 'Example':'1', 'Help':'The input "1" would place the object on the first row in the layout grid.'},
				'Placement.Column':{'Type':{'Type':'Integer'}, 'Mandatory':'*', 'Example':'1', 'Help':'The input "1" would place the object on the first column in the layout grid.'},
				'Placement.Colspan':{'Type':{'Type':'Integer'}, 'Example':'2', 'Help':'Control how many columns this object would occupy.'},
				'Placement.Rowspan':{'Type':{'Type':'Integer'}, 'Example':'2', 'Help':'Control how many rows this object would occupy.'},
				'Placement.Alignment':{'Type':{'Type':'Enum', 'Values':['E', 'N', 'S', 'W', 'NW', 'NE', 'SE', 'SW']}, 'Example':'SE', 'Help':'Controls the alignment of the object.\nE = East, N = North, W = West & S = South.\nCan be combined to SE, NW, NE, SW.'},
			},
		},
		'GUI:Entry.Change':{
			'Version':1,
			'Title':'Changes a GUI entry',
			'Description':'',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Mandatory':'ID', 'Default':'EntryID', 'Example':'Temp', 'Help':'The input "Temp" changes a GUI input entry with the ID of "Temp".'},
				'IDs':{'Type':{'Type':'List'}, 'Mandatory':'ID', 'Default':['ID1', 'ID2'], 'Example':['Temp1', 'Temp2'], 'Help':'The input "Temp1", "Temp2" changes a GUI input entry with the ID of "Temp1" and "Temp2".'},
				'Value':{'Type':{'Type':'String', 'LengthMax':128}, 'Example':'50', 'Help':'The input "50" displays the text as the pre filled value of the entry.'},
				'Value.Placeholder':{'Type':{'Type':'String', 'LengthMax':128}, 'Example':'50', 'Help':'The input "50" displays the placeholder text for the entry.\nIf a Value has been specified, the placeholder will be ignored'},
				'Width':{'Type':{'Type':'Integer', 'Min':1, 'Max':1024}, 'Example':'80', 'Help':'Sets the width of the object to 80.'},
				'Background':{'Type':{'Type':'String', 'LengthMax':32}, 'Example':'Blue', 'Help':'Sets the background of the object.'},
				'OnChange.Trigger':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'Controls if the OnChange logic should be triggered for a Value change.'},
				'Disabled':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'Controls if the input field is disabled or not.'},
				'Readonly':{'Type':{'Type':'Boolean'}, 'Example':False, 'Help':'Controls if the input field is readonly or not.'},
			},
		},
		'GUI:Textbox.Add':{
			'Version':2,
			'Title':'Creates a GUI textbox',
			'Description':'',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Mandatory':'*', 'Default':'TextboxID', 'Example':'Temp', 'Help':'The input "Temp" creates a GUI input entry with the ID of "Temp".\nThis is later used to identify the entry object.'},
				'FrameID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Example':'Frame1', 'Help':'Specifies into which frame the object should be placed if not the main one.'},
				'WindowID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Example':'Window1', 'Help':'Specifies into which window the object should be placed if not the main one.'},
				'Value':{'Type':{'Type':'String', 'LengthMax':128}, 'Example':'50', 'Help':'The input "50" displays the text as the pre filled value of the entry.'},
				'Width':{'Type':{'Type':'Integer', 'Min':1, 'Max':1024}, 'Example':'80', 'Help':'Sets the width of the object to 80.'},
				'Background':{'Type':{'Type':'String', 'LengthMax':32}, 'Example':'Blue', 'Help':'Sets the background of the object.'},
				'OnChange':{'Type':{'Type':'List'}, 'Steps':True},
				'Disabled':{'Type':{'Type':'Boolean'}, 'Example':'true', 'Help':'Controls if the input field is disabled or not.'},
				'Readonly':{'Type':{'Type':'Boolean'}, 'Example':'false', 'Help':'Controls if the input field is readonly or not.'},
				'Placement.Row':{'Type':{'Type':'Integer'}, 'Mandatory':'*', 'Example':'1', 'Help':'The input "1" would place the object on the first row in the layout grid.'},
				'Placement.Column':{'Type':{'Type':'Integer'}, 'Mandatory':'*', 'Example':'1', 'Help':'The input "1" would place the object on the first column in the layout grid.'},
				'Placement.Colspan':{'Type':{'Type':'Integer'}, 'Example':'2', 'Help':'Control how many columns this object would occupy.'},
				'Placement.Rowspan':{'Type':{'Type':'Integer'}, 'Example':'2', 'Help':'Control how many rows this object would occupy.'},
				'Placement.Alignment':{'Type':{'Type':'Enum', 'Values':['E', 'N', 'S', 'W', 'NW', 'NE', 'SE', 'SW']}, 'Example':'SE', 'Help':'Controls the alignment of the object.\nE = East, N = North, W = West & S = South.\nCan be combined to SE, NW, NE, SW.'},
			},
		},
		'GUI:TextBox.Change':{
			'Version':1,
			'Title':'Changes a GUI textbox',
			'Description':'',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Mandatory':'ID', 'Default':'TextboxID', 'Example':'Temp', 'Help':'The input "Temp" changes a GUI textbox with the ID of "Temp".'},
				'IDs':{'Type':{'Type':'List'}, 'Mandatory':'ID', 'Default':['ID1', 'ID2'], 'Example':['Temp1', 'Temp2'], 'Help':'The input "Temp1", "Temp2" changes a GUI textbox with the ID of "Temp1" and "Temp2".'},
				'Value':{'Type':{'Type':'String', 'LengthMax':128}, 'Example':'50', 'Help':'The input "50" displays the text as the pre filled value of the entry.'},
				'Width':{'Type':{'Type':'Integer', 'Min':1, 'Max':1024}, 'Example':'80', 'Help':'Sets the width of the object to 80.'},
				'Background':{'Type':{'Type':'String', 'LengthMax':32}, 'Example':'Blue', 'Help':'Sets the background of the object.'},
				'OnChange.Trigger':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'Controls if the OnChange logic should be triggered for a Value change.'},
				'Disabled':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'Controls if the input field is disabled or not.'},
				'Readonly':{'Type':{'Type':'Boolean'}, 'Example':False, 'Help':'Controls if the input field is readonly or not.'},
			},
		},
		'GUI:CheckBox.Add':{
			'Version':2,
			'Title':'Creates a GUI checkbox',
			'Description':'',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Mandatory':'*', 'Default':'CheckBoxID', 'Example':'Temp', 'Help':'The input "Temp" creates a GUI checkbox with the ID of "Temp".\nThis is later used to identify the checkbox object.'},
				'FrameID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Example':'Frame1', 'Help':'Specifies into which frame the object should be placed if not the main one.'},
				'WindowID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Example':'Window1', 'Help':'Specifies into which window the object should be placed if not the main one.'},
				'Text':{'Type':{'Type':'String', 'LengthMax':256}, 'Example':'50', 'Help':'The input "50" displays the text to the right of the checkbox.'},
				'Checked':{'Type':{'Type':'Boolean'}, 'Example':'true', 'Help':'Controls if the checkbox is checked or not.'},
				'Border':{'Type':{'Type':'Integer', 'Min':0, 'Max':32}, 'Example':'3', 'Help':'Sets the border width of the object to 3.'},
				'Border.Color':{'Type':{'Type':'String', 'LengthMax':32}, 'Example':'Gold', 'Help':'Sets the border color of the object.'},
				'Width':{'Type':{'Type':'Integer', 'Min':1, 'Max':1024}, 'Example':'30', 'Help':'Sets the width of the object to 30.'},
				'Height':{'Type':{'Type':'Integer', 'Min':1, 'Max':1024}, 'Example':'209', 'Help':'Sets the height of the object to 200.'},
				'Width.Checkbox':{'Type':{'Type':'Integer', 'Min':1, 'Max':1024}, 'Example':'20', 'Help':'Sets the width of the checkbox to 20.'},
				'Height.Checkbox':{'Type':{'Type':'Integer', 'Min':1, 'Max':1024}, 'Example':'20', 'Help':'Sets the height of the checkbox to 20.'},
				'Background':{'Type':{'Type':'String', 'LengthMax':32}, 'Example':'Blue', 'Help':'Sets the background of the object.'},
				'Background.Checkbox':{'Type':{'Type':'String', 'LengthMax':32}, 'Example':'Blue', 'Help':'Sets the background of the checkbox.'},
				'OnChange':{'Type':{'Type':'List'}, 'Steps':True, 'Help':'A list of steps which are performed if the checkbox is changed.'},
				'OnChange.Checked':{'Type':{'Type':'List'}, 'Steps':True, 'Help':'A list of steps which are performed if the checkbox is checked.'},
				'OnChange.Unchecked':{'Type':{'Type':'List'}, 'Steps':True, 'Help':'A list of steps which are performed if the checkbox is unchecked.'},
				'Disabled':{'Type':{'Type':'Boolean'}, 'Example':'true', 'Help':'Controls if the input field is disabled or not.'},
				'Placement.Row':{'Type':{'Type':'Integer'}, 'Mandatory':'*', 'Example':'1', 'Help':'The input "1" would place the object on the first row in the layout grid.'},
				'Placement.Column':{'Type':{'Type':'Integer'}, 'Mandatory':'*', 'Example':'1', 'Help':'The input "1" would place the object on the first column in the layout grid.'},
				'Placement.Colspan':{'Type':{'Type':'Integer'}, 'Example':'2', 'Help':'Control how many columns this object would occupy.'},
				'Placement.Rowspan':{'Type':{'Type':'Integer'}, 'Example':'2', 'Help':'Control how many rows this object would occupy.'},
				'Placement.Alignment':{'Type':{'Type':'Enum', 'Values':['E', 'N', 'S', 'W', 'NW', 'NE', 'SE', 'SW']}, 'Example':'SE', 'Help':'Controls the alignment of the object.\nE = East, N = North, W = West & S = South.\nCan be combined to SE, NW, NE, SW.'},
			},
		},
		'GUI:CheckBox.Change':{
			'Version':1,
			'Title':'Change a GUI checkbox',
			'Description':'',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Mandatory':'*', 'Default':'CheckBoxID', 'Example':'Temp', 'Help':'The input "Temp" changes a GUI checkbox with the ID of "Temp".'},
				'Text':{'Type':{'Type':'String', 'LengthMax':256}, 'Example':'50', 'Help':'The input "50" displays the text to the right of the checkbox.'},
				'Checked':{'Type':{'Type':'Boolean'}, 'Example':'true', 'Help':'Controls if the checkbox is checked or not.'},
				'Border':{'Type':{'Type':'Integer', 'Min':0, 'Max':32}, 'Example':'3', 'Help':'Sets the border width of the object to 3.'},
				'Border.Color':{'Type':{'Type':'String', 'LengthMax':32}, 'Example':'Gold', 'Help':'Sets the border color of the object.'},
				'Width':{'Type':{'Type':'Integer', 'Min':1, 'Max':1024}, 'Example':'30', 'Help':'Sets the width of the object to 30.'},
				'Height':{'Type':{'Type':'Integer', 'Min':1, 'Max':1024}, 'Example':'209', 'Help':'Sets the height of the object to 200.'},
				'Width.Checkbox':{'Type':{'Type':'Integer', 'Min':1, 'Max':1024}, 'Example':'20', 'Help':'Sets the width of the checkbox to 20.'},
				'Height.Checkbox':{'Type':{'Type':'Integer', 'Min':1, 'Max':1024}, 'Example':'20', 'Help':'Sets the height of the checkbox to 20.'},
				'Background':{'Type':{'Type':'String', 'LengthMax':32}, 'Example':'Blue', 'Help':'Sets the background of the object.'},
				'Background.Checkbox':{'Type':{'Type':'String', 'LengthMax':32}, 'Example':'Blue', 'Help':'Sets the background of the checkbox.'},
				'Disabled':{'Type':{'Type':'Boolean'}, 'Example':'true', 'Help':'Controls if the input field is disabled or not.'},
			},
		},
		'GUI:Label.Add':{
			'Version':2,
			'Title':'Creates a label',
			'Description':'',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Mandatory':'*', 'Default':'LabelID', 'Example':'Temp', 'Help':'The input "Temp" identifies the label.'},
				'FrameID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Example':'Frame1', 'Help':'Specifies into which frame the object should be placed if not the main one.'},
				'WindowID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Example':'Window1', 'Help':'Specifies into which window the object should be placed if not the main one.'},
				'Text':{'Type':{'Type':'String', 'LengthMax':64000}, 'Example':'50', 'Help':'The input "50" displays the text as the label.'},
				'Width':{'Type':{'Type':'Integer', 'Min':1, 'Max':1024}, 'Example':'80', 'Help':'Sets the width of the object to 80.'},
				'Background':{'Type':{'Type':'String', 'LengthMax':32}, 'Example':'Blue', 'Help':'Sets the background of the object.'},
				'Placement.Row':{'Type':{'Type':'Integer'}, 'Mandatory':'*', 'Example':'1', 'Help':'The input "1" would place the object on the first row in the layout grid.'},
				'Placement.Column':{'Type':{'Type':'Integer'}, 'Mandatory':'*', 'Example':'1', 'Help':'The input "1" would place the object on the first column in the layout grid.'},
				'Placement.Colspan':{'Type':{'Type':'Integer'}, 'Example':'2', 'Help':'Control how many columns this object would occupy.'},
				'Placement.Rowspan':{'Type':{'Type':'Integer'}, 'Example':'2', 'Help':'Control how many rows this object would occupy.'},
				'Placement.Alignment':{'Type':{'Type':'Enum', 'Values':['E', 'N', 'S', 'W', 'NW', 'NE', 'SE', 'SW']}, 'Example':'SE', 'Help':'Controls the alignment of the object.\nE = East, N = North, W = West & S = South.\nCan be combined to SE, NW, NE, SW.'},
			},
		},
		'GUI:Label.Change':{
			'Version':1,
			'Title':'Changes a label',
			'Description':'',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Mandatory':'ID', 'Default':'LabelID', 'Example':'Temp', 'Help':'The input "Temp" identifies the label.'},
				'IDs':{'Type':{'Type':'List'}, 'Mandatory':'ID', 'Default':['ID1', 'ID2'], 'Example':['Temp1', 'Temp2'], 'Help':'The input "Temp1", "Temp2" changes a GUI input label with the ID of "Temp1" and "Temp2".'},
				'Text':{'Type':{'Type':'String', 'LengthMax':64000}, 'Example':'50', 'Help':'The input "50" displays the text as the label.'},
				'Width':{'Type':{'Type':'Integer', 'Min':1, 'Max':1024}, 'Example':'80', 'Help':'Sets the width of the object to 80.'},
				'Background':{'Type':{'Type':'String', 'LengthMax':32}, 'Example':'Blue', 'Help':'Sets the background of the object.'},
			},
		},
		'GUI:ComboBox.Add':{
			'Version':2,
			'Title':'Creates a GUI combobox',
			'Description':'',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Mandatory':'*', 'Default':'ComboBoxID', 'Example':'Temp', 'Help':'The input "Temp" identifies the ComboBox.'},
				'FrameID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Example':'Frame1', 'Help':'Specifies into which frame the object should be placed if not the main one.'},
				'WindowID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Example':'Window1', 'Help':'Specifies into which window the object should be placed if not the main one.'},
				'Values':{'Type':{'Type':'List'}, 'Mandatory':'*', 'Example':['ID #1', 'ID #2'], 'Help':'The input "1" would place the object on the first row in the layout grid.'},
				'OnChange':{'Type':{'Type':'List'}, 'Steps':True},
				'Placement.Row':{'Type':{'Type':'Integer'}, 'Mandatory':'*', 'Example':'1', 'Help':'The input "1" would place the object on the first row in the layout grid.'},
				'Placement.Column':{'Type':{'Type':'Integer'}, 'Mandatory':'*', 'Example':'1', 'Help':'The input "1" would place the object on the first column in the layout grid.'},
				'Placement.Colspan':{'Type':{'Type':'Integer'}, 'Example':'2', 'Help':'Control how many columns this object would occupy.'},
				'Placement.Rowspan':{'Type':{'Type':'Integer'}, 'Example':'2', 'Help':'Control how many rows this object would occupy.'},
				'Placement.Alignment':{'Type':{'Type':'Enum', 'Values':['E', 'N', 'S', 'W', 'NW', 'NE', 'SE', 'SW']}, 'Example':'SE', 'Help':'Controls the alignment of the object.\nE = East, N = North, W = West & S = South.\nCan be combined to SE, NW, NE, SW.'},
			},
		},
		'GUI:DatePicker.Add':{
			'Version':2,
			'Title':'Creates a GUI date picker with calendar',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Mandatory':'*', 'Default':'DatePickerID', 'Example':'Temp', 'Help':'The input "Temp" creates a GUI input entry with the ID of "Temp".\nThis is later used to identify the entry object.'},
				'FrameID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Example':'Frame1', 'Help':'Specifies into which frame the object should be placed if not the main one.'},
				'WindowID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Example':'Window1', 'Help':'Specifies into which window the object should be placed if not the main one.'},
				'Value':{'Type':{'Type':'Date'}, 'Example':'2024-01-01', 'Help':'The input "2024-01-01" displays the text as the pre filled value of the date field.'},
				'Value.Placeholder':{'Type':{'Type':'String', 'LengthMax':10}, 'Example':'YYYY-MM-DD', 'Help':'The placeholder text for the date field.'},
				'Width':{'Type':{'Type':'Integer', 'Min':1, 'Max':1024}, 'Example':'80', 'Help':'Sets the width of the object to 80.'},
				'Background':{'Type':{'Type':'String', 'LengthMax':32}, 'Example':'Blue', 'Help':'Sets the background of the object.'},
				'OnChange':{'Type':{'Type':'List'}, 'Steps':True},
				'Placement.Row':{'Type':{'Type':'Integer'}, 'Mandatory':'*', 'Example':'1', 'Help':'The input "1" would place the object on the first row in the layout grid.'},
				'Placement.Column':{'Type':{'Type':'Integer'}, 'Mandatory':'*', 'Example':'1', 'Help':'The input "1" would place the object on the first column in the layout grid.'},
				'Placement.Colspan':{'Type':{'Type':'Integer'}, 'Example':'2', 'Help':'Control how many columns this object would occupy.'},
				'Placement.Rowspan':{'Type':{'Type':'Integer'}, 'Example':'2', 'Help':'Control how many rows this object would occupy.'},
				'Placement.Alignment':{'Type':{'Type':'Enum', 'Values':['E', 'N', 'S', 'W', 'NW', 'NE', 'SE', 'SW']}, 'Example':'SE', 'Help':'Controls the alignment of the object.\nE = East, N = North, W = West & S = South.\nCan be combined to SE, NW, NE, SW.'},
			},
		},
		'GUI:DatePicker.Change':{
			'Version':2,
			'Title':'Changes a GUI date picker',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Mandatory':'*', 'Default':'DatePickerID', 'Example':'Temp', 'Help':'The input "Temp" creates a GUI input entry with the ID of "Temp".\nThis is later used to identify the entry object.'},
				'Value':{'Type':{'Type':'Date'}, 'Example':'2024-01-01', 'Help':'Changes the date of the DatePicker.'},
				'Width':{'Type':{'Type':'Integer', 'Min':1, 'Max':1024}, 'Example':'80', 'Help':'Sets the width of the object to 80.'},
				'Background':{'Type':{'Type':'String', 'LengthMax':32}, 'Example':'Blue', 'Help':'Sets the background of the object.'},
				'OnChange.Trigger':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'Controls if the OnChange logic should be triggered for a Value change.'},
			},
		},
		'GUI:Frame.Add':{
			'Version':2,
			'Title':'Adds a GUI frame',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Mandatory':'*', 'Example':'Frame1', 'Help':'The input "Frame1" creates a GUI frame with the ID of "Frame1".\nThis is later used to identify the frame object amd for other functions to use with the input FrameID.'},
				'FrameID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Example':'Frame1', 'Help':'Specifies into which frame the object should be placed if not the main one.'},
				'WindowID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Example':'Window1', 'Help':'Specifies into which window the object should be placed if not the main one.'},
				'Width':{'Type':{'Type':'Integer', 'Min':1, 'Max':1024}, 'Example':80, 'Help':'Sets the width of the object to 80.'},
				'Height':{'Type':{'Type':'Integer', 'Min':1, 'Max':1024}, 'Example':80, 'Help':'Sets the height of the object to 80.'},
				'Background':{'Type':{'Type':'String', 'LengthMax':32}, 'Example':'Blue', 'Help':'Sets the background of the object.'},
				'Placement.Row':{'Type':{'Type':'Integer'}, 'Mandatory':'*', 'Example':'1', 'Help':'The input "1" would place the object on the first row in the layout grid.'},
				'Placement.Column':{'Type':{'Type':'Integer'}, 'Mandatory':'*', 'Example':'1', 'Help':'The input "1" would place the object on the first column in the layout grid.'},
				'Placement.Colspan':{'Type':{'Type':'Integer'}, 'Example':'2', 'Help':'Control how many columns this object would occupy.'},
				'Placement.Rowspan':{'Type':{'Type':'Integer'}, 'Example':'2', 'Help':'Control how many rows this object would occupy.'},
				'Placement.Alignment':{'Type':{'Type':'Enum', 'Values':['E', 'N', 'S', 'W', 'NW', 'NE', 'SE', 'SW']}, 'Example':'SE', 'Help':'Controls the alignment of the object.\nE = East, N = North, W = West & S = South.\nCan be combined to SE, NW, NE, SW.'},
			},
		},
		'GUI:Frame.Change':{
			'Version':1,
			'Title':'Changes a GUI frame',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Mandatory':'*', 'Example':'Frame1', 'Help':'The input "Frame1" modifies the GUI frame with the ID of "Frame1".'},
				'Background':{'Type':{'Type':'String', 'LengthMax':32}, 'Example':'Blue', 'Help':'Sets the background of the object.'},
			},
		},
		'GUI:Treeview.Add':{
			'Version':2,
			'Title':'Adds a GUI treeview table',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Mandatory':'*', 'Example':'TV1', 'Help':'The input "TV1" creates a GUI treeview with the ID of "TV1".'},
				'FrameID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Example':'Frame1', 'Help':'Specifies into which frame the object should be placed if not the main one.'},
				'WindowID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Example':'Window1', 'Help':'Specifies into which window the object should be placed if not the main one.'},
				'Columns':{'Type':{'Type':'List'}, 'Example':[{"Title":"Name", "Width":100, "Width.Min":50, "Anchor":"w"}, {"Title":"Status", "Width":50, "Width.Min":50, "Anchor":"e"}], 'Help':"""A list of the columns in the treeview, each column is a dict with the following fields:
* Title - The title of the column
* Alignment - How the header is anchored, valid values are n, ne, e, se, s, sw, w, nw, or center
* Width - The default width of the column
* Width.Min - The minimum width a column can be compressed to"""},
				'Tree':{'Type':{'Type':'List'}, 'Example':[{"Action":"Add.1D", "Key1D":"ORDIM_C-E012", "Open":True}, {"Action":"Add.2D", "Key1D":"ORDIM_C-E012", "Key2D":"DL", "Values":["OK", "Downloaded successfully"]}, {"Action":"Change.1D", "Key1D":"ORDIM_C-E022", "Values":["OK", "*"]}], 'Help':"""A list of dicts with the tree config to be executed:
* Action:
	- Add.1D - Adds a new 1st level
	- Change.1D - Changes an existing 1st level
	- Add.2D - Adds a new 2nd level
	- Change.2D - Changes an existing 2nd level
* Key1D - The key to identify the 1st tree level and what's displayed in the tree view
* Key2D - 2D only, The key to identify the 2nd tree level and what's displayed in the tree view
* Open - 1D only, changes if the tree is open or not
* Values - A list of the column values besides the key"""},
				'Height':{'Type':{'Type':'Integer', 'Min':1, 'Max':128}, 'Example':10, 'Help':'Sets the height to this amount of rows.'},
				'Placement.Row':{'Type':{'Type':'Integer'}, 'Mandatory':'*', 'Example':'1', 'Help':'The input "1" would place the object on the first row in the layout grid.'},
				'Placement.Column':{'Type':{'Type':'Integer'}, 'Mandatory':'*', 'Example':'1', 'Help':'The input "1" would place the object on the first column in the layout grid.'},
				'Placement.Colspan':{'Type':{'Type':'Integer'}, 'Example':'2', 'Help':'Control how many columns this object would occupy.'},
				'Placement.Rowspan':{'Type':{'Type':'Integer'}, 'Example':'2', 'Help':'Control how many rows this object would occupy.'},
				'Placement.Alignment':{'Type':{'Type':'Enum', 'Values':['E', 'N', 'S', 'W', 'NW', 'NE', 'SE', 'SW']}, 'Example':'SE', 'Help':'Controls the alignment of the object.\nE = East, N = North, W = West & S = South.\nCan be combined to SE, NW, NE, SW.'},
			},
		},
		'GUI:Treeview.Change':{
			'Version':1,
			'Title':'Change a GUI treeview table',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Mandatory':'*', 'Example':'TV1', 'Help':'The input "TV1" creates a GUI treeview with the ID of "TV1".'},
				'Tree':{'Type':{'Type':'List'}, 'Example':[{"Action":"Add.2D", "Key1D":"ORDIM_C-E022", "Key2D":"UL", "Values":["NOK", "Upload failed"]}, {"Action":"Change.1D", "Key1D":"ORDIM_C-E022", "Values":["NOK", "*"]}], 'Help':"""A list of dicts with the tree config to be executed:
* Action:
	- Add.1D - Adds a new 1st level
	- Change.1D - Changes an existing 1st level
	- Add.2D - Adds a new 2nd level
	- Change.2D - Changes an existing 2nd level
* Key1D - The key to identify the 1st tree level and what's displayed in the tree view
* Key2D - 2D only, The key to identify the 2nd tree level and what's displayed in the tree view
* Open - 1D only, changes if the tree is open or not
* Values - A list of the column values besides the key

"""},
			},
		},
		'GUI:Table.Add':{
			'Version':1,
			'Title':'Adds a GUI table',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Mandatory':'*', 'Example':'Table1', 'Help':'The input "Table1" creates a GUI table with the ID of "Table1".'},
				'Table.Data':{'Type':{'Type':'List'}, 'Mandatory':'*', 'Example':[['ID', 'Name'], [1, 'John'], [2, 'Anna']], 'Help':'A 2D list of values for the table.'},
				'Table.Width':{'Type':{'Type':'Integer'}, 'Example':400, 'Help':'Sets the width of the table.'},
				'Table.Height':{'Type':{'Type':'Integer'}, 'Example':200, 'Help':'Sets the height of the table.'},
				'Table.Opts':{'Type':{'Type':'Dict'}, 'Example':{"header_bg": "blue"}, 'Help':"""A dict of options to change how the table looks:
* top_left_bg - Sets the background of the top left box.
* top_left_fg - Sets the font color of the top left box.
* header_bg - Sets the background of the headers.
* header_fg - Sets the font color of the headers.
* index_bg - Sets the background of the index rows.
* index_fg - Sets the font color of the index rows.
* table_bg - Sets the background of the data table.
* table_fg - Sets the font color of the data table."""},
				'Placement.Row':{'Type':{'Type':'Integer'}, 'Mandatory':'*', 'Example':'1', 'Help':'The input "1" would place the object on the first row in the layout grid.'},
				'Placement.Column':{'Type':{'Type':'Integer'}, 'Mandatory':'*', 'Example':'1', 'Help':'The input "1" would place the object on the first column in the layout grid.'},
				'Placement.Colspan':{'Type':{'Type':'Integer'}, 'Example':'2', 'Help':'Control how many columns this object would occupy.'},
				'Placement.Rowspan':{'Type':{'Type':'Integer'}, 'Example':'2', 'Help':'Control how many rows this object would occupy.'},
				'Placement.Alignment':{'Type':{'Type':'Enum', 'Values':['E', 'N', 'S', 'W', 'NW', 'NE', 'SE', 'SW']}, 'Example':'SE', 'Help':'Controls the alignment of the object.\nE = East, N = North, W = West & S = South.\nCan be combined to SE, NW, NE, SW.'},
			},
		},
		'GUI:Table.Change':{
			'Version':1,
			'Title':'Change a GUI table',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Mandatory':'*', 'Example':'Table1', 'Help':'ID of the table to change.'},
				'Table.Data':{'Type':{'Type':'List'}, 'Mandatory':'*', 'Example':[['ID', 'Name'], [1, 'John'], [2, 'Anna']], 'Help':'A 2D list of values for the table.'},
				'Table.Width':{'Type':{'Type':'Integer'}, 'Example':400, 'Help':'Sets the width of the table.'},
				'Table.Height':{'Type':{'Type':'Integer'}, 'Example':200, 'Help':'Sets the height of the table.'},
				'Table.Opts':{'Type':{'Type':'Dict'}, 'Example':{"header_bg":"blue"}, 'Help':"""A dict of options to change how the table looks:
* top_left_bg - Sets the background of the top left box.
* top_left_fg - Sets the font color of the top left box.
* header_bg - Sets the background of the headers.
* header_fg - Sets the font color of the headers.
* index_bg - Sets the background of the index rows.
* index_fg - Sets the font color of the index rows.
* table_bg - Sets the background of the data table.
* table_fg - Sets the font color of the data table."""},
				'Debug.Table.Set_Options':{'Debug':True, 'Type':{'Type':'Dict'}, 'Example':{"header_bg":"blue"}, 'Help':"A dict of options to change how the table looks, no limitations"},
			},
		},
		'GUI:WindowForm.Add':{
			'Version':1,
			'Title':'Adds a GUI new window form',
			'Input':{
				'ID':{},
				'Title':{},
				'Geometry':{'Example':'300x200'},
				'StartPos.Width':{'Type':{'Type':'String', 'LengthMin':2, 'LengthMax':6}, 'Example':'+200', 'Help':'Specifies where the new window should popup in relation to the current one.'},
				'StartPos.Height':{'Type':{'Type':'String', 'LengthMin':2, 'LengthMax':6}, 'Example':'-200', 'Help':'Specifies where the new window should popup in relation to the current one.'},
				'Resizable.Width':{},
				'Resizable.Height':{},
			},
		},
		'GUI:WindowForm.Change':{
			'Version':1,
			'Title':'Change a GUI window form',
			'Input':{
				'ID':{},
				'Focus':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'If True, calls focus to this window.'},
				'Destroy':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'If True, destroys this object.'},
			},
		},
		'GUI:ProgressBar.Add':{
			'Version':3,
			'Title':'Adds a GUI progress bar',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Mandatory':'*', 'Example':'PB1', 'Help':'ID of the progress bar to add.'},
				'Width':{'Type':{'Type':'Integer'}, 'Example':400, 'Help':'Sets the width of the progress bar.'},
				'Height':{'Type':{'Type':'Integer'}, 'Example':15, 'Help':'Sets the height of the progress bar.'},
				'Vertical':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'If True, draws the progress bar vertically.'},
				'Progress':{'Type':{'Type':'Integer', 'Min':0, 'Max':100}, 'Example':75, 'Help':'Sets the progression of the progress bar (0 - 100).'},
				'ProgressScale':{'Type':{'Type':'Integer', 'Min':0, 'Max':999999999}, 'Example':1024, 'Help':'Sets the progress scale, if set to 1000 and progress to 100, progress gets converted to 10.'},
				'ProgressColor':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':32}, 'Example':'Blue', 'Help':'Sets the color of the progress bar.'},
				'ProgressColor.Range':{'Type':{'Type':'List'}, 'Example':['Yellow', 'Blue', 'Red'], 'Help':'A list of colors which are then selected based on the current progression (max 100 entries).'},
				'ProgressColor.RangePreset':{'Type':{'Type':'Enum', 'Values':['']}, 'Example':'Sunset', 'Help':"""A list of preset color ranges:
* Traffic Flow - Red -> Green.
* Status Spectrum - Red -> Yellow -> Green.
* Twilight Drift - Blue -> Purple.
* Sunset - Orange -> Pink -> Purple.
* Ocean - Teal -> Blue -> Navy.
* Cool Ice - White -> Light blue -> Cyan.
* Rainbow - Red -> Orange -> Yellow -> Green -> Blue -> Indigo -> Violet."""},
				'Placement.Row':{'Type':{'Type':'Integer'}, 'Mandatory':'*', 'Example':'1', 'Help':'The input "1" would place the object on the first row in the layout grid.'},
				'Placement.Column':{'Type':{'Type':'Integer'}, 'Mandatory':'*', 'Example':'1', 'Help':'The input "1" would place the object on the first column in the layout grid.'},
				'Placement.Colspan':{'Type':{'Type':'Integer'}, 'Example':'2', 'Help':'Control how many columns this object would occupy.'},
				'Placement.Rowspan':{'Type':{'Type':'Integer'}, 'Example':'2', 'Help':'Control how many rows this object would occupy.'},
				'Placement.Alignment':{'Type':{'Type':'Enum', 'Values':['E', 'N', 'S', 'W', 'NW', 'NE', 'SE', 'SW']}, 'Example':'SE', 'Help':'Controls the alignment of the object.\nE = East, N = North, W = West & S = South.\nCan be combined to SE, NW, NE, SW.'},
			},
		},
		'GUI:ProgressBar.Change':{
			'Version':3,
			'Title':'Change a GUI progress bar',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Mandatory':'*', 'Example':'PB1', 'Help':'ID of the progress bar to change.'},
				'Progress':{'Type':{'Type':'Integer', 'Min':0, 'Max':100}, 'Example':75, 'Help':'Sets the progression of the progress bar (0 - 100).'},
				'ProgressScale':{'Type':{'Type':'Integer', 'Min':0, 'Max':999999999}, 'Example':1024, 'Help':'Sets the progress scale, if set to 1000 and progress to 100, progress gets converted to 10.'},
				'ProgressColor':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':32}, 'Example':'Blue', 'Help':'Sets the color of the progress bar.'},
				'ProgressColor.Range':{'Type':{'Type':'List'}, 'Example':['Yellow', 'Blue', 'Red'], 'Help':'A list of colors which are then selected based on the current progression (max 100 entries).'},
				'ProgressColor.RangePreset':{'Type':{'Type':'Enum', 'Values':['']}, 'Example':'Sunset', 'Help':"""A list of preset color ranges:
* Traffic Flow - Red -> Green.
* Status Spectrum - Red -> Yellow -> Green.
* Twilight Drift - Blue -> Purple.
* Sunset - Orange -> Pink -> Purple.
* Ocean - Teal -> Blue -> Navy.
* Cool Ice - White -> Light blue -> Cyan.
* Rainbow - Red -> Orange -> Yellow -> Green -> Blue -> Indigo -> Violet."""},
			},
		},
		'GUI:Objects.Count':{
			'Version':2,
			'Title':'Count the number of GUI objects based on filters',
			'Input':{
				'Filter.Type':{},
				'Filter.ID':{},
				'Filter.Background':{},
				'Filter.Width':{},
				'Filter.Height':{},
				'Filter.Border.Color':{},
				'Filter.Readonly':{},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}},
				'UpdateGUI.Value':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'Entry##TEMP', 'Help':'Updates the GUI Entry instance TEMP with the input value.'},
				'UpdateGUI.Value.Trigger':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'If True, triggers the GUI change steps if available.'},
			},
		},
		'GUI:InputDialog.Action':{
			'Version':3,
			'Title':'Triggers a input dialog popup',
			'Input':{
				'Title':{'Type':{'Type':'String', 'LengthMin':0, 'LengthMax':512}, 'Example':'Confirmation window', 'Help':'Sets the title of the input popup.'},
				'Text':{'Type':{'Type':'String', 'LengthMin':0, 'LengthMax':512}, 'Example':'Confirm by typing OK.', 'Help':'Sets the text of the input popup.'},
				'OnCancel':{'Type':{'Type':'List'}, 'Steps':True, 'Help':'Executes these steps if the Cancel or close button is used.'},
				'OnOK':{'Type':{'Type':'List'}, 'Steps':True, 'Help':'Executes these steps if the OK button or enter is used.'},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}},
				'UpdateGUI.Value':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'Entry##TEMP', 'Help':'Updates the GUI Entry instance TEMP with the input value.'},
				'UpdateGUI.Value.Trigger':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'If True, triggers the GUI change steps if available.'},
			},
		},
		'GUI:FileDialog.Action':{
			'Version':3,
			'Title':'Popup to select file(s)',
			'Input':{
				'Title':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':512}, 'Example':'Input file', 'Help':'Title of the file input dialog.'},
				'Directory':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':512}, 'Example':'C:\\Temp\\', 'Help':'A prefilled path for the dialog.'},
				'Directory.Downloads':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'If True and Directory is not used, this will try to use the users download folder.'},
				'File':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':256}, 'Example':'Data.DAT', 'Help':'A prefilled file for the dialog.'},
				'FileTypes':{'Type':{'Type':'List'}, 'Example':[["Texts","*.txt"], ["Images", "*.jpg;*.jpeg;*.png"]], 'Help':'A list of lists of file ext\'s which are allowed to be selected.\nMultiple ext\'s can be used by separating them with ";".'},
				'Multiple':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'Controls if the input should accept multiple files or not, if used, the return will be a list of files.'},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}},
				'UpdateGUI.Value':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'Entry##TEMP', 'Help':'Updates the GUI Entry instance TEMP with the input value.'},
				'UpdateGUI.Value.Trigger':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'If True, triggers the GUI change steps if available.'},
			},
		},
		'GUI:Values.Export':{
			'Version':2,
			'Title':'Exports all values from the GUI objects',
			'Description':'Exports a list of dicts with the Type, ID and Value keys for all available objects in the GUI system.',
			'Input':{
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}},
			},
		},
		'GUI:Values.Import':{
			'Version':2,
			'Title':'Imports values to GUI objects',
			'Input':{
				'Data':{'Type':{'Type':'List'}, 'Help':"""A list of dicts with the data for the object to update:
* Type - The object type (Entry, DataPicker and so on).
* ID - The object ID to be updated.
* Value - The value to update the object with"""},
				'Trigger':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'Controls if the OnChange logic should be triggered for the Value changes.'},
			},
		},
		'GUI:Defaults':{
			'Version':2,
			'Title':'Used to set defaults for GUI objects',
			'Input':{
				'Type':{'Type':{'Type':'Enum', 'Values':['Window', 'Position']}, 'Help':"""The type of default value to change:
* Window - Set the main window for GUI objects.
* Position - Sets a default position variable (these values can then be used for "Placement.Row" or "Placement.Column" as "%Segment1%+1" or "%Segment1%=%Segment1%+1")."""},
				'Window.Type':{'Type':{'Type':'Enum', 'Values':['Form', 'FrameID', 'WindowID']}, 'Help':"""The type of default value to change:
* Form - The main form window.
* FrameID - Used in conbination with Window.ID to set the default FrameID.
* WindowID - Used in conbination with Window.ID to set the default WindowID."""},
				'Window.ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Example':'Frame1', 'Help':'Used with Form.Type to specify the Frame or Window.'},
				'Position.ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Example':'Segment1', 'Help':'The ID for the new position variable.'},
				'Position.Value':{'Type':{'Type':'Integer', 'Min':0, 'Max':1024}, 'Example':10, 'Help':'Sets the value for the Position.ID.'},
				'Positions.Dict':{'Type':{'Type':'Dict'}, 'Example':{'Segment1':1, 'Segment2':2}, 'Help':'A dict is used to set multiple positions at once, the key is the ID.'},
			}
		},
		'SQL:Table.Create':{
			'Version':2,
			'Title':'Creates a SQL table',
			'Description':'',
			'Input':{
				'SQLite.File':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':512}, 'Example':'O:\\\\Data\\\\Test.csv', 'Help':'Specifies the windows path to the SQLite database file.'},
				'Table':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':512}, 'Mandatory':'*', 'Example':'Table1', 'Help':'The table name to be created'},
				'Columns':{'Type':{'Type':'Dict'}, 'Example':{'ID':'INTEGER', 'Name':'TEXT'}, 'Help':'A dict with the table columns and their type.'},
				'Create.IfNotExists':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'If True, table creation will be skipped if it already exists.'},
			},
		},
		'SQL:Table.Drop':{
			'Version':2,
			'Title':'Drops a SQL table',
			'Description':'',
			'Input':{
				'SQLite.File':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':512}, 'Example':'O:\\\\Data\\\\Test.csv', 'Help':'Specifies the windows path to the SQLite database file.'},
				'Table':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':512}, 'Mandatory':'*', 'Example':'Table1', 'Help':'The table name to be dropped'},
				'Drop.IfExists':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'If True, no error will be generated if the table doesn\'t exist.'},
			},
		},
		'SQL:Table.DataColumnDetermination':{
			'Version':2,
			'Title':'Determins the column types based on the input data',
			'Description':'',
			'Input':{
				'Data':{},
#				'DataVariable':{},
				'Columns':{},
#				'ColumnsVariable':{},
				'ColumnPrimary':{},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'TEMP_VALUE', 'Help':'Stores the result into the variable name provided.'},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'TEMP_VALUE', 'Help':'Stores the result into the variable name provided.'},
			},
		},
		'SQL:Table.Insert':{
			'Version':3,
			'Title':'Inserts data into a table',
			'Description':'',
			'Input':{
				'SQLite.File':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':512}, 'Example':'O:\\\\Data\\\\Test.csv', 'Help':'Specifies the windows path to the SQLite database file.'},
				'Table':{'Mandatory':'*'},
				'Columns':{'Mandatory':'*'},
				'Values':{},
#				'ValuesVariable':{},
				'RemoveVariable':{'Type':{'Type':'Boolean'}, 'Help':'Deletes the variables after the table inserts has been executed.'},
				'Function.OnError':{'Steps':True},
				'Function.ErrorVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'ERROR_TEMP_VALUE', 'Help':'If there is an error executing the command, stores the error into this variable.'},
				'Function.ErrorVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'ERROR_TEMP_VALUE', 'Help':'If there is an error executing the command, stores the error into this global variable.'},
			},
		},
		'SQL:Query.Select':{
			'Version':3,
			'Title':'Select data',
			'Description':'',
			'Input':{
				'SQLite.File':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':512}, 'Example':'O:\\\\Data\\\\Test.csv', 'Help':'Specifies the windows path to the SQLite database file.'},
				'Query':{'Type':{'Type':'String', 'LengthMin':6, 'LengthMax':64000}, 'Mandatory':'*', 'Example':'SELECT COUNT(*) FROM `Temp`', 'Help':'Executes the provided query.'},
				'ReturnType':{'Type':{'Type':'Enum', 'Values':['String', 'Integer', 'Decimal', 'List', 'ListDict']}, 'Mandatory':'*', 'Example':'String', 'Help':"""Decides what kind of value that\'s returned. Valid values are:
String - Converts the result into a string
Integer - Converts the result into an integer
Decimal - Converts the result into a float
List - Returns the result as a 2D list
ListDict - Returns the result as a list of dicts (headers as dict keys)"""},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'TEMP_VALUE', 'Help':'Stores the result into the variable name provided.'},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'TEMP_VALUE', 'Help':'Stores the result into the variable name provided.'},
				'UpdateGUI.Value':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'Entry##TEMP', 'Help':'Updates the GUI Entry instance TEMP with the input value.'},
				'UpdateGUI.Value.Trigger':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'Controls if the OnChange logic should be triggered for the Value changes.'},
			},
		},
		'SQL:Query.Select.Mass':{
			'Version':2,
			'Title':'Run multiple select queries',
			'Description':'',
			'Input':{
				'SQLite.File':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':512}, 'Example':'O:\\\\Data\\\\Test.csv', 'Help':'Specifies the windows path to the SQLite database file.'},
				'Queries':{'Type':{'Type':'List'}, 'Mandatory':'*', 'Example':[
					{'ReturnVariable':'Rows', 'ReturnVariable.Global':'RowsGlobal', 'ReturnType':'Integer', 'Query':'SELECT COUNT(*) FROM `Temp`'},
					{'ReturnVariable':'Sum', 'ReturnType':'Decimal', 'Query':'SELECT SUM(Value) FROM `Temp`'},
				], 'Help':"""A list of dicts which are executed and stored based on each entry\'s config:
* Query - Database query to be executed.
* ReturnType - Based on the following options:
	String - Converts the result into a string
	Integer - Converts the result into an integer
	Decimal - Converts the result into a float
	List - Returns the result as a 2D list
	ListDict - Returns the result as a list of dicts (headers as dict keys)
* ReturnVariable - Specifies the variable to store the result in.
* ReturnVariable.Global - Specifies the global variable to store the result in.
* UpdateGUI.Value - Specifies the GUI element to store the result in.
* UpdateGUI.Value.Trigger - True will trigger OnChange steps if available."""},
			},
		},
		'SQL:Query.Select.Easy':{
			'Version':2,
			'Title':'Execute pre defined queries',
			'Description':'',
			'Input':{
				'SQLite.File':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':512}, 'Example':'O:\\\\Data\\\\Test.csv', 'Help':'Specifies the windows path to the SQLite database file.'},
				'DB':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':256}, 'Default':'<MEMORY>', 'Example':'TempDB', 'Help':'Used to select which database to use for the functions which supports it.'},
				'Table':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':256}, 'Example':'TempTable', 'Help':'Used to select which table to use for the functions which supports it.'},
				'DB.Tables':{'Type':{'Type':'Boolean'}, 'Example':'true', 'Help':'Returns a list of all the tables in the database.'},
				'DB.Table.Columns':{'Type':{'Type':'Boolean'}, 'MandatoryInput':['Table'], 'Example':'true', 'Help':'Returns dict with the column name and the type as the value for all the columns for the specified table in the database.'},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'TEMP_VALUE', 'Help':'Stores the result into the variable name provided.'},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'TEMP_VALUE', 'Help':'Stores the result into the global variable name provided.'},
			},
		},
		'DATA:Verify':{
			'Version':2,
			'Title':'Verify if the input value matches the provided check rules',
			'Input':{
				'Value':{'Type':{'Type':'Any'}, 'Mandatory':'SINGLE'},
				'Convert':{'Type':{'Type':'List'}, 'Example':[{'Type':'String', 'Trim':True}], 'Convert':True, 'Help':'A list with dict conversion rules.'},
				'Verify':{'Mandatory':'SINGLE', 'Verify':True},
				'OnTrue':{'Type':{'Type':'List'}, 'Steps':True},
				'OnFalse':{'Type':{'Type':'List'}, 'Steps':True},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'TEMP_VALUE', 'Help':'Stores the result into the variable name provided.'},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'TEMP_VALUE', 'Help':'Stores the result into the global variable name provided.'},
			},
		},
		'DATA:Convert':{
			'Version':4,
			'Title':'Convert data',
			'Input':{
				'Value':{'Type':{'Type':'Any'}, 'Mandatory':'SINGLE'},
				'Convert':{'Type':{'Type':'List'}, 'Mandatory':'SINGLE', 'Convert':True, 'Example':['TRIM', 'INTEGER'], 'Help':'A list of the conversion rules to be used.'},
				'Value.List2D':{'Type':{'Type':'List'}, 'Mandatory':'LIST2D'},
				'Convert.List2D':{'Type':{'Type':'List'}, 'Mandatory':'LIST2D', 'Convert':True},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}},
				'UpdateGUI.Value':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'Entry##TEMP', 'Help':'Updates the GUI Entry instance TEMP with the input value.'},
				'UpdateGUI.Value.Trigger':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'Controls if the OnChange logic should be triggered for the Value changes.'},
				'DebugLog':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':'false', 'Help':'If True, prints debug to console for the processed data (one entry per line).'},
				'DebugLog.Detailed':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':'false', 'Help':'If True, prints what a debug log for the processed data (one entry per field and convert rule).'},
			},
		},
		'DATA:Replace':{
			'Version':4,
			'Title':'Replace part of a string',
			'Input':{
				'Value':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}},
				'Replace.Dict':{'Type':{'Type':'Dict'}, 'Example':'{",":"."}', 'Help':'Replaces all the key values it finds with the matching value from the dict.'},
				'Replace.Dict.Regex':{'Type':{'Type':'Dict'}, 'Example':'{"[a-zA-Z]":""}', 'Help':'Replaces all the regex key values it finds with the matching value from the dict.'},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}},
				'UpdateGUI.Value':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'Entry##TEMP', 'Help':'Updates the GUI Entry instance TEMP with the input value.'},
				'UpdateGUI.Value.Trigger':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'Controls if the OnChange logic should be triggered for the Value changes.'},
			},
		},
		'DATA:Transform':{
			'Version':7,
			'Title':'Used to transform data into something new based on fixed logics',
			'Input':{
				'Value':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*'},
				'Logic':{'Type':{'Type':'Enum', 'Values':['KeyList', 'Count', 'Regex.Findall', '2DList.ToDict', 'String.Modify', 'List.Modify', 'Dict.Modify', 'Dict.ModifyKey']}, 'Mandatory':'*', 'Example':'KeyList', 'Help':"""Specifies which logic that should be used for the value transformation:
* KeyList - Requires a dict or list as value and returns a list of the keys for it.
* Count - Requires a dict or list as value and returns how many entries that are in it.
* Regex.Findall - Captures all the entries matching the Regex and returns them as a list.
* 2DList.ToDict - Transforms a 2D list like [[1, 2], [3, 4]] to a dict like {1:2, 3:4}.
* ArrayToVariables - Copies values from list or dicts into ReturnVariables or UpdateGUI values based on the ArrayToVariables config.
* String.Modify - Modifies the value using Modify.Prefix, Modify.Suffix and Modify.Replace.
* List.Modify - Modifies the entries in a list using Modify.Prefix, Modify.Suffix and Modify.Replace.
* Dict.Modify - Modifies the entries in a dict using Modify.Prefix, Modify.Suffix and Modify.Replace.
* Dict.ModifyKey - Modifies the entries in a dict using Modify.Prefix, Modify.Suffix and Modify.Replace.
* ArrayDiff - Returns a dict or list with all the entries which wasn\'t matched with ArrayDiff.
* ArrayDiff.Matched - Returns a dict or list with the matched entries between Value and ArrayDiff.
* ArrayDiff.Mismatched - Returns a dict or list with the differences between two arrays."""},
				'Regex':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':1024}, 'Example':'[a-zA-Z]*', 'Help':'A regex string used by the Regex logics.'},
				'Regex.List':{'Type':{'Type':'List'}, 'Example':['[a-zA-Z]*', '[0-9]*'], 'Help':'A list of regex strings used by the Regex logics.'},
				'ArrayDiff':{'Type':{'Type':['List', 'Dict']}, 'Example':['[a-zA-Z]*', '[0-9]*'], 'Help':'A list of regex strings used by the Regex logics.'},
				'Modify.Prefix':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':1024}, 'Example':'http://', 'Help':'A prefix string which with be added to the start of each entry in the list.'},
				'Modify.Suffix':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':1024}, 'Example':'?Time=1234', 'Help':'A suffix string which with be added to the end of each entry in the list.'},
				'Modify.Replace':{'Type':{'Type':'Dict'}, 'Example':{"A":"a", "b":"B"}, 'Help':'A dict of replacements which will be executed for each entry in the list.'},
				'ArrayToVariables':{'Type':{'Type':'List'}, 'Example':[{"Keys":["Data", "ID"], "ReturnVariable":"Temp:ID"},	{"Keys":["Data", "Page"], "ReturnVariable":"Temp:Page"}], 'Help':"""A list of dicts with config for the ArrayToVariables logic:
* Keys - List of keys to walk though in a list or dict to get the value, so for instance ["Data", "ID"] would take the dict value Value['Data']['ID'].
* ReturnVariable - Return variable to store the value in.
* ReturnVariable.Global - Global return variable to store the value in.
* UpdateGUI.Value - GUI element to update.
* UpdateGUI.Value.Trigger - True will request to trigger the value change logic."""},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}},
				'UpdateGUI.Value':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'Entry##TEMP', 'Help':'Updates the GUI Entry instance TEMP with the input value.'},
				'UpdateGUI.Value.Trigger':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'Controls if the OnChange logic should be triggered for the Value changes.'},
			},
		},
		'DATA:Date':{
			'Version':3,
			'Title':'Generate a date',
			'Input':{
				'Logic':{'Type':{'Type':'Enum', 'Values':['Current', 'PreviousDay', 'PreviousWorkday', 'PreviousWorkday.MatchKey', 'NextDay', 'NextWorkday', 'NextWorkday.MatchKey']}, 'Mandatory':'*', 'Example':'Current', 'Help':"""Specifies which logic that should be used for generating a date:
* Current - Todays date.
* NextDay - Next day.
* PreviousDay - Previous day.
* NextWorkday - Next workday.
* PreviousWorkday - Previous workday.
* NextMonth - First day of the next month.
* PreviousMonth - Last day of the previous month.
* NextDay.MatchKey - Next workday where MatchKey is used.
* PreviousDay.MatchKey - Previous workday where MatchKey is used.
* NextWorkday.MatchKey - Next workday where MatchKey is used.
* PreviousWorkday.MatchKey - Previous workday where MatchKey is used.
* FirstDay.MatchKey - First day where MatchKey is used.
* LastDay.MatchKey - Last day where MatchKey is used.
* FirstWorkday.MatchKey - First workday where MatchKey is used.
* LastWorkday.MatchKey - Last workday where MatchKey is used."""},
				'Format':{'Type':{'Type':'String'}, 'Example':'%Y-%m-%d', 'Help':'The date format to return, %Y-%m-%d would return YYYY-MM-DD.'},
				'Date':{'Type':{'Type':'Date'}, 'Example':'2025-06-06', 'Help':'Specifies the start date of the calculation instead of current date.'},
				'MatchKey':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':32}, 'Example':'%G/%V/%m', 'Help':'Generates a key for the *.MatchKey logic where the date has to stay with the same MatchKey value.'},
				'BankHolidays':{'Type':{'Type':'List'}, 'Example':['2025-06-06', '2025-12-24', '2025-12-31'], 'Help':'A list of dates which are not workdays.'},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}},
				'UpdateGUI.Value':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'Entry##TEMP', 'Help':'Updates the GUI Entry instance TEMP with the input value.'},
				'UpdateGUI.Value.Trigger':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'Controls if the OnChange logic should be triggered for the Value changes.'},
			},
		},
		'DATA:Calculate':{
			'Version':4,
			'Title':'Used to calculate a string of logic',
			'Description':'',
			'Input':{
				'Calculation':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64000}, 'Example':'int(6*5)/2', 'Help':'Returns the value from the calculation. Valid input consists of the following:\n0 1 2 3 4 5 6 7 8 9 . , + - * / ( ) int float min max round math.ceil math.floor abs statistics.median ([ ])'},
				'Calculation.ToString':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'If True, converts the input Calculation to a string.'},
				'Calculation.Round':{'Type':{'Type':'Integer', 'Min':0, 'Max':12}, 'Example':2, 'Help':'Specifies how many decimals the value should be rounded to.'},
				'Calculation.Ceil':{'Type':{'Type':'Integer', 'Min':0, 'Max':12}, 'Example':2, 'Help':'Specifies how many decimals the value should be rounded up to.'},
				'Calculation.Floor':{'Type':{'Type':'Integer', 'Min':0, 'Max':12}, 'Example':2, 'Help':'Specifies how many decimals the value should be rounded down to.'},
				'Calculation.CleanOperators':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'If True, cleans up duplicate operations like ++ becomes +.'},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}},
				'UpdateGUI.Value':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'Entry##TEMP', 'Help':'Updates the GUI Entry instance TEMP with the input value.'},
				'UpdateGUI.Value.Trigger':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'Controls if the OnChange logic should be triggered for the Value changes.'},
			},
		},
		'DATA:Variable.Set':{
			'Version':5,
			'Title':'Sets a variable to a provided value or GUI clipboard',
			'Description':'',
			'Input':{
				'Value':{'Type':{'Type':'Any'}, 'Mandatory':'VALUE', 'Example':[1, 2, 3], 'Help':'The value to be stored.'},
				'GUI.Clipboard':{'Type':{'Type':'Boolean'}, 'Mandatory':'VALUE', 'Example':True, 'Help':'Takes the value from the GUI clipboard.'},
				'Convert':{'Type':{'Type':'List'}, 'Example':[{'Type':'String', 'Join':', '}], 'Convert':True, 'Help':'A list with dict conversion rules to use for the return value.'},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'VARIABLE'},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'VARIABLE'},
				'Multiple':{'Type':{'Type':'List'}, 'Example':[{'Value':'Price', 'ReturnVariable':'Sum'}, {'Value':'Price2', 'ReturnVariable':'Sum2', 'ReturnVariable.Global':'GlobalSum2'}], 'Help':"""A list of dicts with multiple entries containing the following values:
* Value
* Convert
* ReturnVariable
* ReturnVariable.Global"""},
			},
		},
		'DATA:Variable.Change':{
			'Version':2,
			'Title':'Changes as variable.',
			'Description':'',
			'Input':{
				'Value':{'Type':{'Type':'Any'}, 'Mandatory':'VALUE', 'Example':[1, 2, 3], 'Help':'The value to be used for the change.'},
				'Variable':{'Type':{'Type':'String'}, 'Example':'TempVar', 'Help':'The variable to change.'},
				'Variable.Global':{'Type':{'Type':'String'}, 'Example':'TempVar', 'Help':'The global variable to change.'},
				'Logic':{'Type':{'Type':'Enum', 'Values':['List.Append', 'Numeric.Add', 'Numeric.Remove']}, 'Mandatory':'*', 'Example':'List.Append', 'Help':"""Specifies which logic that should be used for changing the variable:
* List.Add - Adds the value to a variable list.
* Numeric.Add - Adds the value to the variable.
* Numeric.Remove - Subtracts the value from the variable."""},
				'UpdateGUI.Value':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'Entry##TEMP', 'Help':'Updates the GUI Entry instance TEMP with the new value.'},
				'UpdateGUI.Value.Trigger':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'Controls if the OnChange logic should be triggered for the value changes.'},
			},
		},
		'DATA:File.Read':{
			'Version':2,
			'Title':'Read a file',
			'Input':{
				'File':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':512}, 'Mandatory':'*'},
				'Type':{'Type':{'Type':'Enum','Values':['CSV', 'JSON', 'Binary']}, 'Mandatory':'*', 'Example':'JSON', 'Help':'Specifies which type of file it is.'},
				'ReturnVariable.Data':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'Table.Data', 'Help':'Stores the data in the "Table.Data" variable.'},
				'ReturnVariable.Headers':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'Table.Header', 'Help':'Stores the headers as a list in the "Table.Header" variable.'},
				'HeadersFromFile':{'Type':{'Type':'Boolean'}},
				'HeadersVerify':{'Type':{'Type':'Enum'}},
				'CSV.Newline':{'Type':{'Type':'String', 'LengthMin':0, 'LengthMax':12}},
				'CSV.Delimiter':{'Type':{'Type':'String', 'LengthMin':0, 'LengthMax':1}, 'Example':',', 'Help':'Specifies the field separator character.'},
				'CSV.Quotechar':{'Type':{'Type':'String', 'LengthMin':0, 'LengthMax':1}, 'Example':'"', 'Help':'Specifies the field quote character.'},
			}
		},
		'DATA:File.Create':{
			'Version':2,
			'Title':'Create a file',
			'Input':{
				'File':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':512}, 'Mandatory':'*'},
				'Type':{'Type':{'Type':'Enum','Values':['CSV', 'JSON', 'Binary']}, 'Mandatory':'*', 'Example':'CSV', 'Help':"""Specifies which file content that should be created:
* CSV - Saves the Data in a CSV format based on the CSV parameeters provided.
* JSON - Saves the Data as a JSON string."""},
				'Data':{'Type':{'Type':'Any'}, 'Mandatory':'*', 'Example':'<$Table.Data$>', 'Help':'The data to be stored in the file.'},
				'CSV.Headers':{'Type':{'Type':'List'}, 'Example':['ID', 'Name'], 'Help':'A list of the headers for the CSV data.'},
				'CSV.Delimiter':{'Type':{'Type':'String', 'LengthMin':0, 'LengthMax':1}, 'Example':',', 'Help':'Specifies the field separator character.'},
				'CSV.Quotechar':{'Type':{'Type':'String', 'LengthMin':0, 'LengthMax':1}, 'Example':'"', 'Help':'Specifies the field quote character.'},
				'CSV.QuoteRule':{'Type':{'Type':'Enum', 'Values':['All', 'Minimal', 'NonNumeric', 'None', 'Strings']}, 'Example':'Minimal', 'Help':"""Chooses the quoting rule:
* All - All fields gets quoted.
* Minimal - As few fields as possible gets quoted.
* NonNumeric - All non numeric fields gets quoted.
* None - Nothing gets quoted.
* Strings - Strings gets quoted."""},
			},
		},
		'DATA:SAP.UnconvertedTableToList':{
			'Version':3,
			'Title':'Convert a SAP unconverted list input into a list of data and headers',
			'Input':{
				'File':{'Type':{'Type':'String', 'LengthMin':5, 'LengthMax':512}, 'Example':'C:\\\\Tools\\\\SAPData.txt', 'Help':'Which file that should be read for the source data.'},
				'File.Encoding':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':32}, 'Example':'UTF-16', 'Help':'Specifies which encoding the file contains.'},
				'Data':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64000}, 'Example':'<$SAP_DATA$>', 'Help':'String or variable which will be processed.'},
				'OnlyTableNo':{'Type':{'Type':'Integer', 'Min':0, 'Max':1024}, 'Example':'0', 'Help':'If only one table should be returned, specify which one (starts from 0).\nWithout this a list of tables will be returned even if only one table exists in the data.'},
				'ReturnVariable.UnknownLines':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'SAPUC:Unknown', 'Help':'Stores unprocessed lines from the data as a list of lines to the variable name provided.'},
				'ReturnVariable.Headers':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'SAPUC:Headers', 'Help':'Stores header columns as a list to the variable name provided.\nIn OnlyTableNo is not used, it will be a 2D list of headers, one for each table.'},
				'ReturnVariable.Data':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'SAPUC:Data', 'Help':'Stores table data as a 2D list to the variable name provided.\nIn OnlyTableNo is not used, it will be a 3D list of table data, one for each table, line and column.'},
				'Debug.Log':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':'false', 'Help':'If True, prints debug to console for the processed data.'},
				'Debug.Tables.Console':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':'false', 'Help':'If True, prints the extracted tables to consone.'},
			},
		},
		'EXCEL:Open':{
			'Version':1,
			'Title':'Open an Excel file',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'Excel1', 'Help':'The ID which is used to identify the file later on.'},
				'File':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':512}, 'Mandatory':'*', 'Help':'Excel file which will be opened with the specified ID.'},
			},
		},
		'EXCEL:Close':{
			'Version':1,
			'Title':'Close an Excel file',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'Excel1', 'Help':'The ID which is used to identify the open excel file to close.'},
			},
		},
		'EXCEL:Save':{
			'Version':1,
			'Title':'Save an Excel file',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'Excel1', 'Help':'The ID which is used to identify the open excel file.'},
				'File':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':512}, 'Help':'If specified, will save the as provided filename, if not, will save as the original file.'},
				'ErrorIfOpen':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'If True, returns ERROR instead of saving if the program thinks the file is open already (experimental).'},
			},
		},
		'EXCEL:Change':{
			'Version':1,
			'Title':'Change an Excel file cell',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'Excel1', 'Help':'The ID which is used to identify the open excel file.'},
				'Sheet':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Example':'Sheet1', 'Help':'Specifies a specific sheet.'},
				'Cell':{'Type':{'Type':'String', 'LengthMin':2, 'LengthMax':9}, 'Example':'B5', 'Help':'Specifies which cell that should be changed.'},
				'Value':{'Type':{'Type':'Any'}},
				'ValueFormat':{'Type':{'Type':'Enum', 'Values':['Date']}},
				
			},
		},
		'EXCEL:Read':{
			'Version':2,
			'Title':'Read an Excel file',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'Excel1', 'Help':'The ID which is used to identify the open excel file.'},
				'Sheet':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Example':'Sheet1', 'Help':'Specifies a specific sheet.'},
				'Cell':{'Type':{'Type':'String', 'LengthMin':2, 'LengthMax':9}, 'Example':'B5', 'Help':'Specifies which cell that should be read.'},
				'Row':{'Type':{'Type':'Integer', 'Min':1, 'Max':1048576}, 'Mandatory':'SELECTION', 'Example':0, 'Help':'Returns the specified row as a list (starts at line 1).'},
				'Complete':{'Type':{'Type':'Boolean'}, 'Mandatory':'SELECTION', 'Example':True, 'Help':'If True, returns the entire sheet as a 2D list.'},
				'RespectFormatting':{},
				'ReturnVariable':{},
				'ReturnVariable.Globel':{},
			},
		},
		'PANDAS:Open':{
			'Version':2,
			'Title':'Open an Excel file with Pandas',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'DF1', 'Help':'The ID which is used to identify the open pandas file.'},
				'File':{'Type':{'Type':'String', 'LengthMin':5, 'LengthMax':512}, 'Example':'C:\\\\Tools\\\\Data.xlsx', 'Help':'Which file that should be read for the source data.'},
				'HeaderRow':{'Type':{'Type':'Integer', 'Min':0, 'Max':1024}, 'Example':0, 'Help':'Which row that should be used at the header row of the file, starts from 0. If no HeaderRow is provided, no header will be set.'},
				'Debug.Console':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'If True, displays debug steps in console.'},
			},
		},
		'PANDAS:Read':{
			'Version':2,
			'Title':'Reads a pandas file into a 2D list',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'DF1', 'Help':'The ID which is used to identify the open pandas file.'},
				'Nan2None':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'If True, converts numpy.nan values to None.'},
				'Filters':{'Type':{'Type':'List'}, 'Example':[{"Column":"Projekt", "Logic":"=", "Value":"UTL-2250001"}], 'Help':"""A list of dicts which controlls which filters should be used on the sheet for the data selection. Dict legend:
* Column - Which column the filter should be placed on
* Logic - Which logic to be used:
	* = - Equal.
	* != - Not equal.
	* < - Less than.
	* > - Greater than.
	* (=) - Contains.
	* (!=) - Does not contain.
* Value - Which value to use.
* Values - For =, !=, (=) and (!=) a list of values can be used instead of a single value."""},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}},
			}
		},
		'PANDAS:Column.Change':{
			'Version':2,
			'Title':'Change a column with Pandas',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'DF1', 'Help':'The ID which is used to identify the open pandas file.'},
				'Columns.Fill':{'Type':{'Type':'List'}, 'Example':['Name', 'Headcount'], 'Help':'A list of columns which will be filled with the value from the row above if empty.'},
				'Columns.Convert.Integer':{'Type':{'Type':'List'}, 'Example':['EmpID'], 'Help':'A list of columns which will be converted to integers'},
			},
		},
		'PANDAS:Column.Value':{
			'Version':4,
			'Title':'Capture column values with Pandas',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'DF1', 'Help':'The ID which is used to identify the open pandas file.'},
				'Column':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'Price', 'Help':'Specifies for which column the operation should be done on.'},
				'Logic':{'Type':{'Type':'Enum', 'Values':['Sum', 'Count', 'Min', 'Max', 'Average', 'Median', 'CountUnique']}, 'Example':'Sum', 'Help':"""Specifies for what logic should be used. Available options are:
* Sum - Adds up all values in the column.
* Count - Counts the number of rows.
* Min - Returns the lowest value.
* Max - Returns the highest value.
* Average - Returns the average value.
* Median - Returns the median value.
* CountUnique - Counts the number of unique values.
* ListUnique - Returns a list of the unique values."""},
				'Filters':{'Type':{'Type':'List'}, 'Example':[{"Column":"Projekt", "Logic":"=", "Value":"UTL-2250001"}], 'Help':"""A list of dicts which controlls which filters should be used on the sheet for the columns value generation. Dict legend:
* Column - Which column the filter should be placed on
* Logic - Which logic to be used:
	* = - Equal.
	* != - Not equal.
	* < - Less than.
	* > - Greater than.
	* (=) - Contains.
	* (!=) - Does not contain.
* Value - Which value to use.
* Values - For =, !=, (=) and (!=) a list of values can be used instead of a single value."""},
				'Convert':{'Type':{'Type':'List'}, 'Example':[{'Type':'String', 'Join':', '}], 'Convert':True, 'Help':'A list with dict conversion rules to use for the return value.'},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}},
				'UpdateGUI.Value':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'Entry##TEMP', 'Help':'Updates the GUI Entry instance TEMP with the input value.'},
				'UpdateGUI.Value.Trigger':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'Controls if the OnChange logic should be triggered for the Value changes.'},
				'Multiple':{'Type':{'Type':'List'}, 'Example':[{'Column':'Price', 'Logic':'Sum', 'Filters':[{"Column":"Projekt", "Logic":"=", "Value":"UTL-2250001"}], 'ReturnVariable':'TempValue'}], 'Help':"""A list of dicts with multiple entries containing the following values:
* Column
* Logic
* Filters
* Convert
* ReturnVariable
* ReturnVariable.Global
* UpdateGUI.Value
* UpdateGUI.Value.Trigger"""},
			},
		},
		'PANDAS:Create.File':{
			'Version':4,
			'Title':'Create an Excel/CSV file with Pandas',
			'Input':{
				'File':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':512}, 'Mandatory':'*', 'Help':'Filename to write.'},
				'File.Type':{'Type':{'Type':'Enum', 'Values':['CSV', 'Excel']}, 'Mandatory':'*', 'Help':"""File format to write:
* CSV - CSV file format.
* Excel - Excel file format."""},
				'CSV.Separator':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':4}, 'Example':';', 'Help':'Specifies the CSV separator string.'},
				'CSV.QuoteCharacter':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':1}, 'Example':'"', 'Help':'Specifies the CSV quotation character.'},
				'CSV.Quoting':{'Type':{'Type':'Enum', 'Values':['Minimal', 'All', 'NonNumeric', 'None']}, 'Example':'Minimal', 'Help':"""Specifies the quoting rule for CSV:
* Minimal - Only the fields requiring to be quoted will be quoted.
* All - values will be quoted.
* NonNumeric - All non numeric fields will be quoted.
* None - No values will be quoted."""},
				'Sheet':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':32}, 'Example':'Data', 'Help':'Specifies the sheet name if Type supports it.'},
				'Sheet.Replace':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'If the sheet already exists, replaces it.'},
				'Data.List':{'Type':{'Type':'List'}, 'Example':['Leo', 'Anders', 'Anna'], 'Help':'A 1D list of data to be saved in a file.'},
				'Data.ListList':{'Type':{'Type':'List'}, 'Example':[['Leo', 34], ['Anders', 45], ['Anna', 23]], 'Help':'A 2D list of data to be saved in a file.'},
				'Data.Dict':{'Type':{'Type':'Dict'}, 'Example':{'Leo':34, 'Anders':45, 'Anna':23}, 'Help':'A 1D dict of data to be saved in a file.'},
				'Data.DictList':{'Type':{'Type':'Dict'}, 'Example':{'Leo':['Male', 34], 'Anders':['Male', 45], 'Anna':['Female', 23]}, 'Help':'A dict with list values to be saved in a file.'},
				'Convert':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'Searches for dictionaries with a Convert list and a Value variable in the Data and runs it though the conversion logic before writing the file.'},
				'Data.DecimalCharacter':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':1}, 'Example':'.', 'Help':'Specifies the decimal character.'},
				'Data.RoundDecimals':{'Type':{'Type':'Integer'}, 'Example':3, 'Help':'Specifies how many decimals values should be rounded to.'},
				'Header.List':{'Type':{'Type':'List'}, 'Example':['ID', 'Name'], 'Help':'List of header fields.'},
				'Transpose':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'Transposes the provided data.'},
				'Header.Style':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':512}, 'Help':'String with header style.'},
			},
		},
		'IO:File.Exists':{
			'Version':2,
			'Title':'Check if a file exists',
			'Input':{
				'File':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':512}, 'Mandatory':'*'},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'TEMP_VALUE', 'Help':'Stores the result into the variable name provided.'},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'TEMP_VALUE', 'Help':'Stores the result into the global variable name provided.'},
			},
		},
		'IO:File.Info':{
			'Version':1,
			'Title':'Capture information about a file',
			'Input':{
				'File':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':512}, 'Mandatory':'*'},
				'Logic':{'Type':{'Type':'Enum', 'Values':['Size']}, 'Mandatory':'*', 'Example':'Size', 'Help':"""Specifies which logic that should be used for the file information:
* Size - Returns the file size in bytes."""},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'TEMP_VALUE', 'Help':'Stores the result into the variable name provided.'},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'TEMP_VALUE', 'Help':'Stores the result into the global variable name provided.'},
				'UpdateGUI.Value':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'Entry##TEMP', 'Help':'Updates the GUI Entry instance TEMP with the result value.'},
				'UpdateGUI.Value.Trigger':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'Controls if the OnChange logic should be triggered for the value change.'},
			},
		},
		'IO:File.MD5':{
			'Version':2,
			'Title':'Generate a MD5 checksum for a file',
			'Input':{
				'File':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':512}, 'Mandatory':'*'},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'TEMP_VALUE', 'Help':'Stores the result into the variable name provided.'},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'TEMP_VALUE', 'Help':'Stores the result into the global variable name provided.'},
			},
		},
		'IO:File.Copy':{
			'Version':2,
			'Title':'Copy a file',
			'Input':{
				'File.Source':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':512}, 'Mandatory':'*'},
				'File.Destination':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':512}, 'Mandatory':'*'},
				'Overwrite':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'If True, overwrites the destination file if it exists.'},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'TEMP_VALUE', 'Help':'Stores the result into the variable name provided.'},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'TEMP_VALUE', 'Help':'Stores the result into the global variable name provided.'},
			},
		},
		'IO:File.Remove':{
			'Version':1,
			'Title':'Remove a file',
			'Input':{
				'File':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':512}, 'Mandatory':'*', 'Example':'C:\\Users\\Zydox\\AppData\\Local\\Temp\\Test.csv', 'Help':'Deletes a file which is stored in the local temp folder.'},
			},
		},
		'IO:Files.Compare':{
			'Version':2,
			'Title':'Compares two files to see if they match.',
			'Input':{
				'File1':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':512}, 'Mandatory':'*', 'Example':'C:\\Users\\Zydox\\Test1.csv', 'Help':'The first file.'},
				'File2':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':512}, 'Mandatory':'*', 'Example':'C:\\Users\\Zydox\\Test2.csv', 'Help':'The second file.'},
				'MatchRules':{'Type':{'Type':'List'}, 'Default':['Size', 'Metadata', 'MD5.Minimal', 'MD5.Full'], 'Example':['Size', 'Metadata', 'MD5.Minimal'], 'Help':"""A list with which checks that need to match:
* Size - Checks the file sizes.
* Metadata - Checks the file metadata.
* MD5.Minimal - MD5 checks the first, middle and last 16384 bytes of the files. If the files are smaller than 49152 bytes, does a full check.
* MD5.Full - MD5 checks the full files."""},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'TEMP_VALUE', 'Help':'Stores the result into the variable name provided.'},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'TEMP_VALUE', 'Help':'Stores the result into the global variable name provided.'},
				'ReturnVariable.Reason':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'TEMP_VALUE', 'Help':'Stores the result into the variable name provided.'},
				'ReturnVariable.Reason.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'TEMP_VALUE', 'Help':'Stores the result into the global variable name provided.'},
			},
		},
		'IO:Path.Transform':{
			'Version':3,
			'Title':'Transform a path (%OneDrive% into the real path)',
			'Input':{
				'Path':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':512}, 'Example':'%OneDrive%\\Temp\\', 'Help':'Path which needs to be transformed.\nIn this example the path would become "C:\\Users\\Zydox\\OneDrive\\Temp\\".'},
				'Paths.Exist':{'Type':{'Type':'List'}, 'Example':['%OneDrive%\\Temp\\', 'C:\\Temp\\'], 'Help':'Searches though the list of paths and returns the first one which exists, if not exists, a WARNING is returned.'},
				'Path.Suffix':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':512}, 'Example':'Data.csv', 'Help':'Adds something to the end of the valid path.'},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'TEMP_VALUE', 'Help':'Stores the result into the variable name provided.'},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'TEMP_VALUE', 'Help':'Stores the result into the global variable name provided.'},
			},
		},
		'IO:Path.Exists':{
			'Version':2,
			'Title':'Check if a path exists',
			'Input':{
				'Path':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':512}, 'Example':'C:\\Users\\Zydox\\AppData\\Local\\Temp\\', 'Help':'Checks if the path exists.'},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'TEMP_VALUE', 'Help':'Stores the result into the variable name provided.'},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'TEMP_VALUE', 'Help':'Stores the result into the global variable name provided.'},
			},
		},
		'IO:Path.List':{
			'Version':2,
			'Title':'Return the files/folders from a path',
			'Input':{
				'Path':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':512}, 'Example':'C:\\Users\\Zydox\\AppData\\Local\\Temp\\', 'Help':'The path for which content should be returned.'},
				'Path.Remove':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'If True, removes the input Path from the returned values.'},
				'Recursive':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'If True, loops though all paths recursively.'},
				'Files':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'If True, returns all the files in the path.'},
				'Folders':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'If True, returns all folders in the path.'},
				'Size':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'If True, collects the total file size.'},
				'Count':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'If True, counts the files & folders (depending on Files & Folders settings).'},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'TEMP_VALUE', 'Help':'Stores the result into the variable name provided.'},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'TEMP_VALUE', 'Help':'Stores the result into the global variable name provided.'},
				'ReturnVariable.Count':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'TEMP_VALUE', 'Help':'Stores the result into the variable name provided.'},
				'ReturnVariable.Count.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'TEMP_VALUE', 'Help':'Stores the result into the global variable name provided.'},
				'UpdateGUI.Count.Value':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'Entry##TEMP', 'Help':'Updates the GUI Entry instance TEMP with the result value.'},
				'UpdateGUI.Count.Value.Trigger':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'Controls if the OnChange logic should be triggered for the value change.'},
				'ReturnVariable.Size':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'TEMP_VALUE', 'Help':'Stores the result into the variable name provided.'},
				'ReturnVariable.Size.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'TEMP_VALUE', 'Help':'Stores the result into the global variable name provided.'},
				'UpdateGUI.Size.Value':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'Entry##TEMP', 'Help':'Updates the GUI Entry instance TEMP with the result value.'},
				'UpdateGUI.Size.Value.Trigger':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'Controls if the OnChange logic should be triggered for the value change.'},
			},
		},
		'IO:Folder.Create':{
			'Version':1,
			'Title':'Creates a new folder',
			'Input':{
				'Folder':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':512}, 'Example':'C:\\Users\\Zydox\\AppData\\Local\\Temp\\', 'Help':'The folder to be created.'},
			},
		},
		'IO:Flow':{
			'Version':2,
			'Title':'Loads steps from a flow file',
			'Description':'Loads and executes steps from a steps file on read from the local disk or network.',
			'Input':{
				'File':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':512}, 'Mandatory':'*', 'Example':'C:\\Temp\\Steps.JSON', 'Help':'Path to file to run steps from.'},
				'Format':{'Type':{'Type':'Enum', 'Values':['JSON']}, 'Mandatory':'*', 'Example':'JSON', 'Help':'Which format the file contains.'},
			},
		},
		'LOGIC:Sleep':{
			'Version':1,
			'Title':'Adds a sleep to the steps',
			'Description':'Allows the script to take a break for x seconds, usefull for delaying things.',
			'Input':{
				'Seconds':{'Type':{'Type':'Numeric'}, 'Mandatory':'*', 'Example':60, 'Help':'Sleeps for x amount of seconds.'},
			},
		},
		'LOGIC:Threading':{
			'Version':2,
			'Title':'Runs steps in a dedicated thread',
			'Input':{
				'Thread':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'Thread#1', 'Help':'Gives the thread a specific identifier.'},
				'Steps':{'Type':{'Type':'List'}, 'Steps':True, 'Mandatory':'*'},
				'Isolated':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':'false', 'Help':'If True, all variables are isolated from eachother and removed after the thread is done.'},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'INIT_THREAD_ID', 'Help':'Sets the variable to the ID of the thread.'},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'INIT_THREAD_ID', 'Help':'Sets the global variable to the ID of the thread.'},
			},
		},
		'LOGIC:Threading.Wait':{
			'Version':1,
			'Title':'Function will sleep until provided threads have completed',
			'Description':'',
			'Input':{
				'Threads':{'Type':{'Type':'List'}, 'Example':['Thread1', 'Thread2'], 'Help':'This function will sleep until all threads in the list has been completed.'},
				'Wait.Max':{'Type':{'Type':'Numeric'}, 'Example':35.5, 'Help':'Specifies how many seconds this function will wait until returning a failed state.'},
				'Wait.Sleep':{'Type':{'Type':'Numeric'}, 'Example':0.5, 'Help':'Specifies how many seconds this function will wait between each update check.\nDefault is 1 second.'},
				'Return.Status':{'Type':{'Type':'Enum', 'Values':['WARNING', 'ERROR', 'CRASH']}, 'Example':'ERROR', 'Help':'Specifies which status the function will return if the Wait.Max time is exceeded.'},
			},
		},
		'LOGIC:Threading.Queue':{
			'Version':1,
			'Title':'Processes tasks in a queue with threading',
			'Description':'',
			'Input':{
				'Workers':{'Type':{'Type':'Integer'}, 'Example':2, 'Help':'Specifies how many worker threads that should be started.'},
				'List.Steps':{'Type':{'Type':'List'}, 'Example':[], 'Help':'A 2D list with steps to be executed, each first level list will be handled as a seperate task.'},
				'Data.ListList':{'Type':{'Type':'List'}},
				'Data.DictList':{'Type':{'Type':'Dict'}},
				'Data.ListDict':{'Type':{'Type':'List'}},
				'Data.DictDict':{'Type':{'Type':'Dict'}},
				'Data.List':{'Type':{'Type':'List'}},
				'Queue.MappingKey':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':32}, 'Example':'%%', 'Help':'String to be used as prefix and sufix for the replace values.'},
				'Queue.Mapping':{'Type':{'Type':'Dict'}, 'Example':{"COL.1":"$DATA.LIST=1$", "RowID":"$LOOP.ROW$"}, 'Help':"""Allows the steps to be updated with values from the input data. Keywords allowed:
$LOOP.ROW$ - For Data.ListList, the value of the current data row, starts at 0. For Data.DictList, the key
$LOOP.ROW+1$ - For Data.ListList, the value of the current data row, starts at 1
$DATA.ROW$ - Takes the entire entry
$DATA.LIST=0$ - Takes the value from the first column in the Data.ListList or Data.DictList input is used
$DATA.DICT=ID$ - Takes the value from the dict entry with the key ID if the Data.ListDict or Data.DictDict input is used
				"""},
				'Steps':{'Type':{'Type':'List'}, 'Steps':True, 'Mandatory':'*', 'Help':'Steps to be executed. The keys from Loop.Mapping will be replaced by the corresponding value.\nBased on Loop.MappingKey and Loop.Mapping, a step with the value "Button%%RowID%%" would be replaced with "Button0" for the first line in the data, "Button1" for the second and so on.'},
			},
		},
		'LOGIC:Threading.Lock':{
			'Version':1,
			'Title':'Runs steps within a lock',
			'Description':'',
			'Input':{
				'Lock':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'LOCK#1', 'Help':'The identifier for the lock to be used.'},
				'Steps':{'Type':{'Type':'List'}, 'Steps':True, 'Mandatory':'*', 'Help':'Steps to be executed. The keys from Loop.Mapping will be replaced by the corresponding value.\nBased on Loop.MappingKey and Loop.Mapping, a step with the value "Button%%RowID%%" would be replaced with "Button0" for the first line in the data, "Button1" for the second and so on.'},
			},
		},
		'LOGIC:Template.Create':{
			'Version':2,
			'Title':'Creates a template for commonly used steps',
			'Description':"""Used to create a template the allow the reduction of steps in the JSON code.
An input with the keys ID and Name can then be used in the Steps where %%ID%% and %%Name%% will be replaced with the input values provided in the LOGIC:Template call.	""",
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*'},
				'Input':{'Type':{'Type':'Dict'}, 'Mandatory':'*', 'Example':{"ID":{"Type":"String"}, "FrameID":{"Type":"String", "Default":"Frame#Info"}}, 'Help':"""A 2D dict with the input fields as the key and the following values in the dict:
* Type - The input type: Integer, String, Dict, List, Float.
* Default (optional) - The default value to be used if nothing is provided."""},
				'Input.Recurrences':{'Type':{'Type':'Integer', 'Min':1, 'Max':128}, 'Example':1, 'Help':'If used, re-runs the Input logic X amount of times.'},
				'Steps':{'Type':{'Type':'List'}, 'Steps':True, 'Mandatory':'*', 'Help':'A list of the steps to execute each time the template is called.\nInput values with %%INTUP%% will be replaced with the provided values.'},
			},
		},
		'LOGIC:Template':{
			'Version':2,
			'Title':'Uses a generated template',
			'Description':'',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*'},
				'Input':{'Type':{'Type':'Dict'}, 'Steps':True, 'Steps.Dict':True},
				'Debug.Console':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'If True, displays debug steps in console.'},
			},
		},
		'LOGIC:Steps':{
			'Version':2,
			'Title':'Runs a list of steps',
			'Description':'Executes the provided list of steps.\nIf Isolation is provided, execute them in either a new isolation or in a specific provided isolation.',
			'Input':{
				'Isolation':{'Type':{'Type':['String', 'Boolean'], 'LengthMin':1, 'LengthMax':128}, 'Example':'Isolated#1', 'Help':'Runs the provided steps in an isolation, if a string is provided, use that as the isolation key.'},
				'Steps':{'Type':{'Type':'List'}, 'Steps':True, 'Mandatory':'*', 'Help':'Steps to be executed.'},
				'Debug.Console':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'If True, displays debug steps in console.'},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}},
				'ReturnVariable.Status':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}},
				'ReturnVariable.Status.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}},
				'Steps.IgnoreResult':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'If True, this function will return status OK regardless of the outcome of the steps.'},
			},
		},
		'LOGIC:Loop':{
			'Version':3,
			'Title':'Loops though data and executes steps',
			'Input':{
				'Data.ListList':{'Type':{'Type':'List'}},
				'Data.DictList':{'Type':{'Type':'Dict'}},
				'Data.ListDict':{'Type':{'Type':'List'}},
				'Data.DictDict':{'Type':{'Type':'Dict'}},
				'Data.List':{'Type':{'Type':'List'}},
				'Loop.MappingKey':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':32}, 'Example':'%%', 'Help':'String to be used as prefix and sufix for the replace values.'},
				'Loop.Mapping':{'Type':{'Type':'Dict'}, 'Example':{"COL.1":"$DATA.LIST=1$", "RowID":"$LOOP.ROW$"}, 'Help':"""Allows the steps to be updated with values from the input data. Keywords allowed:
$LOOP.ROW$ - For Data.ListList, the value of the current data row, starts at 0. For Data.DictList, the key
$LOOP.ROW+1$ - For Data.ListList, the value of the current data row, starts at 1
$DATA.ROW$ - Takes the entire entry
$DATA.LIST=0$ - Takes the value from the first column in the Data.ListList or Data.DictList input is used
$DATA.DICT=ID$ - Takes the value from the dict entry with the key ID if the Data.ListDict or Data.DictDict input is used
				"""},
				'Steps':{'Type':{'Type':'List'}, 'Steps':True, 'Mandatory':'*', 'Help':'Steps to be executed. The keys from Loop.Mapping will be replaced by the corresponding value.\nBased on Loop.MappingKey and Loop.Mapping, a step with the value "Button%%RowID%%" would be replaced with "Button0" for the first line in the data, "Button1" for the second and so on.'},
				'Debug.Console':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'If True, displays debug steps in console.'},
			},
		},
		'WEB:URL':{
			'Version':6,
			'Title':'Download a URL into a variable',
			'Input':{
				'URL':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':1024}, 'Mandatory':'URL', 'Example':'https://www.omoikane.se/', 'Help':'The URL to access.'},
				'Method':{'Type':{'Type':'Enum', 'Values':['GET', 'POST', 'PUT', 'Windows.Powershell']}, 'Mandatory':'METHOD', 'Example':'GET', 'Help':"""Specifies which method to use:
* GET - Uses requests.GET to process the URL.
* POST - Uses requests.POST to process the URL.
* PUT -Uses requests.PUT to process the URL.
* Windows.Powershell - Uses windows powershell to execute a URL and fetch the result."""},
				'Data.JSON':{'Type':{'Type':'Any'}, 'Example':{'Data':[1, 2]}, 'Help':'JSON data which is sent with the request.'},
				'JSON':{'Type':{'Type':'Boolean'}, 'Example':False, 'Help':'Converts the result from JSON.'},
				'Auth':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'If True, tries to send the SSO auth with the request.'},
				'ValidStatuses':{'Type':{'Type':'List'}, 'Default':[200], 'Example':[200], 'Help':'Specifies which return statuses that are considered valid.'},
				'Status':{'Type':{'Type':'Boolean'}, 'Example':False, 'Help':'Returns the status of the request instead of the content.'},
				'Content':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'Returns requests.content instead of requests.text.'},
				'Redirects':{'Type':{'Type':'Boolean'}, 'Default':True, 'Example':False, 'Help':'False disables redirects.'},
				'Verify':{'Type':{'Type':'Boolean'}, 'Default':True, 'Example':False, 'Help':'False disables TSL verification.'},
				'Verify.DisableWarnings':{'Type':{'Type':'Boolean'}, 'Default':True, 'Example':False, 'Help':'If True, disables the warnings from a false verify.'},
				'Verify.Certifi':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'True uses the certifi.where() logic for TLS verification.'},
				'Files':{'Type':{'Type':'Dict'}, 'Default':None, 'Help':'A dict of files to send though the requests class.'},
				'Proxies':{'Type':{'Type':'Dict'}, 'Default':None, 'Help':'A dict of proxies to send though the requests class.'},
				'Headers':{'Type':{'Type':'Dict'}, 'Default':None, 'Help':'A dict of headers to send though the requests class.'},
				'Powershell.TempFile':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':1024}, 'Example':'C:\\Temp\\TempDownload.tmp', 'Help':'Temporary file to use for the powershell download.'},
				'Powershell.Binary':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'If True, returns the content from Powershell as binary.'},
				'Encrypt':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'If True, encrypts the data to be sent (using the internal key).'},
				'Decrypt':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'If True, decrypts the data recieved (using the internal key).'},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}},
				'ReturnVariable.Status':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}},
				'ReturnVariable.Status.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}},
				'UpdateGUI.Value':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'Entry##TEMP', 'Help':'Updates the GUI Entry instance TEMP with the input value.'},
				'UpdateGUI.Value.Trigger':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'Controls if the OnChange logic should be triggered for the Value changes.'},
				'Debug.Console':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'If True, displays debug steps in console.'},
			},
		},
		'WEB:URL.Encode':{
			'Version':2,
			'Title':'Encode a URL',
			'Input':{
				'URL':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':1024}, 'Mandatory':'URL', 'Example':'https://www.omoikane.se/', 'Help':'The URL to encode.'},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}},
			},
		},
		'WEB:Default.Web.Interal':{
			'Version':1,
			'Title':'Sets defaults for the internal web calls',
			'Input':{
				'Auth':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'If True, tries to send the SSO auth with the request.'},
				'Verify':{'Type':{'Type':'Boolean'}, 'Default':True, 'Example':False, 'Help':'False disables TSL verification.'},
				'Verify.DisableWarnings':{'Type':{'Type':'Boolean'}, 'Default':True, 'Example':False, 'Help':'If True, disables the warnings from a false verify.'},
			},
		},
		'PDF:Create':{
			'Version':2,
			'Title':'Create a PDF file',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'PDF1', 'Help':'The ID which is used to identify the PDF file.'},
				'File':{'Type':{'Type':'String', 'LengthMin':5, 'LengthMax':512}, 'Example':'C:\\\\Tools\\\\Data.pdf', 'Help':'Which file that should be created.'},
				'Width':{},
				'Height':{},
			},
		},
		'PDF:Document.Frames':{
			'Version':1,
			'Title':'Sets frames in the PDF',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'PDF1', 'Help':'The ID which is used to identify the PDF file.'},
				'Split':{'Type':{'Type':'Integer'}, 'Example':2, 'Help':'Specifies many columns the layout should be split into'},
				'Border.Color':{'Type':{'Type':'String', 'LengthMin':7, 'LengthMax':7}, 'Example':'#00FF00', 'Help':'The color of the frame borders, if not used, no borders will be printed.'},
			},
		},
		'PDF:Add.Paragraph':{
			'Version':1,
			'Title':'Add a paragraph to a PDF',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'PDF1', 'Help':'The ID which is used to identify the PDF file.'},
				'Paragraph':{},
			},
		},
		'PDF:Add.Table':{
			'Version':3,
			'Title':'Add a table to a PDF',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'PDF1', 'Help':'The ID which is used to identify the PDF file.'},
				'Data':{'Type':{'Type':'List'}, 'Example':[[1, 2], [3, 4]], 'Help':'A 2D list of the entries for the table.'},
				'Data.Convert':{'Type':{'Type':'List'}, 'Convert':True, 'Example':[{"Type":"Array","Array.Convert":{"String":[{"Type":"String", "Encode":"Latin-1", "Decode":"UTF-8"}]}}], 'Help':'Executes the list of conversion rules on the input Data.'},
				'SpaceBefore':{'Type':{'Type':'Integer'}, 'Example':50, 'Help':'Specifies how many pixles that should be empty before the table if it\'s not in the top of the page'},
				'SpaceAfter':{'Type':{'Type':'Integer'}, 'Example':50, 'Help':'Specifies how many pixles that should be empty after the table if it\'s not in the bottom of the page'},
				'ColumnWidth':{'Type':{'Type':['Integer', 'List']}, 'Example':[10, 20, 30], 'Help':'Specifies the column width in pixles, if a list is provided and there are more columns in the data, the logic will be looped.'},
				'RowHeight':{'Type':{'Type':['Integer', 'List']}, 'Example':25, 'Help':'Specifies the row height in pixles, if a list is provided and there are more rows in the data, the logic will be looped.'},
				'Style':{'Type':{'Type':'List'}, 'Example':[{"Type":"Background", "Area":[1, 1, -2, -2], "Color":"#FF0000"}, {"Type":"Background", "Area":[0, 0, 0, -1], "Color":"#00FF00"}, {"Type":"Text", "Area":[0, 0, 1, -1], "Color":"#0000FF"}], 'Help':"""A list with dicts of stype configs to be used on the table, each dict consists of this:
* Type - Which design type that's used:
	* Background - The background of the cells.
	* Text - The color of the text.
	* Box - Adds a box.
	* Grid - Adds a grid.
	* Align - Aligns the content with (Left, Right or Center in Alignment).
	* VerticalAlign - Aligns the content with (Top, Middle or Bottom in Alignment).
	* FontSize - Sets the font size.
* Area - A list of [starting row, starting column, end row, end column]. -1 would be the last cell, -2 second to last and so on.
* Color - The color to be used.
* Width - The width used by Grid.
* Alignment - Alignment used for Align and VerticalAlign.
* Size - Used by FontSize."""},
				'Span':{'Type':{'Type':'List'}, 'Example':[[0, 1, -1, -1]], 'Help':'A list with lists containing the cells for the box, [starting row, starting column, end row, end column]. -1 would be the last cell, -2 second to last and so on.'}
			},
		},
		'PDF:Add.PageBreak':{
			'Version':1,
			'Title':'Add a page break to a PDF',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'PDF1', 'Help':'The ID which is used to identify the PDF file.'},
			},
		},
		'PDF:Add.Image':{
			'Version':2,
			'Title':'Add an image to a PDF',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'PDF1', 'Help':'The ID which is used to identify the PDF file.'},
				'File':{'Type':{'Type':'String', 'LengthMin':5, 'LengthMax':512}, 'Example':'C:\\\\Tools\\\\Data.png', 'Help':'Which image file that should be used.'},
				'Width':{},
				'Height':{},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'PDF_IMG', 'Help':'Stores the image in the provided variable instead of adding it to the PDF.'},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'PDF_IMG', 'Help':'Stores the image in the provided global variable instead of adding it to the PDF.'},
			},
		},
		'PDF:Close':{
			'Version':2,
			'Title':'Close & save the PDF',
			'Input':{
				'ID':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Mandatory':'*', 'Example':'PDF1', 'Help':'The ID which is used to identify the PDF file.'},
			},
		},
		'IMAGE:QR.Generate':{
			'Version':2,
			'Title':'Generate a QR barcode',
			'Input':{
				'Content':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':4096}, 'Mandatory':'*', 'Example':'https://www.google.se/', 'Help':'The content of the QR code.'},
				'Size':{},
				'Border':{},
				'File':{},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'IO_QR', 'Help':'Stores the QR code in the provided variable, if running is an isolated state, will keep the variable isolated.'},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'IO_QR', 'Help':'Stores the QR code in the provided variable, if running is an isolated state, will keep the data in the global variable instead of the isolated one.'},
			},
		},
		'SCRIPTING:Excel.Open.List':{
			'Version':2,
			'Title':'Captures information about open Excel workbooks',
			'Description':'Function which is used to access information about the open workbooks and sheets in Excel.',
			'Input':{
				'Workbooks':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'If True, captures a list of all open workbooks.'},
				'Workbook':{'Type':{'Type':'String'}, 'Example':'Manuals.xlsx', 'Help':'Specifies a specific workbook.'},
				'Sheets':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'If True, captures a list of all open sheets for the specified workbook.'},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'TEMP_VALUE', 'Help':'Stores the result in the provided variable, if running is an isolated state, will keep the variable isolated.'},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'TEMP_VALUE', 'Help':'Stores the result in the provided variable, if running is an isolated state, will keep the data in the global variable instead of the isolated one.'},
				'Refresh':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'If True, refreshes the list of open Excel workbooks and sheets.'},
			},
		},
		'SCRIPTING:Excel.Read':{
			'Version':2,
			'Title':'Read data from an open Excel workbook sheet',
			'Description':'',
			'Input':{
				'Workbook':{'Type':{'Type':'String'}, 'Example':'Manuals.xlsx', 'Help':'Specifies a specific workbook.'},
				'Sheet':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Example':'Sheet1', 'Help':'Specifies a specific sheet.'},
				'Complete':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'If True, captures whole sheet into a 2D list of texts or values.'},
				'Row':{'Type':{'Type':'Integer'}, 'Example':1, 'Help':'Captures the text or value from the provided row into a list.'},
				'Cell':{'Type':{'Type':'String', 'LengthMin':2, 'LengthMax':9}, 'Example':'B5', 'Help':'Captures the text or value from the provided cell.'},
				'CaptureValues':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'If True, captures the cell values instead of the displayed text.'},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'TEMP_VALUE', 'Help':'Stores the result in the provided variable, if running is an isolated state, will keep the variable isolated.'},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'TEMP_VALUE', 'Help':'Stores the result in the provided variable, if running is an isolated state, will keep the data in the global variable instead of the isolated one.'},
				'Refresh':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'If True, refreshes the list of open Excel workbooks and sheets.'},
			},
		},
		'SCRIPTING:Excel.Write':{
			'Version':1,
			'Title':'Write data to an open Excel workbook sheet',
			'Description':'',
			'Input':{
				'Workbook':{'Type':{'Type':'String'}, 'Example':'Manuals.xlsx', 'Help':'Specifies a specific workbook.'},
				'Sheet':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':64}, 'Example':'Sheet1', 'Help':'Specifies a specific sheet.'},
				'Cell':{'Type':{'Type':'String', 'LengthMin':2, 'LengthMax':9}, 'Example':'B5', 'Help':'Specifies which cell that should be changed.'},
				'Cell.Value':{'Type':{'Type':'Any'}, 'Example':0.67, 'Help':'The value to be written to the cell'},
				'Cell.Color':{'Type':{'Type':'String'}, 'Example':'#901234', 'Help':'Specifies the RGB font color of a cell'},
				'Cell.Background':{'Type':{'Type':'String'}, 'Example':'#123456', 'Help':'Specifies the RGB background color of a cell'},
				'Refresh':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'If True, refreshes the list of open Excel workbooks and sheets.'},
			},
		},
		'SCRIPTING:SAP.Session.Open':{
			'Version':3,
			'Title':'Open a SAP session',
			'Description':'',
			'Input':{
				'Object.SAP':{'Type':{'Type':'String'}, 'Example':'SAP_EWM', 'Help':'Specifies if a specific SAP connection should be used and not the general one from the isolation key.'},
				'System':{'Type':{'Type':'String'}, 'Example':'0885 -- PEW -- EU Azure EWM Production System', 'Help':'Specifies for which system a session should be opened.'},
				'SAPLogon':{'Type':{'Type':'List'}, 'Example':['C:\\Program Files (x86)\\SAP\\FrontEnd\\SapGui\\saplogon.exe'], 'Help':'A list of paths to the saplogon.exe file.'},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'TEMP_VALUE', 'Help':'Stores the result in the provided variable, if running is an isolated state, will keep the variable isolated.'},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'TEMP_VALUE', 'Help':'Stores the result in the provided variable, if running is an isolated state, will keep the data in the global variable instead of the isolated one.'},
				'Debug.Console':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'If True, displays debug steps in console.'},
			},
		},
		'SCRIPTING:SAP.Session.Acquire':{
			'Version':2,
			'Title':'Acquire a SAP session',
			'Description':'',
			'Input':{
				'Object.SAP':{'Type':{'Type':'String'}, 'Example':'SAP_EWM', 'Help':'Specifies if a specific SAP connection should be used and not the general one from the isolation key.'},
				'System':{'Type':{'Type':'String'}, 'Example':'0885 -- PEW -- EU Azure EWM Production System', 'Help':'Specifies for which system a session should be opened.'},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'TEMP_VALUE', 'Help':'Stores the result in the provided variable, if running is an isolated state, will keep the variable isolated.'},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'TEMP_VALUE', 'Help':'Stores the result in the provided variable, if running is an isolated state, will keep the data in the global variable instead of the isolated one.'},
			},
		},
		'SCRIPTING:SAP.Session.Resize':{
			'Version':1,
			'Title':'Resize a SAP session',
			'Description':'',
			'Input':{
				'Object.SAP':{'Type':{'Type':'String'}, 'Example':'SAP_EWM', 'Help':'Specifies if a specific SAP connection should be used and not the general one from the isolation key.'},
				'Minimize':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'If True, minimizes the SAP window.'},
				'Maximize':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'If True, maximizes the SAP window.'},
				'Restore':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'If True, restores the SAP window.'},
				'Width':{'Type':{'Type':'Integer'}, 'Example':1024, 'Help':'Changes the size of the SAP window to this width, needs to be used together with Height.'},
				'Height':{'Type':{'Type':'Integer'}, 'Example':800, 'Help':'Changes the size of the SAP window to this height, needs to be used together with Width.'},
			},
		},
		'SCRIPTING:SAP.Session.Formats':{
			'Version':1,
			'Title':'Sets the number and date format for the SAP session',
			'Description':'',
			'Input':{
				'Object.SAP':{'Type':{'Type':'String'}, 'Example':'SAP_EWM', 'Help':'Specifies if a specific SAP connection should be used and not the general one from the isolation key.'},
				'NumberFormat.Set':{'Type':{'Type':'Enum', 'Values':[None, 'X,XXX,XXX.XX', 'X.XXX.XXX,XX', 'X XXX XXX,XX']}, 'Example':'X XXX XXX,XX', 'Help':'Sets the number format used for values with the prefix <NUMERIC>.\nThe value "123812.34" would become "123 812,34" with the "X XXX XXX,XX" format.'},
				'DateFormat.Set':{'Type':{'Type':'Enum', 'Values':[None, 'YYYY-MM-DD', 'DD.MM.YYYY', 'MM-DD-YYYY', 'YYYY.MM.DD', 'YYYY/MM/DD', 'MM/DD/YYYY']}, 'Exampel':'MM/DD/YYYY', 'Help':'Sets the date format used for values with the prefix <DATE> and <DATETIME>.\nThe value "2025-05-16" would become "05/16/2025" with the "MM/DD/YYYY" format.'},
			},
		},
		'SCRIPTING:SAP.Session.Close':{
			'Version':1,
			'Title':'Close the SAP session',
			'Description':'',
			'Input':{
				'Object.SAP':{'Type':{'Type':'String'}, 'Example':'SAP_EWM', 'Help':'Specifies if a specific SAP connection should be used and not the general one from the isolation key.'},
			},
		},
		'SCRIPTING:SAP.Session.Release':{
			'Version':1,
			'Title':'Release the SAP session',
			'Description':'',
			'Input':{
				'Object.SAP':{'Type':{'Type':'String'}, 'Example':'SAP_EWM', 'Help':'Specifies if a specific SAP connection should be used and not the general one from the isolation key.'},
			},
		},
		'SCRIPTING:SAP.Send.Text':{
			'Version':1,
			'Title':'Sends a text to a SAP field',
			'Description':'',
			'Input':{
				'Object.SAP':{'Type':{'Type':'String'}, 'Example':'SAP_EWM', 'Help':'Specifies if a specific SAP connection should be used and not the general one from the isolation key.'},
				'Field':{'Type':{'Type':'String', 'LengthMin':4, 'LengthMax':512}, 'Example':'wnd[0]/tbar[0]/okcd', 'Help':'Specifies which SAP field that should be used'},
				'Text':{'Type':{'Type':'String'}},
			},
		},
		'SCRIPTING:SAP.Send.Key':{
			'Version':1,
			'Title':'Sends a key to a SAP field',
			'Description':'',
			'Input':{
				'Object.SAP':{'Type':{'Type':'String'}, 'Example':'SAP_EWM', 'Help':'Specifies if a specific SAP connection should be used and not the general one from the isolation key.'},
				'Field':{'Type':{'Type':'String', 'LengthMin':4, 'LengthMax':512}, 'Example':'wnd[0]/tbar[0]/okcd', 'Help':'Specifies which SAP field that should be used'},
				'Key':{'Type':{'Type':['String', 'Integer']}},
			},
		},
		'SCRIPTING:SAP.Send.Select':{
			'Version':1,
			'Title':'Sends a select click to a SAP field',
			'Description':'',
			'Input':{
				'Object.SAP':{'Type':{'Type':'String'}, 'Example':'SAP_EWM', 'Help':'Specifies if a specific SAP connection should be used and not the general one from the isolation key.'},
				'Field':{'Type':{'Type':'String', 'LengthMin':4, 'LengthMax':512}, 'Example':'wnd[0]/tbar[0]/okcd', 'Help':'Specifies which SAP field that should be used'},
			},
		},
		'SCRIPTING:SAP.Send.Selected':{
			'Version':1,
			'Title':'Sends a selected command to a SAP field',
			'Description':'',
			'Input':{
				'Object.SAP':{'Type':{'Type':'String'}, 'Example':'SAP_EWM', 'Help':'Specifies if a specific SAP connection should be used and not the general one from the isolation key.'},
				'Field':{'Type':{'Type':'String', 'LengthMin':4, 'LengthMax':512}, 'Example':'wnd[0]/tbar[0]/okcd', 'Help':'Specifies which SAP field that should be used'},
				'Selected':{'Type':{'Type':'Boolean'}},
			},
		},
		'SCRIPTING:SAP.Send.Press':{
			'Version':1,
			'Title':'Sends a press to a SAP field',
			'Description':'',
			'Input':{
				'Object.SAP':{'Type':{'Type':'String'}, 'Example':'SAP_EWM', 'Help':'Specifies if a specific SAP connection should be used and not the general one from the isolation key.'},
				'Field':{'Type':{'Type':'String', 'LengthMin':4, 'LengthMax':512}, 'Example':'wnd[0]/tbar[0]/okcd', 'Help':'Specifies which SAP field that should be used'},
			},
		},
		'SCRIPTING:SAP.Send.Focus':{
			'Version':1,
			'Title':'Sends a focus to a SAP field',
			'Description':'',
			'Input':{
				'Object.SAP':{'Type':{'Type':'String'}, 'Example':'SAP_EWM', 'Help':'Specifies if a specific SAP connection should be used and not the general one from the isolation key.'},
				'Field':{'Type':{'Type':'String', 'LengthMin':4, 'LengthMax':512}, 'Example':'wnd[0]/tbar[0]/okcd', 'Help':'Specifies which SAP field that should be used'},
			},
		},
		'SCRIPTING:SAP.Send.NodeDoubleClick':{
			'Version':1,
			'Title':'Sends a node double click to a SAP field & node',
			'Description':'',
			'Input':{
				'Object.SAP':{'Type':{'Type':'String'}, 'Example':'SAP_EWM', 'Help':'Specifies if a specific SAP connection should be used and not the general one from the isolation key.'},
				'Field':{'Type':{'Type':'String', 'LengthMin':4, 'LengthMax':512}, 'Example':'wnd[0]/usr/shell/shellcont[0]/shell', 'Help':'Specifies which SAP field that should be used'},
				'Node':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'ZN00000086', 'Help':'Specifies which SAP node that should be double clicked'},
			},
		},
		'SCRIPTING:SAP.Send.PressToolbarContextButton':{
			'Version':1,
			'Title':'Sends a press toolbar context button to a SAP field in a toolbar',
			'Description':'',
			'Input':{
				'Object.SAP':{'Type':{'Type':'String'}, 'Example':'SAP_EWM', 'Help':'Specifies if a specific SAP connection should be used and not the general one from the isolation key.'},
				'Field':{'Type':{'Type':'String', 'LengthMin':4, 'LengthMax':512}, 'Example':'wnd[0]/usr/shell/shellcont[1]/shell/shellcont[0]/shell', 'Help':'Specifies which SAP field that should be used'},
				'Toolbar':{'Type':{'Type':'String', 'LengthMin':4, 'LengthMax':128}, 'Example':'&MB_VARIANT', 'Help':'Specifies which SAP toolbar option that should be used'},
			},
		},
		'SCRIPTING:SAP.Send.SelectContextMenuItem':{
			'Version':1,
			'Title':'Send a select context menu item for a field & item to SAP',
			'Description':'',
			'Input':{
				'Object.SAP':{'Type':{'Type':'String'}, 'Example':'SAP_EWM', 'Help':'Specifies if a specific SAP connection should be used and not the general one from the isolation key.'},
				'Field':{'Type':{'Type':'String', 'LengthMin':4, 'LengthMax':512}, 'Example':'wnd[0]/usr/shell/shellcont[1]/shell/shellcont[0]/shell', 'Help':'Specifies which SAP field that should be used'},
				'Item':{'Type':{'Type':'String', 'LengthMin':4, 'LengthMax':512}, 'Example':'&LOAD', 'Help':'Specifies which SAP menu item that should be used'},
			},
		},
		'SCRIPTING:SAP.Send.ContextMenu':{
			'Version':1,
			'Title':'Send a context menu command to SAP',
			'Description':'',
			'Input':{
				'Object.SAP':{'Type':{'Type':'String'}, 'Example':'SAP_EWM', 'Help':'Specifies if a specific SAP connection should be used and not the general one from the isolation key.'},
				'Field':{'Type':{'Type':'String', 'LengthMin':4, 'LengthMax':512}, 'Example':'wnd[1]/usr/subSUB_CONFIGURATION:SAPLSALV_CUL_LAYOUT_CHOOSE:0500/cntlD500_CONTAINER/shellcont/shell', 'Help':'Specifies which SAP field that should be used'},
			},
		},
		'SCRIPTING:SAP.Send.SelectedRows':{
			'Version':1,
			'Title':'Send a selected rows command to a SAP field',
			'Description':'',
			'Input':{
				'Object.SAP':{'Type':{'Type':'String'}, 'Example':'SAP_EWM', 'Help':'Specifies if a specific SAP connection should be used and not the general one from the isolation key.'},
				'Field':{'Type':{'Type':'String', 'LengthMin':4, 'LengthMax':512}, 'Example':'wnd[1]/usr/subSUB_CONFIGURATION:SAPLSALV_CUL_LAYOUT_CHOOSE:0500/cntlD500_CONTAINER/shellcont/shell', 'Help':'Specifies which SAP field that should be used'},
				'Rows':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':512}, 'Example':'0', 'Help':'Specifies which SAP rows that should be selected'},
			},
		},
		'SCRIPTING:SAP.Send.ClickCurrentCell':{
			'Version':1,
			'Title':'Send a click current cell command to the SAP field',
			'Description':'',
			'Input':{
				'Object.SAP':{'Type':{'Type':'String'}, 'Example':'SAP_EWM', 'Help':'Specifies if a specific SAP connection should be used and not the general one from the isolation key.'},
				'Field':{'Type':{'Type':'String', 'LengthMin':4, 'LengthMax':512}, 'Example':'wnd[1]/usr/subSUB_CONFIGURATION:SAPLSALV_CUL_LAYOUT_CHOOSE:0500/cntlD500_CONTAINER/shellcont/shell', 'Help':'Specifies which SAP field that should be used'},
			},
		},
		'SCRIPTING:SAP.Send.PressToolbarButton':{
			'Version':1,
			'Title':'Send a press toolbar button command to  the SAP field',
			'Description':'',
			'Input':{
				'Object.SAP':{'Type':{'Type':'String'}, 'Example':'SAP_EWM', 'Help':'Specifies if a specific SAP connection should be used and not the general one from the isolation key.'},
				'Field':{'Type':{'Type':'String', 'LengthMin':4, 'LengthMax':512}, 'Example':'wnd[0]/usr/subSUB_RESULT:/SCWM/SAPLUI_PS_OIP_FRMWRK:0200/cntlOIP_SEARCH_RESULT/shellcont/shell', 'Help':'Specifies which SAP field that should be used'},
				'Button':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'CHANGE', 'Help':'Specifies which SAP button that should be used'},
			},
		},
		'SCRIPTING:SAP.Send.SelectedNode':{
			'Version':1,
			'Title':'Send a selected node command to the SAP field',
			'Description':'',
			'Input':{
				'Object.SAP':{'Type':{'Type':'String'}, 'Example':'SAP_EWM', 'Help':'Specifies if a specific SAP connection should be used and not the general one from the isolation key.'},
				'Field':{'Type':{'Type':'String', 'LengthMin':4, 'LengthMax':512}, 'Example':'wnd[0]/shellcont/shell/shellcont[1]/shell[1]', 'Help':'Specifies which SAP field that should be used'},
				'Node':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'          4', 'Help':'Specifies which value should be set for the SAP node.'},
			},
		},
		'SCRIPTING:SAP.Check.Text':{
			'Version':2,
			'Title':'Checks in a SAP text has a specific value/text',
			'Description':'',
			'Input':{
				'Object.SAP':{'Type':{'Type':'String'}, 'Example':'SAP_EWM', 'Help':'Specifies if a specific SAP connection should be used and not the general one from the isolation key.'},
				'Field':{'Type':{'Type':'String', 'LengthMin':4, 'LengthMax':512}, 'Example':'wnd[0]/tbar[0]/okcd', 'Help':'Specifies which SAP field that should be used'},
				'Text':{'Type':{'Type':'String'}, 'Example':'locked by', 'Help':'A text which is searched for.'},
				'WhileFalse.Wait':{'Type':{'Type':'Numeric', 'Min':0, 'Max':128}},
				'WhileFalse.Loops':{'Type':{'Type':'Integer', 'Min':0, 'Max':1024}},
				'WhileFalse.Steps':{'Type':{'Type':'List'}, 'Steps':True, 'Help':'A list of steps which will be executed in each False loop.'},
				'WhileFalse.Wait.Max':{'Type':{'Type':'Numeric', 'Min':0, 'Max':128}},
				'WhileFalse.Wait.Multiplier':{'Type':{'Type':'Numeric', 'Min':0, 'Max':64}},
				'WhileTrue.Wait':{'Type':{'Type':'Numeric', 'Min':0, 'Max':128}},
				'WhileTrue.Loops':{'Type':{'Type':'Integer', 'Min':0, 'Max':1024}},
				'WhileTrue.Steps':{'Type':{'Type':'List'}, 'Steps':True, 'Help':'A list of steps which will be executed in each True loop.'},
				'WhileTrue.Wait.Max':{'Type':{'Type':'Numeric', 'Min':0, 'Max':128}},
				'WhileTrue.Wait.Multiplier':{'Type':{'Type':'Numeric', 'Min':0, 'Max':64}},
				'OnTrue':{'Type':{'Type':'List'}, 'Steps':True, 'Help':'A list of steps which will be executed if the end result is True.'},
				'OnFalse':{'Type':{'Type':'List'}, 'Steps':True, 'Help':'A list of steps which will be executed if the end result is False.'},
				'Debug.Console':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'If True, displays debug steps in console.'},
			},
		},
		'SCRIPTING:SAP.Capture':{
			'Version':2,
			'Title':'Capture SAP data into a variable',
			'Description':'',
			'Input':{
				'Object.SAP':{'Type':{'Type':'String'}, 'Example':'SAP_EWM', 'Help':'Specifies if a specific SAP connection should be used and not the general one from the isolation key.'},
				'Transaction':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'Captures the current SAP transaction.'},
				'NumberFormat':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'Captures the current SAP number format.'},
				'DateFormat':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'Captures the current SAP date format.'},
				'StatusBarText':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'Captures the status bar text'},
				'Field.Text':{'Type':{'Type':'String'}, 'Example':'wnd[0]/tbar[0]/okcd', 'Help':'Captures the text of the provided field.'},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'TEMP_VALUE', 'Help':'Stores the result in the provided variable, if running is an isolated state, will keep the variable isolated.'},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'TEMP_VALUE', 'Help':'Stores the result in the provided variable, if running is an isolated state, will keep the data in the global variable instead of the isolated one.'},
			},
		},
		'SCRIPTING:SAP.LabelList.Search':{
			'Version':2,
			'Title':'Search a SAP label list for a value',
			'Description':'',
			'Input':{
				'Object.SAP':{'Type':{'Type':'String'}, 'Example':'SAP_EWM', 'Help':'Specifies if a specific SAP connection should be used and not the general one from the isolation key.'},
				'Label.RowStart':{'Type':{'Type':'Integer'}},
				'Label':{'Type':{'Type':'String'}},
				'Label.Column':{'Type':{'Type':'Integer'}},
				'Search.Value':{'Type':{'Type':'String'}},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'TEMP_VALUE', 'Help':'Stores the result in the provided variable, if running is an isolated state, will keep the variable isolated.'},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'TEMP_VALUE', 'Help':'Stores the result in the provided variable, if running is an isolated state, will keep the data in the global variable instead of the isolated one.'},
			},
		},
		'SCRIPTING:SAP.Screen.Capture':{
			'Version':2,
			'Title':'Capture the SAP screen as an image file',
			'Description':'',
			'Input':{
				'Object.SAP':{'Type':{'Type':'String'}, 'Example':'SAP_EWM', 'Help':'Specifies if a specific SAP connection should be used and not the general one from the isolation key.'},
				'Window':{'Type':{'Type':'Integer'}, 'Example':0, 'Help':'Captures the wnd[0] window as an image.'},
				'Windows':{'Type':{'Type':'List'}, 'Example':[0, 1], 'Help':'Captures the wnd[0] and wnd[1] windows as a list of images.'},
				'Windows.All':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'Captues all open windows for the session in a list of images.'},
				'File':{'Type':{'Type':'String'}, 'LengthMin':5, 'LengthMax':512, 'Example':'C:\\TEMP\\ScreenCapture.%Window%.jpg', 'Help':'Specifies the path and filename(s) of where to store the captured images (%Window% will be replaced by the window number).'},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'TEMP_VALUE', 'Help':'Stores the result in the provided variable, if running is an isolated state, will keep the variable isolated.'},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'TEMP_VALUE', 'Help':'Stores the result in the provided variable, if running is an isolated state, will keep the data in the global variable instead of the isolated one.'},
			},
		},
		'OMOIKANEV2:SAP_Process.List':{
			'Version':1,
			'Title':'Transforms OmoikaneV2 SAP_Process steps into OmoikaneFlow steps',
			'Description':'Takes a list of dicts from the OmoikaneV2 SAP_Process and transforms the steps into OmoikaneFlows steps.\nThe returned result will be either a list of steps or a dict of lists depending on if Threading is requested or not.',
			'Input':{
				'OmoikaneV2.URL':{'Type':{'Type':'String', 'LengthMin':8, 'LengthMax':32}, 'Mandatory':'*', 'Example':'dev03.omoikanev2dev', 'Help':'Specifies which Omoikane server that should be used.'},
				'OmoikaneV2.URL.Verify':{'Type':{'Type':'Boolean'}, 'Default':True, 'Example':False, 'Help':'False disables TSL verification.'},
				'Format':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'{%ID%{%TITLE%,%SYSTEM%}}', 'Help':''},
				'Systems':{'Type':{'Type':'Dict'}},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'TEMP_VALUE', 'Help':'Stores the result in the provided variable, if running is an isolated state, will keep the variable isolated.'},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'TEMP_VALUE', 'Help':'Stores the result in the provided variable, if running is an isolated state, will keep the data in the global variable instead of the isolated one.'},
			},
		},
		'OMOIKANEV2:SAP_Process.Transform':{
			'Version':3,
			'Title':'Transforms OmoikaneV2 SAP_Process steps into OmoikaneFlow steps',
			'Description':'Takes a list of dicts from the OmoikaneV2 SAP_Process and transforms the steps into OmoikaneFlows steps.\nThe returned result will be either a list of steps or a dict of lists depending on if Threading is requested or not.',
			'Input':{
				'Data':{'Type':{'Type':'List'}},
				'Threading':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'If True, the return result will be a dict with "MetaSegments" as the key for the list of steps.'},
				'OmoikaneURL':{'Type':{'Type':'String'}, 'LengthMin':10, 'LengthMax':512, 'Example':'https://omoikanev2dev.emea.tdworldwide.com/', 'Help':'Specifies URL to the OmoikaneV2 server to be used.'},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'TEMP_VALUE', 'Help':'Stores the result in the provided variable, if running is an isolated state, will keep the variable isolated.'},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'TEMP_VALUE', 'Help':'Stores the result in the provided variable, if running is an isolated state, will keep the data in the global variable instead of the isolated one.'},
				'Debug.Console':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'If True, displays debug steps in console.'},
				'Steps.Before':{'Type':{'Type':'List'}, 'Steps':True, 'Help':'A list of steps which will be executed before the processing starts.'},
				'Steps.After':{'Type':{'Type':'List'}, 'Steps':True, 'Help':'A list of steps which will be executed after the processing is completed.'},
				'Steps.Before.Segment':{'Type':{'Type':'Dict'}, 'Steps':True, 'Help':'A list of steps which will be executed before the processing starts for the dict key segment.'},
				'Steps.After.Segment':{'Type':{'Type':'Dict'}, 'Steps':True, 'Help':'A list of steps which will be executed after the processing is completed for the dict key segment.'},
			},
		},
		'OMOIKANEV2:LoadToDB.Upload':{
			'Version':1,
			'Title':'Uploads a file to the OmoikaneV2 LoadToDB system',
			'Description':'',
			'Input':{
				'OmoikaneV2.URL':{'Type':{'Type':'String', 'LengthMin':8, 'LengthMax':32}, 'Mandatory':'*', 'Example':'dev03.omoikanev2dev', 'Help':'Specifies which Omoikane server that should be used.'},
				'OmoikaneV2.URL.Verify':{'Type':{'Type':'Boolean'}, 'Default':True, 'Example':False, 'Help':'False disables TSL verification.'},
				'Compression':{'Type':{'Type':'Enum', 'Values':['LZMA']}, 'Example':'LZMA', 'Help':'Controls which compression that should be used when sending the file.'},
#				'URL':{'Type':{'Type':'String'}, 'LengthMin':5, 'LengthMax':512, 'Example':'https://www.google.com/Upload', 'Help':'Specifies URL to where the file should be sent.'},
				'File':{'Type':{'Type':'String'}, 'LengthMin':5, 'LengthMax':512, 'Example':'C:\\TEMP\\MB51', 'Help':'Specifies the path and filename to upload.'},
				'Steps':{'Type':{'Type':'List'}, 'Steps':True, 'Help':'A list of steps which will be executed after the LoadToDB has been completed.'},
			},
		},
		'OMOIKANEV2:DatabaseQuery':{
			'Version':3,
			'Title':'Executes a DB query against OmoikaneV2',
			'Description':'',
			'Input':{
				'Query':{'Type':{'Type':'String', 'LengthMin':6, 'LengthMax':64000}, 'Mandatory':'*', 'Example':'SELECT COUNT(*) FROM `Temp`', 'Help':'Executes the provided query.'},
				'OmoikaneV2.URL':{'Type':{'Type':'String', 'LengthMin':8, 'LengthMax':32}, 'Mandatory':'*', 'Example':'dev03.omoikanev2dev', 'Help':'Specifies which Omoikane server that should be used.'},
				'OmoikaneV2.URL.Verify':{'Type':{'Type':'Boolean'}, 'Default':True, 'Example':False, 'Help':'False disables TSL verification.'},
				'SQLite.Table':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':32}, 'Example':'DumpTable', 'Help':'If specified, creates the SQLite table and inserts the records into it.'},
				'Return.1D':{'Type':{'Type':'Dict'}, 'Example':{'SWE':{'UpdateGUI.Value':'Entry##ENT_OTS_SWE'}, 'DEN':{'ReturnVariable':'OmoikaneV2:DEN', 'UpdateGUI.Value':'Entry##DEN'}}, 'Help':"""A dict with the 1D keys from the returned result (only works for 1D returns):
* ReturnVariable - Stores the result in the variable provided
* ReturnVariable.Global - Stores the result in the global variable provided
* UpdateGUI.Value - Stores the result in the GUI object provided
* UpdateGUI.Value.Trigger - Used in combination with UpdateGUI.Value, True triggers the OnChange logic if available for the GUI object"""},
				'ReturnVariable.Data':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'Result.Data', 'Help':'Stores the data in the "Result.Data" variable.'},
				'ReturnVariable.Data.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'Result.Data', 'Help':'Stores the data in the "Result.Data" global variable.'},
				'ReturnVariable.Headers':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'Result.Header', 'Help':'Stores the headers as a list in the "Result.Header" variable.'},
				'ReturnVariable.Headers.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'Result.Header', 'Help':'Stores the headers as a list in the "Result.Header" global variable.'},
				'ReturnVariable.1D':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'Stores the column results into variables with the same name as the columns if the query generates one row.'},
				'ReturnVariable.1D.Global':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'Stores the column results into global variables with the same name as the columns if the query generates one row.'},
			},
		},
		'OMOIKANEV2:TimeCapture.Upload':{
			'Version':4,
			'Title':'Uploads a TimeCapture file to OmoikaneV2',
			'Description':'',
			'Input':{
				'File':{'Type':{'Type':'String', 'LengthMin':6, 'LengthMax':64000}, 'Mandatory':'*', 'Example':'SELECT COUNT(*) FROM `Temp`', 'Help':'Executes the provided query.'},
				'OmoikaneV2.URL':{'Type':{'Type':'String', 'LengthMin':8, 'LengthMax':32}, 'Mandatory':'*', 'Example':'dev03.omoikanev2dev', 'Help':'Specifies which Omoikane server that should be used.'},
				'OmoikaneV2.URL.Verify':{'Type':{'Type':'Boolean'}, 'Default':True, 'Example':False, 'Help':'False disables TSL verification.'},
				'OmoikaneV2.Debug':{},
				'OmoikaneV2.JSON':{},
				'Template':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':32}, 'Example':'DumpTable', 'Help':'The TimeCapture template to use for the upload.'},
				'ReturnVariable':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'TEMP_VALUE', 'Help':'Stores the result in the provided variable, if running is an isolated state, will keep the variable isolated.'},
				'ReturnVariable.Global':{'Type':{'Type':'String', 'LengthMin':1, 'LengthMax':128}, 'Example':'TEMP_VALUE', 'Help':'Stores the result in the provided variable, if running is an isolated state, will keep the data in the global variable instead of the isolated one.'},
			},
		},
		'OMOIKANE:Flow':{
			'Version':1,
			'Title':'Executes a steps list from the Omoikane server',
			'Input':{
				'FlowID':{'Type':{'Type':'Integer', 'Min':1, 'Max':65535}, 'Mandatory':'FLOWID', 'Example':1, 'Help':'Which FlowID to download and execute.'},
				'Auth':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'If True, tries to send the SSO auth with the request.'},
				'Redirects':{'Type':{'Type':'Boolean'}, 'Default':True, 'Example':False, 'Help':'False disables redirects.'},
				'Verify':{'Type':{'Type':'Boolean'}, 'Default':True, 'Example':False, 'Help':'False disables TSL verification.'},
				'Verify.DisableWarnings':{'Type':{'Type':'Boolean'}, 'Default':True, 'Example':False, 'Help':'If True, disables the warnings from a false verify.'},
				'Verify.Certifi':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'True uses the certifi.where() logic for TLS verification.'},
				'Proxies':{'Type':{'Type':'Dict'}, 'Default':None, 'Help':'A dict of proxies to send though the requests class.'},
				'Debug.Console':{'Type':{'Type':'Boolean'}, 'Example':True, 'Help':'If True, displays debug steps in console.'},
			},
		},
		'OMOIKANE:Dakimakura.Products.New':{
			'Version':3,
			'Local':True,
			'Dakimakura':True,
			'Title':'Returns a list of products which are new',
			'Description':'',
			'Input':{
				'Products':{'Type':{'Type':'Dict'}, 'Mandatory':'*', 'Example':{'https://URL1':'Title 1', 'https://URL2':'Title 2'}, 'Help':'A dict of product pages and titles.'},
				'Products.AddToDB':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'True means the new entries will be added to the DB.'},
			},
		},
		'OMOIKANE:Dakimakura.Product.Images':{
			'Version':1,
			'Local':True,
			'Dakimakura':True,
			'Title':'Add the missing entries to the database',
			'Description':'',
			'Input':{
				'PageID':{},
				'ProductImages':{'Type':{'Type':'List'}, 'Mandatory':'*', 'Example':['https://URL1.jpg', 'https://URL2.png'], 'Help':'A list of product images.'},
			},
		},
		'OMOIKANE:Dakimakura.Download.Requests':{
			'Version':3,
			'Local':True,
			'Dakimakura':True,
			'Title':'Returns a list pages which needs to be downloaded',
			'Description':'',
			'Input':{
				'Download':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'True means the entries will be downloaded and uploaded to the Omoikane server.'},
				'Download.TempFile':{'Type':{'Type':'String', 'LengthMin':6, 'LengthMax':64000}, 'Example':'C:\\Temp\\Temp.tmp', 'Help':'Temp file to be used by Powershell download.'},
			},
		},
		'OMOIKANE:MovieArchive.Source':{
			'Version':1,
			'Local':False,
			'Dakimakura':False,
			'Title':'Returns an IMDB source page',
			'Description':'',
			'Input':{
				'IMDB':{'Type':{'Type':'String', 'LengthMin':8, 'LengthMax':9}, 'Example':'tt0468569', 'Help':'The IMDB ID for the movie.'},
				'Page':{'Type':{'Type':'Enum', 'Values':['Cast', 'Keywords', 'Main', 'ParentalGuide', 'PosterSmall', 'Quotes', 'Ratings', 'Releaseinfo', 'Taglines']}, 'Example':'Main', 'Help':"""Specifies which type of page to return:
* Cast
* Connections
* Keywords
* Main
* ParentalGuide
* PosterSmall
* Quotes
* Ratings
* Releaseinfo
* Taglines"""},
				'Updated':{'Type':{'Type':'Boolean'}, 'Default':False, 'Example':True, 'Help':'True means the updated version will be fetched instead of the common one.'},
			},
		},
	}
	default_steps = [
		{"Function":"GUI:Form", "Geometry":"400x400", "Title":"Default form"}
	]
	core_diff_steps = [
	]
	
	def __init__ (self) -> None:
		self.fernet_key = ''
		self.tds_fernet_key = ''
	
	
	