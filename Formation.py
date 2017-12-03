#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.image import Image
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
from models.dbDefs import FieldType

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

class LigneModule(BoxLayout):
    desc_module = ObjectProperty(None)
    succes = ObjectProperty(None)
    echec  = ObjectProperty(None)
    def __init__(self, nom, **kwargs):
        self.nom = nom
        super(LigneModule, self).__init__(**kwargs)

class ResultatTest(BoxLayout):
    orientation = 'horizontal'
    def __init__(self, test_class, **kwargs):
        super(ResultatTest, self).__init__(**kwargs)
        bx=None
        if(test_class.mode == FieldType.E_CharField.value):
            bx=TextInput(multiline=False, height=10, width=30)
            self.value = self._textToText
            self.ti = bx.text
            self.add_widget(bx)
        elif(test_class.mode == FieldType.E_BoolField.value):
            bx=CheckBox()
            self.value = self._checkBoxToText
            self.cb = bx.active
            self.add_widget(bx)

    def _textToText(self):
       if(self.ti == None): return ''
       return self.ti

    def _checkBoxToText(self):
       # Cas bizarre
       if(self.cb == None): return ''
       if(self.cb == True):
           return 'True'
       else:
           return 'False'


class LigneTest(BoxLayout):
    label_module = ObjectProperty(None)
    def __init__(self, test_class, **kwargs):
        self.nom_module = test_class.nom
        super(LigneTest, self).__init__(**kwargs)
        self.result = ResultatTest(test_class)#, pos_hint={'left': 1})
        self.add_widget(self.result)
        
class LinedBox(BoxLayout):
    pass

class NoteEvaluation(BoxLayout):
    pass

class PanneauEvaluation(BoxLayout):
    core = ObjectProperty(None)
    photo = ObjectProperty(None)
    bandeau = ObjectProperty(None)
    nom_eluve = ObjectProperty(None)
    nom_eleve = ObjectProperty(None)
    liste_modules = ObjectProperty(None)
    #def __init__(self, liste_modules, nom_eleve, **kwargs):
    def __init__(self, **kwargs):
        super(PanneauEvaluation, self).__init__(**kwargs)
        self.listes_test=list()

    def creer_env(self, liste_modules, nom_eleve):
        self.core.bind(minimum_height=self.core.setter('height'))
        print('Mon eluve est:', self.nom_eluve)
        core = self.core
        self.nom_eleve.text = nom_eleve
        # Il nous faut simplement le chemin vers la photo...
        # Ca nous fait une petite requête en plus!!!
        self.eleve = formation_db.trouver_eleve(nom_eleve)
        self.photo.source = self.eleve.photo_path
        self.liste_modules = liste_modules[:]
        for module in liste_modules:
            mod = LigneModule(nom=module.nom, height=20)
            core.add_widget(mod)
            bx=LinedBox(orientation='vertical', size_hint_y=None, spacing=10, height=40*len(module.tests))
            core.add_widget(bx)
            for test in module.tests:
                test=LigneTest(test, height=20)
                self.listes_test.append(test)
                bx.add_widget(test)
            bx=LinedBox(orientation='vertical', size_hint_y=None, height=5)

class PanneauNote(BoxLayout):
    textinput = ObjectProperty(None)
    consultation = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PanneauNote, self).__init__(**kwargs)
        self.liste_notes = list()
        self.liste_notes_view = ListeView([], False, self.on_affiche_note)
        #self.consultation.add_widget(self.liste_notes_view)
        
    def sauvegarde_texte(self):
        if not self.textinput.text:
            return
        note_tuple = (datetime.datetime.now().strftime('%Hh%Mm%Ss'), self.textinput.text)
        self.liste_notes.append(note_tuple)
        try:
            self.consultation.add_widget(self.liste_notes_view)
        except:
            pass
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
    panneaueval = ObjectProperty(None)
    def __init__(self, nom_cours, **kwargs):
        cours = formation_db.trouver_cours(nom_cours)
        self.liste_modules = cours.modules
        super(EcranEleve, self).__init__(**kwargs)
        self.panneaueval.creer_env(self.liste_modules, self.name)
        #panpan=PanneauEvaluation(liste_modules=self.liste_modules, nom_eleve=self.name, size_hint=(1,None))
        #panpan.bind(minimum_height=panpan.setter('height'))
        #rol = ScrollView(size_hint=(1, None), size=(self.width, self.height))
        #rol.add_widget(panpan)
        #self.panneaueval.add_widget(rol)
        #self.panneaueval.add_widget(panpan)
        #self.panneaueval.add_widget(PanneauEvaluation(liste_modules=liste_modules, nom_eleve=self.name, size_hint=(1,None), size=(self.width, self.height)))

class DefaultTab(Screen):
    pass

class PanneauGroupe(BoxLayout):
    colonne_eleves = ObjectProperty(None)
    scm = ObjectProperty(None)

    def on_choix_eleve(self, liste_nom_eleve, liste_eleve):
        if not liste_eleve:
            return
        self.scm.current = liste_eleve[0].__str__()

    def __init__(self, liste_eleves, nom_cours, **kwargs):
        super(PanneauGroupe, self).__init__(**kwargs)
        self.nom_cours = nom_cours
        self.liste_choix_eleves = ListeView(
                                 [{'text': eleve.__str__(), 'elem': eleve}
                                 for eleve in liste_eleves],
                                 False, self.on_choix_eleve)
        self.colonne_eleves.add_widget(self.liste_choix_eleves)

        self.scm.add_widget(DefaultTab(name='default'))
        # Maintenant il faut creer les panneaux pour chaque élève
        for eleve in liste_eleves:
            self.scm.add_widget(EcranEleve(name=eleve.__str__(), nom_cours=nom_cours))
        self.scm.current = 'default'

class PanneauFinFormation(BoxLayout):
    pass

class Formation(Screen):
    nb = ObjectProperty(None)

    def change_data_set(self, new_dic):
        liste_groupe = [{'text': nom_groupe}
                        for nom_groupe in new_dic.keys()]
        self.liste_choix_groupe.setDataDict(liste_groupe)
        # Il faut créer les nouvelles pages pour les nouveaux arrivants
        # on utilise pour cela les set et moyen d'exclusion qu'ils offrent!!!
        # TODO: trouver comment mettre à plat un dictionnaire sous forme de liste

    def __init__(self, retour_accueil, titre, parent_scm, dict_eleves_par_groupe, liste_presents, **kwargs):
        self.titre = titre
        self.retour_accueil = retour_accueil
        self.parent_scm = parent_scm
        self.dict_eleves = dict_eleves_par_groupe
        super(Formation, self).__init__(**kwargs)

        for nom_groupe in self.dict_eleves.keys():
            tb = TabbedPanelItem(text=nom_groupe)
            panneaugr = PanneauGroupe(self.dict_eleves[nom_groupe], nom_cours=titre)
            tb.add_widget(panneaugr)
            self.nb.add_widget(tb)

        fin = TabbedPanelItem(text='Terminer')
        fin.add_widget(PanneauFinFormation())
        self.nb.add_widget(fin)
