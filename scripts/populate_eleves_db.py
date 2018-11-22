#!/usr/bin/env python3
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
from models.Cours import _create_tables
from models.Trombi import *

from scripts.poplib import ajout_eleve

def ajout_eleve_blank(nom, prenom):
    ajout_eleve(nom, prenom, "1/1/2000", "06.00.11.22.33", "anonyme@snsm.fr", "Stagiaire", "12/09/2018", "data/portraits/" + '_'.join([prenom, nom, "2018"]))

def initier_eleves():
    try:
        database.drop_table(Eleve)
    except:
        print("Pas possible supprimer la base")
    _create_tables()

#    ajout_eleve("Creac'h", "Thierry", "01/01/1990", "06.12.23.34.45", "john@doe.org", 'Stagiaire', "12/12/2012", "")
#    ajout_eleve("Roué", "Aurélien", "01/01/1990", "06.12.23.34.45", "john@doe.org", 'Stagiaire', "12/12/2012", "")
#    ajout_eleve("Deniel", "Gilles", "01/01/1990", "06.12.23.34.45", "john@doe.org", 'Stagiaire', "12/12/2012", "")
#    ajout_eleve("Bevoust", "Marc", "01/01/1990", "06.12.23.34.45", "john@doe.org", 'Stagiaire', "12/12/2012", "")
#    ajout_eleve("Hellio", "Grégory", "01/01/1990", "06.12.23.34.45", "john@doe.org", 'Stagiaire', "12/12/2012", "")
#    ajout_eleve("Joly", "Jean-Claude", "01/01/1990", "06.12.23.34.45", "john@doe.org", 'Stagiaire', "12/12/2012", "")
#    ajout_eleve("Milin", "Guy-Pierre", "01/01/1990", "06.12.23.34.45", "john@doe.org", 'Formateur', "12/12/2012", "")
#    ajout_eleve("Prigent", "Jocelyn", "01/01/1990", "06.12.23.34.45", "john@doe.org", 'Formateur', "12/12/2012", "")
#

    ajout_eleve_blank("ANDRIAMAHEFA", "Saul")
    ajout_eleve_blank("DELAPRE", "Alexis")
    ajout_eleve_blank("VASSAL", "Anna")
    ajout_eleve_blank("BEUCHET", "Bréval")
    ajout_eleve_blank("BRIERE", "Bertille")
    ajout_eleve_blank("CALANDO", "Camille")
    ajout_eleve_blank("COLLET", "Nathan")
    ajout_eleve_blank("PESTEL", "Houarn")
    ajout_eleve_blank("TROUMELIN", "Ewen")
    ajout_eleve_blank("SOLIVERES", "Bleuenn")
    ajout_eleve_blank("DUPRE", "Lucien")
    ajout_eleve_blank("DUPRE", "Antonin")
    ajout_eleve_blank("POTARD", "Arnaud")
    ajout_eleve_blank("CRENN", "Brendan")
    ajout_eleve_blank("JAOUEN-BACHELIER", "Hugo")
    ajout_eleve_blank("BECHEN", "Pierre")
    ajout_eleve_blank("GRIMAL", "Titouan")
    ajout_eleve_blank("PERHIRIN", "Eliott")
    ajout_eleve_blank("LEVREL", "Eloan")
    ajout_eleve_blank("PRIMEL", "Nathan")
    ajout_eleve_blank("MADEC", "Paul")
    ajout_eleve_blank("WISPELAERE", "Pierre")
    ajout_eleve_blank("CHAPEL", "Thomas")
    ajout_eleve_blank("SZEWCZYK", "Thomas")
    ajout_eleve_blank("BOUSSIR", "Yussra")
    ajout_eleve_blank("DELAPRE", "Alexis")
    ajout_eleve_blank("KERDUFF", "Largo")
    ajout_eleve_blank("GUENEUGUES", "Manon")
    ajout_eleve_blank("MORIN", "Guillaume")
    ajout_eleve_blank("NICOLAS", "Alix")
    ajout_eleve_blank("SALOMON", "Auguste")

#    ajout_eleve("De La Fleur", "Jean-Sébastien", "12/09/2000", "06.12.23.34.45", "dfff@sqdfze.com", 'Stagiaire', "12/12/2012", "./pics/portrait2.jpg")
#    ajout_eleve("Paddutout", "Antoine", "12/09/2001", "06.12.23.34.43", "fzoef@sqdfze.com", 'Stagiaire', "12/12/2012", "./pics/portrait3.jpg")
#    ajout_eleve("Deloin", "Caroline", "12/10/2001", "06.12.23.34.40", "fronon@sqdfze.com", 'Stagiaire', "12/12/2012", "./pics/portrait4.jpg")
#    ajout_eleve("Bëchameline", "Christophe", "12/9/2000", "06.12.23.34.37", "iseese@sqdfze.com", 'Ancien', "12/12/2012", "./pics/portrait5.jpg", nom_cfi='Brest')
#    ajout_eleve("De Troicatre", "Jean-Paul", "12/9/1998", "06.12.23.34.32", "fritz@sqdfze.com", 'Ancien', "12/12/2012", "./pics/portrait6.jpg", nom_cfi='Quimper')
#    ajout_eleve("Deré", "Odile", "12/9/1999", "06.12.23.34.29", "ffdoeizu@sqdfze.com", 'Ancien', "12/12/2012", "./pics/portrait7.jpg", nom_cfi='Brest')
#    ajout_eleve("Le Bouille", "Patrick", "12/8/1999", "06.12.23.34.22", "jose@bouse.com", 'Stagiaire', "12/12/2012", "./pics/portrait71.jpg")
#    ajout_eleve("Juliojulio", "Jacques", "12/9/1998", "06.12.23.34.32", "fritz@sqdfze.com", 'Ancien', "12/12/2012", "./pics/portrait6.jpg", nom_cfi='Quimper')
#    ajout_eleve("Abaziour", "Emile", "12/9/1999", "06.12.23.34.29", "ffdoeizu@sqdfze.com", 'Ancien', "12/12/2012", "./pics/portrait7.jpg", nom_cfi='Brest')
#    ajout_eleve("Verbatim", "Vincent", "12/8/1999", "06.12.23.34.22", "jose@bouse.com", 'Stagiaire', "12/12/2012", "./pics/portrait71.jpg")
#    ajout_eleve("Du Rest", "Marie-Antoinette", "12/9/1998", "06.12.23.34.32", "fritz@sqdfze.com", 'Ancien', "12/12/2012", "./pics/portrait6.jpg", nom_cfi='Quimper')
#    ajout_eleve("Abdique", "Yves", "12/9/1999", "06.12.23.34.29", "ffdoeizu@sqdfze.com", 'Ancien', "12/12/2012", "./pics/portrait7.jpg", nom_cfi='Brest')
#    ajout_eleve("Dobipierre Hountch", "Anatole", "12/9/1999", "06.12.23.34.29", "ffdoeizu@sqdfze.com", 'Formateur', "12/12/2012", "./pics/portrait7.jpg", nom_cfi='Quimper')
#    ajout_eleve("Bové", "José", "12/9/1999", "06.12.23.34.29", "ffdoeizu@sqdfze.com", 'Stagiaire', "12/12/2012", "./pics/portrait7.jpg", nom_cfi='Quimper')
#    ajout_eleve("Verbatim", "Etienne", "12/8/1999", "06.12.23.34.22", "jose@bouse.com", 'Stagiaire', "12/12/2012", "./pics/portrait71.jpg")

if __name__ == '__main__':
    initier_eleves()
