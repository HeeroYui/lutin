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
import os

class System(system.System):
	def __init__(self, target):
		system.System.__init__(self)
		# create some HELP:
		self.help="pthread : Generic multithreading system\n Can be install with the package:\n    - pthread-dev"
		# check if the library exist:
		if     not os.path.isfile("/usr/include/pthread.h"):
			# we did not find the library reqiested (just return) (automaticly set at false)
			return;
		self.valid = True
		# todo : create a searcher of the presence of the library:
		self.add_export_flag("link-lib", "pthread")
		self.add_header_file([
		    "/usr/include/sched.h",
		    "/usr/include/pthread.h"
		    ],
		    clip_path="/usr/include/")


