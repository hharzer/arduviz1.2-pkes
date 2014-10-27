##@package Parser
# This module provides a Parser, that extracts all necessary informations.
#

import MyKivyWidgets

##
# The Parser class.
# @param self.RootWidget
# @param self.SerialCom The serial communication.
# It is given as argument to the constructor of the widgets.
# This is needed to allow callbacks.
class Parser(object):
	def __init__(self,SerialCom):
		self.RootWidget = None
		self.SerialCom = SerialCom
	##
	# Gets block, purifies it and parses it, depending on the starting sign.
	# ('#' for widget structure, '+' for setting text.)
	# 
	def parseblock(self,block):

		block = self.deleteunwanted(block)

		print "BLOCK : " , block

		if(block[0] == '#'):

			self.RootWidget = self.parseWidgetTree_start(block)
			return(0,self.RootWidget)

		if(block[0] == '+'):

			IdTextTuple = self.parseText(block)
			return (1,IdTextTuple)

	##
	# Purifies list from carriage return ('\n' and '\r').
	#
	def deleteunwanted(self,ls):
		purified_ls = []
		i = 0
		while(i < len(ls)):
			if( (ls[i] != '\n') and (ls[i] != '\r') ):
				purified_ls.append(ls[i])
			i += 1
		return purified_ls

	##
	# Parses text from list.
	#
	def parseText(self,ls):
		uid = (ord(ls[1]) - 48)
		return (uid,''.join(ls[2:-1]) )

	##
	# Parses WidgetTree. (used by parseWidgetTree_start)
	#
	def parseWidgetTree(self,root,ls):
		lslength = len(ls)
		stopid = root.Uid
		x = 0

		while ( (x < lslength)  and ( (ord(ls[x+1]) -48) != stopid) and len(ls) > (x+1) ):
			
			if(ls[x] == 'L'):
				newlayout = MyKivyWidgets.MyLayout((ord(ls[x+1]) - 48))
				root.add_widget(newlayout)

				x = 2 + x + self.parseWidgetTree(newlayout,ls[x+2:])

			if(ls[x] == 'B'):
				text = "Button " + ((str((ord(ls[x+1]) -48))))

				root.add_widget(MyKivyWidgets.MyButton( (ord(ls[x+1]) - 48) ,self.SerialCom,text))

			if(ls[x] == 'T'):
				text = "Label " + (str((ord(ls[x+1]) -48)))

				root.add_widget(MyKivyWidgets.MyLabel( (ord(ls[x+1]) -48) ,text)) 

			if(ls[x] == 'I'):
				text = "Input " + (str((ord(ls[x+1]) -48)))

				root.add_widget(MyKivyWidgets.MyInput( ord(ls[x+1]) - 48 ,self.SerialCom,text))

			if(ls[x] == 'D'):
				text = "Diagramm " + (str((ord(ls[x+1]) -48)))

				root.add_widget(MyKivyWidgets.MyDiagramm (ord(ls[x+1]) -48) )

			x += 2
		return x

	##
	# Starts parsing a WidgetTree from list.
	#
	def parseWidgetTree_start(self,ls):

		root = MyKivyWidgets.MyGridLayout(ord (ls[2]) -48)
		ls = ls[3:]
		print "ls[3:]", ls;
		##print 
		self.parseWidgetTree(root,ls)
		return root
