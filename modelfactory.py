from diplomes import ssa_model, pse1_model
import formation_db

from models.Cours import BilanModule

_MODELS = {
        'Piscine': None,
        'SSA TPC': ssa_model,
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

class PrintBilan(object):
    statut = None
    date = None
    commentaires = None
    def __init__(self, statut, date, commentaires):
        self.statut = statut
        self.date = date
        self.commentaires = commentaires
 
# For the moment, on ne se fait pas ierch'
class PrintResultat(PrintBilan):
    pass
    
def print_resultat(nom_cours, liste_modules, nom_eleve):
    bilans_modules = list()
    resultats_tests = list()
    try:
        cours = formation_db.trouver_cours(nom=[nom_cours])[0]
    #liste_modules = formation_db.trouver_modules_par_cours([nom_cours])
        eleve = formation_db.trouver_eleve(nom=nom_eleve)
    except Exception as e:
        print ("Peut pas marcher: ", e)
    _print_resultat(cours, liste_modules, eleve)
    

def _print_resultat(cours, liste_modules, eleve):
    les_modules = list()
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
           liste_bilans = [PrintBilan(statut=BilanModule.NONFAIT, date='', commentaires='')]
       else:
           liste_bilans = [PrintBilan(b.statut, b.date, b.commentaires) for b in _liste_bilans]
       mod = PrintModule(module.nom, module.description, 
                         liste_bilans, liste_tests)
       les_modules.append(mod)
    model = _MODELS[cours.nom]
    if not model:
        print ("Oups... no printer function for cours :", cours.nom)
        return
    model.populate_file('toto.xlsx',
                        nom_eleve=eleve.nom, prenom_eleve = eleve.prenom,
                        bilans_modules = les_modules)
