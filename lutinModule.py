#!/usr/bin/python
import sys
import os
import inspect
import fnmatch
import lutinModule as module
import lutinHost as host
import lutinTools
import lutinDebug as debug
import lutinHeritage as heritage
import lutinDepend as dependency
import lutinMultiprocess
import lutinEnv

class Module:
	
	##
	## @brief Module class represent all system needed for a specific
	## 	module like 
	## 		- type (bin/lib ...)
	## 		- dependency
	## 		- flags
	## 		- files
	## 		- ...
	##
	def __init__(self, file, moduleName, moduleType):
		## Remove all variable to prevent error of multiple deffinition of the module ...
		self.originFile=''
		self.originFolder=''
		# type of the module:
		self.type='LIBRARY'
		# Name of the module
		self.name=moduleName
		# Dependency list:
		self.depends=[]
		# Documentation list:
		self.documentation = None
		# export PATH
		self.export_path=[]
		self.local_path=[]
		self.export_flags_ld=[]
		self.export_flags_cc=[]
		self.export_flags_xx=[]
		self.export_flags_m=[]
		self.export_flags_mm=[]
		# list of all flags:
		self.flags_ld=[]
		self.flags_cc=[]
		self.flags_xx=[]
		self.flags_m=[]
		self.flags_mm=[]
		self.flags_s=[]
		self.flags_ar=[]
		# sources list:
		self.src=[]
		# copy files and folders:
		self.files=[]
		self.folders=[]
		self.isbuild=False
		## end of basic INIT ...
		if    moduleType == 'BINARY' \
		   or moduleType == 'LIBRARY' \
		   or moduleType == 'PACKAGE' \
		   or moduleType == 'PREBUILD':
			self.type=moduleType
		else :
			debug.error('for module "%s"' %moduleName)
			debug.error('    ==> error : "%s" ' %moduleType)
			raise 'Input value error'
		self.originFile = file;
		self.originFolder = lutinTools.get_current_path(self.originFile)
		self.localHeritage = heritage.heritage(self)
		
		self.packageProp = { "COMPAGNY_TYPE" : set(""),
		                     "COMPAGNY_NAME" : set(""),
		                     "COMPAGNY_NAME2" : set(""),
		                     "MAINTAINER" : set([]),
		                     "ICON" : set(""),
		                     "SECTION" : set([]),
		                     "PRIORITY" : set(""),
		                     "DESCRIPTION" : set(""),
		                     "VERSION" : set("0.0.0"),
		                     "NAME" : set("no-name"), # name of the application
		                     "ANDROID_MANIFEST" : "", # By default generate the manifest
		                     "ANDROID_JAVA_FILES" : ["DEFAULT"], # when user want to create his own services and activities
		                     "ANDROID_RESOURCES" : [],
		                     "ANDROID_APPL_TYPE" : "APPL", # the other mode is "WALLPAPER" ... and later "WIDGET"
		                     "ANDROID_WALLPAPER_PROPERTIES" : [], # To create properties of the wallpaper (no use of EWOL display)
		                     "RIGHT" : []
		                    }
		
	
	##
	## @brief add Some copilation flags for this module (and only this one)
	##
	def add_extra_compile_flags(self):
		self.compile_flags_CC([
			"-Wall",
			"-Wsign-compare",
			"-Wreturn-type",
			"-Wint-to-pointer-cast",
			"-Wno-write-strings"]);
		#only for gcc : "-Wunused-variable", "-Wunused-but-set-variable",
	
	##
	## @brief remove all unneeded warning on compilation ==> for extern libs ...
	##
	def remove_compile_warning(self):
		self.compile_flags_CC([
			"-Wno-int-to-pointer-cast"
			]);
		self.compile_flags_XX([
			"-Wno-c++11-narrowing"
			])
		# only for gcc :"-Wno-unused-but-set-variable"
	
	##
	## @brief Commands for running gcc to compile a m++ file.
	##
	def compile_mm_to_o(self, file, binary, target, depancy):
		file_src, file_dst, file_depend, file_cmd = target.file_generate_object(binary,self.name,self.originFolder,file)
		# create the command line befor requesting start:
		cmdLine=lutinTools.list_to_str([
			target.xx,
			"-o", file_dst ,
			target.global_include_cc,
			lutinTools.add_prefix("-I",self.export_path),
			lutinTools.add_prefix("-I",self.local_path),
			lutinTools.add_prefix("-I",depancy.path),
			target.global_flags_cc,
			target.global_flags_mm,
			depancy.flags_cc,
			depancy.flags_mm,
			self.flags_mm,
			self.flags_cc,
			self.export_flags_mm,
			self.export_flags_cc,
			"-c -MMD -MP -g",
			"-x objective-c++",
			file_src])
		# check the dependency for this file :
		if False==dependency.need_re_build(file_dst, file_src, file_depend, file_cmd, cmdLine):
			return file_dst
		lutinTools.create_directory_of_file(file_dst)
		comment = ["m++", self.name, "<==", file]
		#process element
		lutinMultiprocess.run_in_pool(cmdLine, comment, file_cmd)
		return file_dst
	
	##
	## @brief Commands for running gcc to compile a m file.
	##
	def compile_m_to_o(self, file, binary, target, depancy):
		file_src, file_dst, file_depend, file_cmd = target.file_generate_object(binary,self.name,self.originFolder,file)
		# create the command line befor requesting start:
		cmdLine=lutinTools.list_to_str([
			target.cc,
			"-o", file_dst ,
			target.global_include_cc,
			lutinTools.add_prefix("-I",self.export_path),
			lutinTools.add_prefix("-I",self.local_path),
			lutinTools.add_prefix("-I",depancy.path),
			target.global_flags_cc,
			target.global_flags_m,
			depancy.flags_cc,
			depancy.flags_m,
			self.flags_m,
			self.flags_cc,
			self.export_flags_m,
			self.export_flags_cc,
			"-c -MMD -MP -g",
			"-x objective-c",
			file_src])
		# check the dependency for this file :
		if False==dependency.need_re_build(file_dst, file_src, file_depend, file_cmd, cmdLine):
			return file_dst
		lutinTools.create_directory_of_file(file_dst)
		comment = ["m", self.name, "<==", file]
		#process element
		lutinMultiprocess.run_in_pool(cmdLine, comment, file_cmd)
		return file_dst
	
	##
	## @brief Commands for running gcc to compile a C++ file.
	##
	def compile_xx_to_o(self, file, binary, target, depancy):
		file_src, file_dst, file_depend, file_cmd = target.file_generate_object(binary,self.name,self.originFolder,file)
		# create the command line befor requesting start:
		cmdLine=lutinTools.list_to_str([
			target.xx,
			"-o", file_dst ,
			target.global_include_cc,
			lutinTools.add_prefix("-I",self.export_path),
			lutinTools.add_prefix("-I",self.local_path),
			lutinTools.add_prefix("-I",depancy.path),
			target.global_flags_cc,
			target.global_flags_xx,
			depancy.flags_cc,
			depancy.flags_xx,
			self.flags_xx,
			self.flags_cc,
			self.export_flags_xx,
			self.export_flags_cc,
			" -c -MMD -MP -g ",
			file_src])
		# check the dependency for this file :
		if False==dependency.need_re_build(file_dst, file_src, file_depend, file_cmd, cmdLine):
			return file_dst
		lutinTools.create_directory_of_file(file_dst)
		comment = ["c++", self.name, "<==", file]
		#process element
		lutinMultiprocess.run_in_pool(cmdLine, comment, file_cmd)
		return file_dst
	
	##
	## @brief Commands for running gcc to compile a C file.
	##
	def compile_cc_to_o(self, file, binary, target, depancy):
		file_src, file_dst, file_depend, file_cmd = target.file_generate_object(binary,self.name,self.originFolder,file)
		# create the command line befor requesting start:
		cmdLine=lutinTools.list_to_str([
			target.cc,
			"-o", file_dst,
			target.global_include_cc,
			lutinTools.add_prefix("-I",self.export_path),
			lutinTools.add_prefix("-I",self.local_path),
			lutinTools.add_prefix("-I",depancy.path),
			target.global_flags_cc,
			depancy.flags_cc,
			self.flags_cc,
			self.export_flags_cc,
			" -c -MMD -MP -g ",
			file_src])
		
		# check the dependency for this file :
		if False==dependency.need_re_build(file_dst, file_src, file_depend, file_cmd, cmdLine):
			return file_dst
		lutinTools.create_directory_of_file(file_dst)
		comment = ["c", self.name, "<==", file]
		# process element
		lutinMultiprocess.run_in_pool(cmdLine, comment, file_cmd)
		return file_dst
	
	
	##
	## @brief Commands for running ar.
	##
	def link_to_a(self, file, binary, target, depancy):
		file_src, file_dst, file_depend, file_cmd = target.generate_file(binary, self.name,self.originFolder,file,"lib-static")
		#$(Q)$(TARGET_AR) $(TARGET_GLOBAL_ARFLAGS) $(PRIVATE_ARFLAGS) $@ $(PRIVATE_ALL_OBJECTS)
		cmdLine=lutinTools.list_to_str([
			target.ar,
			target.global_flags_ar,
			self.flags_ar,
			file_dst,
			file_src])#,
			#depancy.src])
		
		# check the dependency for this file :
		if False==dependency.need_re_package(file_dst, file_src, True, file_cmd, cmdLine) \
				and False==dependency.need_re_package(file_dst, depancy.src, False, file_cmd, cmdLine):
			return file_dst
		lutinTools.create_directory_of_file(file_dst)
		debug.print_element("StaticLib", self.name, "==>", file_dst)
		# explicitly remove the destination to prevent error ...
		if os.path.exists(file_dst) and os.path.isfile(file_dst):
			os.remove(file_dst)
		lutinMultiprocess.run_command(cmdLine)
		#$(Q)$(TARGET_RANLIB) $@
		cmdLineRanLib=lutinTools.list_to_str([
			target.ranlib,
			file_dst ])
		lutinMultiprocess.run_command(cmdLineRanLib)
		# write cmd line only after to prevent errors ...
		lutinMultiprocess.store_command(cmdLine, file_cmd)
		return file_dst
	
	
	##
	## @brief Commands for running gcc to link a shared library.
	##
	def link_to_so(self, file, binary, target, depancy, libName=""):
		if libName=="":
			libName = self.name
		file_src, file_dst, file_depend, file_cmd = target.generate_file(binary, libName,self.originFolder,file,"lib-shared")
		#create command Line
		cmdLine=lutinTools.list_to_str([
			target.xx,
			"-o", file_dst,
			target.global_sysroot,
			"-shared",
			file_src,
			depancy.src,
			self.flags_ld,
			depancy.flags_ld,
			target.global_flags_ld])
		
		# check the dependency for this file :
		if     dependency.need_re_package(file_dst, file_src, True, file_cmd, cmdLine) == False \
		   and dependency.need_re_package(file_dst, depancy.src, False, file_cmd, cmdLine) == False:
			return tmpList[1]
		lutinTools.create_directory_of_file(file_dst)
		debug.print_element("SharedLib", libName, "==>", file_dst)
		lutinMultiprocess.run_command(cmdLine)
		if    "release"==target.buildMode \
		   or lutinEnv.get_force_strip_mode()==True:
			# get the file size of the non strip file
			originSize = lutinTools.file_size(file_dst);
			debug.print_element("SharedLib(strip)", libName, "", "")
			cmdLineStrip=lutinTools.list_to_str([
				target.strip,
				file_dst])
			lutinMultiprocess.run_command(cmdLineStrip)
			# get the stip size of the binary
			stripSize = lutinTools.file_size(file_dst)
			debug.debug("file reduce size : " + str(originSize/1024) + "ko ==> " + str(stripSize/1024) + "ko")
		# write cmd line only after to prevent errors ...
		lutinMultiprocess.store_command(cmdLine, file_cmd)
		#debug.print_element("SharedLib", self.name, "==>", tmpList[1])
	
	
	##
	## @brief Commands for running gcc to link an executable.
	##
	def link_to_bin(self, file, binary, target, depancy):
		file_src, file_dst, file_depend, file_cmd = target.generate_file(binary, self.name,self.originFolder,file,"bin")
		#create comdLine : 
		cmdLine=lutinTools.list_to_str([
			target.xx,
			"-o", file_dst,
			target.global_sysroot,
			file_src,
			depancy.src,
			self.flags_ld,
			depancy.flags_ld,
			target.global_flags_ld])
		# check the dependency for this file :
		if False==dependency.need_re_package(file_dst, file_src, True, file_cmd, cmdLine) \
				and False==dependency.need_re_package(file_dst, depancy.src, False, file_cmd, cmdLine):
			return file_dst
		lutinTools.create_directory_of_file(file_dst)
		debug.print_element("Executable", self.name, "==>", file_dst)
		
		lutinMultiprocess.run_command(cmdLine)
		if    "release"==target.buildMode \
		   or lutinEnv.get_force_strip_mode()==True:
			# get the file size of the non strip file
			originSize = lutinTools.file_size(file_dst);
			debug.print_element("Executable(strip)", self.name, "", "")
			cmdLineStrip=lutinTools.list_to_str([
				target.strip,
				file_dst])
			lutinMultiprocess.run_command(cmdLineStrip)
			# get the stip size of the binary
			stripSize = lutinTools.file_size(file_dst)
			debug.debug("file reduce size : " + str(originSize/1024) + "ko ==> " + str(stripSize/1024) + "ko")
		# write cmd line only after to prevent errors ...
		lutinMultiprocess.store_command(cmdLine, file_cmd)
		
	
	##
	## @brief Commands for copying files
	##
	def files_to_staging(self, binaryName, target):
		for element in self.files:
			debug.verbose("Might copy file : " + element[0] + " ==> " + element[1])
			target.add_file_staging(self.originFolder+"/"+element[0], element[1])
	
	##
	## @brief Commands for copying files
	##
	def folders_to_staging(self, binaryName, target):
		for element in self.folders:
			debug.verbose("Might copy folder : " + element[0] + "==>" + element[1])
			lutinTools.copy_anything_target(target, self.originFolder+"/"+element[0],element[1])
	
	# call here to build the module
	def build(self, target, packageName):
		# ckeck if not previously build
		if target.is_module_build(self.name)==True:
			return self.localHeritage
		
		if     packageName==None \
		   and (    self.type=="BINARY" \
		         or self.type=="PACKAGE" ) :
			# this is the endpoint binary ...
			packageName = self.name
		else :
			# TODO : Set it better ...
			None
		
		# build dependency befor
		listSubFileNeededTobuild = []
		subHeritage = heritage.heritage(None)
		for dep in self.depends:
			inherit = target.build(dep, packageName)
			# add at the heritage list :
			subHeritage.add_sub(inherit)
		
		# build local sources
		for file in self.src:
			#debug.info(" " + self.name + " <== " + file);
			fileExt = file.split(".")[-1]
			if    fileExt == "c" \
			   or fileExt == "C":
				resFile = self.compile_cc_to_o(file, packageName, target, subHeritage)
				listSubFileNeededTobuild.append(resFile)
			elif    fileExt == "cpp" \
			     or fileExt == "CPP" \
			     or fileExt == "cxx" \
			     or fileExt == "CXX" \
			     or fileExt == "xx" \
			     or fileExt == "XX":
				resFile = self.compile_xx_to_o(file, packageName, target, subHeritage)
				listSubFileNeededTobuild.append(resFile)
			elif    fileExt == "mm" \
			     or fileExt == "MM":
				resFile = self.compile_mm_to_o(file, packageName, target, subHeritage)
				listSubFileNeededTobuild.append(resFile)
			else:
				debug.verbose(" TODO : gcc " + self.originFolder + "/" + file)
		# when multiprocess availlable, we need to synchronize here ...
		lutinMultiprocess.pool_synchrosize()
		
		# generate end point:
		if self.type=='PREBUILD':
			# nothing to add ==> just dependence
			None
		elif self.type=='LIBRARY':
			resFile = self.link_to_a(listSubFileNeededTobuild, packageName, target, subHeritage)
			self.localHeritage.add_sources(resFile)
		elif self.type=='BINARY':
			resFile = self.link_to_bin(listSubFileNeededTobuild, packageName, target, subHeritage)
			# generate tree for this special binary
			target.clean_module_tree()
			self.build_tree(target, self.name)
			target.copy_to_staging(self.name)
		elif self.type=="PACKAGE":
			if target.name=="Android":
				# special case for android wrapper :
				resFile = self.link_to_so(listSubFileNeededTobuild, packageName, target, subHeritage, "libewol")
			else:
				resFile = self.link_to_bin(listSubFileNeededTobuild, packageName, target, subHeritage)
			target.clean_module_tree()
			# generate tree for this special binary
			self.build_tree(target, self.name)
			target.copy_to_staging(self.name)
			if target.endGeneratePackage==True:
				# generate the package with his properties ...
				target.make_package(self.name, self.packageProp, self.originFolder + "/..")
		else:
			debug.error("Dit not know the element type ... (impossible case) type=" + self.type)
			
		self.localHeritage.add_sub(subHeritage)
		# return local dependency ...
		return self.localHeritage
	
	# call here to build the module
	def build_tree(self, target, packageName):
		# ckeck if not previously build
		if target.is_module_buildTree(self.name)==True:
			return
		debug.verbose("build tree of " + self.name)
		# add all the elements (first added only one keep ==> permit to everload sublib element)
		self.files_to_staging(packageName, target)
		self.folders_to_staging(packageName, target)
		#build tree of all submodules
		for dep in self.depends:
			inherit = target.build_tree(dep, packageName)
	
	
	# call here to clean the module
	def clean(self, target):
		if self.type=='PREBUILD':
			# nothing to add ==> just dependence
			None
		elif self.type=='LIBRARY':
			# remove folder of the lib ... for this targer
			folderbuild = target.get_build_folder(self.name)
			debug.info("remove folder : '" + folderbuild + "'")
			lutinTools.remove_folder_and_sub_folder(folderbuild)
		elif    self.type=='BINARY' \
		     or self.type=='PACKAGE':
			# remove folder of the lib ... for this targer
			folderbuild = target.get_build_folder(self.name)
			debug.info("remove folder : '" + folderbuild + "'")
			lutinTools.remove_folder_and_sub_folder(folderbuild)
			folderStaging = target.get_staging_folder(self.name)
			debug.info("remove folder : '" + folderStaging + "'")
			lutinTools.remove_folder_and_sub_folder(folderStaging)
		else:
			debug.error("Dit not know the element type ... (impossible case) type=" + self.type)
	
	def append_and_check(self, listout, newElement, order):
		for element in listout:
			if element==newElement:
				return
		listout.append(newElement)
		if True==order:
			listout.sort()
	
	def append_to_internalList(self, listout, list, order=False):
		if type(list) == type(str()):
			self.append_and_check(listout, list, order)
		else:
			# mulyiple imput in the list ...
			for elem in list:
				self.append_and_check(listout, elem, order)
	
	def add_module_depend(self, list):
		self.append_to_internalList(self.depends, list, True)
	
	def add_export_path(self, list):
		self.append_to_internalList(self.export_path, list)
	
	def add_path(self, list):
		self.append_to_internalList(self.local_path, list)
	
	def add_export_flag_LD(self, list):
		self.append_to_internalList(self.export_flags_ld, list)
	
	def add_export_flag_CC(self, list):
		self.append_to_internalList(self.export_flags_cc, list)
	
	def add_export_flag_XX(self, list):
		self.append_to_internalList(self.export_flags_xx, list)
	
	def add_export_flag_M(self, list):
		self.append_to_internalList(self.export_flags_m, list)
	
	def add_export_flag_MM(self, list):
		self.append_to_internalList(self.export_flags_mm, list)
	
	# add the link flag at the module
	def compile_flags_LD(self, list):
		self.append_to_internalList(self.flags_ld, list)
	
	def compile_flags_CC(self, list):
		self.append_to_internalList(self.flags_cc, list)
	
	def compile_flags_XX(self, list):
		self.append_to_internalList(self.flags_xx, list)
	
	def compile_flags_M(self, list):
		self.append_to_internalList(self.flags_m, list)
	
	def compile_flags_MM(self, list):
		self.append_to_internalList(self.flags_mm, list)
	
	def compile_flags_S(self, list):
		self.append_to_internalList(self.flags_s, list)
	
	def add_src_file(self, list):
		self.append_to_internalList(self.src, list, True)
	
	def copy_file(self, src, dst):
		self.files.append([src,dst])
	
	def copy_folder(self, src, dst):
		self.folders.append([src,dst])
	
	def print_list(self, description, list):
		if len(list) > 0:
			print '        %s' %description
			for elem in list:
				print '            %s' %elem
	
	def display(self, target):
		print '-----------------------------------------------'
		print ' package : "%s"' %self.name
		print '-----------------------------------------------'
		print '    type:"%s"' %self.type
		print '    file:"%s"' %self.originFile
		print '    folder:"%s"' %self.originFolder
		self.print_list('depends',self.depends)
		self.print_list('flags_ld',self.flags_ld)
		self.print_list('flags_cc',self.flags_cc)
		self.print_list('flags_xx',self.flags_xx)
		self.print_list('flags_m',self.flags_m)
		self.print_list('flags_mm',self.flags_mm)
		self.print_list('flags_s',self.flags_s)
		self.print_list('src',self.src)
		self.print_list('files',self.files)
		self.print_list('folders',self.folders)
		self.print_list('export_path',self.export_path)
		self.print_list('export_flags_ld',self.export_flags_ld)
		self.print_list('export_flags_cc',self.export_flags_cc)
		self.print_list('export_flags_xx',self.export_flags_xx)
		self.print_list('export_flags_m',self.export_flags_m)
		self.print_list('export_flags_mm',self.export_flags_mm)
		self.print_list('local_path',self.local_path)
	
	def pkg_set(self, variable, value):
		if "COMPAGNY_TYPE" == variable:
			#	com : Commercial
			#	net : Network??
			#	org : Organisation
			#	gov : Governement
			#	mil : Military
			#	edu : Education
			#	pri : Private
			#	museum : ...
			if     "com" != value \
			   and "net" != value \
			   and "org" != value \
			   and "gov" != value \
			   and "mil" != value \
			   and "edu" != value \
			   and "pri" != value \
			   and "museum" != value:
				debug.error("can not set the value for this Input : '" + variable + "' : '" + value + "'")
			else:
				self.packageProp[variable] = value
		elif "COMPAGNY_NAME" == variable:
			self.packageProp[variable] = value
			val2 = value.lower()
			val2 = val2.replace(' ', '')
			val2 = val2.replace('-', '')
			val2 = val2.replace('_', '')
			self.packageProp["COMPAGNY_NAME2"] = val2
		elif "ICON" == variable:
			self.packageProp[variable] = value
		elif "MAINTAINER" == variable:
			self.packageProp[variable] = value
		elif "SECTION" == variable:
			# project section : (must be separate by coma
			#    refer to : http://packages.debian.org/sid/
			#        admin cli-mono comm database debian-installer
			#        debug doc editors electronics devel embedded
			#        fonts games gnome gnu-r gnustep graphics
			#        hamradio haskell httpd interpreters java
			#        kde kernel libdevel libs lisp localization
			#        mail math misc net news ocaml oldlibs otherosfs
			#        perl php python ruby science shells sound tex
			#        text utils vcs video virtual web x11 xfce zope ...
			self.packageProp[variable] = value
		elif "PRIORITY" == variable:
			#list = ["required","important","standard","optional","extra"]
			#if isinstance(value, list):
			if     "required" != value \
			   and "important" != value \
			   and "standard" != value \
			   and "optional" != value \
			   and "extra" != value:
				debug.error("can not set the value for this Input : '" + variable + "' : '" + value + "'")
			else:
				self.packageProp[variable] = value
		elif "DESCRIPTION" == variable:
			self.packageProp[variable] = value
		elif "VERSION" == variable:
			self.packageProp[variable] = value
		elif "NAME" == variable:
			self.packageProp[variable] = value
		elif "ANDROID_MANIFEST" == variable:
			self.packageProp[variable] = value
		elif "ANDROID_JAVA_FILES" == variable:
			self.packageProp[variable] = value
		elif "RIGHT" == variable:
			self.packageProp[variable] = value
		elif "ANDROID_RESOURCES" == variable:
			self.packageProp[variable] = value
		elif "ANDROID_APPL_TYPE" == variable:
			self.packageProp[variable] = value
		else:
			debug.error("not know pak element : '" + variable + "'")
	
	def pkg_add(self, variable, value):
		# TODO : Check values...
		self.packageProp[variable].append(value)
		



