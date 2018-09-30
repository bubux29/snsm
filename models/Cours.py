# -*- coding: utf-8 -*-
import peewee
from playhouse.fields import ManyToManyField
from models.Trombi import Eleve
from models.dbDefs import FieldType, FieldsDescription
import datetime

GROUPE_ANCIENS='Anciens'

database = peewee.SqliteDatabase("snsm.db")

# Relations:
# un résultat référence un test et un élève (de manière unique)
# une journée de formation référence :
#   - plusieurs élèves via une table intermédiaire (histoire de rajouter
#        un nom au groupe ou pas: TODO décision)
#   - plusieurs modules de formation

# Ainsi:
# Si on souhaite connaître la liste des modules suivis par un élève, on parcourt
# l'ensemble de la table des journées où l'élève est listé et on liste
# l'ensemble des modules vus ce jour-là!
# Pour commencer une évaluation, pour chaque élève on liste l'ensemble des 
# résultats (via un formulaire en supportant les déjà "passés").
# Pour connaître les compétences d'un élève, on consulte la table des résultats
# qui doit être remplie dès l'ajout de l'élève dans un cours. L'état par défaut
# du résultat doit être "Non passé". Pour construire la liste des résultats
# on se base sur la liste des tests (attention en cas de mise à jour de la base
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

class Categorie (BaseModel):
    nom = peewee.CharField(max_length=64)
    def __str__(self):
        return self.nom

# Un module de formation c'est:
# - un nom
# - une description
class ModuleFormation (BaseModel):
    nom = peewee.CharField(max_length=32, null=False, unique=True)
    categorie = peewee.CharField(max_length=32, null=True)
    description = peewee.TextField(null=False, verbose_name=u"Détail du module de formation à réaliser")
    cours = peewee.ForeignKeyField(Cours, related_name="modules")
    requis = ['nom', 'categorie', 'description', 'cours']
    affichage = [('nom', 200), ('cours', 100), ('categorie', 100)]
    largeur_cellule_min = peewee.IntegerField(verbose_name='Largeur minimum de la colonne qui doit afficher le contenu du module')
    class Meta:
        order_by = ('cours', 'categorie',)
        indexes = (
            (('nom', 'cours'), True),
        )
    def __str__(self):
        return self.nom

# Un test c'est:
# - un nom
# - OneToOneField vers catégorie
# - une description
class Test (BaseModel):
    mode = peewee.IntegerField (choices=FieldsDescription, default=FieldType.E_CharField)
    nom = peewee.CharField(max_length=32, null=False)
    description = peewee.TextField(null=False, verbose_name=u"Détail du test à passer par l'évalué")
    #cours = peewee.ForeignKeyField(Cours, related_name="tests")
    module = peewee.ForeignKeyField(ModuleFormation, related_name="tests")
    requis = ['nom', 'description', 'module']
    affichage = [('nom', 200), ('description', 400)]
    class Meta:
        order_by = ('module',)
        indexes = (
            (('nom', 'module'), True),
        )
    def __str__(self):
        return self.nom

class Lieu (BaseModel):
    lieu = peewee.CharField(max_length=64, unique=True)
    description = peewee.TextField()
    affichage = [('lieu', 120), ('description', 300)]
    requis = ['lieu', 'description']
    class Meta:
        order_by = ('lieu',)
    def __str__(self):
        return self.lieu

class Groupe (BaseModel):
     nom = peewee.CharField(unique=True)
     date_creation = peewee.DateTimeField(verbose_name=u"Date de création du groupe", default=datetime.datetime.now)
     participants = ManyToManyField(Eleve, related_name="fait_partie")
     cours = ManyToManyField(Cours, related_name="groupes_attaches")

     affichage = [('nom', 200), ('cours', 200), ('participants', 400)]
     requis = ['nom', 'participants', 'cours']

     def __str__(self):
         return self.nom
     
