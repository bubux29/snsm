# -*- coding: utf-8 -*-
#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.behaviors import ButtonBehavior
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

from texteentree import TexteEntree

import formation_db
from cellview import ListView, cells, ImageViewCell, getmember

import log

import inspect
from models import Cours, Trombi, dbHelper
from models.dbHelper import whatType
from models.dbDefs import FieldType
from tablelayout import TableView
from filepreview import FilePreview
from pops import question_pop

def err(text):
    log.err("GESTION", text)
def info(text):
    log.info("GESTION", text)

Gestion = Builder.load_file('Gestion.kv')

class GestionTextInput(TexteEntree):
    current_values = ObjectProperty(None)
    multiline = False
    def on_current_values(self, instance, value):
        if self.current_values:
            self.text = self.current_values
    def get_value(self):
        return self.text

class GestionListeChoixUnique(Button):
    def __init__(self, titre, liste_de_val, current_values, cls_associee = None, **kwargs):
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
        if current_values:
            self.text = current_values

    def get_value(self):
        if self.cls_associee:
            # Choix unique: premier element d'une eventuelle liste
            return trouver_elems(self.cls_associee, [self.text])[0]
        else:
            return self.text

class GestionListeChoixMultiples(BoxLayout):
    def __init__(self, liste_choix, current_values, cls_associee=None, **kwargs):
        super(GestionListeChoixMultiples, self).__init__(**kwargs)
        self.choix = ListView(liste_choix)
        self.cls_associee = cls_associee
        self.add_widget(self.choix)
        if current_values:
            self.choix.set_selected(current_values)
    # On propage la largeur à la vue
    def on_size(self, instance, value):
        self.choix.size = self.size
    def get_value(self):
        # S'il y a une classe associée, il faut alors trouver les
        # objets en fonction des noms choisis
        cls = self.cls_associee
        # L'object ListView contient déjà les références vers les objets
        # et non seulement vers un nom
        return self.choix.get_selected()

class GestionChoixDate(TexteEntree):
    current_values = ObjectProperty(None)
    def on_current_values(self, instance, value):
        if self.current_values:
            self.text = self.current_values
    def get_value(self):
        return self.text

class GestionChoixPhoto(ButtonBehavior, Image):
    def on_press(self):
        content = FilePreview('pics/*.png', valider=self.set_image, annuler=self.fin_popup)
        self._popup = Popup(title='Choix image', content = content,
                            size_hint=(.9, .9))
        self._popup.open()
    def set_image(self, path):
        self.source = path[0]
        self.fin_popup()
    def fin_popup(self):
        self._popup.dismiss()
    def get_value(self):
        return self.source

def gti(nom_champ, class_obj, current_values = None):
    # Si jamais, dans le design, on limite les choix à un ensemble fermé
    if getmember(class_obj, 'choices'):
        liste_de_vals = [ value for enum, value in class_obj.choices ]
        return GestionListeChoixUnique(nom_champ, liste_de_vals, current_values=current_values)
    else:
        return GestionTextInput(current_values=current_values)
def dp(nom_champ, class_obj, current_values = None):
    return GestionChoixDate(multiline='False', size_hint=(None, .1), current_values=current_values)
def cb(nom_champ, class_obj, current_values = None):
    # Not implemented yet...
    return CheckBox()
def dc(nom_champ, class_obj, current_values = None):
    liste_de_vals = [ u.__str__() for u in formation_db.liste_all_from(class_obj.rel_model)]
    return GestionListeChoixUnique(nom_champ, liste_de_vals, current_values, class_obj.rel_model)
def ddc(nom_champ, class_obj, current_values = None):
    l = [ c for c in formation_db.liste_all_from(class_obj.rel_model) ]
    return GestionListeChoixMultiples(l, current_values, class_obj.rel_model)
def ib(nom_champ, classe_obj, current_values = None):
    return GestionChoixPhoto(source = current_values, height=50)
        

