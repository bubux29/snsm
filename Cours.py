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
from listeview import ListeView
from trombiview import TrombiView

MainCoursMenu = Builder.load_file("Cours.kv")

def err(text):
    log.err("COURS", text)
def info(text):
    log.info("COURS", text)

class CoursRetourBox(BoxLayout):
    cours_bl = ObjectProperty(None)
    retour = ObjectProperty(None)
    #retour_accueil = ObjectProperty(None)
    #manager = ObjectProperty(None)
    #titre = ObjectProperty(None)
    def __init__(self, **kwargs):
        #self.fbind('retour_accueil', self.updates, 'retour_accueil')
        #self.fbind('titre', self.updates, 'titre')
        #self.fbind('manager', self.updates, 'manager')
        super(CoursRetourBox, self).__init__(**kwargs)

    def updates(self, name=None, source=None, value=None):
        if name == 'retour_accueil':
            self.retour_accueil = value
        elif name == 'titre':
            self.titre = value
        elif name == 'manager':
            self.manager = value

    def init(self, retour_accueil, titre, manager):
        #self.retour.bind(on_press=retour_accueil)
        self.retour_accueil = retour_accueil
        self.titre = titre
        self.manager = manager

class CoursGroupeExistant(Screen):
    retour = ObjectProperty(None)
    bl = ObjectProperty(None)
    def on_choix_groupe(self, index):
        print ("Voici l'index: " + self.nom_de_lieux[index])

    def __init__(self, retour_accueil, titre, parent_scm, **kwargs):
        self.titre = titre
        self.retour_accueil = retour_accueil
        self.parent_scm = parent_scm
        super(CoursGroupeExistant, self).__init__(**kwargs)
        self.retour.init(retour_accueil, titre, parent_scm)
        liste_groupe = [{'text': groupe.nom} for groupe in formation_db.liste_groupes_all()]
        self.liste_choix_groupe = ListeView(liste_groupe, False)
        #popup_grp = Popup(content=self.liste_choix_groupe, title='Liste des groupe')
        self.bl.add_widget(self.liste_choix_groupe)

def init_liste_cours_popup(popuplist, on_choix):
    nom_de_cours = list()
    for cours in formation_db.liste_cours_all():
        nom_de_cours.append(cours.nom)
    popuplist.init(nom_de_cours, "Cours existants", on_choix)
    popuplist.hint_xy = (.3,.3)

class CoursGroupeNouveau(Screen):
    bouton_choix_cours = ObjectProperty(None)
    bouton_choix_eleves = ObjectProperty(None)
    retour = ObjectProperty(None)

    def on_choix_groupes(self, instance):
        print("et mange ces index :")
        for i in self.liste_choix_cours.liste_des_index:
            print(i)
        
    def __init__(self, retour_accueil, titre, parent_scm, **kwargs):
        # On positionne l'environnement nécessaire pour que tous les attributs
        # soient vus initialisés par les classes sous-jacentes
        self.titre = titre
        self.retour_accueil = retour_accueil
        self.parent_scm = parent_scm
        super(CoursGroupeNouveau, self).__init__(**kwargs)
        self.retour.init(retour_accueil, titre, parent_scm)
        self.cours_db = formation_db.liste_cours_all()
        liste_cours = [{'text': cour.nom} for cour in self.cours_db]
        self.liste_choix_cours = ListeView(liste_cours, True)
        popup_grp = Popup(content=self.liste_choix_cours, title='Liste des cours', on_dismiss=self.on_choix_groupes)
        popup_grp.size_hint = (.3,.3)
        self.bouton_choix_cours.bind(on_press=popup_grp.open)
        liste_eleves = [{'nom': eleves.__str__(), 'photo': eleves.photo_path} for eleves in formation_db.liste_eleves_all()]
        self.liste_choix_eleves = TrombiView(liste_eleves, True)
        popup_lvs = Popup(content=self.liste_choix_eleves, title='Trombi')
        popup_lvs.size_hint = (.3,.9)
        self.bouton_choix_eleves.bind(on_press=popup_lvs.open)
        
 
class CoursChoixGroupe(Screen):
    existant = ObjectProperty(None)
    temporaire = ObjectProperty(None)
    nouveau = ObjectProperty(None)
    retour = ObjectProperty(None)
    def __init__(self, titre, retour_accueil, parent_scm, **kwargs):
        self.titre = titre
        self.retour_accueil = retour_accueil
        self.parent_scm = parent_scm
        super(CoursChoixGroupe, self).__init__(**kwargs)
        self.retour.init(retour_accueil, titre, parent_scm)
        parent_scm.add_widget(CoursGroupeNouveau(name='ng', titre=titre, retour_accueil=retour_accueil, parent_scm=parent_scm))
        parent_scm.add_widget(CoursGroupeExistant(name='ex', titre=titre, retour_accueil=retour_accueil, parent_scm=parent_scm))

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
