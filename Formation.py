# -*- coding: utf-8 -*-
#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.accordion import Accordion
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.tabbedpanel import TabbedPanelItem, TabbedPanelHeader
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.lang import Builder

from kivy.properties import ObjectProperty, BooleanProperty, ListProperty, StringProperty
from kivy.uix.videoplayer import VideoPlayer

from collections import OrderedDict
import datetime, os, sys, time

import log
import formation_db
import scripts.poplib
from listeview import ListeView
from trombiview import TrombiView
from models.dbDefs import FieldType
from models.Cours import Resultat, BilanModule
from dropdownmenu import DropDownMenu
from cellview import StdCellView
from tablelayout import TableView
from choix import ChoixUnique

import pops

from videorecorder import VideoRecorder

poplib = scripts.poplib
tototal = list()

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
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
        except:
            pass

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
    def __init__(self, module, resultat, eleve, **kwargs):
        self.nom = module.nom
        self.module = module
        self.eleve = eleve
        ### TODO: voir comment copier un resultat, histoire de pouvoir
        ###       faire une comparaison complète avant d'enregistrer un nouveau
        ###       bilan
        self.origine = resultat.statut
        self.nom_groupe_toggle = eleve.__str__()
        super(LigneModule, self).__init__(**kwargs)
        if resultat.statut == BilanModule.SUCCES:
            self.succes.state = 'down'
        elif resultat.statut == BilanModule.ECHEC:
            self.echec.state = 'down'
    def bilan(self):
        if self.succes.state == 'down':
            return BilanModule.SUCCES
        elif self.echec.state == 'down':
            return BilanModule.ECHEC
        else:
            return BilanModule.NONFAIT

class ValidationResultat(ChoixUnique):
    def __init__(self, **kwargs):
        liste_choix=[ u[0] for u in Resultat.TEST_RESULTAT_CHOIX ]
        super(ValidationResultat, self).__init__(liste_choix, **kwargs)

class _ValidationResultat(Button):
    def __init__(self, statut, **kwargs):
        self.text = 'Res'
        self.height = 10
        super(ValidationResultat, self).__init__(**kwargs)
        self.text = statut
        self.dropdown = DropDown()
        for u in Resultat.TEST_RESULTAT_CHOIX:
            btn = Button(text=u[0], size_hint_y=None, height=20)
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)
        self.dropdown.bind(on_select=lambda instance,
                           x: setattr(self, 'text', x))
        self.bind(on_release=self.dropdown.open)

class ResultatTest(BoxLayout):
    orientation = 'horizontal'
    def __init__(self, test_eleve, test_class, **kwargs):
        self.test_eleve = test_eleve
        super(ResultatTest, self).__init__(**kwargs)
        bx=None
        if(test_class.mode == FieldType.E_CharField.value):
            bx=TextInput(multiline=False, height=10, width=30)
            self.value = self._textToText
            self.ti = bx
            bu = ValidationResultat(prechoix=test_eleve.statut)
            self.add_widget(bu)
            self.tv = bu
            self.statut = self._statut
            # On récupère le résultat du test (s'il y en a)
            if test_eleve.resultat:
                bx.text = test_eleve.resultat
            self.add_widget(bx)
        elif(test_class.mode == FieldType.E_TestResField.value):
            bx = ValidationResultat(prechoix=test_eleve.statut)
            self.add_widget(bx)
            self.value = self._textToText
            self.ti = bx
            self.tv = bx
            self.statut = self._statut
        # On ne sait pas trop si ce type a un sens...
        # à confirmer à l'utilisation
        #elif(test_class.mode == FieldType.E_BoolField.value):
            #bx=CheckBox()
            #self.value = self._checkBoxToText
            #self.cb = bx.active
            #self.add_widget(bx)
        else:
            print('Type de résultat non encore géré:', test_class.mode)

    def _textToText(self):
       if(self.ti == None): return ''
       return self.ti.text

    def _statut(self):
       if(self.tv == None): return
       return self.tv.text

    def _checkBoxToText(self):
       # Cas bizarre
       if(self.cb == None): return ''
       if(self.cb == True):
           return 'True'
       else:
           return 'False'

class LigneTest(BoxLayout):
    label_module = ObjectProperty(None)
    def __init__(self, eleve, resultat, test_class, **kwargs):
        self.nom = test_class.nom
        self.test_class = test_class
        self.eleve = eleve
        self.statut_origine = resultat.statut
        super(LigneTest, self).__init__(**kwargs)
        self.result = ResultatTest(resultat, test_class, pos_hint={'left': 1}, size_hint_x=.3)
        self.add_widget(self.result)
    def statut(self):
        return self.result.statut()
    def value(self):
        return self.result.value()

