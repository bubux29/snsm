# -*- coding: utf-8 -*-
from models.Cours import *
from models.Cours import _connect_to_db, _disconnect_db, _create_tables
from models.Trombi import Eleve

def init_db():
    _create_tables()

def connect_to_db():
    _connect_to_db()

def disconnect_db():
    _disconnect_db()

def ajouter_cours(name):
    cours = Cours.create(nom=name)
    cours.save()

def trouver_cours(nom=None):
    if nom == None:
        return list(Cours.select())
    else:
        return list(Cours.select().where(Cours.nom << nom))

def trouver_par_nom(nom, classe):
    return classe.get(classe.nom == nom)

def trouver_eleve(nom, cls = None):
    eleve = Eleve.get(Eleve.prenom + ' ' + Eleve.nom == nom)
    return eleve

def trouver_groupe(noms=None):
    if noms == None:
        return list(Groupe.select())
    else:
        return list(Groupe.select().where(Groupe.nom << noms))

def trouver_formateurs(noms=None):
    if noms == None:
        return list(Eleve.select().where(Eleve.statut == 'Formateur'))
    else:
        return list(Eleve.select().where(Eleve.statut == 'Formateur').where(Eleve.nom << noms))

def trouver_lieux(noms=None):
    if noms == None:
        return list(Lieu.select())
    else:
        return list(Lieu.select().where(Lieu.lieu << noms))

def liste_par_classe(cls, rule=None):
    if rule:
        return list(cls.select().where(rule))
    else:
        return list(cls.select())

def liste_cours_all():
    return Cours.select()

def liste_cours_by_nom(noms_cours):
    return Cours.select().where(Cours.nom << noms_cours)

def liste_lieux_all():
    return Lieu.select()

def liste_groupes_all():
    return Groupe.select()

def liste_tests_all():
    return liste_all_from(Test)

def liste_modules_all():
    return liste_all_from(ModuleFormation)

def liste_all_from(classe):
    return classe.select()

def trouver_resultats_tests_par_eleves(test, eleve):
    ##return list(Resultat.select().where(Resultat.eleve == eleve and Resultat.test == test))[0]
    luste = list(Resultat.select().where(Resultat.eleve << eleve).where(Resultat.test << test))
    return luste

#def trouver_bilans_module_par_eleve(module, eleve):
    #luste = list(BilanModule.select().where(BilanModule.eleve == eleve and BilanModule.module == module))
    #return luste

def trouver_modules_par_cours(cours):
    return list(ModuleFormation.select().where(ModuleFormation.cours << cours))

def trouver_bilans_par_eleve(eleves, modules):
    return list(BilanModule.select().where(BilanModule.module << modules).where(BilanModule.eleve << eleves))

def trouver_tests_par_modules(modules):
    return list(Test.select().where(Test.module << modules))

#Through.select(Through,Groupe,Cours).join(Cours).switch(Through).join(Groupe).where(Cours.nom << nom_cours):
def trouver_groupes_par_cours(noms_cours):
    Through=Groupe.cours.get_through_model()
    return list(Groupe.select(Through,Groupe,Cours).join(Through).join(Cours).where(Cours.nom << noms_cours))
    #return Groupe.select().where(Groupe.cours << liste_cours)

def liste_eleves_all():
    return Eleve.select()

def liste_eleves_by_statut(noms):
    return Eleve.select().where(Eleve.statut << noms)

def liste_eleves_by_groupe(noms_groupes):
    Through = Eleve.fait_partie.get_through_model()
    return list(Eleve.select(Through,Eleve,Groupe).join(Through).join(Groupe).where(Groupe.nom << noms_groupes).order_by(Eleve.nom))

def ajouter_lieu_db(nom, desc):
    lieu = Lieu.create(lieu=nom, description=desc)
    lieu.save()

def ajouter_eleve_db(nom, prenom, date, is_form, embauche):
    eleve = Eleve.create(nom=nom, prenom=prenom, date_naissance=date, is_formateur=is_form, date_entree=embauche)
    eleve.save()

def ajouter_journee_formation_db(date, lieu, cours, formateur, participants, modules_vus):
     journee = JourneeFormation.create(date=date)
     lieu.activities.add(journee)
     cours.journees.add(journee)
     formateur.formateur_sur.add(journee)
     for p in participants:
         p.a_participe_le.add(journee)
     for m in modules_vus:
         m.etudie_le.add(journee)
     journee.save()
