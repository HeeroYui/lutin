#!/usr/bin/python
##
## @author Edouard DUPIN
##
## @copyright 2012, Edouard DUPIN, all right reserved
##
## @license APACHE v2.0 (see license file)
##

import sys
import copy
import lutinDebug as debug


def append_to_list(listout, list):
	if type(list) == type(str()):
		if list not in listout:
			listout.append(list)
	else:
		# mulyiple imput in the list ...
		for elem in list:
			if elem not in listout:
				listout.append(elem)



class HeritageList:
	def __init__(self, heritage = None):
		self.flags={}
		# sources list:
		self.src=[]
		self.path=[]
		
		self.listHeritage=[]
		if heritage != None:
			self.add_heritage(heritage)
	
	def add_heritage(self, heritage):
		if    type(heritage) == type(None) \
		   or heritage.name == "":
			return
		for element in self.listHeritage:
			if element.name == heritage.name:
				return
		self.listHeritage.append(heritage)
		self.regenerateTree()
		
	def add_heritage_list(self, heritage_list):
		if type(heritage_list) == type(None):
			return
		for herit in heritage_list.listHeritage:
			find = False
			for element in self.listHeritage:
				if element.name == herit.name:
					find = True
			if find == False:
				self.listHeritage.append(herit)
		self.regenerateTree()
	
	def regenerateTree(self):
		self.flags={}
		# sources list:
		self.src=[]
		self.path=[]
		# reorder heritage list :
		listHeritage = self.listHeritage
		self.listHeritage = []
		# first step : add all lib with no dependency:
		for herit in listHeritage:
			if len(herit.depends) == 0:
				self.listHeritage.append(herit)
				listHeritage.remove(herit)
		while len(listHeritage) > 0:
			currentHeritageSize = len(listHeritage)
			debug.verbose("list heritage = " + str([[x.name, x.depends] for x in listHeritage]))
			# Add element only when all dependence are resolved
			for herit in listHeritage:
				listDependsName = [y.name for y in self.listHeritage]
				if all(x in listDependsName for x in herit.depends) == True:
					listHeritage.remove(herit)
					self.listHeritage.append(herit)
			if currentHeritageSize == len(listHeritage):
				debug.warning("Not resolve dependency between the library ==> can be a cyclic dependency !!!")
				for herit in listHeritage:
					self.listHeritage.append(herit)
				listHeritage = []
				debug.warning("new heritage list:")
				for element in self.listHeritage:
					debug.warning("	" + element.name + " " + str(element.depends))
		debug.verbose("new heritage list:")
		for element in self.listHeritage:
			debug.verbose("	" + element.name + " " + str(element.depends))
		for element in reversed(self.listHeritage):
			debug.debug("elem : " + str(element.flags))
			for flags in element.flags:
				value = element.flags[flags]
				debug.debug("    elem : " + str(flags))
				if flags not in self.flags:
					self.flags[flags] = value
				else:
					append_to_list(self.flags[flags], value)
			append_to_list(self.path, element.path)
			append_to_list(self.src, element.src)
			"""
			if self.flags_xx_version < element.flags_xx_version:
				self.flags_xx_version = element.flags_xx_version
			if self.flags_cc_version < element.flags_cc_version:
				self.flags_cc_version = element.flags_cc_version
			"""


class heritage:
	def __init__(self, module):
		self.name=""
		self.depends=[]
		## Remove all variable to prevent error of multiple definition
		# all the parameter that the upper classe need when build
		self.flags={}
		# sources list:
		self.src=[]
		self.path=[]
		# update is set at true when data are newly created ==> force upper element to update
		self.hasBeenUpdated=False
		
		if type(module) != type(None):
			# all the parameter that the upper classe need when build
			self.name = module.name
			self.depends = copy.deepcopy(module.depends)
			self.flags = module.flags["export"]
			self.path = module.path["export"]
			if "c++-version" in self.flags:
				self.flags["c++-version"] = self.flags["c++-version"]["api-version"]
			if "c-version" in self.flags:
				self.flags["c-version"] = self.flags["c-version"]["api-version"]
			
	
	def add_depends(self, depend):
		self.depends.append(depend)
	
	def add_import_path(self, list):
		append_to_list(self.path, list)
	
	def add_sources(self, list):
		append_to_list(self.src, list)
	
	def need_update(self, list):
		self.hasBeenUpdated=True
	
	def add_sub(self, other):
		if type(other) == type(None):
			debug.verbose("input of the heriatege class is None !!!")
			return
		if other.hasBeenUpdated == True:
			self.hasBeenUpdated = True
		for flags in other.flags:
			value = other.flags[flags]
			if flags not in self.flags:
				self.flags[flags] = value
			else:
				append_to_list(self.flags[flags], value)
		self.add_import_path(other.path)
		self.add_sources(other.src)
		"""
		if self.flags_xx_version < module.xx_version_api:
			self.flags_xx_version = module.xx_version_api
		if self.flags_cc_version < module.cc_version_api:
			self.flags_cc_version = module.cc_version_api
		"""


