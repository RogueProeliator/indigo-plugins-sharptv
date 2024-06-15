#! /usr/bin/env python
# -*- coding: utf-8 -*-
#######################################################################################
# Sharp TV Network Remote Control by RogueProeliator <rp@rogueproeliator.com>
#######################################################################################

# region  Python imports

import indigo
from RPFramework.RPFrameworkTelnetDevice import RPFrameworkTelnetDevice
from RPFramework.RPFrameworkCommand import RPFrameworkCommand

# endregion


class SharpTvNetworkRemoteDevice(RPFrameworkTelnetDevice):

	#######################################################################################
	# region Class construction and destruction methods
	# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
	# Constructor called once upon plugin class receiving a command to start device
	# communication. The plugin will call other commands when needed, simply zero out the
	# member variables
	# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
	def __init__(self, plugin, device):
		super().__init__(plugin, device)

	# endregion
	#######################################################################################
		
	#######################################################################################
	# region Validation and GUI functions
	# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
	# This routine is called to retrieve a dynamic list of elements for an action (or
	# other ConfigUI based) routine
	# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
	def getConfigDialogMenuItems(self, filter, valuesDict, typeId, targetId):
		self.host_plugin.logger.debug("SharpTV device received request for source list menu items")
		available_inputs = []
		available_inputs.append(("RCKY36  ", "Toggle Input"))
		
		tv_tuner_label = self.indigoDevice.pluginProps.get("input0Label", "")
		if tv_tuner_label != "":
			available_inputs.append(("ITVD0   ", tv_tuner_label))
		
		for i in range(1,9):
			label_name = self.indigoDevice.pluginProps.get(f"input{i}Label", "")
			if label_name != "":
				available_inputs.append((f"IAVD{i}   ", label_name))
		return available_inputs

	# endregion
	#######################################################################################

	#######################################################################################
	# region Processing and command functions
	# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
	# This routine will process the commands that are not processed automatically by the
	# base class; it will be called on a concurrent thread
	# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
	def handle_unmanaged_command_in_queue(self, ip_connection, rp_command):
		if rp_command.command_name == "createTuneCommands":
			# this command payload will be the channel - either an analog of digital
			# channel so we must parse that out
			try:
				flt_channel = float(rp_command.command_payload)
			except:
				# this means an invalid tune command was received
				self.host_plugin.logger.warning(u'Ignored tune command to empty or invalid channel number')
				return
				
			if flt_channel <= 135:
				# this is an analog tune command...
				analog_values_dict = indigo.Dict()
				analog_values_dict["channelNumber"] = rp_command.command_payload
				self.host_plugin.executeAction(None, "tuneToAnalogChannel", self.indigoDevice.id, analog_values_dict)
			else:
				self.host_plugin.logger.warning("Digital channel tune not yet supported")
		
	# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
	# This routine should return a touple of information about the connection - in the
	# format of (ipAddress/HostName, portNumber)
	# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
	def get_device_address_info(self):
		return (self.indigoDevice.pluginProps.get("ipAddress", ""), int(self.indigoDevice.pluginProps.get("portNumber", "10002")))
		
		