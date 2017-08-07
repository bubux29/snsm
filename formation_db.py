
from models.Cours import Cours
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

def liste_cours_all():
    return Cours.select()

def ajouter_lieu_db(nom, desc):
    lieu = Lieu.create(lieu=nom, description=desc)
    lieu.save()

def ajouter_eleve_db(nom, prenom, date, is_form, embauche):
    eleve = Eleve.create(nom=nom, prenom=prenom, date_naissance=date, is_formateur=is_form, date_entree=embauche)
    eleve.save()

def ajouter_journee_formation_db():
     date = peewee.DateTimeField(verbose_name="Date du jour de la formation")
     lieu = peewee.ForeignKeyField(Lieu, related_name="activites")
     cours = peewee.ForeignKeyField(Cours, related_name="journees")
     formateur = peewee.ForeignKeyField(Eleve,
                                   null=True,
                                   related_name="formateur_sur",
                                   verbose_name="Nom du formateur présent pour la journée (un seul nom autorisé)",)
     participants = ManyToManyField(Eleve, related_name="a_participe_a")
     modules_vus = ManyToManyField(ModuleFormation, related_name="modules")
