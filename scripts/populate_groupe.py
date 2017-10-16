#!/usr/bin/env python3
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
from models.Cours import *
from models.Trombi import *
from formation_db import *
cours=liste_cours_all()
eleves=liste_eleves_all()
from datetime import *
Groupe.create( nom="bunnix").save()
Groupe.create(nom="tutu").save()
Groupe.create(nom="Première année").save()
Groupe.create(nom="toto").save()
grp=Groupe.get(Groupe.nom=="toto")
for e in eleves:
    print(e)
    e.fait_partie.add(grp)

for c in cours:
    print(c)
    c.groupes_attaches.add(grp)

grp=Groupe.get(Groupe.nom=="bunnix")
grp.cours.add(Cours.get(Cours.nom=="Piscine"))
