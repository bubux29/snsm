#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.lang import Builder

from kivy.properties import ObjectProperty

import log
import formation_db
from ComboEdit import ComboEdit

MainCoursMenu = Builder.load_file("Cours.kv")

def err(text):
    log.err("COURS", text)
def info(text):
    log.info("COURS", text)

class CoursGroupeNouveau(Screen):
    choix_cours = ObjectProperty(None)
    def __init__(self, **kwargs):
        self.choix_cours.options = [Button(text=str(x)) for x in formation_db.liste_cours_all()]
        
class CoursGroupeExistant:
    def on_choix_groupe(self, index):
        print ("Voici l'index: " + self.nom_de_lieux[index])

    def __init__(self, **kwargs):
        self.nom_de_groupes = list()
        for groupe in formation_db.liste_groupes_all():
            self.nom_de_groupes.append(groupe.nom + ' (' + groupe.cours + ')')
        self.popup = PopupList(self.nom_de_groupes,
                               "Groupes existants",
                               self.on_choix_groupe)

class CoursChoixGroupe(Screen):
    existant = ObjectProperty(None)
    temporaire = ObjectProperty(None)
    nouveau = ObjectProperty(None)
    retour = ObjectProperty(None)
    def __init__(self, titre, retour_accueil, parent_scm, **kwargs):
        super(CoursChoixGroupe, self).__init__(**kwargs)
        self.retour.bind(on_press=retour_accueil)
        self.titre = titre
        parent_scm.add_widget(CoursGroupeNouveau(name='ng'))

#class MainCoursMenu(BoxLayout):
class MainCoursMenu(Screen):
    titre = ObjectProperty(None)
    retour = ObjectProperty(None)
    demarrer_formation = ObjectProperty(None)
    gerer_groupes = ObjectProperty(None)
    demarrer_evaluation = ObjectProperty(None)
    consulter_evaluation = ObjectProperty(None)
    consulter_fiches = ObjectProperty(None)
    def __init__(self, titre, retour_accueil, parent_scm, **kwargs):
        super(MainCoursMenu, self).__init__(**kwargs)
        self.retour.bind(on_press=retour_accueil)
        parent_scm.add_widget(CoursChoixGroupe(name='df', titre=titre, retour_accueil=retour_accueil, parent_scm=parent_scm))

class MainCoursScreenManager(BoxLayout):
    def __init__(self, titre, retour_accueil, **kwargs):
        super(MainCoursScreenManager, self).__init__(**kwargs)
        self.titre = titre
        self.scm = ScreenManager()
        self.add_widget(self.scm)
        self.scm.add_widget(MainCoursMenu(name=titre, titre=titre, retour_accueil=retour_accueil, parent_scm=self.scm))
        self.scm.current = titre