# Une journée de formation c'est:
# - une date
# - un lieu
# - un nom de formateur
# - un groupe qui a fait la formation (on créera en base autant de journée de
#                                      formation qu'il y a eu de groupe)
# - un ManyToManyField vers Module de Formation
# - des notes prises pendant le cours
class JourneeFormation (BaseModel):
     # La date de la journée doit être renseignée automatiquement à la création
     # Par contre, on se fiche de mettre à jour la date quand on modifie
     # l'instance (auto_now_add & auto_now)
     date = peewee.DateTimeField(verbose_name="Date du jour de la formation",
                                 default=datetime.datetime.now)
     lieu = peewee.ForeignKeyField(Lieu, related_name="activites")
     cours = peewee.ForeignKeyField(Cours, related_name="journees")
     formateur = peewee.ForeignKeyField(Eleve,
                                   null=True,
                                   related_name="formateur_sur",
                                   verbose_name=u"Nom du formateur présent pour la journée (un seul nom autorisé)",)
     #groupe_participants = peewee.ForeignKeyField(Groupe, related_name="a_participe_le")
     #modules_vus = ManyToManyField(ModuleFormation, related_name="etudie_le")
     #notes = peewee.TextField(verbose_name="Notes prises lors du cours")
     notes = peewee.TextField(verbose_name="Mise en situation")
     class Meta:
        order_by = ('date',)
        indexes = (
           (('date', 'cours'), True),
        )
     def __str__(self):
        return self.cours.__str__() + ' ' + self.date

# Il faut créer une page qui crée automatiquement l'ensemble des résultats
# d'un élève aux tests d'un cours
# Elle peut s'appeler: "Inscription d'un élève à un cours" (par exemple)
class Resultat (BaseModel):
    SUCCES = 'I'
    ECHEC = '0'
    NONFAIT = 'NT'
    TEST_RESULTAT_CHOIX = (
       (SUCCES, u'succès'),
       (ECHEC, u'échec'),
    )
    statut = peewee.CharField (max_length=2, choices=TEST_RESULTAT_CHOIX, default=NONFAIT)
    eleve = peewee.ForeignKeyField(Eleve)
    test  = peewee.ForeignKeyField(Test)
    resultat = peewee.TextField(null=True, verbose_name=u"Résultat du test")
    date = peewee.ForeignKeyField(JourneeFormation)
    commentaires = peewee.TextField(null=True,
                   verbose_name=u"Avis de l'examinateur quant au passage de l'élève sur ce test")
    affichage = [('eleve', 200), ('test', 120), ('statut', 60), ('commentaires', 300)]
    class Meta:
        order_by = ('eleve',)
        #indexes = (
            #(('eleve', 'test', 'date'), True)
        #)
    def __str__(self):
        return self.test.nom

    def synthese(liste_resultats):
        s = [ b.statut for b in liste_resultats ]
        if Resultat.SUCCES in s:
            return Resultat.SUCCES
        if Resultat.ECHEC in s:
            return Resultat.ECHEC
        return Resultat.NONFAIT

class BilanModule (BaseModel):
    SUCCES = '1'
    ECHEC = '0'
    NONFAIT = 'NT'
    MODULE_RESULTAT_CHOIX = (
       (SUCCES, 'succès'),
       (ECHEC, u'échec'),
    )
    statut = peewee.CharField (max_length=2, choices=MODULE_RESULTAT_CHOIX, default=NONFAIT)
    eleve = peewee.ForeignKeyField(Eleve)
    module  = peewee.ForeignKeyField(ModuleFormation)
    date = peewee.ForeignKeyField(JourneeFormation)
    commentaires = peewee.TextField(null=True, verbose_name=u"Avis de l'examinateur quant au passage de l'élève sur ce module")
    class Meta:
        order_by = ('date',)
        #indexes = (
            #(('eleve', 'module', 'date'), True)
        #)
    def __str__(self):
        return self.statut
    def synthese(liste_bilans):
        s = [ b.statut for b in liste_bilans ]
        if BilanModule.SUCCES in s:
            return BilanModule.SUCCES
        if BilanModule.ECHEC in s:
            return BilanModule.ECHEC
        return BilanModule.NONFAIT

def _connect_to_db():
    database.connect()

def _disconnect_db():
    database.close()

def _create_tables():
    #database.connect()
    # Dans le cas de champs ManyToMany, il faut générer explicitement les
    # bases de données transverses...
    database.create_tables([
        Cours, 
        Eleve,
        Test, 
        ModuleFormation, 
        Lieu, 
        Groupe, 
        Groupe.participants.get_through_model(), 
        Eleve.fait_partie.get_through_model(),
        Cours.groupes_attaches.get_through_model(), 
        Groupe.cours.get_through_model(), 
        JourneeFormation, 
        Resultat
    ],
    safe=True)

    database.close()
