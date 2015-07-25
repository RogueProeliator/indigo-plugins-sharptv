#! /usr/bin/env python
# -*- coding: utf-8 -*-
#/////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////////////////////
# Sharp TV Network Remote Control by RogueProeliator <rp@rogueproeliator.com>
# 	See plugin.py for more plugin details and information
#/////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////////////////////

#/////////////////////////////////////////////////////////////////////////////////////////
# Python imports
#/////////////////////////////////////////////////////////////////////////////////////////
import functools
import httplib
import os
import Queue
import re
import string
import sys
import threading
import telnetlib
import time
import urllib

import indigo
import RPFramework

#/////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////////////////////
# SharpTvNetworkRemoteDevice
#	Handles the configuration of a single Roku device that is connected to this plugin;
#	this class does all the 'grunt work' of communications with the Roku
#/////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////////////////////
class SharpTvNetworkRemoteDevice(RPFramework.RPFrameworkTelnetDevice.RPFrameworkTelnetDevice):
	
	#/////////////////////////////////////////////////////////////////////////////////////
	# Class construction and destruction methods
	#/////////////////////////////////////////////////////////////////////////////////////
	#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
	# Constructor called once upon plugin class receiving a command to start device
	# communication. The plugin will call other commands when needed, simply zero out the
	# member variables
	#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
	def __init__(self, plugin, device):
		super(SharpTvNetworkRemoteDevice, self).__init__(plugin, device)
		
		
	#/////////////////////////////////////////////////////////////////////////////////////
	# Validation and GUI functions
	#/////////////////////////////////////////////////////////////////////////////////////
	#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
	# This routine is called to retrieve a dynamic list of elements for an action (or
	# other ConfigUI based) routine
	#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
	def getConfigDialogMenuItems(self, filter, valuesDict, typeId, targetId):
		self.hostPlugin.logDebugMessage("SharpTV device received request for source list menu items", RPFramework.RPFrameworkPlugin.DEBUGLEVEL_MED)
		availableInputs = []
		availableInputs.append(("RCKY36  ", "Toggle Input"))
		
		tvTunerLabel = self.indigoDevice.pluginProps.get("input0Label", "")
		if tvTunerLabel != "":
			availableInputs.append(("ITVD0   ", tvTunerLabel))
		
		for i in range(1,9):
			labelName = self.indigoDevice.pluginProps.get("input" + str(i) + "Label", "")
			if labelName != "":
				availableInputs.append(("IAVD" + str(i) + "   ", labelName))
		return availableInputs
		
		
	#/////////////////////////////////////////////////////////////////////////////////////
	# Processing and command functions
	#/////////////////////////////////////////////////////////////////////////////////////
	#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
	# This routine will process the commands that are not processed automatically by the
	# base class; it will be called on a concurrent thread
	#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
	def handleUnmanagedCommandInQueue(self, ipConnection, rpCommand):
		if rpCommand.commandName == "createTuneCommands":
			# this command payload will be the channel - either an analog of digital
			# channel so we must parse that out
			try:
				fltChannel = float(rpCommand.commandPayload)
			except:
				# this means an invalid tune command was received
				indigo.server.log("Ignored tune command to empty or invalid channel number")
				return
				
			if fltChannel <= 135:
				# this is an analog tune command...
				analogValuesDict = indigo.Dict()
				analogValuesDict['channelNumber'] = rpCommand.commandPayload
				self.hostPlugin.executeAction(None, 'tuneToAnalogChannel', self.indigoDevice.id, analogValuesDict)
			else:
				indigo.server.log("Digital channel tune not yet supported", isError=False)
		
	#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
	# This routine should return a touple of information about the connection - in the
	# format of (ipAddress/HostName, portNumber)
	#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
	def getDeviceAddressInfo(self):
		return (self.indigoDevice.pluginProps.get("ipAddress", ""), int(self.indigoDevice.pluginProps.get("portNumber", "10002")))
		
		