# -*- coding: utf-8 -*-
#!/usr/bin/env python3

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader, TabbedPanelItem
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.lang import Builder

from collections import OrderedDict

from kivy.properties import ObjectProperty, BooleanProperty

import log
import formation_db
from modelfactory import print_resultat
from models.Cours import GROUPE_ANCIENS, BilanModule, Resultat
from Formation import Formation
from trombiview import TrombiView

from tablelayout import TableView
from cellview import StdCellView, ListView

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

class GroupesAccordion(Accordion):
    orientation = 'vertical'

    def empty(self):
        self.clear_widgets()

class TitreEtButton(BoxLayout):
    def on_selection_tous(self, button):
        self.parent.parent.parent.on_selection_tous(button.state)

class GroupeAccordionTitle(TitreEtButton):
    pass

class GroupeAccordion(AccordionItem):
    groupe = ObjectProperty(None)
    title_template = 'GroupeAccordionTitle'
    def __init__(self, groupe, **kwargs):
        self.groupe = groupe
        self.title=self.groupe.__str__()
        data = sorted([ e for e in self.groupe.participants ], key=lambda x: x.nom)
        self.listview = ListView(data=data, has_search=True)
        self.eleves = data[:]
        super(GroupeAccordion, self).__init__(**kwargs)
        self.add_widget(self.listview)

    def __str__(self):
        return self.groupe.__str__()
    def on_width(self, instance, value):
        self.listview.width = self.width
    def on_height(self, instance, value):
        self.listview.height = self.height - self.container_title.height
    def on_selection_tous(self, value):
        if value == 'down':
            self.listview.set_selected(self.eleves)
        else:
            self.listview.set_selected([])

class CoursGroupeExistant(Screen):
    retour = ObjectProperty(None)
    bl = ObjectProperty(None)

    def on_selection(self):
        # Pour la formation, nous avons besoin de trier l'ensemble des présents
        # par groupe...
        self.dict_eleve = OrderedDict()
        liste_selectionnes = list()
        for grp_table in self.root_accordion.children:
            selected = grp_table.listview.get_selected()
            if selected:
                self.dict_eleve[grp_table.groupe.nom] = list(selected)

        # Si la formation n'a pas déjà débuté
        if not self.formation_wid:
            self.formation_wid = Formation(name='fo',
                                      retour_selection=self.name,
                                      titre=self.titre,
                                      parent_scm=self.parent_scm,
                                      dict_eleves_par_groupe=self.dict_eleve)
            self.parent_scm.add_widget(self.formation_wid)
        else:
            self.formation_wid.change_data_set(self.dict_eleve)
        self.parent.transition.direction = 'left'
        self.parent.current = 'fo'

    def on_enter(self, *args):
        if self.formation_wid and self.formation_wid.deja_enregistre:
            # Si le formateur a enregistré les résultats de la mise en situation
            # on peut remettre à jour la sélection
            pass

    def __init__(self, retour_accueil, titre, parent_scm, **kwargs):
        self.titre = titre
        self.retour_accueil = retour_accueil
        self.parent_scm = parent_scm
        self.liste_presents = list()
        self.liste_anciens = list()
        self.groupe_anciens = None
        self.anciens = list()
        self.liste_groupes = list()
        self.formation_wid = None
        self.root_accordion = GroupesAccordion()
        self.groupe_accordion = list()
        super(CoursGroupeExistant, self).__init__(**kwargs)
        self.retour.init(retour_accueil, titre, parent_scm)
        self.selections = None

    def on_pre_enter(self):
        self.update_panneau()

    def liste_groupe_accordion(self):
        return [accItem.groupe for accItem in self.root_accordion.children]

    # Quand on entre sur le panneau, on le construit
    # Cela permet de le mettre à jour quand un groupe ou un élève a été ajouté
    def update_panneau(self):
        titre = self.titre
        if self.selections:
            #if self.formation_wid and self.formation_wid.deja_enregistre:
            self.root_accordion.empty()
            self.selections.remove_widget(self.root_accordion)
            self.bl.remove_widget(self.selections)

        self.selections = CoursGroupeSelection()
        self.selections.add_widget(self.root_accordion)
        self.related_groupes = formation_db.trouver_groupes_par_cours([titre])
        # Liste des groupes des stagiaires
        liste_groupe = [groupe for groupe in self.related_groupes]
        liste_groupe_accordion = [] #self.liste_groupe_accordion()
        liste_nouveaux_groupes = [ grp for grp in liste_groupe if grp not in liste_groupe_accordion ]
        for grp in liste_nouveaux_groupes:
            it = GroupeAccordion(groupe=grp)
            self.root_accordion.add_widget(it)
        #self.root_accordion.show_off()
        self.bl.add_widget(self.selections)

