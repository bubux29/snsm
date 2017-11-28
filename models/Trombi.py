# -*- coding: utf-8 -*-
import peewee

database = peewee.SqliteDatabase("snsm.db")

# Un eleve, c'est:
#   - un nom
#   - un prenom
#   - une date de naissance
#   - un statut ("benevole", "eleve")
#   - une date d'entree dans la SNSM
class Eleve(peewee.Model):
    STAGIAIRE = 'Stagiaire'
    FORMATEUR = 'Formateur'
    ANCIEN = 'Ancien'
    STATUT_ELEVE = (
       (STAGIAIRE, 'stagiaire'),
       (FORMATEUR, 'formateur et ancien'),
       (ANCIEN, 'ancien'),
    )
    nom = peewee.CharField(max_length=50, verbose_name="Nom de famille")
    prenom = peewee.CharField(max_length=50, verbose_name="Prénom")
    date_naissance = peewee.DateTimeField(verbose_name="Date de naissance")
    telephone = peewee.CharField(max_length=16, verbose_name="Numéro de téléphone")
    courriel = peewee.CharField(max_length=64, verbose_name="Adresse courrier électronique")
    statut = peewee.CharField(max_length=16, choices=STATUT_ELEVE, default=None, verbose_name="Statut de l'élève")
    date_entree = peewee.DateTimeField(verbose_name="Date de première adhésion")
    photo_path = peewee.CharField(max_length=256, verbose_name="Photo")
    nom_cfi = peewee.CharField(max_length=64, null=True, verbose_name="CFI d'origine (seulement si formateur ou ancien)")
    requis = ['nom', 'prenom', 'date_naissance', 'telephone', 'courriel', 'statut', 'photo_path', 'nom_cfi']
    affichage = ['nom', 'prenom', 'courriel', 'statut']
    image = ['photo_path']
    class Meta:
        database = database
    def __str__(self):
        return self.prenom + " " + self.nom
