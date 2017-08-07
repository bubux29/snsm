#!/usr/bin/env python3

from kivy.app import App
#kivy.require("1.8.0")
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.widget import Widget

#Widgets = Builder.load_file("SimpleKivy2.kv")

class Widgets(Widget):
    pass
	

class SimpleKivy2(App):
    def build(self):
        return Widgets()
		

if __name__ == "__main__":
    SimpleKivy2().run()