class ConsultationEvaluationsGroupe(TabbedPanelItem):
    def __init__(self, parentscm, liste_modules, liste_eleves, **kwargs):
        super(ConsultationEvaluationsGroupe, self).__init__(**kwargs)
        self.liste_modules = liste_modules
        self.liste_eleves = liste_eleves
        self.main_box = BoxLayout(orientation='vertical')
        self.add_widget(self.main_box)
#        self.recap = self.build_recap_test(liste_eleves, liste_modules)
#        #self.main_box.add_widget(TableView(data=self.recap, width=700, height=400))
#        self.tabview = TableView(data=self.recap, height=400)
#        self.main_box.add_widget(self.tabview)
        self.prin = Button(text='Imprimer', size_hint=[.1, .2],
                      on_press=self.print_result)
#        self.main_box.add_widget(self.prin)
#        # Il faut que la table s'élargisse en fonction de la mainbox (son contenant)
#        self.main_box.bind(width=self.tabview.setter('width'))

    def update(self):
        self.recap = self.build_recap_test(self.liste_eleves, self.liste_modules)
        self.tabview = TableView(data=self.recap, height=400, width=self.main_box.width)
        self.main_box.clear_widgets()
        self.main_box.add_widget(self.tabview)
        self.main_box.add_widget(self.prin)
        self.main_box.bind(width=self.tabview.setter('width'))

    def print_result(self, dummy):
        if not self.liste_modules: return
        nom_cours = self.liste_modules[0].cours.nom
        # On n'imprime que les sélectionnés
        liste_eleves = [line[0].hidden for line in self.tabview.get_selected()]
        if not liste_eleves:
            liste_eleves = self.liste_eleves
        for eleve in liste_eleves:
            print_resultat(self.liste_modules[0].cours.nom, eleve.__str__(),
                            self.liste_modules)

    def build_recap_test(self, liste_eleves, liste_modules):
        recap = list()
        for eleve in liste_eleves:
            eleve_dict = OrderedDict()
            eleve_dict['nom'] = StdCellView.factory('E_CharField',
                                                    eleve.__str__(),
                                                    width=180, name='nom')
            eleve_dict['nom'].hidden = eleve
            for module in liste_modules:
                for test in formation_db.trouver_tests_par_modules([module]):
                    try:
                        lr = formation_db.trouver_resultats_tests_par_eleves([test], [eleve])
                        r = Resultat.synthese(lr)
                    except Exception as e:
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
        self.liste_obj_recap = list()
        for gr in liste_groupes:
            ce = ConsultationEvaluationsGroupe(parentscm, liste_modules, gr.participants, text=gr.__str__())
            nb.add_widget(ce)
            self.liste_obj_recap.append(ce)
        retour = TabbedPanelHeader(text='Retour')
        retour.bind(on_release=self.retour)
        nb.add_widget(retour)

    def on_pre_enter(self, *args):
        for c in self.liste_obj_recap:
            c.update()

    def retour(self, instance):
        self.parentscm.transition.direction = 'right'
        self.parentscm.current = self.nom_cours

 
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
