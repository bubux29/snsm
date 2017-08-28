#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.lang import Builder

from kivy.properties import ObjectProperty
import KivyCalendar

import log

def err(text):
	log.err("EXPERT", text)
def info(text):
	log.info("EXPERT", text)

class MenuComment(BoxLayout):
	comments_txt = ObjectProperty(None)
	valider_btn = ObjectProperty(None)
	def __init__(self, popup=None, **kwargs):
		super(BoxLayout, self).__init__(**kwargs)
		self.orientation = "vertical"
		#self.size_hint = (.5,.5)
		self.popup=popup

	def on_valider(self, inst):
		if self.popup != None:
			self.popup.dismiss()

class ExpertMenuSub(RelativeLayout):
	def __init__(self, submenu, go_back_home, **kwargs):
		super(RelativeLayout, self).__init__(**kwargs)
		self.size_hint = (1,1)
		retour=Button(text='Retour',
				pos_hint={"top": 1, "center_x": .15},
				size_hint=(None, .1))
		retour.bind(on_release=go_back_home)
		self.add_widget(retour)
		self.add_widget(submenu)
		valid=Button(text='OK',
                             pos_hint={"top": .2, "center_x": .9},
                             size_hint=(None, .1))
		valid.bind(on_release=self.on_valid)
		self.add_widget(valid)

		# Pick all what's new
		self.retour = retour
		self.valid=valid
		self.submenu=submenu
		self.go_back_home=go_back_home

	def on_valid(self, inst):
		if self.submenu.check_on_valid():
			# Be careful to never use any instance in go_home call!!
			self.go_back_home(None)

def _pop_(popup, title, text):
	if popup == None:
		popup = Popup(title=title)
		content = MenuComment()
		content.valider_btn.bind(on_release=popup.dismiss)
		popup.content = content
		popup.size_hint = (0.5, 0.5)
	content.comments_txt.text=text
	popup.open()

def pop_warn(popup, text):
	_pop_(popup, "Attention", text)

def pop_ok(popup, text):
	_pop_(popup, "Validé", text)

class ExpertMenuEleves(BoxLayout):
	nom = ObjectProperty(None)
	prenom = ObjectProperty(None)
	naissance = ObjectProperty(None)
	popup_warning = ObjectProperty(None)
	popup_ok = ObjectProperty(None)
	debformation = ObjectProperty(None)
	telephone = ObjectProperty(None)
	courriel = ObjectProperty(None)
	est_formateur = ObjectProperty(None)
	def check_on_valid(self):
		if not self.naissance.text or not self.prenom.text or not self.nom.text or not self.courriel.text:
			pop_warn(self.popup_warning, "Veuillez remplir tous les éléments")
			return False
		else:
			pop_ok(self.popup_ok, "Le stagiaire " + self.prenom.text + " " + self.nom.text + " a bien été ajouté")
			return True

class ExpertMenuLabel(Label):
	pass

class ExpertMenuInput(TextInput):
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
		self.eleves = ExpertMenuSub(ExpertMenuEleves(), self.go_home)
		self.main = ExpertMenuMain().creer(self.swap_layout, self.eleves)
		self.currentLayout = self.main
		# De toute façon, on ne doit mettre qu'un widget
		self.main.orientation='vertical'
		if (self.currentLayout == None):
			info("fuckup")
		self.mainLayout.add_widget(self.currentLayout)
		return self

	def go_home(self, button_clicked):
		self.swap_layout(self.main)

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
