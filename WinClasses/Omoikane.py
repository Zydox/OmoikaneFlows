# Copyright (c) 2025-2026 Erik Persson
# Licensed for free use only. Copying, modification, or redistribution prohibited.

# -*- coding: utf-8 -*-
import builtins
from Functions.Common import *
from Functions.DataHandling import *
for name in dir ():
	if not name.startswith ("_"):
		builtins.__dict__[name] = globals ()[name]
import io
builtins.io = io

class Omoikane:
	def __init__ (self, cls_steps = None):
		self.cls_steps = cls_steps
	
	
	def dynamic_function (self, function, to_class = True):
		if to_class is True:
			func = {}
			exec (function['Code'], func)
			setattr (Omoikane, function['Function'], func[function['Function']])
		else:
			exec (function['Code'], globals ())
			builtins.__dict__[function['Function']] = globals ()[function['Function']]
	
	
	def execute (self, running_steps, isolation = None, **opts):
		try:
			if opts['Function'] == 'OMOIKANE:Dakimakura.Products.New':
				return self.step_dakimakura_products_new (isolation, **opts)
			elif opts['Function'] == 'OMOIKANE:Dakimakura.Download.Requests':
				return self.step_dakimakura_download_requests (isolation, **opts)
			elif opts['Function'] == 'OMOIKANE:Dakimakura.Product.Images':
				return self.step_dakimakura_product_images (isolation, **opts)
			elif opts['Function'] == 'OMOIKANE:MovieArchive.Source':
				return self.step_moviearchive_source (isolation, **opts)
			elif opts['Function'] == 'OMOIKANE:Flow':
				return self.step_flow (isolation, **opts)
			return False, {'Status':'WARNING', 'Title':'OMOIKANE:execute: Aborted', 'Message':'Unknown step=' + str (opts)}
		except Exception as e:
			st = internal_zyd_stacktrace (e, FunctionOpts=opts)
			return False, {'Status':'CRASH', 'Title':'OMOIKANE:execute: Crashed', 'Message':'Crashed with the error: ' + str (e) + ' for step:\n' + str (opts), 'StackTrace':st}
	
	
	def step_flow (self, isolation, **opts):
		if 'FlowID' not in opts or not isinstance (opts['FlowID'], int):
			return False, {'Status':'WARNING', 'Title':'OMOIKANE:step_flow: Aborted', 'Message':'No valid FlowID was provided.'}

		debug_console = (True if 'Debug.Console' in opts and opts['Debug.Console'] is True else False)
		url_opts = {
			'URL':'https://www.omoikane.se/APIs/Flows?ID=' + str (opts['FlowID']),
			'Method':'GET',
			'JSON':True,
		}
		for opt in ['Auth', 'Redirects', 'Verify', 'Verify.DisableWarnings', 'Verify.Certifi', 'Proxies']:
			if opt in opts:
				url_opts[opt] = opts[opt]
		
		if debug_console is True:
			print ('+==[ step_flow ]=============================================================')
			print ('URL_opts=' + str (url_opts))
		
		status, result = self.step_url (isolation, **url_opts)
		if debug_console is True:
			print ('URL_status=' + str (status))
			print ('URL_result=' + str (result))
		
		if status is True and 'Status' in result and result['Status'] == 'OK' and 'Data' in result and isinstance (result['Data'], dict) and 'Status' in result['Data'] and result['Data']['Status'] == 'OK' and 'Steps' in result['Data'] and isinstance (result['Data']['Steps'], list):
			status, result = self.cls_steps.execute_steps (result['Data']['Steps'], isolation)
			if debug_console is True:
				print ('Steps_status=' + str (status))
				print ('Steps_result=' + str (result))

		if debug_console is True:
			print ('-============================================================================')
		
		return True, {'Status':'OK'}

	
	
	def step_dakimakura_products_new (self, isolation, **opts):
		if 'Products' not in opts or not isinstance (opts['Products'], dict):
			return False, {'Status':'WARNING', 'Title':'OMOIKANE:step_dakimakura_products_new: Aborted', 'Message':'No Products dict provided.'}
		
		json = {'Products':opts['Products']}
		if 'Products.AddToDB' in opts and opts['Products.AddToDB'] is True:
			json['AddToDB'] = True
		result = self.cls_steps.cls_web.internal_web ('https://www.omoikane.se/', **{'Method':'POST', 'Data.JSON':json, 'JSON':True})
		if isinstance (result, dict) and 'Status' in result and result['Status'] == 'OK' and 'Data' in result:
			print ('OMOIKANE:step_dakimakura_products_new::OK::' + str (result['Data']))
		
		return True, {'Status':'OK'}
	
	
	def step_dakimakura_download_requests (self, isolation, **opts):
		result = self.cls_steps.cls_web.internal_web ('https://www.omoikane.se/', **{'Method':'GET', 'JSON':True})
		uploads = 0
		if isinstance (result, dict) and 'Status' in result and result['Status'] == 'OK' and 'Data' in result and isinstance (result['Data'], list) and len (result['Data']) > 0:
			if 'Download' in opts and opts['Download'] is True and 'Download.TempFile' in opts:
				for entry in result['Data']:
#					print ('\n\tDOWNLOAD=' + str (entry))
					result_download = self.cls_steps.cls_web.internal_web (entry[2], **{'Method':'Windows.Powershell', 'Powershell.Binary':True, 'Powershell.TempFile':opts['Download.TempFile']})
					if isinstance (result_download, bytes):
						result_upload = self.cls_steps.cls_web.internal_web ('https://www.omoikane.se/', **{'JSON':True, 'Files':{
								'File':('Page.html', io.BytesIO (result_download), 'text/html'),
								'Post.JSON':('', io.BytesIO (zyd_json ({'Type':entry[0], 'ID':entry[1]}, Internal=True, Encode=True).encode ('utf-8')), 'application/json'),
							}})
#						print ('\n\tUPLOAD::' + str (result_upload))
						if isinstance (result_upload, dict) and 'Status' in result_upload and result_upload['Status'] == 'OK':
							uploads += 1
						else:
							return False, {'Status':'ERROR', 'Title':'OMOIKANE:step_dakimakura_download_requests: Aborted', 'Message':'Upload failed with the following error:\n' + str (result_upload)}
					else:
						return False, {'Status':'ERROR', 'Title':'OMOIKANE:step_dakimakura_download_requests: Aborted', 'Message':'Download failed with the following error:\n' + str (result_download)}
		
		return True, {'Status':'OK', 'Uploads':uploads, 'Data':result['Data']}
	
	
	def step_dakimakura_product_images (self, isolation, **opts):
		if 'PageID' not in opts or not isinstance (opts['PageID'], int):
			return False, {'Status':'WARNING', 'Title':'OMOIKANE:step_dakimakura_product_images: Aborted', 'Message':'No PageID integer provided.'}
		if 'ProductImages' not in opts or not isinstance (opts['ProductImages'], list):
			return False, {'Status':'WARNING', 'Title':'OMOIKANE:step_dakimakura_product_images: Aborted', 'Message':'No ProductImages list provided.'}
		if len (opts['ProductImages']) > 0:
			result = self.cls_steps.cls_web.internal_web ('https://www.omoikane.se/', **{'Method':'GET', 'Data.JSON':{'ID':opts['PageID'], 'URLs':opts['ProductImages']}, 'JSON':True})
			print (result)
			
		return True, {'Status':'OK', 'Data':None}
	
	
	def step_moviearchive_source (self, isolation, **opts):
		page_opts = {
			'IMDB':opts['IMDB'],
			'Page':opts['Page'],
			'Updated':(True if 'Updated' in opts and opts['Updated'] is True else False),
		}
		result = self.cls_steps.cls_web.internal_web ('https://www.omoikane.se/APIs/MovieArchive/DownloadSource' + ('?TDS=1' if self.cls_steps.tds is True else ''), **{'Method':'GET', 'Encrypt':True, 'Decrypt':True, 'Content':True, 'Data.JSON':page_opts})
		if 'ReturnVariable' in opts and isinstance (opts['ReturnVariable'], str):
			self.cls_steps.internal_value_set_value (isolation, 'Variable', result, opts['ReturnVariable'])
		if 'ReturnVariable.Global' in opts and isinstance (opts['ReturnVariable.Global'], str):
			self.cls_steps.internal_value_set_value (None, 'Variable', result, opts['ReturnVariable.Global'])
		
		return True, {'Status':'OK'}
