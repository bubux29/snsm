#!/usr/bin/env python3
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
from models.Cours import _create_tables
from models.Trombi import *

from scripts.poplib import ajout_eleve

def initier_eleves():
    try:
        database.drop_table(Eleve)
    except:
        print("Pas possible supprimer la base")
    _create_tables()

    ajout_eleve("De La Fleur", "Jean-Sébastien", "12/09/2000", "06.12.23.34.45", "dfff@sqdfze.com", 'Stagiaire', "12/12/2012", "./pics/portrait2.jpg")
    ajout_eleve("Paddutout", "Antoine", "12/09/2001", "06.12.23.34.43", "fzoef@sqdfze.com", 'Stagiaire', "12/12/2012", "./pics/portrait3.jpg")
    ajout_eleve("Deloin", "Caroline", "12/10/2001", "06.12.23.34.40", "fronon@sqdfze.com", 'Stagiaire', "12/12/2012", "./pics/portrait4.jpg")
    ajout_eleve("Bëchameline", "Christophe", "12/9/2000", "06.12.23.34.37", "iseese@sqdfze.com", 'Ancien', "12/12/2012", "./pics/portrait5.jpg", nom_cfi='Brest')
    ajout_eleve("De Troicatre", "Jean-Paul", "12/9/1998", "06.12.23.34.32", "fritz@sqdfze.com", 'Ancien', "12/12/2012", "./pics/portrait6.jpg", nom_cfi='Quimper')
    ajout_eleve("Deré", "Odile", "12/9/1999", "06.12.23.34.29", "ffdoeizu@sqdfze.com", 'Ancien', "12/12/2012", "./pics/portrait7.jpg", nom_cfi='Brest')
    ajout_eleve("Le Bouille", "Patrick", "12/8/1999", "06.12.23.34.22", "jose@bouse.com", 'Stagiaire', "12/12/2012", "./pics/portrait71.jpg")
    ajout_eleve("Juliojulio", "Jacques", "12/9/1998", "06.12.23.34.32", "fritz@sqdfze.com", 'Ancien', "12/12/2012", "./pics/portrait6.jpg", nom_cfi='Quimper')
    ajout_eleve("Abaziour", "Emile", "12/9/1999", "06.12.23.34.29", "ffdoeizu@sqdfze.com", 'Ancien', "12/12/2012", "./pics/portrait7.jpg", nom_cfi='Brest')
    ajout_eleve("Verbatim", "Vincent", "12/8/1999", "06.12.23.34.22", "jose@bouse.com", 'Stagiaire', "12/12/2012", "./pics/portrait71.jpg")
    ajout_eleve("Du Rest", "Marie-Antoinette", "12/9/1998", "06.12.23.34.32", "fritz@sqdfze.com", 'Ancien', "12/12/2012", "./pics/portrait6.jpg", nom_cfi='Quimper')
    ajout_eleve("Abdique", "Yves", "12/9/1999", "06.12.23.34.29", "ffdoeizu@sqdfze.com", 'Ancien', "12/12/2012", "./pics/portrait7.jpg", nom_cfi='Brest')
    ajout_eleve("Dobipierre Hountch", "Anatole", "12/9/1999", "06.12.23.34.29", "ffdoeizu@sqdfze.com", 'Formateur', "12/12/2012", "./pics/portrait7.jpg", nom_cfi='Quimper')
    ajout_eleve("Bové", "José", "12/9/1999", "06.12.23.34.29", "ffdoeizu@sqdfze.com", 'Stagiaire', "12/12/2012", "./pics/portrait7.jpg", nom_cfi='Quimper')
    ajout_eleve("Verbatim", "Etienne", "12/8/1999", "06.12.23.34.22", "jose@bouse.com", 'Stagiaire', "12/12/2012", "./pics/portrait71.jpg")

if __name__ == '__main__':
    initier_eleves()
