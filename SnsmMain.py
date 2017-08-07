#!/usr/bin/env python3
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.lang import Builder

from Apropos import Apropos
from MainMenu import MainMenu

SnsmMain = Builder.load_file("Main.kv")

class Main(Widget):
	pass

class SnsmMain(App):
	def build(self):
		return Main()

