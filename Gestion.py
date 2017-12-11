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

from listeview import ListeView

import log
import formation_db

import inspect
from models import Cours, Trombi, dbHelper
from models.dbDefs import FieldType

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
        box.add_widget(widgetDict[ty[0]](name, fdict[name]))
    box.add_widget(Widget())
    return box

def generateGridConsultation(classe):
    box=GridLayout(cols=len(classe.affichage))
    # Sur la première ligne on met les champs
    for name in classe.affichage:
        box.add_widget(Label(text=name))
    return box

class GestionEleves(Screen):
    def __init__(self, parentscm, **kwargs):
        super(GestionEleves, self).__init__(**kwargs)
        self.parentscm = parentscm
        self.parentscm.add_widget(GestionNouvelEleve(name='NouvelEleve', parentscm=parentscm))
        self.parentscm.add_widget(GestionConsultationEleves(name='ElevesParGroupe', parentscm=parentscm, pargroupe=True))
        self.parentscm.add_widget(GestionConsultationEleves(name='TousEleves', parentscm=parentscm))

class GestionNouvelEleve(Screen):
    core = ObjectProperty(None)
    def __init__(self, parentscm, **kwargs):
        super(GestionNouvelEleve, self).__init__(**kwargs)
        self.parentscm = parentscm
        self.core.add_widget(generateForm(Trombi.Eleve))
    def enregistreNouvelEleve(self):
        print('OK podium')

class PanneauDetailsEleve(BoxLayout):
    eleve = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(PanneauDetailsEleve, self).__init__(**kwargs)
        # Il aurait fallu que le self.eleve soit défini maintenant, ce qui n'est
        # pas le cacas!!
        self.drawn=False

    def draw(self):
        if self.drawn == False:
            self.drawn=True
        else:
            return
        self.add_widget(Image(source=self.eleve.photo_path))
        self.add_widget(Label(text=self.eleve.__str__()))

class PanneauConsultationEleve(Screen):
    eleve = ObjectProperty(None)
    def __init__(self, eleve, **kwargs):
        self.eleve=eleve
        super(PanneauConsultationEleve, self).__init__(**kwargs)

class DefaultTab(Screen):
    pass

class GestionConsultationEleves(Screen):
    principal = ObjectProperty(None)
    def on_choix_groupe(self, liste_nom_groupe, liste_groupe):
        for groupe in liste_groupe:
            self.liste_choix_eleves.data = [
                                     {'text': eleve.__str__(), 'elem': eleve}
                                     for eleve in
                                         sorted(
                                             groupe.participants,
                                             key=lambda eleve: eleve.__str__()
                                         )
                                     ]

    def on_choix_eleve(self, liste_noms, liste_eleves):
        for nom in liste_noms:
            self.scm.current=nom

    def on_retour(self, hein):
        self.parentscm.transition.direction='right'
        self.parentscm.current='GestionEleves'

    def __init__(self, parentscm, pargroupe=False, **kwargs):
        super(GestionConsultationEleves, self).__init__(**kwargs)
        self.parentscm = parentscm
        groupes=None
        liste_eleves=[{'text': eleve.__str__(), 'elem': eleve}
                       for eleve in formation_db.liste_eleves_all()]
        bi=BoxLayout(orientation='vertical', size_hint=(.2,1))
        self.principal.add_widget(bi)
        button=Button(text='Retour', on_press=self.on_retour, size_hint=(1,.1))
        bi.add_widget(button)
        if pargroupe == True:
            groupes=formation_db.liste_groupes_all()
            liste_groupes=[{'text': groupe.__str__(), 'elem': groupe}
                          for groupe in formation_db.liste_groupes_all()]
            self.liste_choix_groupe = ListeView(liste_groupes,
                                                False, self.on_choix_groupe)
            bi.add_widget(Label(text='Groupe', size_hint=(1,.1)))
            bi.add_widget(self.liste_choix_groupe)

            bi=BoxLayout(orientation='vertical', size_hint=(.2,1))
            self.principal.add_widget(bi)
            liste_eleves=[{'text': eleve.__str__(), 'elem': eleve}
                          for eleve in []]
        self.liste_choix_eleves = ListeView(liste_eleves,
                                               False, self.on_choix_eleve)
        bi=BoxLayout(orientation='vertical', size_hint=(.2,1))
        bi.add_widget(Label(text='Eleve', size_hint=(1,.1)))
        bi.add_widget(self.liste_choix_eleves)
        self.principal.add_widget(bi)

        # Création des panneaux des élèves
        self.scm = ScreenManager()
        self.scm.add_widget(DefaultTab(name='default'))
        for eleve in formation_db.liste_eleves_all():
            self.scm.add_widget(PanneauConsultationEleve(name=eleve.__str__(), eleve=eleve))
        self.principal.add_widget(self.scm)

class GestionEvaluationGroupes(Screen):
    def __init__(self, parentscm, nom_cours, **kwargs):
        liste_groupes = formation_db.trouver_groupes_par_cours(nom_cours)
        liste_modules = formation_db.trouver_modules_par_cours(nom_cours)
        # Construction du dictionnaire à afficher:
        liste_bilans = list()
        for groupe in liste_groupes:
            for eleve in groupe.participants:
                dic = dict()
                dic['nom'] = eleve.__str__()
                liste_bilans = formation_db.trouver_bilans_par_eleve(eleve, liste_modules)
                for bilan in liste_bilans:
                    module = bilan.module
                    dic[module.nom] = bilan.__str__()
                liste_bilans.append(dic)
        self.add_widget(TableView(liste_bilans, '400dp'))

class GestionCours(Screen):
    pass

class GestionLieux(Screen):
    def __init__(self, parentscm, **kwargs):
        super(GestionLieux, self).__init__(**kwargs)
        self.parentscm = parentscm

class NouveauModule(Screen):
    core = ObjectProperty(None)
    def __init__(self, parentscm, **kwargs):
        super(NouveauModule, self).__init__(**kwargs)
        self.parentscm = parentscm
        self.core.add_widget(generateForm(Cours.ModuleFormation))

class GestionModules(Screen):
    core = ObjectProperty(None)
    def __init__(self, parentscm, **kwargs):
        super(GestionModules, self).__init__(**kwargs)
        self.parentscm = parentscm
        self.core.add_widget(generateGridConsultation(Cours.ModuleFormation))
        self.parentscm.add_widget(NouveauModule(name='NouveauModule', parentscm=parentscm))

class GestionTests(Screen):
    def __init__(self, parentscm, **kwargs):
        super(GestionTests, self).__init__(**kwargs)
        self.parentscm = parentscm

class GestionMenuPrincipal(Screen):
    def __init__(self, parentscm, **kwargs):
        super(GestionMenuPrincipal, self).__init__(**kwargs)
        self.parentscm=parentscm
        self.parentscm.add_widget(GestionEleves(name='GestionEleves', parentscm=parentscm))
        self.parentscm.add_widget(GestionLieux(name='GestionLieux', parentscm=parentscm))
        self.parentscm.add_widget(GestionModules(name='GestionModules', parentscm=parentscm))
        self.parentscm.add_widget(GestionTests(name='GestionTests', parentscm=parentscm))

class GestionSCM(ScreenManager):
    def __init__(self, **kwargs):
        super(GestionSCM, self).__init__(**kwargs)
        self.add_widget(GestionMenuPrincipal(name='GestionMenuPrincipal', parentscm=self))
        self.current = 'GestionMenuPrincipal'
