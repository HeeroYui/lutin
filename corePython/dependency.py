#!/usr/bin/python
import os
import debug
import environement


def NeedReBuild(dst, src, dependFile):
	debug.verbose("Resuest check of dependency of :")
	debug.verbose("		dst='" + dst + "'")
	debug.verbose("		str='" + src + "'")
	debug.verbose("		dept='" + dependFile + "'")
	# if force mode selected ==> just force rebuild ...
	if environement.GetForceMode():
		debug.verbose("			==> must rebuild (force mode)")
		return True
	
	# check if the destination existed:
	if False==os.path.exists(dst):
		debug.verbose("			==> must rebuild (dst does not exist)")
		return True
	# chek the basic date if the 2 files
	if os.path.getmtime(src) > os.path.getmtime(dst):
		debug.verbose("			==> must rebuild (source time greater)")
		return True
	# now we need to parse the file to find all the dependency file
	#	file is done like
	#		file : \
	#		 dep1 \
	#		 dep2
	#		
	#		dep2 : \
	#		 dep4
	#
	
	if False==os.path.exists(dependFile):
		debug.verbose("			==> must rebuild (no depending file)")
		return True
	
	debug.verbose("			start parsing dependency file : '" + dependFile + "'")
	file = open(dependFile, "r")
	for curLine in file.readlines():
		# normal file : end with : ": \\n"
		curLine = curLine[:len(curLine)-1]
		testFile=""
		if curLine[len(curLine)-3:] == ': \\' \
				or curLine[len(curLine)-2:] == ': ' \
				or curLine[len(curLine)-1:] == ':':
			debug.verbose("				Line (no check (already done) : '" + curLine + "'");
		elif curLine[len(curLine)-2:] == ' \\':
			testFile = curLine[1:len(curLine)-2]
			debug.verbose("				Line (might check1) : '" + testFile + "'");
		elif len(curLine) == 0:
			debug.verbose("				Line (Not parsed) : '" + curLine + "'");
		else:
			testFile = curLine[1:]
			debug.verbose("				Line (might check2) : '" + testFile + "'");
		# really check files:
		if testFile!="":
			debug.verbose("					==> test");
			if False==os.path.exists(testFile):
				debug.warning("			==> must rebuild (a dependency file does not exist)")
				return True
			if os.path.getmtime(testFile) > os.path.getmtime(dst):
				debug.warning("			==> must rebuild (a dependency file time is newer)")
				return True
	
	debug.verbose("			==> Not rebuild (all dependency is OK)")
	return False



def NeedRePackage(dst, srcList, mustHaveSrc):
	debug.verbose("Resuest check of dependency of :")
	debug.verbose("		dst='" + dst + "'")
	debug.verbose("		src()=")
	for src in srcList:
		debug.verbose("			'" + src + "'")
	
	if mustHaveSrc==False and len(srcList)==0:
		return False
	
	# if force mode selected ==> just force rebuild ...
	if environement.GetForceMode():
		debug.verbose("			==> must re-package (force mode)")
		return True
	
	# check if the destination existed:
	if False==os.path.exists(dst):
		debug.verbose("			==> must re-package (dst does not exist)")
		return True
	# chek the basic date if the 2 files
	if len(srcList)==0:
		debug.verbose("			==> must re-package (no source ???)")
		return True
	for src in srcList:
		if os.path.getmtime(src) > os.path.getmtime(dst):
			debug.verbose("			==> must re-package (source time greater) : '" + src + "'")
			return True
	
	debug.verbose("			==> Not re-package (all dependency is OK)")
	return False



