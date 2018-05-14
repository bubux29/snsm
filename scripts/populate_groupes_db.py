#!/usr/bin/env python3
import sys
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
from models.Cours import _create_tables, GROUPE_ANCIENS
from models.Cours import Groupe, database
from models.Trombi import *
from formation_db import *
from datetime import *
import formation_db

from scripts.poplib import ajout_groupe

# On initie un premier groupe qui contient les anciens
def groupes_dans_cours():
    liste_cours=formation_db.trouver_cours()
    try:
        ajout_groupe(GROUPE_ANCIENS, liste_cours)
    except:
        print(sys.exc_info())
#    GROUPES_MATCH = [(GROUPE_ANCIENS, TOUS_COURS)]
#    for gt in GROUPES_MATCH:
#        try:
#            print('Ajouting groupe', gt[0])
#            ajout_groupe(gt[0], gt[1])
#        except:
#            print(sys.exc_info())

def initier_groupes():
    groupes_dans_cours()
    eleves=liste_eleves_all()
    
    lancien=formation_db.trouver_groupe([GROUPE_ANCIENS])
    if len(lancien) == 0:
        print('Pas de groupe ANCIEN défini')
        return
    ancien = lancien[0]
    if not ancien.participants:
        eleves=formation_db.liste_eleves_by_statut(['Formateur', 'Ancien'])
        ancien.participants.add(eleves)
    
    for grp in Groupe.select():
        print('Le', grp.__str__())
        for eleve in grp.participants:
            print(' -', eleve)

if __name__ == '__main__':
    initier_groupes()
