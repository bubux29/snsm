#!/usr/bin/env python3
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
from models.Cours import *
from models.Trombi import *
from formation_db import *
cours=liste_cours_all()
eleves=liste_eleves_all()
from datetime import *
if not Groupe.get(Groupe.nom=="bunnix"):
    Groupe.create(nom="bunnix").save()
    Groupe.create(nom="tutu").save()
    Groupe.create(nom="Première année").save()
    Groupe.create(nom="toto").save()

grp=Groupe.get(Groupe.nom=="toto")
if not grp.participants:
    grp.participants.add(liste_eleves_all())
#for e in eleves:
    #print(e)
    #e.fait_partie.add(Groupe.get(Groupe.nom=="Première année"))

for c in cours:
    print(c)
    if not c.groupes_attaches:
        c.groupes_attaches.add(grp)

grp=Groupe.get(Groupe.nom=="bunnix")
if not grp.cours:
    grp.cours.add(Cours.get(Cours.nom=="Piscine"))
grp=Groupe.get(Groupe.nom=="Première année")
if not grp.cours:
    grp.cours.add(Cours.get(Cours.nom=="Piscine"))
if not grp.participants:
    grp.participants.add(liste_eleves_all())
