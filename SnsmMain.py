#!/usr/bin/env python3
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.properties import ObjectProperty

from Apropos import Apropos
from MainMenu import MainMenu

import formation_db
import log

SnsmMain = Builder.load_file("Main.kv")

def info(text):
	log.info('MAIN', text)

class Main(Widget):
	current_cours = ""
	menu_cours = ObjectProperty(None)

	def bouton_presse(self, instance):
		info('On passe à %s' % instance.text)	
		self.current_cours = instance.text

	#def __init__(self, **kwargs):
		#super(Main, self).__init__(**kwargs)
	def creer(self):
		menu_cours = self.menu_cours
		for cours in formation_db.liste_cours_all():
			button = Button(text=str(cours),
					color=(1,1,1,1),
					font_size=20, size_hint=(1,0.1),
					markup=True)
			menu_cours.add_widget(button)
			button.bind(on_press=self.bouton_presse)
		return self


class SnsmMain(App):
	def build(self):
		return Main().creer()

