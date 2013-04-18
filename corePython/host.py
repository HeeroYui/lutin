#!/usr/bin/python
import platform
import debug

# print os.name # ==> 'posix'
if platform.system() == "Linux":
	OS = "Linux"
elif platform.system() == "Windows":
	OS = "Windows"
elif platform.system() == "Darwin":
	OS = "Windows"
else:
	debug.error("Unknow the Host OS ... '" + platform.system() + "'")

debug.debug(" host.OS = " + OS)