class LinedBox(BoxLayout):
    pass

class NoteEvaluation(BoxLayout):
    pass

class PanneauEvaluation(ScrollView):
    core = ObjectProperty(None)
    photo = ObjectProperty(None)
    bandeau = ObjectProperty(None)
    nom_eleve = StringProperty(None)
    label_eleve = ObjectProperty(None)
    liste_modules = ObjectProperty(None)
    photo_height = 80

    # Des qu'on positionne la liste des modules, on établit l'affichage
    def on_liste_modules(self, instance, value):
        start_func = time.time()
        toto = list()
        tutu = list()
        core = self.core
        self.liste_bilans = list()
        self.liste_tests=list()
        for module in self.liste_modules:
            try:
                start_lolo = time.time()
                lisres = formation_db.trouver_bilans_par_eleve([self.eleve],
                                                               [module])
                end_lolo = time.time()
                toto.append(end_lolo - start_lolo)
                res = lisres[len(lisres) - 1]
            except:
                res = BilanModule(eleve=self.eleve, module=module)
            mod = LigneModule(module=module, resultat=res, eleve=self.eleve,
                              height=20)
            self.liste_bilans.append(mod)
            core.add_widget(mod)
            bx=LinedBox(orientation='vertical', size_hint_y=None,
                        spacing=10, height=40*(len(module.tests) + 1))
            core.add_widget(bx)
            core.height += mod.height
            core.height += bx.height
            for test in module.tests:
                try:
                    start_lulu = time.time()
                    lisres = formation_db.trouver_resultats_tests_par_eleves(
                                                         [test], [self.eleve])
                    end_lulu = time.time()
                    tutu.append(end_lulu - start_lulu)
                   #resultat = Resultat.synthese(lisres)
                    resultat = lisres[len(lisres) - 1]
                except Exception as e:
                   #print('Pas de résultat pour', self.eleve.__str__(),
                         #'sur', test.nom, e)
                   # On se crée un résultat bidon
                    resultat = Resultat(test=test, eleve=self.eleve)
                test=LigneTest(self.eleve, resultat, test, height=20)
                self.liste_tests.append(test)
                bx.add_widget(test)
            bs=BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
            bs.add_widget(Label(text='Note:', size_hint_x=.1, pos_hint={'right':1}))
            mod.commentaires = TextInput(height=50)
            bs.add_widget(mod.commentaires)
            bx.add_widget(bs)
        end_func = time.time()
        tototal.append(end_func - start_func)
        print ('Total', len(tototal), ':', end_func - start_func)
        print ('Subs:', sum(toto))
        print ('Subs:', sum(tutu))
    def on_nom_eleve(self, instance, value):
        self.label_eleve.text = self.nom_eleve
        # Il nous faut simplement le chemin vers la photo...
        # Ca nous fait une petite requête en plus!!!
        self.eleve = formation_db.trouver_eleve(self.nom_eleve)
        self.photo.source = self.eleve.photo_path

    def calcule_bilans(self):
        # On retourne, par module: le tuple:
        #         (module, SUCCES/ECHEC/NT)
        return [ (bil.module, bil.bilan(), bil.commentaires, bil.origine) 
                 for bil in self.liste_bilans ]
    def calcule_resultats(self):
        # On retourne, par tests, le tuple:
        #         (nom_test, SUCCES/ECHEC/NT, valeur)
        return [ (res.test_class, res.statut(), res.value(), res.statut_origine)
                 for res in self.liste_tests ]

class PanneauNote(BoxLayout):
    textinput = ObjectProperty(None)
    consultation = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PanneauNote, self).__init__(**kwargs)
        self.liste_notes = list()
        self.liste_notes_view = ListeView([], False, self.on_affiche_note)
        
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
    liste_modules = ListProperty(None)
    def __init__(self, nom_cours, **kwargs):
        cours = formation_db.trouver_cours([nom_cours])[0]
        self.liste_modules = cours.modules
        super(EcranEleve, self).__init__(**kwargs)

    def bilan_eleve(self):
        return self.panneaueval.calcule_bilans()
    def resultats_eleve(self):
        return self.panneaueval.calcule_resultats()

class DefaultTab(Screen):
    pass

