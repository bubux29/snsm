#!/usr/bin/env python3
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.properties import ObjectProperty

from Apropos import Apropos
from MainMenu import ExpertMenuLayout
#from Cours import MainCoursMenu
from Cours import MainCoursScreenManager

import formation_db
import log

SnsmMain = Builder.load_file("Main.kv")

def info(text):
    log.info('MAIN', text)

class Menu_Principal():
    cours = ObjectProperty(None)

class Main(Widget):
    current_cours = ""
    notebook = ObjectProperty(None)

    def bouton_presse(self, instance):
        nom_cours = instance.text
        self.current_cours = nom_cours
        if not self.cours_sm.has_screen(nom_cours):
            cours = Screen(name=nom_cours)
            #cours.add_widget(MainCoursMenu(nom_cours, self.retour_accueil))
            cours.add_widget(MainCoursScreenManager(nom_cours, self.retour_accueil))
            self.cours_sm.add_widget(cours)
        self.cours_sm.transition.direction = 'left'
        self.cours_sm.current = nom_cours
        self.accueil_tab.text = nom_cours
 
    def retour_accueil(self, instance):
        info('Retour accueil')
        self.cours_sm.transition.direction = 'right'
        self.cours_sm.current = 'menu_principal'
        self.accueil_tab.text = 'Accueil'

    #def __init__(self, **kwargs):
        #super(Main, self).__init__(**kwargs)
    def creer(self):
        self.cours_sm = ScreenManager()
        self.cours_sm.size_hint = (1,1)
        menu_cours = BoxLayout(orientation="vertical", padding=40)
        boutons = GridLayout(cols=2)
        menu_cours.add_widget(boutons)

        for cours in formation_db.liste_cours_all():
            button = Button(text=str(cours),
                    color=(1,1,1,1),
                    font_size=20, size_hint=(1,0.1),
                    markup=True)
            boutons.add_widget(button)
            button.bind(on_press=self.bouton_presse)
        scm = Screen(name='menu_principal')
        scm.add_widget(menu_cours)
        self.cours_sm.add_widget(scm)
        self.cours_sm.current = scm.name

        # Ajout de l'écran d'accueil aux onglets
        tab = TabbedPanelItem()
        tab.text = "Accueil"
        tab.add_widget(self.cours_sm)
        self.notebook.add_widget(tab)
        self.notebook.set_def_tab(tab)
        self.accueil_tab = tab

        # Ajout de l'écran de gestion aux onglets
        tab = TabbedPanelItem()
        tab.text = "Gérer"
        tab.add_widget(ExpertMenuLayout().creer())
        self.notebook.add_widget(tab)
        self.gestion_tab = tab

        # Ajout de l'écran d'Apropos aux onglets
        tab = TabbedPanelItem()
        tab.text = "A propos"
        tab.add_widget(Label(text="Bienvenue à la SNSM"))
        self.notebook.add_widget(tab)
        self.apropos_tab = tab
        
        return self


class SnsmMain(App):
    def build(self):
        return Main().creer()

