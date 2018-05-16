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
    def get_value(self):
        return self.text

class GestionListeChoixUnique(Button):
    def __init__(self, titre, liste_de_val, cls_associee = None, **kwargs):
        super(GestionListeChoixUnique, self).__init__(text=titre, **kwargs)
        self.cls_associee = cls_associee
        dropdown = DropDown()
        for value in liste_de_val:
            btn = Button(text=value, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)
        self.bind(on_release=dropdown.open)
        self.dropdown = dropdown
        dropdown.bind(on_select=lambda instance, x: setattr(self, 'text', x))
    def get_value(self):
        if self.cls_associee:
            # Choix unique: premier element d'une eventuelle liste
            return trouver_elems(self.cls_associee, [self.text])[0]
        else:
            return self.text

class GestionListeChoixMultiples(BoxLayout):
    def __init__(self, liste_choix, cls_associee=None, **kwargs):
        super(GestionListeChoixMultiples, self).__init__(**kwargs)
        self.choix = ListeView(liste_choix, True)
        self.cls_associee = cls_associee
        self.add_widget(self.choix)
    def get_value(self):
        # S'il y a une classe associée, il faut alors trouver les
        # objets en fonction des noms choisis
        cls = self.cls_associee
        if cls:
            return trouver_elems(cls, self.choix.liste_des_textes)
        else:
            return self.choix.liste_des_textes

class GestionChoixDate(DatePicker):
    def get_value(self):
        [self.text]

def gti(nom_champ, class_obj, current_values = None):
    # Si jamais, dans le design, on limite les choix à un ensemble fermé
    if getmember(class_obj, 'choices'):
        liste_de_vals = [ value for enum, value in class_obj.choices ]
        return GestionListeChoixUnique(nom_champ, liste_de_vals)
    else:
        return GestionTextInput()
def dp(nom_champ, class_obj, current_values = None):
    return GestionChoixDate(multiline='False', size_hint=(None, .1), pHint=(0.4, 0.4))
def cb(nom_champ, class_obj, current_values = None):
    return CheckBox()
def dc(nom_champ, class_obj, current_values = None):
    liste_de_vals = [ u.__str__() for u in formation_db.liste_all_from(class_obj.rel_model)]
    return GestionListeChoixUnique(nom_champ, liste_de_vals, class_obj.rel_model)
def ddc(nom_champ, class_obj, current_values = None):
    l = [ {'text': c.__str__()} for c in formation_db.liste_all_from(class_obj.rel_model) ]
    return GestionListeChoixMultiples(l, class_obj.rel_model)
        

widgetDict=dict(
E_CharField=gti,
E_TextField=gti,
E_DateField=dp,
E_BoolField=cb,
E_LinkField=dc,
E_MultiLinkField=ddc,
)

def trouver_func(cls):
    return {
            Trombi.Eleve: formation_db.trouver_eleve
           }.get(cls, formation_db.trouver_par_nom)

def trouver_elems(cls, liste_textes):
    func = trouver_func(cls)
    return [ func(nom, cls) for nom in liste_textes ]

def generateForm(classe, instance = None):
    box=GridLayout(cols=2)
    fdict=dict([ (name, obj)
              for name, obj in inspect.getmembers(classe,
                                        lambda x: dbHelper.isType(type(x)))
              if classe.requis.count(name)])
    box.reponses = list()
    for nom_champ in classe.requis:
        box.add_widget(Label(text=fdict[nom_champ].verbose_name))
        ty=dbHelper.whatType(type(fdict[nom_champ]))
        if instance:
            values = getmember(instance, nom_champ)
        else:
            values = None
        reponse = widgetDict[ty](nom_champ, fdict[nom_champ], values)
        reponse.champ = nom_champ
        box.add_widget(reponse)
        box.reponses.append(reponse)
    box.add_widget(Widget())
    return box

def is_related(classe, elem):
    return whatType(type(getmember(classe, elem))) == 'E_MultiLinkField' \
            or whatType(type(getmember(classe, elem))) == 'E_LinkField'

def ajouter_nouveau(classe, **elems):
    # Malheureusement, la création d'un nouvel objet en base ne peut pas se faire
    # directement avec des cross-reference (ManyToMany).
    # On crée d'abord l'objet, ensuite on ajoute les cross-ref
    cross_ref = { cr: elems[cr] for cr in elems.keys()
                    if is_related(classe, cr) }
    not_cross_ref = { r: elems[r] for r in elems.keys()
                        if r not in cross_ref }
    obj = classe.create(**not_cross_ref)
    for elem in cross_ref.keys():
        getmember(obj, elem).add(cross_ref[elem])
    obj.save()

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
            # TODO: tester les champs qui ne sont pas ManyToMany
            # puis créer l'objet avec uniquement les champs qui ne sont pas 
            # ManyToMany, ensuite, pour chacun des ManyToMany, rajouter les
            # champs... merci peewee :-)
            nouveau[reponse.champ] = reponse.get_value()
            print('Au champ', reponse.champ, 'on a', nouveau[reponse.champ])
        try:
            print(nouveau)
            ajouter_nouveau(self.classe, **nouveau)
            #le_ptit = self.classe.create(**nouveau)
            #le_ptit.save()
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
        
    def on_pre_enter(self):
        self.updatelist()
        self.propagatesize(None, None)

    def propagatesize(self, instance, pos):
        self.tableView.size = self.core.size

    def updatelist(self):
        if self.tableView:
            self.core.remove_widget(self.tableView)
        self.tableView = TableView(data=consultationElements(self.classe))
        self.core.add_widget(self.tableView)

    def supprimer_elem(self):
        pass

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