class PanneauGroupe(BoxLayout):
    colonne_eleves = ObjectProperty(None)
    scm = ObjectProperty(None)

    def on_choix_eleve(self, liste_nom_eleve, liste_eleve):
        if not liste_eleve:
            return
        self.scm.current = liste_eleve[0].__str__()

    def supprime_eleve(self, eleve):
        self.liste_eleves.remove(eleve)
        self.liste_choix_eleves.setDataDict(
                                       [{'text': eleve.__str__(), 'elem': eleve}
                                        for eleve in self.liste_eleves])

    def ajoute_nouvel_eleve(self, eleve):
        self.liste_eleves.append(eleve)
        
        self.liste_choix_eleves.setDataDict(
                                       [{'text': eleve.__str__(), 'elem': eleve}
                                        for eleve in self.liste_eleves])
        self.scm.add_widget(EcranEleve(name=eleve.__str__(), nom_cours=self.nom_cours))

    def __init__(self, liste_eleves, nom_cours, **kwargs):
        super(PanneauGroupe, self).__init__(**kwargs)
        self.nom_cours = nom_cours
        self.liste_eleves = liste_eleves
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
    ligne_formateur = ObjectProperty(None)
    ligne_lieu = ObjectProperty(None)
    mise_en_situation = ObjectProperty(None)
    terminerbutton = ObjectProperty(None)
    recapitulatif = ObjectProperty(None)
    def __init__(self, terminaison, recap, **kwargs):
        self.orientation = 'vertical'
        super(PanneauFinFormation, self).__init__(**kwargs)
        drop_list=[f.nom for f in formation_db.trouver_formateurs()]
        self.dpf = DropDownMenu(text='', drop_list=drop_list,
                                               size_hint_x=.3, size_hint_y=None,
                                               height=30)
        self.ligne_formateur.add_widget(self.dpf)

        drop_list = [ l.lieu for l in formation_db.liste_lieux_all() ]
        self.dpl = DropDownMenu(text='', drop_list=drop_list,
                                               size_hint_x=.3, size_hint_y=None,
                                               height=30)
        self.ligne_lieu.add_widget(self.dpl)
        
        self.terminerbutton.bind(on_release=terminaison)
        self.former_bilans = None
        self.recap = recap

    def nom_formateur(self):
        return self.dpf.text

    def nom_lieu(self):
        return self.dpl.text

    def nom_mise_en_situation(self):
        return self.mise_en_situation.text
    def on_size(self, instance, value):
        self.former_bilans.width = self.width

    def update(self, instance):
        if self.former_bilans:
            self.recapitulatif.remove_widget(self.former_bilans)
        # Petit recap
        self.former_bilans = TableView(data=self.recap(), width=600, height=200)
        self.recapitulatif.add_widget(self.former_bilans)
        self.recapitulatif.width = self.width

class AccordeonEleves(Accordion):
    def ajouter_eleve(self, nom, image, contenu):
        item = AccordeonEleve

class ElevesEnFormation(Accordion):
    liste_eleves = ListProperty([])
    orientation = 'vertical'
    def on_liste_eleves(self, instance, value):
        pass

