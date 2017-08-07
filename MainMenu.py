#!/usr/bin/env python3
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.lang import Builder

class MainMenu(Widget):
	pass

MainMenu = Builder.load_file ("MainMenu.kv")
