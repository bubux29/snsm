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

TOUS_COURS=formation_db.trouver_cours()
GROUPES_MATCH=[
  ('Groupe1', ['Piscine', 'SSA TPC']),
  ('Groupe2', ['Piscine', 'PSE1 Technicités']),
  ('Groupe3', ['Piscine']),
  (GROUPE_ANCIENS, TOUS_COURS),
  ('Groupe4', ['SSA TPC']),
  ('Groupe5', ['PSE1 Technicités']),
  ('Groupe6', ['SSA TPC', 'PSE1 Technicités'])
]

def groupes_dans_cours():
    for gt in GROUPES_MATCH:
        try:
            ajout_groupe(gt[0], gt[1])
        except:
            print(sys.exc_info())
    
def initier_groupes():
    eleves=liste_eleves_all()
    
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
    groupes_dans_cours()
    initier_groupes()
