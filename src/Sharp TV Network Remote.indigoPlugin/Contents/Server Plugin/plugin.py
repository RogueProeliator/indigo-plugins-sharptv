#! /usr/bin/env python
# -*- coding: utf-8 -*-
#######################################################################################
# Sharp TV Network Remote Control by RogueProeliator <rp@rogueproeliator.com>
#######################################################################################

# region Python imports
import indigo

from RPFramework.RPFrameworkPlugin import RPFrameworkPlugin
import sharpTvNetworkRemoteDevice
#endregion


class Plugin(RPFrameworkPlugin):

	#######################################################################################
	# region Class construction and destruction methods
	# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
	# Constructor called once upon plugin class creation; set up the device tracking
	# variables for later use
	# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
	def __init__(self, plugin_id, plugin_display_name, plugin_version, plugin_prefs):
		# RP framework base class's init method
		super().__init__(plugin_id, plugin_display_name, plugin_version, plugin_prefs, managed_device_class_module=sharpTvNetworkRemoteDevice)

	# endregion
	#######################################################################################

	#######################################################################################
	# region MenuItem handlers
	# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
	# This method will be called whenever the user has clicked the menus in order to
	# enable the power-on setting for TV(s)
	# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
	def enable_power_on_commands(self, valuesDict, typeId):
		# this callback method must also do the validation... check to ensure that
		# at least one TV has been selected from the list
		errors_dict = indigo.Dict()
		tv_list = valuesDict.get("targetTVs")
		
		if len(tv_list) == 0:
			errors_dict["targetTVs"] = "Please select the TV(s) desired"
			return False, valuesDict, errors_dict
		else:
			# log the fact that we are starting this command...
			self.logger.info("Executing Enable Power On Commands...")
			
			# queue up the command for each selected device... this may be done via the
			# execute action method
			param_values = indigo.Dict()
			param_values["powerOnMessageState"] = "2"
			for tv_device in tv_list:
				self.executeAction(None, "changeTVPowerOnMessages", int(tv_device), param_values)
			return True, valuesDict, indigo.Dict()
			
	# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
	# This routine will be called from the user executing the menu item action to send
	# an arbitrary command code to the Onkyo receiver
	# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
	def send_arbitrary_command(self, valuesDict, typeId):
		try:
			device_id = valuesDict.get("targetDevice", "0")
			command_code = valuesDict.get("commandToSend", "")
			
			if device_id == "" or device_id == "0":
				# no device was selected
				error_dict = indigo.Dict()
				error_dict["targetDevice"] = "Please select a device"
				return False, valuesDict, error_dict
			elif command_code == "":
				error_dict = indigo.Dict()
				error_dict["commandToSend"] = "Enter command to send"
				return False, valuesDict, error_dict
			else:
				action_params = indigo.Dict()
				action_params["commandCode"] = command_code.ljust(8, ' ')
				self.executeAction(pluginAction=None, indigoActionId="sendArbitraryCommand", indigoDeviceId=int(device_id), paramValues=action_params)
				return True, valuesDict
		except:
			self.logger.exception("Exception while executing send arbitrary command")
			return False, valuesDict

	# endregion
	#######################################################################################
