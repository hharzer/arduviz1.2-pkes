##@package MyKivyWidgets
#
#This module provides own costum widgets (with own Uids), derived from common kivy widgets.
#
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from functools import partial

##
# Widget for Gridlayout.
#
class MyGridLayout(GridLayout):
	def __init__(self,Uid):
		super(MyGridLayout,self).__init__()
		self.Uid = Uid
		self.cols = 2
##
# Widget for BoxLayout
#
class MyLayout(BoxLayout):
	def __init__(self,Uid):
		super(MyLayout,self).__init__(orientation='vertical')
		self.Uid = Uid

##
# Widget for Label
#
class MyLabel(Label):
	def __init__(self,Uid,Text="DEFAULT"):
		super(MyLabel,self).__init__(text=Text)
		self.Uid = Uid
##
# Widget for Button
#
class MyButton(Button):
	def __init__(self,Uid,SerialCom,Text="DEFAULT"):
		super(MyButton,self).__init__(text=Text)
		self.Uid = Uid
		self.bind(on_press = partial(SerialCom.sendCB,self.uid))

##
# Widget for TextInput
#
class MyInput(TextInput):
	def __init__(self,Uid,SerialCom,Text="Default Eingabe"):
		super(MyInput,self).__init__(text=Text,multiline=False)
		self.Uid = Uid
		self.bind( on_text_validate = partial(SerialCom.sendTxt,self.text ))

##
# Widget for the port selection in the main menu.
#
class PortSelection(BoxLayout):
	def __init__(self,Uid):
		super(PortSelection,self).__init__(orientation='horizontal')
		self.Uid = Uid
		self.Text_PortInfo = TextInput(text='Type port in the TextInput.\ne.g.:\n \t\t Linux = /dev/ttyACM0 \n \t\t Win = COM2 \n \t\t MacOS = /dev/usb.modem1411',readonly=True,background_color=[0,0,0,255],foreground_color=[1,1,1,1],padding=[50,20,50,20])
		self.Text_PortInput = TextInput(text='/dev/ttyACM0',padding=[150,120,150,20])
		self.add_widget(self.Text_PortInfo)
		self.add_widget(self.Text_PortInput)

##
# Greeting Window Content
#
class GreetingContent(BoxLayout):
	def __init__(self,Popup):
		super(GreetingContent,self).__init__(orientation='vertical')
		self.TextInfo = Label(text='Welcome.\n')
		self.CloseButton = Button(text='Okey')
		self.add_widget(self.TextInfo)
		self.add_widget(self.CloseButton)
		self.CloseButton.bind(on_press=Popup.dismiss)

##
# Template widget for Diagramm, not implemented yet.
#
class MyDiagramm(Label):
	def __init__(self,Uid,Text="DEFAULT"):
		super(MyDiagramm,self).__init__(text=Text)
		self.Uid = Uid




		
