
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

def trouver_cours(name):
    cours = Cours.get(Cours.nom == name)
    return cours

def _liste_by(cls, rule):
    return cls.select().where(rule)

def liste_cours_all():
    return Cours.select()

def liste_cours_by_nom(noms_cours):
    return Cours.select().where(Cours.nom << noms_cours)

def liste_lieux_all():
    return Lieu.select()

def liste_groupes_all():
    return Groupe.select()


#Through.select(Through,Groupe,Cours).join(Cours).switch(Through).join(Groupe).where(Cours.nom << nom_cours):
def liste_groupes_by_cours(noms_cours):
    Through=Groupe.cours.get_through_model()
    return list(Groupe.select(Through,Groupe,Cours).join(Through).join(Cours).where(Cours.nom << noms_cours))

    return Groupe.select().where(Groupe.cours << liste_cours)

def liste_eleves_all():
    return Eleve.select()

def liste_eleves_by_statut(noms):
    return Eleve.select().where(Eleve.statut << noms)

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
