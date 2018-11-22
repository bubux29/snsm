#!/usr/bin/env python3
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
from models.Cours import *

from scripts.poplib import ajout_lieu

def initier_lieux():
    pp=Lieu.create(lieu="Piscine de Foch", description="Piscine Foch")
    pp.save()
    ss=Lieu.create(lieu="Port de Brest", description="Port de commerce de Brest")
    ss.save()

if __name__ == '__main__':
    initier_lieux()
