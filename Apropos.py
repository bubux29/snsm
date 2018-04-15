# -*- coding: utf-8 -*-
#!/usr/bin/env python3
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.lang import Builder

class Apropos(Widget):
	pass

Apropos = Builder.load_file ("Apropos.kv")
