#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.lang import Builder

from kivy.properties import ObjectProperty

import log
import formation_db

MainCoursMenu = Builder.load_file("Cours.kv")

def err(text):
    log.err("COURS", text)
def info(text):
    log.info("COURS", text)

class MainCoursMenu(BoxLayout):
    titre = ObjectProperty(None)
    def __init__(self, titre, **kwargs):
        super(BoxLayout, self).__init__(**kwargs)
        self.titre.text = titre
