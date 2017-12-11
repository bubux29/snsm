#!/usr/bin/env python3

from models.Cours import *
import formation_db

database.drop_table(BilanModule)
database.create_table(BilanModule)

def ajout_res(module, eleve):
    try:
        res=BilanModule(statut=BilanModule.NONFAIT, module=module, eleve=eleve)
        res.save()
    except Exception as e:
        print('Ajout', module.nom, 'pour', eleve.__str__(), 'impossible (' + e + ')')
        return

    print('Ajout', module.nom, 'pour', eleve.__str__(), 'fait')

liste_modules=formation_db.liste_modules_all()[:]
liste_eleves=formation_db.liste_eleves_all()[:]

for t in liste_modules:
    for e in liste_eleves:
        ajout_res(t,e)

