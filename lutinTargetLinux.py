#!/usr/bin/python
import lutinDebug as debug
import lutinTarget
import lutinTools
import os
import stat

class Target(lutinTarget.Target):
	def __init__(self, typeCompilator, debugMode, generatePackage):
		lutinTarget.Target.__init__(self, "Linux", typeCompilator, debugMode, generatePackage, "", "")
	
	def generateListSeparateComa(self, list):
		result = ""
		fistTime = True
		for elem in list:
			if fistTime == True:
				fistTime = False
			else:
				result += ","
			result += elem
		return result
	
	def MakePackage(self, pkgName, pkgProperties):
		# http://alp.developpez.com/tutoriels/debian/creer-paquet/
		debug.debug("------------------------------------------------------------------------")
		debug.info("Generate package '" + pkgName + "' v"+pkgProperties["VERSION"])
		debug.debug("------------------------------------------------------------------------")
		self.GetStagingFolder(pkgName)
		targetOutFolderDebian=self.GetStagingFolder(pkgName) + "/DEBIAN/"
		finalFileControl = targetOutFolderDebian + "control"
		finalFilepostRm = targetOutFolderDebian + "postrm"
		# create the folders :
		lutinTools.CreateDirectoryOfFile(finalFileControl)
		lutinTools.CreateDirectoryOfFile(finalFilepostRm)
		## Create the control file
		tmpFile = open(finalFileControl, 'w')
		tmpFile.write("Package: " + pkgName + "\n")
		tmpFile.write("Version: " + pkgProperties["VERSION"] + "\n")
		tmpFile.write("Section: " + self.generateListSeparateComa(pkgProperties["SECTION"]) + "\n")
		tmpFile.write("Priority: " + pkgProperties["PRIORITY"] + "\n")
		tmpFile.write("Architecture: all\n")
		tmpFile.write("Depends: bash\n")
		tmpFile.write("Maintainer: " + self.generateListSeparateComa(pkgProperties["MAINTAINER"]) + "\n")
		tmpFile.write("Description: " + pkgProperties["DESCRIPTION"] + "\n")
		tmpFile.write("\n")
		tmpFile.flush()
		tmpFile.close()
		## Create the PostRm
		tmpFile = open(finalFilepostRm, 'w')
		tmpFile.write("#!/bin/bash\n")
		tmpFile.write("touch ~/." + pkgName + "\n")
		if pkgName != "":
			tmpFile.write("touch ~/.local/share/" + pkgName + "\n")
			tmpFile.write("rm -r ~/.local/share/" + pkgName + "\n")
		tmpFile.write("\n")
		tmpFile.flush()
		tmpFile.close()
		## Enable Execution in script
		os.chmod(finalFilepostRm, stat.S_IRWXU + stat.S_IRGRP + stat.S_IXGRP + stat.S_IROTH + stat.S_IXOTH);
		# copy licence and information : 
		lutinTools.CopyFile("os-Linux/README", self.GetStagingFolder(pkgName) + "/usr/share/doc/"+ pkgName + "/README")
		lutinTools.CopyFile("license.txt", self.GetStagingFolder(pkgName) + "/usr/share/doc/"+ pkgName + "/copyright")
		lutinTools.CopyFile("changelog", self.GetStagingFolder(pkgName) + "/usr/share/doc/"+ pkgName + "/changelog")
		debug.debug("pachage : " + self.GetStagingFolder(pkgName) + "/" + pkgName + ".deb")
		os.system("cd " + self.GetStagingFolder("") + " ; dpkg-deb --build " + pkgName)
		lutinTools.CreateDirectoryOfFile(self.GetFinalFolder())
		lutinTools.CopyFile(self.GetStagingFolder("") + "/" + pkgName + self.suffix_package, self.GetFinalFolder() + "/" + pkgName + self.suffix_package)
	
	def InstallPackage(self, pkgName):
		debug.debug("------------------------------------------------------------------------")
		debug.info("Install package '" + pkgName + "'")
		debug.debug("------------------------------------------------------------------------")
		os.system("sudo dpkg -i " + self.GetFinalFolder() + "/" + pkgName + self.suffix_package)
	
	def UnInstallPackage(self, pkgName):
		debug.debug("------------------------------------------------------------------------")
		debug.info("Un-Install package '" + pkgName + "'")
		debug.debug("------------------------------------------------------------------------")
		os.system("sudo dpkg -r " + self.GetFinalFolder() + "/" + pkgName + self.suffix_package)