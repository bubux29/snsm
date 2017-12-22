#!/usr/bin/env python3
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
from models.Cours import *

from scripts.poplib import ajout_lieu

def initier_lieux():
    pp=Lieu.create(lieu="Piscine de Recouvrance", description="Piscine de Recouvrance où qu'on peut se baigner")
    pp.save()
    ss=Lieu.create(lieu="Plage de nudistes", description="Plage où qu'on peut faire du bateau moteur qui va vite")
    ss.save()

if __name__ == '__main__':
    initier_lieux()
