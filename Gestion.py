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

from kivy.properties import ObjectProperty, StringProperty
from KivyCalendar import DatePicker

from collections import OrderedDict

from listeview import ListeView
from cellview import cells, ImageViewCell, getmember

import log
import formation_db

import inspect
from models import Cours, Trombi, dbHelper
from models.dbHelper import whatType
from models.dbDefs import FieldType
from tablelayout import TableView

def err(text):
    log.err("GESTION", text)
def info(text):
    log.info("GESTION", text)

Gestion = Builder.load_file('Gestion.kv')

class GestionTextInput(TextInput):
    pass

def dropdown_btn(titre, liste_de_val, **kwargs):
    chbtn = Button(text=titre, **kwargs)
    dropdown = DropDown()
    for value in liste_de_val:
        btn = Button(text=value, size_hint_y=None, height=40)
        btn.bind(on_release=lambda btn: dropdown.select(btn.text))
        dropdown.add_widget(btn)
    chbtn.bind(on_release=dropdown.open)
    chbtn.dropdown = dropdown
    dropdown.bind(on_select=lambda instance, x: setattr(chbtn, 'text', x))
    return chbtn

# Il faudra utiliser rel_model en cas de LinkField

def gti(nom_champ, class_obj):
    # Si jamais, dans le design, on limite les choix à un ensemble fermé
    if getmember(class_obj, 'choices'):
        liste_de_vals = [ value for enum, value in class_obj.choices ]
        return dropdown_btn(nom_champ, liste_de_vals)
    else:
        return GestionTextInput()
def dp(nom_champ, class_obj):
    return DatePicker(multiline='False', size_hint=(None, .1), pHint=(0.4, 0.4))
def cb(nom_champ, class_obj):
    return CheckBox()
def dc(nom_champ, class_obj):
    liste_de_vals = [ u.__str__() for u in formation_db.liste_all_from(class_obj.rel_model)]
    return dropdown_btn(nom_champ, liste_de_vals)
def ddc(nom_champ, class_obj):
    bx = BoxLayout()
    l = [ {'text': c.__str__()} for c in formation_db.liste_all_from(class_obj.rel_model) ]
    bx.add_widget(ListeView(l, True))
    return bx
        

widgetDict=dict(
E_CharField=gti,
E_TextField=gti,
E_DateField=dp,
E_BoolField=cb,
E_LinkField=dc,
E_MultiLinkField=ddc,
)

def generateForm(classe):
    box=GridLayout(cols=2)
    fdict=dict([ (name, obj)
              for name, obj in inspect.getmembers(classe,
                                        lambda x: dbHelper.isType(type(x)))
              if classe.requis.count(name)])
    box.reponses = list()
    for nom_champ in classe.requis:
        box.add_widget(Label(text=fdict[nom_champ].verbose_name))
        ty=dbHelper.whatType(type(fdict[nom_champ]))
        reponse = widgetDict[ty](nom_champ, fdict[nom_champ])
        reponse.champ = nom_champ
        box.add_widget(reponse)
        box.reponses.append(reponse)
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

class NouveauModele(Screen):
    classe = ObjectProperty(None)
    precedent = StringProperty('')
    def __init__(self, parentscm, **kwargs):
        super(NouveauModele, self).__init__(**kwargs)
        self.parentscm = parentscm
        self.core.add_widget(self.form)

    def on_classe(self, instance, value):
        self.form = generateForm(self.classe)

    def sauvegarder(self):
        nouveau = dict()
        for reponse in self.form.reponses:
            nouveau[reponse.champ] = reponse.get_value()
        try:
            le_ptit = self.classe.create(**nouveau)
            le_ptit.save()
        except Exception as e:
            print('Ajout', self.classe, 'not possib:', e)

class GestionModele(Screen):
    def __init__(self, parentscm, classe, **kwargs):
        super(GestionModele, self).__init__(**kwargs)
        self.parentscm = parentscm
        self.classe = classe
        self.core.bind(size=self.propagatesize)
        self.tableView = None
        self.updatelist()
        nouveau = self.name + '_nouveau'
        self.nouveau = NouveauModele(name=nouveau,
                                    parentscm=parentscm,
                                    precedent=self.name,
                                    classe=classe)
        self.parentscm.add_widget(self.nouveau)
        
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
        self.parentscm.add_widget(GestionModele(name='GestionGroupes',
                                                parentscm=parentscm,
                                                classe=Cours.Groupe))

class GestionSCM(ScreenManager):
    def __init__(self, **kwargs):
        super(GestionSCM, self).__init__(**kwargs)
        self.add_widget(GestionMenuPrincipal(name='GestionMenuPrincipal', parentscm=self))
        self.current = 'GestionMenuPrincipal'
