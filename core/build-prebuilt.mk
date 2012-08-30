###############################################################################
## @file prebuilt.mk
## @author Edouard DUPIN
## @date 17-08-2012
## @project EWOL
##
## Register a prebuilt module.
###############################################################################

LOCAL_MODULE_CLASS := PREBUILT

ifeq ("$(LOCAL_MODULE_FILENAME)","")
LOCAL_MODULE_FILENAME := $(LOCAL_MODULE).done
endif

$(local-add-module)