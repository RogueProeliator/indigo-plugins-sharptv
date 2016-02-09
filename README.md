#Introduction
This Indigo 6.0+ plugin allows Indigo to control Sharp AQUOS televisions via their network (IP) control protocol. Sharp's protocol is very robust and, as a result, this plugin is able to both read and set nearly every aspect of the television - from volume/channel through configurations such as picture mode, aspect ratio, etc.

#Hardware Requirements
This plugin should work with any network-connected Sharp AQUOS television which supports IP control via ethernet or WiFi (it does not handle RS232 connections to the television); generally speaking if your television is supported by the official Sharp TV Remote (mobile) application then this plugin is able to control the hardware. The plugin has been tested with the following hardware:

-LC-XXLE650U Series (XX specifies the diagonal size for individual models)
-LC-60C6500U (Costo/Sam's version of above)
-PRO-70X5FD (Elite series)

If you have tested it successfully (or unsuccessfully) with other models and feel inclined to share, please let me know and I will update this list. Note that some televisions may not support all features provided by the plugin (e.g. have fewer HDMI inputs) in which case the unsupported commands will be ignored by the television and "do nothing".

#Enabling Network Control of the Television - *Important Step*
The first step is to ensure that your television is connected to the network; the menu system will vary by model, but generally speaking you will find the network settings under Menu->Initial Setup->Internet Setup. The exact settings/steps you use will depend upon your connection method (wired/wireless), but either method should result in the ability to view the current network settings on the IP Setup screen (under Internet Settings). Please take note of the IP address as you will need this when setting up the device in Indigo.

Before the television will allow any network remote (mobile application, desktop application, this plugin, etc.) to connect, you must enable the AQUOS Remote setting in the appropriate menu/settings screen. As before, the exact sequence of menu options may vary by model, but generally you will go to Menu->Initial Setup->Internet Setup->AQUOS Remote Control. This screen allows you to enable the AQUOS remote control. Please take note of the port number assigned, viewable on the Detailed settings area of the AQUOS remote as you will need that as well when setting up the device in Indigo (the default value is 10002).

On this same settings screen(s) you may optionally add a username/password which will be required of any device connecting to the television. This plugin supports both unauthenticated connections and those requiring the username/password.

#Installation and Configuration
###Obtaining the Plugin
The latest released version of the plugin is available for download [here](http://www.duncanware.com/Downloads/IndigoHomeAutomation/Plugins/SharpTvNetworkRemote/SharpTvNetworkRemote.zip). This download is a ZIP archive of the .indigoPlugin file. ALternatively, you may pull from this source repository, but must also pull the [RPFramework](https://github.com/RogueProeliator/IndigoPlugins-RPFramework), add its contents to the plugin directory under 'Server Plugin'.

###Configuring the Plugin
Upon first installation you will be asked to configure the plugin; please see the instructions on the configuration screen for more information. Most users will be fine with the defaults unless an email is desired when a new version is released.
![](<Documentation and Information/Help Images/SharpTvPluginConfig.png>)

#Plugin Devices
Each television that you wish to control should be created as an Indigo Device; In the Device Settings you will need to enter the television's IP address and network port setup for the AQUOS remote as obtained when setting up the television (see "Enabling Network Control of the Television" above). Note that if you ever lose connection with your television, you may need to return here to enter the IP Address again if it has picked up a new address on the network.
![](<Documentation and Information/Help Images/SharpTvDeviceConfig.png>)

#Enabling POWER ON Commands - *Important Requirement*
By default the television will be setup to only accept remote control of the television when the television is powered on (turning the power off will drop connection to the plugin). The plugin, however, is able to configure the TV to listen for Power On messages whenever it is in standby mode (obviously while in standby mode other commands are useless/ignored). To enable this feature go through the Indigo menus to Plugins->Sharp TV Network Remote Plugin->Setup TV for Network-On; select your TV device(s) and click the Run button.

![](<Documentation and Information/Help Images/SharpTvNetworkOnSetup.png>)

#Available Actions
###Toggle/Set TV Power
These actions will power on/off the television; please note that you must have completed the steps above ("Enabling POWER ON Commands") in order for the Power ON command to be accepted by the television.

###Set Volume Level / Mute / Set Closed Captioning
These actions control the "direct" setting of a volume to a specific value (0-60) and controlling the muted/CC status of the TV. Note that if you want to adjust the volume up/down incrementally then this must be done by sending a remote key (see the appropriate action below).

###Select TV Input / Tune to Analog Channel / Channel Selector Actions
These actions control the input and tuner of the television for setting the source of the display. Note that currently only analog television (direct tune) is supported, but a future version of the plugin may allow access to the QAM tuner for setting XXXX.YYY style digital channels. The "channel selector" methods are present as a convenience for you when creating control pages. The channel selector acts as a placeholder for the user entring a channel via a number-pad style interface. Digits may be added (or removed) by buttons on the number page until the user presses a "Go" button at which time you should execute the Tune to Channel Selector action; this will also clear the selector to allow for new input.

###Set Picture Mode / Aspect Correction / Surround Sound / Sleep Timer
These actions will set the respective setting on the TV as if you had gone through the menu system or, in the case of Toggle, used the appropriate button on the remote control.

###Send Remote Key
This action will send (via the network) a command that acts as if the selected button was pressed on the remote.

#Available Device States
This plugin will track the current status/setting of many of the features of the television; examples include volume, current input, current channel, etc. Any changes done via the plugin/Indigo should be reflected in these device states nearly immediately. However, changes done via an external control (physical remote, buttons on the TV) will not be reflected until the plugin polls the television for its state. By default this occurs every 90 seconds, but you may customize this in the Device Properties within Indigo.
