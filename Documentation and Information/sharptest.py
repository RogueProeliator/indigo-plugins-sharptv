#! /usr/bin/env python
# -*- coding: utf-8 -*-
import functools
import httplib
import Queue
import os
import re
import string
import socket
import sys
import threading
import telnetlib
import time
import urllib

if __name__ == '__main__':
	try:
		ipConnection = telnetlib.Telnet("172.16.1.136", 10002, 3)
		inData = ipConnection.read_until("Login:")
		print inData
		ipConnection.write("username\r")
		inData = ipConnection.read_until("Password:")
		print inData
		ipConnection.write("password\r")
		inData = ipConnection.read_until("\r", 1.5)
		print inData
		
		# issue command for "POWER ON COMMAND SETTINGS"
		#print "Issuing Power On Command to IP ON"
		#ipConnection.write("RSPW2   \r")
		#inData = ipConnection.read_until("\r", 1.5)
		#print inData
		
		#print "Name: "
		ipConnection.write("TVNM1   \r")
		inData = ipConnection.read_until("\r", 3)
		print inData
		
		print "Model: "
		ipConnection.write("MNRD1   \r")
		inData = ipConnection.read_until("\r", 3)
		print inData
		
		#print "Software Version: "
		#ipConnection.write("SWVN1   \r")
		#inData = ipConnection.read_until("\r", 3)
		#print inData
		
		#print "IP Protocol Version: "
		#ipConnection.write("IPPV1   \r")
		#inData = ipConnection.read_until("\r", 3)
		#print inData
		
		#print "Sending Ch Request - Analog "
		#ipConnection.write("DCCH??? \r")
		#inData = ipConnection.read_until("\r", 3)
		#print inData
		
		#print "Sending Ch Request - Digital "
		#ipConnection.write("DC2U??? \r")
		#inData = ipConnection.read_until("\r", 3)
		#print inData
		
		#print "Current Volume: "
		#ipConnection.write("VOLM??  \r")
		#inData = ipConnection.read_until("\r", 3)
		#print inData
		
		#print "Mute: "
		#ipConnection.write("MUTE?   \r")
		#inData = ipConnection.read_until("\r", 3)
		#print inData
		
		#print "Input: "
		#ipConnection.write("IAVD?   \r")
		#inData = ipConnection.read_until("\r", 3)
		#print inData
		
		#print "Read Power: "
		#ipConnection.write("POWR?   \r")
		#inData = ipConnection.read_until("\r", 3)
		#print inData
		
		#print "A/V Mode: "
		#ipConnection.write("AVMD?   \r")
		#inData = ipConnection.read_until("\r", 3)
		#print inData
		
		#print "View Mode: "
		#ipConnection.write("WIDE?   \r")
		#inData = ipConnection.read_until("\r", 3)
		#print inData
		
		#print "Surround: "
		#ipConnection.write("ACSU?   \r")
		#inData = ipConnection.read_until("\r", 3)
		#print inData
		
		#print "Sleep Timer: "
		#ipConnection.write("OFTM?   \r")
		#inData = ipConnection.read_until("\r", 3)
		#print inData
		
		#print "Closed Captioning: "
		#ipConnection.write("CLCP?   \r")
		#inData = ipConnection.read_until("\r", 3)
		#print inData
		
		#print "Input: "
		#ipConnection.write("ITGD?   \r")
		#inData = ipConnection.read_until("\r", 3)
		#print inData
		
		#print "Sending MENU "
		#ipConnection.write("RCKY38  \r")
		#inData = ipConnection.read_until("\r", 3)
		#print inData
		
		#print "Sending Return "
		#ipConnection.write("RCKY45  \r")
		#inData = ipConnection.read_until("\r", 3)
		#print inData
		
		#print "Sending Ch + "
		#ipConnection.write("RCKY34  \r")
		#inData = ipConnection.read_until("\r", 3)
		#print inData
	except Exception as e:
		print "Exception: " + str(e)
	