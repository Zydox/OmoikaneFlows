# Copyright (c) 2025-2026 Erik Persson
# Licensed for free use only. Copying, modification, or redistribution prohibited.

from cryptography.fernet import Fernet
from Functions.Common import *
from Functions.DataHandling import *
from logging import exception, error
import builtins
import bz2
import calendar
import certifi
import copy
import csv
import customtkinter
import datetime
import filecmp
import hashlib
import io
import json
import math
import multiprocessing
import numpy
import openpyxl
import openpyxl.styles
import os
import pandas
import pathlib
import PIL
import PIL.Image
import platform
import pythoncom
import pywintypes
import qrcode
import queue
import re
import reportlab
import reportlab.lib
import reportlab.platypus
import requests
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import tk
import tkinter
import tksheet
import treepoem
import urllib3
import win32com.client
import xlrd
import Classes.Flows
import WinClasses.Steps
import WinClasses.Web

# print (sys.argv)

class OmoikaneFlows:
	class_mapping = {
		'GUI':'GUI',
		'DATA':'Data',
		'LOGIC':'Logic',
		'IO':'IO',
		'SQL':'SQL',
		'CORE':'Core',
		'WEB':'Web',
		'PDF':'PDF',
		'IMAGE':'Image',
		'EXCEL':'Excel',
		'PANDAS':'Pandas',
		'OMOIKANE':'Omoikane',
		'OMOIKANEV2':'OmoikaneV2',
		'OMOIKANEV3':'OmoikaneV3',
		'SCRIPTING':'Scripting',
	}
	def __init__ (self):
		self.version = '%Core%.%Functions%.%Versions% (%InternalFunctions%.%InternalVersions%)'
		self.cls_flows = Classes.Flows.Flows ()
		self.cls_web = WinClasses.Web.Web (None)
		self.cls_steps = WinClasses.Steps.Steps ()
		if len (self.cls_flows.fernet_key) > 0:
			self.fernet = Fernet (self.cls_flows.fernet_key)
		self.init_generations ()
	
	
	def init_generations (self):
		self.userinfo = {
			'User':os.getlogin (),
			'IP':self.cls_steps.internal_local_ip (),
			'Hostname':platform.node (),
			'Domain':os.environ.get ('USERDOMAIN'),
			'Python':str (sys.version_info[0]) + '.' + str (sys.version_info[1]) + '.' + str (sys.version_info[2]),
		}
		versions = 0
		functions = 0
		for func in self.cls_flows.functions.values ():
			if 'Version' in func and isinstance (func['Version'], int):
				versions += func['Version']
				functions += 1
		self.version = self.version.replace ('%Core%', str (self.cls_flows.version_core)).replace ('%Versions%', str (versions)).replace ('%Functions%', str (functions)).replace ('%InternalFunctions%', str (len (self.cls_flows.versions))).replace ('%InternalVersions%', str (sum (self.cls_flows.versions.values ())))
		self.cls_steps.version = copy.deepcopy (self.version)
		self.cls_steps.userinfo = copy.deepcopy (self.userinfo)
	
opts = {
	'Online':True,
}
start = True
if len (sys.argv) > 1:
	for argv in sys.argv[1:]:
		if argv.startswith ('--StepsFile='):
			opts['StepsFile'] = argv[argv.find ('=') + 1:]
		elif argv == '--Offline':
			opts['Online'] = False
		elif argv.startswith ('--WindowsPos='):
			opts['WindowsPos'] = argv[argv.find ('=') + 1:]
		elif argv.startswith ('--Scripting='):
			opts['Scripting'] = argv[argv.find ('=') + 1:]
		elif argv.startswith ('--External='):
			opts['External'] = argv[argv.find ('=') + 1:]
		elif argv.startswith ('--OmoikaneV2='):
			opts['OmoikaneV2'] = argv[argv.find ('=') + 1:]
		elif argv.startswith ('--OmoikaneV3='):
			opts['OmoikaneV3'] = argv[argv.find ('=') + 1:]
		elif argv.startswith ('--Debug.File='):
			opts['Debug.File'] = argv[argv.find ('=') + 1:]
			if '--Debug.File.Instant' in sys.argv:
				opts['Debug.File.Instant'] = True
		elif argv.startswith ('--Debug.File.Reset'):
			opts['Debug.File.Reset'] = True
		elif argv == '--Version':
			opts['Online'] = False
			opts['Version'] = True
		elif argv == '--License':
			opts['Online'] = False
			opts['License'] = True
		elif argv.startswith ('--FernetKey='):
			opts['FernetKey'] = argv[argv.find ('=') + 1:]
		
		
		elif argv.startswith ('--Help'):
			start = False
			print ('OmoikaneWin cmd arguments:')
			print ('--StepsFile=<FILE>     Accepts a JSON formatted file with steps to execute')
			print ('--WindowsPos=<X+Y>     X+Y GUI start position, example value would be 2800+150')
			print ('--Scripting=<FILE>     Dynamically loaded scripting file')
			print ('--Debug.File=<FILE>    Writes debug into a file (must contain OmoikaneFlows in the name)')
			print ('--Debug.File.Reset     Empties the debug file')
			print ('--Debug.File.Instant   Writes the debug file as soon as a log entry comes')
			print ('--Offline              Doesn\'t try to load the code updates from the online server')
			print ('--Version              Displays the current version')
			print ('--License              Displays the license')
			print ('--Help                 Displays this help')
			print ('--FernetKey=<KEY>      Specifies which Fernet key to use')


cls_of = OmoikaneFlows ()
if 'Online' in opts and opts['Online'] is True:
	pass
if start is True:
	cls_of.cls_steps.start (**opts)
