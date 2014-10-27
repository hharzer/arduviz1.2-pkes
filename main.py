##@package main
# This module provides the kivy app, and some global variables.
#

#My Imports
import SerialThread
import time
import ObjectHandlerThread
import MyKivyWidgets

#Kivy Imports
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from functools import partial
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView

btn_connect = Button(text='Connect.')
btn_connect_autoreconnect = Button(text='Connect with auto reconnection.')

lbl_waiting = Label(text='...Connecting...')
input_port = TextInput(text="/dev/ttyACM0")

#popup_greeting = Popup(title='Welcome',auto_dismiss=False,size_hint=(.6, .6))
##popup_greeting = ModalView(auto_dismiss=False,size_hint=(.6, .6))
#popup_greeting.content = MyKivyWidgets.GreetingContent(popup_greeting);

# @param oh global objecthandler 
# @param ws global widgetscreen
oh = None
ws = None

## 
#  Main Screen of the app.	
class MainScreen(GridLayout):
	def __init__(self, **kwargs):
		super(MainScreen, self).__init__(cols = 1,**kwargs)
		self.PortSelection = MyKivyWidgets.PortSelection(99)
		self.btn_connect = Button(text='Connect.')
		self.btn_connect_autoreconnect = Button(text='Connect with auto reconnection.')

		self.btn_connect_autoreconnect.bind(on_press=partial(self.start_connecting,autoreconnect = True))
		self.btn_connect.bind(on_press=partial(self.start_connecting,autoreconnect = False))
		self.GreetingPopup = Popup(title='Welcome',auto_dismiss=False,size_hint=(.8, .8))
		self.GreetingPopup.content = MyKivyWidgets.GreetingContent(self.GreetingPopup)
		
		##self.GreetingPopup.bind(on_dismiss=self.add_WaitingScreen())
		
		##self.GreetingPopup.open()
		##self.add_widget(Button(text="ArduViz",font_size=32));
	
		self.add_WaitingScreen()

	##
	# Adds the in code predifined waiting screen.
	def add_WaitingScreen(self):
		self.add_widget(self.PortSelection)
		self.add_widget(self.btn_connect)
		self.add_widget(self.btn_connect_autoreconnect)
		return False
	##
	# Adds a widget / widget-tree on the screen.
	def add_WidgetTree(self,Widget):
		global ws
		ws.add_widget(Widget)
		##ws.add_widget(TestWidgetTree)

	##
	# Removes all widgets.
	def removeall(self):
		ws.clear_widgets(children=None)

	##
	# Starts the Main Thread.
	@staticmethod
	def start_connecting(self,**kwargs):
			global oh

			autoreconnect = kwargs.get('autoreconnect')

			oh = ObjectHandlerThread.ObjectHandler(ws,autoreconnect,ws.PortSelection.Text_PortInput.text)
			ws.removeall
			ws.add_widget(lbl_waiting)
			oh.start()

##
# Builds the app.
class ArduVizDemo(App):
    def build(self):
    	global ws
    	##popup_greeting.open()
    	ws = MainScreen()
    	return ws

if __name__ == '__main__':
	ArduVizDemo().run()





