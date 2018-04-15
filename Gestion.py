# -*- coding: utf-8 -*-
#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.lang import Builder

from kivy.properties import ObjectProperty
from KivyCalendar import DatePicker

from collections import OrderedDict

from listeview import ListeView
from cellview import cells, ImageViewCell, getmember

import log
import formation_db

import inspect
from models import Cours, Trombi, dbHelper
from models.dbDefs import FieldType
from tablelayout import TableView

def err(text):
    log.err("GESTION", text)
def info(text):
    log.info("GESTION", text)

Gestion = Builder.load_file('Gestion.kv')

class GestionTextInput(TextInput):
    pass

def gti(nom_champ, class_obj):
    return GestionTextInput()
def dp(nom_champ, class_obj):
    return DatePicker(multiline='False', size_hint=(None, .1), pHint=(0.4, 0.4))
def cb(nom_champ, class_obj):
    return CheckBox()
def dc(nom_champ, class_obj):
    chbtn = Button(text=nom_champ)
    dropdown = DropDown()
    for u in formation_db.liste_all_from(class_obj.rel_model):
        btn = Button(text=u.__str__(), size_hint_y=None, height=40)
        dropdown.add_widget(btn)
    chbtn.bind(on_release=dropdown.open)
    return chbtn

widgetDict=dict(
E_CharField=gti,
E_TextField=gti,
E_DateField=dp,
E_BoolField=cb,
E_LinkField=dc,
)

def generateForm(classe):
    box=GridLayout(cols=2)
    fdict=dict([ (name, obj)
              for name, obj in inspect.getmembers(classe,
                                        lambda x: dbHelper.isType(type(x)))
              if classe.requis.count(name)])
    for name in classe.requis:
        box.add_widget(Label(text=fdict[name].verbose_name))
        ty=dbHelper.whatType(type(fdict[name]))
        box.add_widget(widgetDict[ty](name, fdict[name]))
    box.add_widget(Widget())
    return box

def consultationElements(classe):
    elems = list()
    # D'abord, on voit s'il y a une image dans le modèle
    try:
        chemin = getmember(classe, 'image')[0]
    except Exception as e:
        chemin = ''
    for elem in formation_db.liste_par_classe(classe):
        elem_details = OrderedDict()
        if chemin:
            path = getmember(elem, chemin)
            elem_details[chemin] = ImageViewCell(path, width=80, name='Photo')
        elem_details = cells(elem, elem_details)
        elems.append(elem_details)
    return elems

class GestionModele(Screen):
    def __init__(self, parentscm, classe, **kwargs):
        super(GestionModele, self).__init__(**kwargs)
        self.parentscm = parentscm
        self.classe = classe
        self.core.bind(size=self.propagatesize)
        self.tableView = None
        self.updatelist()
        
    def propagatesize(self, instance, pos):
        self.tableView.size = self.core.size

    def updatelist(self):
        if self.tableView:
            self.core.remove_widget(self.tableView)
        self.tableView = TableView(data=consultationElements(self.classe))
        self.core.add_widget(self.tableView)

class GestionMenuPrincipal(Screen):
    def __init__(self, parentscm, **kwargs):
        super(GestionMenuPrincipal, self).__init__(**kwargs)
        self.parentscm=parentscm
        self.parentscm.add_widget(GestionModele(name='GestionEleves',
                                                parentscm=parentscm,
                                                classe=Trombi.Eleve))
        self.parentscm.add_widget(GestionModele(name='GestionLieux',
                                                parentscm=parentscm,
                                                classe=Cours.Lieu))
        self.parentscm.add_widget(GestionModele(name='GestionModules',
                                                parentscm=parentscm,
                                                classe=Cours.ModuleFormation))
        self.parentscm.add_widget(GestionModele(name='GestionTests',
                                                parentscm=parentscm,
                                                classe=Cours.Test))

class GestionSCM(ScreenManager):
    def __init__(self, **kwargs):
        super(GestionSCM, self).__init__(**kwargs)
        self.add_widget(GestionMenuPrincipal(name='GestionMenuPrincipal', parentscm=self))
        self.current = 'GestionMenuPrincipal'
