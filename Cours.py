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
from models.Cours import GROUPE_ANCIENS
from Formation import Formation
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
    def __init__(self, **kwargs):
        super(CoursRetourBox, self).__init__(**kwargs)

    def updates(self, name=None, source=None, value=None):
        if name == 'retour_accueil':
            self.retour_accueil = value
        elif name == 'titre':
            self.titre = value
        elif name == 'manager':
            self.manager = value

    def init(self, retour_accueil, titre, manager):
        self.retour_accueil = retour_accueil
        self.titre = titre
        self.manager = manager

class CoursGroupeExistant(Screen):
    retour = ObjectProperty(None)
    bl = ObjectProperty(None)

    def on_selection(self):
        # Pour la formation, nous avons besoin de trier l'ensemble des présents
        # par groupe...
        self.dict_eleve = dict()
        liste_eleves = self.liste_presents + self.liste_anciens
        presents_set = set(liste_eleves)
        self.liste_groupes.append(self.groupe_anciens)
        for groupe in sorted(self.liste_groupes, key=lambda x: x.nom):
            eleves_set = set(groupe.participants)
            eleves_pour_ce_groupe = list(eleves_set & presents_set)
            # On ajoute le groupe uniquement s'il contient des élèves présents
            if eleves_pour_ce_groupe:
                self.dict_eleve[groupe.nom] = eleves_pour_ce_groupe

        # Si la formation n'a pas déjà débuté
        if not self.formation_wid:
            self.parent_scm.add_widget(
                            Formation(name='fo',
                                      retour_accueil=self.retour_accueil,
                                      titre=self.titre,
                                      parent_scm=self.parent_scm,
                                      dict_eleves_par_groupe=self.dict_eleve,
                                      liste_presents=liste_eleves
                            ))
        else:
            self.formation_wid.change_data_set(self.dict_eleve)
        self.parent.current = 'fo'

    def on_choix_presents(self, liste_noms, liste_eleves):
        # A chaque fois, la liste des groupes (donc la liste complète des élèves
        # peut avoir été augmentée, du coup, pour être sûr, on reprend cette
        # liste
        self.liste_presents = liste_eleves[:]

    def on_choix_groupe(self, liste_noms, liste_groupes):
        # Des qu'on sélectionne ou déselectionne un groupe, il faut mettre à
        # jour la liste des élèves... cette liste permettra de choisir les
        # absents.
        self.eleves = list(formation_db.liste_eleves_by_groupe(liste_noms))
        # On gère l'unicité des noms d'élèves grâce au 'set' du python...
        # Fort pratique!!
        ll = set(self.eleves)
        dic = sorted([{'text': participant.__str__(), 'elem': participant}
               for participant in ll], key=lambda x: x['text'])
        self.liste_choix_presents.setDataDict(dic)
        self.liste_groupes = liste_groupes

    def on_ancien_tri_nom(self, ti, value):
        dic = sorted([{'text': participant.__str__(), 'elem': participant}
            for participant in self.anciens
            if value in participant.__str__().lower()], key=lambda x: x['text'])
        self.liste_choix_anciens.setDataDict(dic)

    def on_choix_anciens(self, liste_noms, liste_anciens):
        self.liste_anciens = liste_anciens[:]

    def __init__(self, retour_accueil, titre, parent_scm, **kwargs):
        self.titre = titre
        self.retour_accueil = retour_accueil
        self.parent_scm = parent_scm
        self.liste_presents = list()
        self.liste_anciens = list()
        self.formation_wid = None
        super(CoursGroupeExistant, self).__init__(**kwargs)
        self.retour.init(retour_accueil, titre, parent_scm)
        self.related_groupes = formation_db.liste_groupes_by_cours([titre])
        # Liste des groupes des stagiaires
        liste_groupe = [{'text': groupe.nom, 'elem': groupe}
                      for groupe in self.related_groupes
                         if groupe.nom != GROUPE_ANCIENS]
        self.liste_choix_groupe = ListeView(liste_groupe,
                                            True, self.on_choix_groupe)
        self.bl.add_widget(self.liste_choix_groupe)
        # Liste d'appel des stagiaires
        self.liste_choix_presents = ListeView(
                              [{'text': eleve.nom + eleve.prenom, 'elem': eleve}
                              for eleve in []],
                              True, self.on_choix_presents
                              )
        self.bl.add_widget(self.liste_choix_presents)
        # Pour les anciens, il faut rajouter une texte entry pour pouvoir
        # chercher par nom
        ba = BoxLayout(orientation='vertical')
        self.bl.add_widget(ba)
        ti = TextInput(size_hint=(1,.1), multiline=False)
        ti.bind(text=self.on_ancien_tri_nom)
        ba.add_widget(ti)
        self.groupe_anciens = [groupe for groupe in self.related_groupes
                              if groupe.nom == GROUPE_ANCIENS][0]
        self.anciens = self.groupe_anciens.participants[:]
        self.liste_choix_anciens = ListeView(
                       sorted([{'text': eleve.nom + eleve.prenom, 'elem': eleve}
                          for eleve in self.anciens], key=lambda x: x['text']),
                              True, self.on_choix_anciens
                              )
        ba.add_widget(self.liste_choix_anciens)
                              

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
