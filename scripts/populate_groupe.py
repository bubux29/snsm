#!/usr/bin/env python3
import sys
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
from models.Cours import *
from models.Trombi import *
from formation_db import *
cours=liste_cours_all()
eleves=liste_eleves_all()
from datetime import *
import formation_db

def create_groupe(nom_groupe, noms_cours):
    try:
        groupe, _ = Groupe.get_or_create(nom=nom_groupe)
        groupe.save()
    except:
        e = sys.exc_info()[0]
        print(nom_groupe, 'existe déjà (', e,')')
    finally:
        groupe.cours.add(formation_db.liste_cours_by_nom(noms_cours))

for gt in [('Groupe1', ['Piscine']), ('Groupe2', ['Piscine']), ('Groupe3', ['Piscine']), (GROUPE_ANCIENS, ['Piscine', 'Secourisme']), ('Groupe4', ['Secourisme']), ('Groupe5', ['Secourisme']), ('Groupe6', ['Secourisme'])]:
    try:
        create_groupe(gt[0], gt[1])
    except:
        print(sys.exc_info())

ancien=Groupe.get(Groupe.nom=='Anciens')
if not ancien.participants:
    eleves=formation_db.liste_eleves_by_statut(['Formateur', 'Ancien'])
    ancien.participants.add(eleves)

try:
    Groupe.get(Groupe.nom=='Groupe3').participants.add(Eleve.get(Eleve.nom=='Bové'))
    Groupe.get(Groupe.nom=='Groupe1').participants.add(Eleve.select().where(Eleve.nom != 'Bové', Eleve.statut=='Stagiaire'))
except:
    print('Les groupes ont déjà été rempli')

for grp in Groupe.select():
    print('Le', grp.__str__())
    for eleve in grp.participants:
        print(' -', eleve)
