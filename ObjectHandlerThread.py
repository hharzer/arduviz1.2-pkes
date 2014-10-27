##@package ObjectHandlerThread
# This module provides the ObjectHandler,
# which handles the flow of the data and actions between the Parser,
# SerialCommunication and the widget tree.
#

import SerialThread
import Parser
import time
import os
import sys
import signal
import MyKivyWidgets
import threading 
import time
import atexit


##
# Handles the flow of Data from the SerialThread.
# Inserts these Data (if one block available) to the Parser and Handles the extracted Informations/Operations.
# @param self.SerialCom The SerialCommunication thread
# @param self.Parser The Parser object
# @param self.RootWidget The widget screen.
# @param self.ws The selected port.
# @param self.autoreconnect The option to determine if autoreconnect is wanted.
class ObjectHandler(threading.Thread):
	def __init__(self,widgetscreen,autoreconnect,port):
		threading.Thread.__init__(self)

		self.SerialCom = SerialThread.SerialCom(autoreconnect = autoreconnect,port = port)
		self.Parser = Parser.Parser(self.SerialCom)
		self.RootWidget = None
		self.ws = widgetscreen
		self.selectedport = None
		self.autoreconnect = autoreconnect

	##
	# Checks itself and traverses all Children,
	# to find the wanted Widget by uid iteratively.
	# Returns the widget or none if its not found.
	# @param uid The widgets' universal identification of the wanted widget.
    # @param RootWidget The option to determine if autoreconnect is wanted.
	def getWidget_byuid(self,uid,RootWidget):
		childlist = [RootWidget]
		while(childlist != []):
			cur = childlist.pop()
			if cur.Uid == uid:
				return cur
			for child in cur.children:
				childlist.append(child)
		return None

	##
	# Looks if the SerialThread self.SerialCom has any block to parse.
	# In case of true, the Parser does his job and parses the wanted informations. 
	# Depending on the these informations, the widgetscreen of the app is manipulated via self.ws .
	#
	def getData(self):
		if(self.SerialCom.get_blockamount() > 0):

			##print "blockamount:", self.SerialCom.get_blockamount()
			try:
				block = self.SerialCom.getnextblock()
				##print "block:", block

				ParsedTuple = self.Parser.parseblock(block)
			
			except Exception as e:
				print "EXCEPTION_:",e
				print "InputQueue>",self.SerialCom.InputQueue

			## LayoutStructure = 0
			try:
				if(ParsedTuple[0] == 0):

					self.RootWidget = ParsedTuple[1]
					self.ws.removeall()
					self.ws.add_WidgetTree(ParsedTuple[1])
			except Exception as e:
				print "EXCEPTION_:",e
				print "InputQueue>",self.SerialCom.InputQueue
			## setText '+' = 1
			try:
				if(ParsedTuple[0] == 1):
					self.getWidget_byuid(ParsedTuple[1][0],self.RootWidget).text = ParsedTuple[1][1]
			
			except Exception as e:
				print "EXCEPTION_:",e
				print "InputQueue>",self.SerialCom.InputQueue

		elif(self.SerialCom.get_blockamount() == 0 and self.SerialCom.connected == True):
			pass

	##
	# Starts the SerialCommunication
	def startCommunication(self):
		self.SerialCom.start()

	##
	# Sets SerialCommunications' port. 
	def setCommunicationport(self,port):
		self.SerialCom.firstselectedport = port##first port that was selected to remember( needed for autosearch over modulo value )
		self.SerialCom.setport(port) ##update port to the in widget 'Text_InputPort' selected

	##
	# The starting point of the ObjectHandler.
	# Contains the main loop, and control of dataflow.
	#
	def run(self):
		print "#####################################################################"
		print "###                                                               ###"
		print "###          A R D U V I Z _ V E R S I O N _ 1.2                  ###"
		print "###                                                               ###"
		print "#####################################################################"
		print ">ObjectHandlerThread started"

		self.startCommunication()
		
		lastconnectedstate = True ## to toggle between actions depending on states
		firstconnect = True ## to differ what to do when state changes


		while 1:
			if(self.SerialCom.connected == True and self.SerialCom.availableBlocks > 0):
				
				##print "blockamount", self.SerialCom.get_blockamount()

				lastconnectedstate = True
				firstconnect = False
				self.getData()
			
			if(self.SerialCom.connected == False):

				if lastconnectedstate:
					self.ws.removeall()
					self.ws.add_widget(MyKivyWidgets.MyLabel(99,"...Connecting..."))
					lastconnectedstate = False

				if self.SerialCom.keeprunning == False and self.autoreconnect == False:
					self.ws.removeall()
					self.ws.add_widget(MyKivyWidgets.MyLabel(99,"...Wasnt able to connect to port..."))
					time.sleep(2)
					self.ws.removeall()
					print ">stopping ObjectHandlerThread."
					self.ws.add_WaitingScreen()
					break

				## Actions for Handling when connection was lost

				if not firstconnect and self.autoreconnect == False: ##without autreoconnect, get back to the Waiting screen and end thread
					self.ws.removeall()
					self.SerialCom.keeprunning = False
					print ">stopping ObjectHandlerThread."
					self.ws.add_WaitingScreen()
					break

			else: ## with autoreconnect
				pass

			

					