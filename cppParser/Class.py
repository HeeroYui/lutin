#!/usr/bin/python
try :
	# normal install module
	import ply.lex as lex
except ImportError :
	# local module
	import lex
import os
import sys
import re
import Node
import lutinDebug as debug

import inspect

class Class(Node.Node):
	def __init__(self):
		
		# List of the class name (with their namespace : [['ewol','widget','plop'], ...])
		self.parents = []
		
		# CPP section:
		self.namespaces = []
		self.classes = []
		# C section:
		self.structs = []
		self.variables = []
		self.methodes = []
		self.unions = []
		self.types = []
		
	
	
	def to_str(self):
		return ""



