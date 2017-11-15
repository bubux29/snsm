#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder

from kivy.properties import ObjectProperty
import KivyCalendar

import log
import formation_db
import peewee # OK: ça n'a rien à faire ici...

import inspect
from models import Cours, Trombi

def err(text):
    log.err("GESTION", text)
def info(text):
    log.info("GESTION", text)

Gestion = Builder.load_file('Gestion.kv')

def generateForm(classe):
    box=GridLayout(cols=2)
    for name, obj in inspect.getmembers(classe):
        if type(obj) == peewee.CharField:
            box.add_widget(Label(text=name))
            box.add_widget(Label(text='coucou'))
    return box

class GestionEleves(Screen):
    def __init__(self, parentscm, **kwargs):
        super(GestionEleves, self).__init__(**kwargs)
        self.parentscm = parentscm
        self.parentscm.add_widget(GestionNouvelEleve(name='NouvelEleve', parentscm=parentscm))
        self.parentscm.add_widget(GestionConsultationEleves(name='ElevesParGroupe', parentscm=parentscm, groupes=formation_db.liste_groupes_all()))
        self.parentscm.add_widget(GestionConsultationEleves(name='TousEleves', parentscm=parentscm))

class GestionNouvelEleve(Screen):
    def __init__(self, parentscm, **kwargs):
        super(GestionNouvelEleve, self).__init__(**kwargs)
        self.parentscm = parentscm

        self.add_widget(generateForm(Trombi.Eleve))

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
