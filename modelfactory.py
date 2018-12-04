# -*- coding: utf-8 -*-
from diplomes import ssa_model, pse1_model
from diplomes.base import exporte_resultat
import formation_db
import xlsxwriter

from collections import OrderedDict

from models.Cours import BilanModule, Resultat

_MODELS = {
        'Piscine': None,
        'SSA TPC': ssa_model.ssa_tpc,
        'SSA Technicités': ssa_model.ssa_tech,
        'PSE1 Technicités': pse1_model.pse1_tech
        }

class PrintTest(object):
    nom_test = None
    description_test = None
    liste_resultats = None
    def __init__(self, nom_test=nom_test, description_test=description_test,
                       liste_resultats=liste_resultats, **kwargs):
        self.nom_test = nom_test
        self.description_test = description_test
        self.liste_resultats = liste_resultats

    def bilan_test(self, resultat = None):
        if not resultat:
            return self.synthese()
        return self.conversion(resultat)

    def conversion(self, resultat):
        if resultat == Resultat.SUCCES:
            return 1
        elif resultat == Resultat.ECHEC:
            return -1
        else:
            return 0

    def synthese(self):
        synthese = Resultat.synthese(self.liste_resultats)
        return self.conversion(synthese)
        

class PrintModule(object):
    nom_module = None
    description_module = None
    liste_bilans = None
    liste_tests = None
    def __init__(self, nom_module, description_module,
                       liste_bilans, liste_tests):
        self.nom_module = nom_module
        self.description_module = description_module
        self.liste_bilans = liste_bilans
        self.liste_tests = liste_tests

class PrintDate(object):
    date = None
    nom_formateur = None
    nom_mise_en_situation = None
    def __init__(self, journee_formation):
        self.date = journee_formation.date
        self.formateur = journee_formation.formateur.__str__()
        self.nom_mise_en_situation = journee_formation.notes

class PrintBilan(object):
    statut = None
    date = None
    commentaires = None
    def __init__(self, statut, date, commentaires):
        self.statut = statut
        if date:
            self.date = PrintDate(date)
        self.commentaires = commentaires
 
# For the moment, on ne se fait pas ierch'
class PrintResultat(PrintBilan):
    pass
    
def print_resultat(nom_cours, nom_eleve, liste_modules=None):
    bilans_modules = list()
    resultats_tests = list()
    try:
        cours = formation_db.trouver_cours(nom=[nom_cours])[0]
        if liste_modules == None:
            liste_modules = formation_db.trouver_modules_par_cours([cours])
        eleve = formation_db.trouver_eleve(nom=nom_eleve)
    except Exception as e:
        raise
        return
    _print_resultat(cours, liste_modules, eleve)
    

def _print_resultat(cours, liste_modules, eleve):
    les_modules = OrderedDict()
    for module in liste_modules:
       liste_tests = list()
       for test in module.tests:
           res = formation_db.trouver_resultats_tests_par_eleves([test], [eleve])
           liste_res = [PrintResultat(r.statut, r.date, r.commentaires)
                        for r in res]
           t = PrintTest(nom_test=test.nom, description_test=test.description,
                         liste_resultats=liste_res)
           liste_tests.append(t)
       _liste_bilans = formation_db.trouver_bilans_par_eleve([eleve], [module])
       if not _liste_bilans:
           liste_bilans = [PrintBilan(statut=BilanModule.NONFAIT, date=None, commentaires='')]
       else:
           liste_bilans = [PrintBilan(b.statut, b.date, b.commentaires) for b in _liste_bilans]
       mod = PrintModule(module.nom, module.description, 
                         liste_bilans, liste_tests)
       les_modules[module.description] = mod
    if cours.nom not in _MODELS.keys():
        print ("Oups... no printer function for cours :", cours.nom)
        return
    model = _MODELS[cours.nom]
    exporte_resultat(model, 'imprim', nom_eleve=eleve.nom, prenom_eleve = eleve.prenom,
                        bilans_par_module = les_modules)

