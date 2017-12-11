#!/usr/bin/env python3

from models.Cours import *
import formation_db

database.drop_table(Resultat)
database.create_table(Resultat)

def ajout_res(test, eleve):
    try:
        res=Resultat(statut=Resultat.NONFAIT, test=test, eleve=eleve)
        res.save()
    except Exception as e:
        print('Ajout', test.nom, 'pour', eleve.__str__(), 'impossible (' + e + ')')
        return

    print('Ajout', test.nom, 'pour', eleve.__str__(), 'fait')

liste_tests=formation_db.liste_tests_all()[:]
liste_eleves=formation_db.liste_eleves_all()[:]

for t in liste_tests:
    for e in liste_eleves:
        ajout_res(t,e)