moduleList=[]
__startModuleName="lutin_"

def import_path(path):
	global moduleList
	matches = []
	debug.debug('Start find sub File : "%s"' %path)
	for root, dirnames, filenames in os.walk(path):
		tmpList = fnmatch.filter(filenames, __startModuleName + "*.py")
		# Import the module :
		for filename in tmpList:
			debug.debug('    Find a file : "%s"' %os.path.join(root, filename))
			#matches.append(os.path.join(root, filename))
			sys.path.append(os.path.dirname(os.path.join(root, filename)) )
			moduleName = filename.replace('.py', '')
			moduleName = moduleName.replace(__startModuleName, '')
			debug.debug("integrate module: '" + moduleName + "' from '" + os.path.join(root, filename) + "'")
			moduleList.append([moduleName,os.path.join(root, filename)])

def load_module(target, name):
	global moduleList
	for mod in moduleList:
		if mod[0] == name:
			sys.path.append(os.path.dirname(mod[1]))
			theModule = __import__(__startModuleName + name)
			#try:
			tmpElement = theModule.create(target)
			if (tmpElement == None) :
				debug.debug("Request load module '" + name + "' not define for this platform")
			else:
				target.add_module(tmpElement)
			#except:
			#	debug.error(" no function 'Create' in the module : " + mod[0] + " from:'" + mod[1] + "'")

def list_all_module():
	global moduleList
	tmpListName = []
	for mod in moduleList:
		tmpListName.append(mod[0])
	return tmpListName

def list_all_module_with_desc():
	global moduleList
	tmpList = []
	for mod in moduleList:
		sys.path.append(os.path.dirname(mod[1]))
		theModule = __import__("lutin_" + mod[0])
		try:
			tmpdesc = theModule.get_desc()
			tmpList.append([mod[0], tmpdesc])
		except:
			debug.warning("has no naeme : " + mod[0])
			tmpList.append([mod[0], ""])
	return tmpList


