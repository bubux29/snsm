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

from kivy.uix.videoplayer import VideoPlayer

import datetime, os, sys

from kivy.properties import ObjectProperty, BooleanProperty

import log
import formation_db
from ComboEdit import ComboEdit
from listeview import ListeView
from trombiview import TrombiView

from videorecorder import VideoRecorder

def err(text):
    log.err("FORMATION", text)
def info(text):
    log.info("FORMATION", text)

Formation = Builder.load_file("Formation.kv")

VIDEO_PATH="./data/video"

class Video():
    def __init__(self, eleve, date):
        self.nom = date
        self.path = VIDEO_PATH + "/" + eleve + "/" + date + ".avi"
        try:
            #print("je crée:", os.path.dirname(self.path))
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
        except:
            pass
        #print("On sauve:", self.path)

class PanneauVideo(BoxLayout):
    capture_bouton = ObjectProperty(None)
    consultation = ObjectProperty(None)
    camera = ObjectProperty(None)
    enregistrement_en_cours = False
    name = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PanneauVideo, self).__init__(**kwargs)
        self.liste_video = list()
        self.liste_video_view = ListeView([], False, self.on_affiche_video)
        #self.consultation.add_widget(self.liste_video)
        self.current_video = None
        self.popup = Popup(title='Video', on_dismiss=self.resume_video)
        self.popup.size_hint = (.8, .8)

    def on_affiche_video(self, nom_video, video):
        if not video : return
        print("On va jouer:", video[0].path)
        self.playing_video = VideoPlayer(source=video[0].path, state='play')
        self.popup.content = self.playing_video
        # On arrête les enregistrements quand on affiche une vidéo
        # TODO: savoir si on le fait vraiment ou pas!
        self.play_video(False)
        self.popup.open()

    def stop_enreg(self):
        if self.enregistrement_en_cours == False:
            return
        self.capture_bouton.text = "Capture"
        self.enregistrement_en_cours = False
        self.enreg_thread.stop()
        self.liste_video.append(self.current_video)
        self.current_video = None
        # Putain mais comment on fait pour avoir les ids initialisés dans le
        # constructeur ????!!!!
        try:
            self.consultation.add_widget(self.liste_video_view)
        except:
            pass
        self.liste_video_view.setDataDict([{'text': vid.nom, 'elem': vid} for vid in self.liste_video])

    def start_enreg(self):
        self.capture_bouton.text = "Stop Capture"
        self.enregistrement_en_cours = True
        timestr = datetime.datetime.now().strftime('%Hh%Mm%Ss')
        self.current_video = Video(self.name, timestr)
        #self.enreg_thread = VideoRecorder("foformation.avi")
        self.enreg_thread = VideoRecorder(self.current_video.path)
        self.enreg_thread.start()

    def resume_video(self, *extras):
        self.play_video(True)
        # On évite de se reprendre la sélection de la vidéo au moment de la
        # modification de la liste des vidéos (i-e après capture d'une vidéo)
        self.liste_video_view.clear_selection()

    def play_video(self, bo):
        self.camera.play=bo
        if bo == False:
            self.stop_enreg()

    def capture(self):
        if self.enregistrement_en_cours == True:
            self.stop_enreg()
        else:
            self.start_enreg()

class PanneauNote(BoxLayout):
    textinput = ObjectProperty(None)
    consultation = ObjectProperty(None)
    main = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(PanneauNote, self).__init__(**kwargs)
        self.liste_notes = list()
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
        self.liste_notes_view.setDataDict([{'text': tup[0], 'elem': tup}
                                     for tup in self.liste_notes])
        self.liste_notes_view.clear_selection()

    def on_affiche_note(self, liste_nom_note, liste_notes):
        if not liste_nom_note:
            self.textinput.text = ""
            return
        self.textinput.text = liste_notes[0][1]

class EcranEleve(Screen):
    notebook = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(EcranEleve, self).__init__(**kwargs)

class DefaultTab(Screen):
    pass

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
                                     for eleve in
                                         sorted(
                                             self.dict_eleves[nom_groupe], 
                                             key=lambda eleve: eleve.__str__()
                                         )
                                     ]

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
                                 [{'text': eleve.__str__(), 'elem': eleve}
                                 for eleve in []],
                                 False, self.on_choix_eleve)
        self.colonne_eleves.add_widget(self.liste_choix_eleves)

        self.scm.add_widget(DefaultTab(name='default'))
        # Maintenant il faut creer les panneaux pour chaque élève
        for eleve in liste_presents:
            self.scm.add_widget(EcranEleve(name=eleve.__str__()))
        self.scm.current = 'default'
