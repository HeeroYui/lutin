#!/usr/bin/python
# -*- coding: utf-8 -*-
##
## @author Edouard DUPIN
##
## @copyright 2012, Edouard DUPIN, all right reserved
##
## @license APACHE v2.0 (see license file)
##

from lutin import debug
from lutin import system
from lutin import tools
from lutin import env
import os

class System(system.System):
	def __init__(self, target):
		system.System.__init__(self)
		# create some HELP:
		self.help="uuid: Unique ID library"
		# check if the library exist:
		if     not os.path.isfile("/usr/include/uuid/uuid.h"):
			# we did not find the library reqiested (just return) (automaticly set at false)
			return;
		self.valid = True
		self.add_module_depend([
		    'c'
		    ])
		# todo : create a searcher of the presence of the library:
		self.add_export_flag("link-lib", "uuid")
		if env.get_isolate_system() == False:
			self.add_header_file([
			    "/usr/include/uuid/*",
			    ],
			    destination_path="uuid",
			    recursive=True)