class Formation(Screen):
    nb = ObjectProperty(None)
    deja_enregistre = BooleanProperty(False)

    def change_data_set(self, new_dic):
        liste_groupe = [{'text': nom_groupe}
                        for nom_groupe in new_dic.keys()]
        current_groupes = self.dict_panneau_groupe.keys()
        for groupe in liste_groupe:
            nom_groupe = groupe['text']
            if not new_dic[nom_groupe]:
                # Si c'est vide
                continue
            # Si le groupe n'existe pas, on crée le panneau et le rajoute
            if not nom_groupe in current_groupes:
                tb = TabbedPanelItem(text=nom_groupe)
                panneaugr = PanneauGroupe(new_dic[nom_groupe],
                                          nom_cours=self.titre)
                self.dict_panneau_groupe[nom_groupe] = panneaugr
                tb.add_widget(panneaugr)
                # Parce qu'à la SNSM, on aime quand c'est bien fait!
                self.nb.remove_widget(self.panneau_fin)
                self.nb.remove_widget(self.panneau_retour)
                self.nb.add_widget(tb)
                self.nb.add_widget(self.panneau_fin)
                self.nb.add_widget(self.panneau_retour)
            else:
                # Maintenant on gère les nouveaux élèves
                nouveaux_eleves = [eleve for eleve in new_dic[nom_groupe]
                                 if not eleve in self.dict_eleves[nom_groupe]]
                rejetes = [ eleve for eleve in self.dict_eleves[nom_groupe]
                            if not eleve in new_dic[nom_groupe] ]
                panneaugr = self.dict_panneau_groupe[nom_groupe]
                for ne in nouveaux_eleves:
                    panneaugr.ajoute_nouvel_eleve(ne)
                # Et on vire les autres
                for mm in rejetes:
                    panneaugr.supprime_eleve(mm)
           
    def terminaison(self, instance):
        if self.deja_enregistre:
            print('putain, le mec a déjà validé une fois...')
        nom_formateur = self.panfin.nom_formateur()
        formateurs = formation_db.trouver_formateurs(noms=[nom_formateur])
        if not formateurs:
            pops.pop_warn(None, 'Renseigner le nom du formateur')
            return
        formateur = formateurs[0]
        nom_lieu = self.panfin.nom_lieu()
        mise_en_situation = self.panfin.nom_mise_en_situation()
        lieux = formation_db.trouver_lieux(noms=[nom_lieu])
        if not lieux:
            pops.pop_warn(None,
                          'Renseigner le lieu de la formation d\'aujourd\'hui')
            return
        lieu = lieux[0]

        if not mise_en_situation:
            pops.pop_warn(None,
                        'Renseigner le détail de la mise en situation')
            return

        cours = formation_db.trouver_cours([self.titre])
        if not cours:
            pops.pop_warn('Erreur interne: le cours', self.titre, 'a disparu de la base de données... Mieux vaut quitter')
            return
        cour = cours[0]

        jf = poplib.ajout_jf(lieu=lieu, cours=cour, formateur=formateur,
                             notes=mise_en_situation)

        for pangr in self.dict_panneau_groupe.values():
            current_scm = pangr.scm
            for eleve in pangr.liste_eleves:
                s = current_scm.get_screen(eleve.__str__())
                for module, resultat, commentaires, origine in s.bilan_eleve():
                    #bilan = BilanModule(module=module, statut=resultat,
                    # Si le bilan est NT, on ne crée pas de Bilan
                    if resultat == BilanModule.NONFAIT:
                        continue
                    if resultat == origine: 
                        continue
                    bilan = poplib.ajout_bilan(module=module, statut=resultat,
                                             commentaires=commentaires,
                                             eleve=eleve, date=jf)
                for test, statut, resultat, origine in s.resultats_eleve():
                    # Si le statut est NT, on ne crée pas de Resultat
                    if statut == Resultat.NONFAIT:
                        continue
                    if statut == origine:
                        continue
                    res = poplib.ajout_res(test=test, eleve=eleve, date=jf,
                                           resultat=resultat, statut=statut)
        self.deja_enregistre = True

    def recapitulatif(self):
        # Pour l'affichage du récapitulatif, on utilise le tablelayout
        # Il faut donc construire les cellules selon le contenu du BilanModule
        recap = list()
        for pangr in self.dict_panneau_groupe.values():
            current_scm = pangr.scm
            for eleve in pangr.liste_eleves:
                eleve_dict = OrderedDict()
                eleve_dict['nom'] = StdCellView.factory('E_CharField',
                                                        eleve.__str__(),
                                                        width=180,
                                                        name='nom')
                for module, resultat, commentaires, origine in \
                          current_scm.get_screen(eleve.__str__()).bilan_eleve():
                    nom_module = module.nom
                    eleve_dict[nom_module] = StdCellView.factory(
                                                          'E_CharField',
                                                          resultat,
                                                          width=100, 
                                                          name=nom_module)
                recap.append(eleve_dict)
        return recap
                
    def retour(self, instance):
        self.parent_scm.transition.direction = 'right'
        self.parent_scm.current = self.retour_selection

    def __init__(self, retour_selection, titre, parent_scm, dict_eleves_par_groupe, **kwargs):
        self.titre = titre
        self.retour_selection = retour_selection
        self.parent_scm = parent_scm
        self.dict_eleves = dict_eleves_par_groupe
        self.dict_panneau_groupe = dict()
        super(Formation, self).__init__(**kwargs)

        for nom_groupe in self.dict_eleves.keys():
            tb = TabbedPanelItem(text=nom_groupe)
            panneaugr = PanneauGroupe(self.dict_eleves[nom_groupe], nom_cours=titre)
            self.dict_panneau_groupe[nom_groupe] = panneaugr
            tb.add_widget(panneaugr)
            self.nb.add_widget(tb)

        fin = TabbedPanelItem(text='Terminer')
        self.panfin = PanneauFinFormation(self.terminaison, self.recapitulatif)
        fin.add_widget(self.panfin)
        fin.bind(on_release=self.panfin.update)
        self.nb.add_widget(fin)
        self.panneau_fin = fin
        retour = TabbedPanelHeader(text='Retour')
        retour.bind(on_release=self.retour)
        self.nb.add_widget(retour)
        self.panneau_retour = retour
