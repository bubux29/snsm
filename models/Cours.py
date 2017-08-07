# -*- coding: utf-8 -*-
import peewee
from playhouse.fields import ManyToManyField
from models.Trombi import Eleve

from log import *

database = peewee.SqliteDatabase("snsm.db")

# Relations:
# un résultat référence un test et un élève (de manière unique)
# une journée de formation référence :
#   - plusieurs élèves via une table intermédiaire (histoire de rajouter
#        un nom au groupe ou pas: TODO décision)
#   - plusieurs modules de formation

# Ainsi:
# Si on souhaite connaître la liste des modules suivis par un élève, on parcourt
# l'ensemble de la table des journées où l'élève est listé et on liste
# l'ensemble des modules vus ce jour-là!
# Pour commencer une évaluation, pour chaque élève on liste l'ensemble des 
# résultats (via un formulaire en supportant les déjà "passés").
# Pour connaître les compétences d'un élève, on consulte la table des résultats
# qui doit être remplie dès l'ajout de l'élève dans un cours. L'état par défaut
# du résultat doit être "Non passé". Pour construire la liste des résultats
# on se base sur la liste des tests (attention en cas de mise à jour de la base
# des tests...)
# Un cours est un ensemble de modules de formation ainsi qu'un ensemble de
# tests.

class BaseModel(peewee.Model):
    class Meta:
       database = database

# Un cours c'est:
# - un nom (genre Cours, PSE1...)
# - un ManyToManyField vers Test
# - un ManyToManyField vers Module de formation
# - un ManyToManyField vers Journée de formation (TODO: à confirmer!)
# - un ManyToManyField vers Résultat
class Cours (BaseModel):
    nom = peewee.CharField(max_length=32, unique=True)
    #liste_tests = peewee.ManyToManyField('Test')
    #liste_modules = peewee.ManyToManyField('ModuleFormation')
    #liste_journee = models.ManyToManyField('JourneeFormation')
    #resultats_eleve = models.ManyToManyField('Resultat')
    def __str__(self):
        return self.nom
    # on declare cette methode si l'on souhaite voir apparaitre le bon nom
    # dans l'onglet d'Administration
    class Meta:
        order_by = ('nom',)
    def __unicode__(self):
        return self.nom

class Categorie (peewee.Model):
    nom = peewee.CharField(max_length=64)
    class Meta:
        database = database
    def __str__(self):
        return self.nom

# Un test c'est:
# - un nom
# - OneToOneField vers catégorie
# - une description
class Test (peewee.Model):
    nom = peewee.CharField(max_length=32, null=False)
    categorie = peewee.CharField(max_length=32, null=False)
    description = peewee.TextField(null=False, verbose_name="Détail du test à passer par l'évalué")
    cours = peewee.ForeignKeyField(Cours, related_name="tests")
    class Meta:
        order_by = ('categorie',)
    def __str__(self):
        return self.nom

# Un module de formation c'est:
# - un nom
# - une description
class ModuleFormation (peewee.Model):
    nom = peewee.CharField(max_length=32, null=False, unique=True)
    categorie = peewee.CharField(max_length=32, null=True)
    description = peewee.TextField(null=False, verbose_name="Détail du module de formation à réaliser")
    cours = peewee.ForeignKeyField(Cours, related_name="modules")
    class Meta:
        order_by = ('categorie',)
    def __str__(self):
        return self.nom

class Lieu (peewee.Model):
    lieu = peewee.CharField(max_length=64, unique=True)
    description = peewee.TextField()
    class Meta:
        order_by = ('lieu',)
    def __str__(self):
        return self.lieu

# Une journée de formation c'est:
# - une date
# - un lieu
# - un nom de formateur
# - un ManyToManyField vers Eleve
# - un ManyToManyField vers Module de Formation
class JourneeFormation (peewee.Model):
     # La date de la journée doit être renseignée automatiquement à la création
     # Par contre, on se fiche de mettre à jour la date quand on modifie
     # l'instance (auto_now_add & auto_now)
     date = peewee.DateTimeField(verbose_name="Date du jour de la formation")
     lieu = peewee.ForeignKeyField(Lieu, related_name="activites")
     cours = peewee.ForeignKeyField(Cours, related_name="journees")
     formateur = peewee.ForeignKeyField(Eleve,
                                   null=True,
                                   related_name="formateur_sur",
                                   verbose_name="Nom du formateur présent pour la journée (un seul nom autorisé)",)
     participants = ManyToManyField(Eleve, related_name="a_participe_a")
     modules_vus = ManyToManyField(ModuleFormation, related_name="modules")
     class Meta:
        order_by = ('date',)
     def __str__(self):
        return self.modules_vus

# Il faut créer une page qui crée automatiquement l'ensemble des résultats
# d'un élève aux tests d'un cours
# Elle peut s'appeler: "Inscription d'un élève à un cours" (par exemple)
class Resultat (peewee.Model):
    SUCCES = 'OK'
    ECHEC = 'KO'
    NONFAIT = 'NT'
    TEST_RESULTAT_CHOIX = (
       (SUCCES, 'succès'),
       (ECHEC, 'échec'),
       (NONFAIT, 'non passé'),
    )
    statut = peewee.CharField (max_length=2, choices=TEST_RESULTAT_CHOIX, default=NONFAIT)
    eleve = peewee.ForeignKeyField(Eleve)
    test  = peewee.ForeignKeyField(Test)
    cours = peewee.ForeignKeyField(Cours, null=True)
    commentaires = peewee.TextField(null=True, verbose_name="Avis de l'examinateur quant au passage de l'élève sur ce test")
    class Meta:
        indexes = ( (('eleve', 'test'), True), (('eleve', 'cours'), True),)
    def __str__(self):
        return self.test.nom

def _connect_to_db():
    database.connect()

def _disconnect_db():
    database.close()

def _create_tables():
    database.connect()
    database.create_tables([Eleve, Cours, Resultat, JourneeFormation, Test, ModuleFormation, Lieu], True)
    database.close()
