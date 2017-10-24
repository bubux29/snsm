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

import datetime

from kivy.properties import ObjectProperty

import log
import formation_db
from ComboEdit import ComboEdit
from listeview import ListeView
from trombiview import TrombiView

def err(text):
    log.err("FORMATION", text)
def info(text):
    log.info("FORMATION", text)

Formation = Builder.load_file("Formation.kv")

class PanneauNote(BoxLayout):
    textinput = ObjectProperty(None)
    consultation = ObjectProperty(None)
    main = ObjectProperty(None)
    liste_notes = list()
    def __init__(self, **kwargs):
        super(PanneauNote, self).__init__(**kwargs)
        self.liste_notes_view = ListeView([], False, self.on_affiche_note)
        #self.main.add_widget(self.liste_notes_view)
        #self.consultation.add_widget(self.liste_notes_view)
        
    def sauvegarde_texte(self):
        note_tuple = (datetime.datetime.now().strftime('%Hh%Mm%Ss'), self.textinput.text)
        self.liste_notes.append(note_tuple)
        try:
            self.consultation.add_widget(self.liste_notes_view)
        except:
            pass
            #print("déjà ajouté")
        #self.liste_notes_view.data = []
        self.liste_notes_view.data = [{'text': tup[0], 'elem': tup}
                                     for tup in self.liste_notes]
        print('je fais de la purée avec:', self.liste_notes_view.data)

    def on_affiche_note(self, liste_nom_note, liste_notes):
        if not liste_nom_note: return
        print("voila la liste")
        for i in liste_notes:
            print("j'ai", i[1])
        self.textinput.text = liste_notes[0][1]

class EcranEleve(Screen):
    notebook = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(EcranEleve, self).__init__(**kwargs)

class Formation(Screen):
    colonne_eleves = ObjectProperty(None)
    colonne_groupes = ObjectProperty(None)
    scm = ObjectProperty(None)

    def on_choix_eleve(self, liste_nom_eleve, liste_eleve):
        if not liste_eleve:
            return
        self.scm.current = liste_eleve[0].__str__()

    def on_choix_groupe(self, liste_nom_groupe, empty):
        for nom_groupe in liste_nom_groupe:
            self.liste_choix_eleves.data = [
                                     {'text': eleve.__str__(), 'elem': eleve}
                                     for eleve in self.dict_eleves[nom_groupe]]

    def __init__(self, retour_accueil, titre, parent_scm, dict_eleves_par_groupe, liste_presents, **kwargs):
        self.titre = titre
        self.retour_accueil = retour_accueil
        self.parent_scm = parent_scm
        self.dict_eleves = dict_eleves_par_groupe
        super(Formation, self).__init__(**kwargs)
        liste_groupe = [{'text': nom_groupe}
                        for nom_groupe in self.dict_eleves.keys()]
        self.liste_choix_groupe = ListeView(
                                       liste_groupe,
                                       False, self.on_choix_groupe)
        self.colonne_groupes.add_widget(self.liste_choix_groupe)
        self.liste_choix_eleves = ListeView(
                                 [{'text': eleve.nom + eleve.prenom,
                                   'elem': eleve} for eleve in []],
                                 False, self.on_choix_eleve)
        self.colonne_eleves.add_widget(self.liste_choix_eleves)

        # Maintenant il faut creer les panneaux pour chaque élève
        for eleve in liste_presents:
            self.scm.add_widget(EcranEleve(name=eleve.__str__()))
