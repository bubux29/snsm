# -*- coding: utf-8 -*-
#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader, TabbedPanelItem
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.lang import Builder

from collections import OrderedDict

from kivy.properties import ObjectProperty

import log
import formation_db
from modelfactory import print_resultat
from models.Cours import GROUPE_ANCIENS, BilanModule, Resultat
from Formation import Formation
from ComboEdit import ComboEdit
from listeview import ListeView
from trombiview import TrombiView

from tablelayout import TableView
from cellview import StdCellView

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

class CoursGroupeSelection(GridLayout):
    pass

class CoursGroupeExistant(Screen):
    retour = ObjectProperty(None)
    bl = ObjectProperty(None)

    def on_selection(self):
        # Pour la formation, nous avons besoin de trier l'ensemble des présents
        # par groupe...
        self.dict_eleve = OrderedDict()
        liste_eleves = self.liste_presents + self.liste_anciens
        presents_set = set(liste_eleves)
        if self.groupe_anciens:
            self.liste_groupes.append(self.groupe_anciens)
        for groupe in sorted(self.liste_groupes, key=lambda x: x.nom):
            eleves_set = set(groupe.participants)
            eleves_pour_ce_groupe = list(eleves_set & presents_set)
            # On ajoute le groupe uniquement s'il contient des élèves présents
            if eleves_pour_ce_groupe:
                self.dict_eleve[groupe.nom] = eleves_pour_ce_groupe

        # Si la formation n'a pas déjà débuté
        if not self.formation_wid:
            self.formation_wid = Formation(name='fo',
                                      retour_selection=self.name,
                                      titre=self.titre,
                                      parent_scm=self.parent_scm,
                                      dict_eleves_par_groupe=self.dict_eleve,
                                      liste_presents=liste_eleves)
            self.parent_scm.add_widget(self.formation_wid)
        else:
            self.formation_wid.change_data_set(self.dict_eleve)
        self.parent.transition.direction = 'left'
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
        self.anciens = list()
        self.liste_groupes = list()
        self.formation_wid = None
        super(CoursGroupeExistant, self).__init__(**kwargs)
        self.retour.init(retour_accueil, titre, parent_scm)
        self.selections = None

    def on_pre_enter(self):
        self.update_panneau()

    def update_panneau(self):
        titre = self.titre
        if self.selections:
            self.bl.remove_widget(self.selections)

        self.selections = CoursGroupeSelection()
        self.related_groupes = formation_db.trouver_groupes_par_cours([titre])
        # Liste des groupes des stagiaires
        liste_groupe = [{'text': groupe.nom, 'elem': groupe}
                      for groupe in self.related_groupes
                         if groupe.nom != GROUPE_ANCIENS]
        self.liste_choix_groupe = ListeView(liste_groupe,
                                            True, self.on_choix_groupe)
        self.selections.add_widget(self.liste_choix_groupe)
        # Liste d'appel des stagiaires
        self.liste_choix_presents = ListeView(
                              [{'text': eleve.nom + eleve.prenom, 'elem': eleve}
                              for eleve in []],
                              True, self.on_choix_presents
                              )
        self.selections.add_widget(self.liste_choix_presents)

        groupes_anciens = [groupe for groupe in self.related_groupes
                              if groupe.nom == GROUPE_ANCIENS]
        if groupes_anciens:
            self.groupe_anciens = groupes_anciens[0]
            # Pour les anciens, il faut rajouter une texte entry pour pouvoir
            # chercher par nom
            ba = BoxLayout(orientation='vertical')
            self.selections.add_widget(ba)
            ti = TextInput(size_hint=(1,.1), multiline=False)
            ti.bind(text=self.on_ancien_tri_nom)
            ba.add_widget(ti)
            self.anciens = self.groupe_anciens.participants[:]
            self.liste_choix_anciens = ListeView(
                       sorted([{'text': eleve.nom + eleve.prenom, 'elem': eleve}
                          for eleve in self.anciens], key=lambda x: x['text']),
                              True, self.on_choix_anciens
                              )
            ba.add_widget(self.liste_choix_anciens)
        self.bl.add_widget(self.selections)

def init_liste_cours_popup(popuplist, on_choix):
    nom_de_cours = list()
    for cours in formation_db.liste_cours_all():
        nom_de_cours.append(cours.nom)
    popuplist.init(nom_de_cours, "Cours existants", on_choix)
    popuplist.hint_xy = (.3,.3)

