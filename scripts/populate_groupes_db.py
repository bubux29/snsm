#!/usr/bin/env python3
import sys
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
from models.Cours import _create_tables
from models.Cours import Groupe, database
from models.Trombi import *
from formation_db import *
from datetime import *
import formation_db

from scripts.poplib import ajout_groupe

def initier_groupes():
    cours=formation_db.trouver_cours()
    eleves=liste_eleves_all()
    
    for gt in [('Groupe1', ['Piscine', 'SSA TPC']), ('Groupe2', ['Piscine']), ('Groupe3', ['Piscine']), (GROUPE_ANCIENS, cours), ('Groupe4', ['Secourisme', 'SSA TPC']), ('Groupe5', ['Secourisme']), ('Groupe6', ['Secourisme'])]:
        try:
            ajout_groupe(gt[0], gt[1])
        except:
            print(sys.exc_info())
    
    ancien=Groupe.get(Groupe.nom=='Anciens')
    if not ancien.participants:
        eleves=formation_db.liste_eleves_by_statut(['Formateur', 'Ancien'])
        ancien.participants.add(eleves)
    
    Groupe.get(Groupe.nom=='Groupe3').participants.add(Eleve.get(Eleve.nom=='Du Rest'))
    Groupe.get(Groupe.nom=='Groupe1').participants.add(Eleve.select().where(Eleve.nom != 'Du Rest', Eleve.statut=='Stagiaire'))
    Groupe.get(Groupe.nom=='Groupe6').participants.add(Eleve.get(Eleve.nom=='Bové'))
    Groupe.get(Groupe.nom=='Groupe4').participants.add(Eleve.select().where(Eleve.nom != 'Bové', Eleve.statut=='Stagiaire'))
    
    for grp in Groupe.select():
        print('Le', grp.__str__())
        for eleve in grp.participants:
            print(' -', eleve)

if __name__ == '__main__':
    initier_groupes()
