#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.lang import Builder

from kivy.properties import ObjectProperty
from KivyCalendar import DatePicker

import log
import formation_db

import inspect
from models import Cours, Trombi, dbHelper

def err(text):
    log.err("GESTION", text)
def info(text):
    log.info("GESTION", text)

Gestion = Builder.load_file('Gestion.kv')

class GestionTextInput(TextInput):
    pass

def gti():
    return GestionTextInput()
def dp():
    return DatePicker(multiline='False', size_hint=(None, .1), pHint=(0.4, 0.4))
def cb():
    return CheckBox()
widgetDict=dict(
E_CharField=gti,
E_TextField=gti,
E_DateField=dp,
E_BoolField=cb
)

def generateForm(classe):
    box=GridLayout(cols=2)
    fdict=dict([ (name, obj)
              for name, obj in inspect.getmembers(classe,
                                        lambda x: dbHelper.isType(type(x)))
              if classe.affichage.count(name)])
    for name in classe.affichage:
        box.add_widget(Label(text=fdict[name].verbose_name))
        ty=dbHelper.whatType(type(fdict[name]))
        box.add_widget(widgetDict[ty[0]]())
    return box

class GestionEleves(Screen):
    def __init__(self, parentscm, **kwargs):
        super(GestionEleves, self).__init__(**kwargs)
        self.parentscm = parentscm
        self.parentscm.add_widget(GestionNouvelEleve(name='NouvelEleve', parentscm=parentscm))
        self.parentscm.add_widget(GestionConsultationEleves(name='ElevesParGroupe', parentscm=parentscm, groupes=formation_db.liste_groupes_all()))
        self.parentscm.add_widget(GestionConsultationEleves(name='TousEleves', parentscm=parentscm))

class GestionNouvelEleve(Screen):
    core = ObjectProperty(None)
    def __init__(self, parentscm, **kwargs):
        super(GestionNouvelEleve, self).__init__(**kwargs)
        self.parentscm = parentscm

        self.core.add_widget(generateForm(Trombi.Eleve))

class GestionConsultationEleves(Screen):
    def __init__(self, parentscm, groupes=None, **kwargs):
        super(GestionConsultationEleves, self).__init__(**kwargs)
        self.parentscm = parentscm
        print("Groupes:", groupes)

class GestionCours(Screen):
    pass

class GestionLieux(Screen):
    def __init__(self, parentscm, **kwargs):
        super(GestionLieux, self).__init__(**kwargs)
        self.parentscm = parentscm

class GestionMenuPrincipal(Screen):
    def __init__(self, parentscm, **kwargs):
        super(GestionMenuPrincipal, self).__init__(**kwargs)
        self.parentscm=parentscm
        self.parentscm.add_widget(GestionEleves(name='GestionEleves', parentscm=parentscm))
        self.parentscm.add_widget(GestionLieux(name='GestionLieux', parentscm=parentscm))

class GestionSCM(ScreenManager):
    def __init__(self, **kwargs):
        super(GestionSCM, self).__init__(**kwargs)
        self.add_widget(GestionMenuPrincipal(name='GestionMenuPrincipal', parentscm=self))
        self.current = 'GestionMenuPrincipal'