class ConsultationEvaluationsGroupe(TabbedPanelItem):
    def __init__(self, parentscm, liste_modules, liste_eleves, **kwargs):
        super(ConsultationEvaluationsGroupe, self).__init__(**kwargs)
        self.liste_modules = liste_modules
        self.liste_eleves = liste_eleves
        self.main_box = BoxLayout(orientation='vertical')
        self.add_widget(self.main_box)
        self.recap = self.build_recap_test(liste_eleves, liste_modules)
        self.main_box.add_widget(TableView(data=self.recap, width=700, height=400))
        prin = Button(text='Imprimer', size_hint=[.1, .2],
                      on_press=self.print_result)
        self.main_box.add_widget(prin)

    def print_result(self, dummy):
        if not self.liste_modules: return
        nom_cours = self.liste_modules[0].cours.nom
        for eleve in self.liste_eleves:
            print_resultat(self.liste_modules[0].cours.nom, self.liste_modules, eleve.__str__())

    def build_recap_test(self, liste_eleves, liste_modules):
        recap = list()
        for eleve in liste_eleves:
            eleve_dict = OrderedDict()
            eleve_dict['nom'] = StdCellView.factory('E_CharField',
                                                    eleve.__str__(),
                                                    width=180, name='nom')
            for module in liste_modules:
                for test in formation_db.trouver_tests_par_modules([module]):
                    try:
                        lr = formation_db.trouver_resultats_tests_par_eleves([test], [eleve])
                        r = Resultat.synthese(lr)
                    except Exception as e:
                        print("prout", e)
                        r = Resultat(eleve=eleve, test=test).statut
                    nom_test = test.nom
                    eleve_dict[nom_test] = StdCellView.factory(
                                                    'E_CharField',
                                                    r,
                                                    width=140,
                                                    name=nom_test)

            recap.append(eleve_dict)
        return recap

    def build_recap_module(self, liste_eleves, liste_modules):
        recap = list()
        for eleve in liste_eleves:
            eleve_dict = OrderedDict()
            eleve_dict['nom'] = StdCellView.factory('E_CharField',
                                                    eleve.__str__(),
                                                    width=180, name='nom')
            for module in liste_modules:
                try:
                    l = formation_db.trouver_bilans_par_eleve([eleve], [module])
                    s = BilanModule.synthese(l)
                except Exception as e:
                    s = BilanModule(eleve=eleve, module=module).statut
                nom_module = module.nom
                eleve_dict[nom_module] = StdCellView.factory(
                                                     'E_CharField',
                                                     s,
                                                     #width=module.largeur_cellule_min,
                                                     width=140,
                                                     name=nom_module)
            recap.append(eleve_dict)
        return recap

class CoursConsultationEvaluations(Screen):
    def __init__(self, parentscm, nom_cours, **kwargs):
        self.nom_cours = nom_cours
        self.parentscm = parentscm
        super(CoursConsultationEvaluations, self).__init__(**kwargs)
        nb = TabbedPanel(cols=1, spacing=5, padding=5, do_default_tab=False)
        self.add_widget(nb)
        liste_groupes = formation_db.trouver_groupes_par_cours([nom_cours])
        liste_modules = formation_db.trouver_modules_par_cours(formation_db.trouver_cours([nom_cours]))
        for gr in liste_groupes:
            ce = ConsultationEvaluationsGroupe(parentscm, liste_modules, gr.participants, text=gr.__str__())
            nb.add_widget(ce)
        retour = TabbedPanelHeader(text='Retour')
        retour.bind(on_release=self.retour)
        nb.add_widget(retour)

    def retour(self, instance):
        self.parentscm.transition.direction = 'right'
        self.parentscm.current = self.nom_cours

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

#class MainCoursMenu(BoxLayout):
class MainCoursMenu(Screen):
    retour = ObjectProperty(None)
    def __init__(self, titre, retour_accueil, parent_scm, **kwargs):
        super(MainCoursMenu, self).__init__(**kwargs)
        self.retour_accueil = retour_accueil
        parent_scm.add_widget(CoursGroupeExistant(name='ex', titre=titre, retour_accueil=retour_accueil, parent_scm=parent_scm))
        parent_scm.add_widget(CoursConsultationEvaluations(name='ce',
                                                          parentscm=parent_scm,
                                                          nom_cours=titre))

class MainCoursScreenManager(BoxLayout):
    def __init__(self, titre, retour_accueil, **kwargs):
        super(MainCoursScreenManager, self).__init__(**kwargs)
        self.titre = titre
        self.scm = ScreenManager()
        self.add_widget(self.scm)
        self.scm.add_widget(MainCoursMenu(name=titre, titre=titre, retour_accueil=retour_accueil, parent_scm=self.scm))
        self.scm.current = titre
