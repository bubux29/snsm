#!/usr/bin/env python3
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.lang import Builder

from kivy.properties import ObjectProperty
import KivyCalendar

import log

def err(text):
	log.err("EXPERT", text)
def info(text):
	log.info("EXPERT", text)

class ExpertMenuEleves(BoxLayout):
	pass

class ExpertMenuMain(BoxLayout):
	eleves_bouton = ObjectProperty(None)

	def __init__(self, **kwargs):
		super(ExpertMenuMain, self).__init__(**kwargs)
		info("Init expertmenumain")

	def bind_eleve(self, fun):
		self.swap_fun(self.eleve_layout)
	def creer(self, fun, lvlayout):
		self.eleve_layout = lvlayout
		self.swap_fun = fun
		self.eleves_bouton.bind(on_release=self.bind_eleve)
		return self

class ExpertMenuLayout(Widget):
	mainLayout = ObjectProperty(None)
	main = None
	eleves = None
	currentLayout = None
	#def __init__(self, **kwargs):
		#super(ExpertMenu, self).__init__(**kwargs)

	def creer(self):
		info("coucou les cons")
		#self.main = ExpertMenuMain()
		#self.mainLayout.add_widget(Label(text="coucou"))
		self.eleves = ExpertMenuEleves()
		self.main = ExpertMenuMain().creer(self.swap_layout, self.eleves)
		self.currentLayout = self.main
		if (self.currentLayout == None):
			info("fuckup")
		self.mainLayout.add_widget(self.currentLayout)
		return self

	def swap_layout(self, layout_new):
		if  (self.currentLayout.parent):
			self.mainLayout.remove_widget(self.currentLayout)
		if not (layout_new.parent):
			self.currentLayout = layout_new
			self.mainLayout.add_widget(layout_new)
		else:
			err("Oops")


class MainMenu(Widget):
	menu_cours = ObjectProperty(None)

MainMenu = Builder.load_file ("MainMenu.kv")
