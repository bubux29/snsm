#!/usr/bin/env python3

from scripts.poplib import ajout_mf, ajout_cours, ajout_test
from models.dbDefs import FieldType

def initier_mf_piscine():
    ajout_cours('Piscine')
    ajout_mf('100m', 'Piscine', 'à voir', 'Faire 100m et sortir de l\'eau', 50)
    ajout_mf('250m', 'Piscine', 'à voir', 'Faire 200m et sortir de l\'eau', 50)

    ajout_test('Apnée 1', '100m', 'Faire une apnée', FieldType.E_TestResField.value)
    ajout_test('Apnée 2', '100m', 'Faire une apnée', FieldType.E_TestResField.value)
    ajout_test('Temps 100m', '100m', 'Faire 100m', FieldType.E_CharField.value)
 
    ajout_test('Temps 200m', '250m', 'Nager', FieldType.E_CharField.value)
    ajout_test('Temps 250m', '250m', 'Nager', FieldType.E_CharField.value)

if __name__ == '__main__':
    initier_mf_piscine()
