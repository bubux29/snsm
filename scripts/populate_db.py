#!/usr/bin/env python3

from scripts.populate_eleves_db import initier_eleves
from scripts.populate_groupes_db import initier_groupes
from scripts.populate_lieu_db import initier_lieux
from scripts.populate_piscine import initier_mf_piscine
from scripts.populate_PSE1 import initier_pse1_tech
from scripts.populate_ssa import initier_ssa
from scripts.poplib import creer_tables

def populate_db():
    print('Création des tables')
    creer_tables()
    #print('Création des élèves')
    #initier_eleves()
    print('Création des cours')
    initier_mf_piscine()
    initier_ssa()
    initier_pse1_tech()
    #print('Création des groupes')
    #initier_groupes()
    #print('Création des lieux')
    #initier_lieux()

if __name__ == '__main__':
    populate_db()
