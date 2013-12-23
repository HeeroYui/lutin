#!/usr/bin/python
import lutinDebug as debug
import lutinTarget
import lutinTools
import os
import stat

class Target(lutinTarget.Target):
	def __init__(self, typeCompilator, debugMode, generatePackage):
		cross = ""
		
		# http://biolpc22.york.ac.uk/pub/linux-mac-cross/
		# http://devs.openttd.org/~truebrain/compile-farm/apple-darwin9.txt
		lutinTarget.Target.__init__(self, "MacOs", typeCompilator, debugMode, generatePackage, "", cross)
		
		self.folder_bin="/MacOS"
		self.folder_lib="/lib"
		self.folder_data="/Resources"
		self.folder_doc="/doc"
		
		self.suffix_lib_static='.a'
		self.suffix_lib_dynamic='.dylib'
		self.suffix_binary=''
		self.suffix_package=''
		
	
	def get_staging_folder(self, binaryName):
		return lutinTools.get_run_folder() + self.folder_out + self.folder_staging + "/" + binaryName + ".app/Contents/"
	
	def get_staging_folder_data(self, binaryName):
		return self.get_staging_folder(binaryName) + self.folder_data + "/"
	
	def make_package(self, pkgName, pkgProperties, basePkgPath):
		debug.debug("------------------------------------------------------------------------")
		debug.info("Generate package '" + pkgName + "'")
		debug.debug("------------------------------------------------------------------------")
		# http://www.sandroid.org/imcross/#Deployment
		infoFile=self.get_staging_folder(pkgName) + "/Info.plist"
		# Create the info file
		tmpFile = open(infoFile, 'w')
		tmpFile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
		tmpFile.write("<!DOCTYPE plist PUBLIC \"-//Apple Computer//DTD PLIST 1.0//EN\" \"http://www.apple.com/DTDs/PropertyList-1.0.dtd\">\n")
		tmpFile.write("<plist version=\"1.0\">\n")
		tmpFile.write("    <dict>\n")
		tmpFile.write("        <key>CFBundleExecutableFile</key>\n")
		tmpFile.write("        <string>"+pkgName+"</string>\n")
		tmpFile.write("        <key>CFBundleName</key>\n")
		tmpFile.write("        <string>"+pkgName+"</string>\n")
		tmpFile.write("        <key>CFBundleIdentifier</key>\n")
		tmpFile.write("        <string>com."+pkgProperties["COMPAGNY_NAME2"]+"."+pkgName+"</string>\n")
		tmpFile.write("        <key>CFBundleIconFile</key>\n")
		tmpFile.write("        <string>"+pkgName+".icns</string>\n")
		tmpFile.write("    </dict>\n")
		tmpFile.write("</plist>\n")
		tmpFile.write("\n\n")
		tmpFile.flush()
		tmpFile.close()
		infoFile=self.get_staging_folder(pkgName) + "/PkgInfo"
		# Create the info file
		tmpFile = open(infoFile, 'w')
		tmpFile.write("APPL?????")
		tmpFile.flush()
		tmpFile.close()
		
		# Must create the tarball of the application 
		#cd $(TARGET_OUT_FINAL)/; tar -cf $(PROJECT_NAME).tar $(PROJECT_NAME).app
		#cd $(TARGET_OUT_FINAL)/; tar -czf $(PROJECT_NAME).tar.gz $(PROJECT_NAME).app
	
	def install_package(self, pkgName):
		debug.debug("------------------------------------------------------------------------")
		debug.info("Install package '" + pkgName + "'")
		debug.debug("------------------------------------------------------------------------")
		debug.warning("    ==> TODO")
		#sudo dpkg -i $(TARGET_OUT_FINAL)/$(PROJECT_NAME) + self.suffix_package
	
	def un_install_package(self, pkgName):
		debug.debug("------------------------------------------------------------------------")
		debug.info("Un-Install package '" + pkgName + "'")
		debug.debug("------------------------------------------------------------------------")
		debug.warning("    ==> TODO")
		#sudo dpkg -r $(TARGET_OUT_FINAL)/$(PROJECT_NAME) + self.suffix_package




