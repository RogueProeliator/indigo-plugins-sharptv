#! /usr/bin/env python
# -*- coding: utf-8 -*-
#/////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////////////////////
# Sharp TV Network Remote Control by RogueProeliator <rp@rogueproeliator.com>
# 	Indigo plugin designed to allow full control of a Sharp AQUOS TV via the IP control
#	protocol (wired or wireless network connection)
#	
#	Command structure based on Sharp's documentation, internet resources and discovered
#	(unpublished) commands.
#
#	Version 1.0:
#		* Initial release of the plugin to Indigo users
#	Version 1.2.8 [5/2014]:
#		* Added auto-reconnect to connection failures or timeouts
#		* Caught exception trying to tune selector when no channel was entered
#	Version 1.3.14:
#		* Added ability to send arbitrary command
#		* Upgraded framework which included additional features
#
#/////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////////////////////


#/////////////////////////////////////////////////////////////////////////////////////////
# Python imports
#/////////////////////////////////////////////////////////////////////////////////////////
import indigo
import random
import re
import select
import socket
import string
import telnetlib
import urllib
import os

import RPFramework
import sharpTvNetworkRemoteDevice


#/////////////////////////////////////////////////////////////////////////////////////////
# Constants and configuration variables
#/////////////////////////////////////////////////////////////////////////////////////////


#/////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////////////////////
# Plugin
#	Primary Indigo plugin class that is universal for all devices (TV instances) to be
#	controlled
#/////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////////////////////
class Plugin(RPFramework.RPFrameworkPlugin.RPFrameworkPlugin):
	
	#/////////////////////////////////////////////////////////////////////////////////////
	# Class construction and destruction methods
	#/////////////////////////////////////////////////////////////////////////////////////
	#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
	# Constructor called once upon plugin class creation; setup the device tracking
	# variables for later use
	#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
	def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
		# RP framework base class's init method
		super(Plugin, self).__init__(pluginId, pluginDisplayName, pluginVersion, pluginPrefs, managedDeviceClassModule=sharpTvNetworkRemoteDevice)
	
	
	#/////////////////////////////////////////////////////////////////////////////////////
	# MenuItem handlers
	#/////////////////////////////////////////////////////////////////////////////////////
	#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
	# This method will be called whenever the user has clicked the menus in order to
	# enable the power-on setting for TV(s)
	#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
	def enablePowerOnCommands(self, valuesDict, typeId):
		# this callback method must also do the validation... check to ensure that
		# at least one TV has been selected from the list
		errorsDict = indigo.Dict()
		tvList = valuesDict.get(u'targetTVs')
		
		if len(tvList) == 0:
			errorsDict[u'targetTVs'] = u'Please select the TV(s) desired'
			return (False, valuesDict, errorsDict)
		else:
			# log the fact that we are starting this command...
			self.logger.info(u'Executing Enable Power On Commands...')
			
			# queue up the command for each selected device... this may be done via the
			# execute action method
			paramValues = indigo.Dict()
			paramValues[u'powerOnMessageState'] = u'2'
			for tvDevice in tvList:
				self.executeAction(None, u'changeTVPowerOnMessages', int(tvDevice), paramValues)
			return (True, valuesDict, indigo.Dict())
			
	#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-	
	# This routine will be called from the user executing the menu item action to send
	# an arbitrary command code to the Onkyo receiver
	#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-	
	def sendArbitraryCommand(self, valuesDict, typeId):
		try:
			deviceId = valuesDict.get(u'targetDevice', u'0')
			commandCode = valuesDict.get(u'commandToSend', u'')
			
			if deviceId == u'' or deviceId == u'0':
				# no device was selected
				errorDict = indigo.Dict()
				errorDict["targetDevice"] = u'Please select a device'
				return (False, valuesDict, errorDict)
			elif commandCode == u'':
				errorDict = indigo.Dict()
				errorDict[u'commandToSend'] = u'Enter command to send'
				return (False, valuesDict, errorDict)
			else:
				actionParams = indigo.Dict()
				actionParams[u'commandCode'] = commandCode.ljust(8, ' ')
				self.executeAction(pluginAction=None, indigoActionId=u'sendArbitraryCommand', indigoDeviceId=int(deviceId), paramValues=actionParams)
				return (True, valuesDict)
		except:
			self.exceptionLog()
			return (False, valuesDict)
			
	