widgetDict=dict(
E_CharField=gti,
E_TextField=gti,
E_DateField=dp,
E_BoolField=cb,
E_LinkField=dc,
E_MultiLinkField=ddc,
E_ImageField=ib,
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
    box.reponses = list()
    # D'abord, on voit s'il y a une image dans le modèle
    try:
        images = getmember(classe, 'image')
        if not images:
            images = []
    except Exception as e:
        images = []

    for image in images:
        if image in classe.requis:
            elem = getmember(classe, image)
            box.add_widget(Label(text=elem.verbose_name))
            if instance:
                values = getmember(instance, image)
            else:
                values = None
            reponse = widgetDict['E_ImageField'](image, elem, values)
            reponse.champ = image
            box.add_widget(reponse)
            box.reponses.append(reponse)
    others = [ champ for champ in classe.requis if champ not in images ]
    fdict=dict([ (name, obj)
              for name, obj in inspect.getmembers(classe,
                                        lambda x: dbHelper.isType(type(x)))
              if name in others])
    for nom_champ in others:
        box.add_widget(Label(text=fdict[nom_champ].verbose_name))
        ty=dbHelper.whatType(type(fdict[nom_champ]))
        if instance:
            values = getmember(instance, nom_champ)
            if is_related(classe, nom_champ):
                values = list(values)
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

def vide_refs(elem):
    elem.clear()

def rajoute_refs_by_names(obj, names):
    obj.add(trouver_elems(type(obj.model_class()), names))

def rajoute_refs(obj, elems):
    obj.add(elems)

def modifier_champ(cls, inst, champ, valeur):
    q = cls.update({getmember(cls, champ): valeur}).where(cls.id == inst.id)
    q.execute()
    # On met à jour la valeur de l'instance qu'on vient de modifier
    # Opération nécessaire : en cas d'absence, il n'y a pas de mise-à-jour
    # si l'instance ne contient qu'un champ dans cette base de donnée...
    # (va comprendre)
    return cls.get(cls.id == inst.id)

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
            elem_details[chemin].hidden = elem
        elem_details = cells(elem, elem_details)
        elems.append(elem_details)
    return elems

class NouveauModele(Screen):
    classe = ObjectProperty(None)
    precedent = StringProperty('')
    instance = ObjectProperty(None)
    def __init__(self, parentscm, **kwargs):
        super(NouveauModele, self).__init__(**kwargs)
        self.parentscm = parentscm
        self.core.add_widget(self.form)

    def on_instance(self, instance, value):
        self.form = generateForm(type(self.instance), self.instance)

    def on_classe(self, instance, value):
        self.form = generateForm(self.classe)

    def sauvegarder(self):
        if not self.instance:
            self.sauvegarder_nouveau()
            self.parentscm.current = self.precedent
            self.parentscm.transition.direction = 'right'
        else:
            self.sauvegarder_modif()
            self.parentscm.current = self.precedent
            self.parentscm.transition.direction = 'right'
            self.parentscm.remove_widget(self)

    def sauvegarder_modif(self):
        inst = self.instance
        cls = type(inst)
        for reponse in self.form.reponses:
            if is_related(cls, reponse.champ):
                champ = getmember(inst, reponse.champ)
                vide_refs(champ)
                rajoute_refs(champ, reponse.get_value())
                inst.save()
            elif reponse.get_value() != getmember(inst, reponse.champ):
                inst = modifier_champ(cls, inst, reponse.champ, reponse.get_value())

    def sauvegarder_nouveau(self):
        nouveau = dict()
        for reponse in self.form.reponses:
            nouveau[reponse.champ] = reponse.get_value()
        try:
            ajouter_nouveau(self.classe, **nouveau)
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
        self.refresh()

    def refresh(self):
        self.updatelist()
        self.propagatesize(None, None)
    def propagatesize(self, instance, pos):
        self.tableView.size = self.core.size

    def updatelist(self):
        if self.tableView:
            self.core.remove_widget(self.tableView)
        self.tableView = TableView(data=consultationElements(self.classe))
        self.core.add_widget(self.tableView)

    def modifier_elem(self):
        to_modif = self.tableView.get_selected()
        if not to_modif:
            return
        # Pour l'instant, on ne gère qu'un seul élément
        # en l'occurence le premier
        to_modif = to_modif[0][0]
        obj = to_modif.hidden
        if self.parentscm.has_screen('modif'):
            self.parentscm.remove_widget(self.parentscm.get_screen('modif'))
        self.modif = NouveauModele(instance=obj,
                                   parentscm=self.parentscm,
                                   precedent=self.name,
                                   name='modif')
        self.parentscm.add_widget(self.modif)
        self.parentscm.transition.direction = 'left'
        self.parentscm.current = 'modif'

    def supprimer_elem(self):
        self.to_delete_obj = list()
        to_delete = self.tableView.get_selected()
        if len(to_delete) == 0:
            return
        text = 'Vous allez supprimer les éléments suivants:\n'
        for row in to_delete:
            c = row[0].hidden
            self.to_delete_obj.append(c)
            text += ' - ' + c.__str__() + '\n'
        question_pop(None, 'Attention suppression', text=text, on_valider=self.suppression, valider_txt='Supprimer')

    def suppression(self):
        for obj in self.to_delete_obj:
            try:
                obj.delete_instance(True, True)
            except Exception as e:
                print('Cannot delete instance:', obj.__str__(), 'because of:', e)
        self.refresh()

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
