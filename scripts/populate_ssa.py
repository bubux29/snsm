#!/usr/bin/env python3
from models.dbDefs import FieldType
from scripts.poplib import ajout_mf, ajout_cours, ajout_test

def initier_cours():
    ajout_cours('SSA TPC')

def initier_modules():
    ajout_mf('Rôle et mission', 'SSA TPC', 'TPC', 'situer son rôle et sa mission au sein d\'un dispositif évolutif et adaptable aux conditions du moment', 100)

    ajout_mf('Analyse risques', 'SSA TPC', 'TPC', 'effectuer une analyse des risques particuliers présents sur sa zone', 100)
    ajout_mf('Actions prévention', 'SSA TPC', 'TPC', 'développer des actions de prévention adaptées aux risques et pratiques sur zone', 100)
    ajout_mf('Dispositif surveillance', 'SSA TPC', 'TPC', 'Participer à un dispositif de surveillance en mettant en oeuvre des techniques opérationnelles adaptées et mettant éventuellement en oeuvre des moyens spécifiques', 100)
    ajout_mf('Gestes PSA', 'SSA TPC', 'TPC', 'Réaliser des gestes de premier secours adaptés', 100)
    ajout_mf('Action coordonnée', 'SSA TPC', 'TPC', 'Participer à une action coordonnée de sauvetage, dans sa zone, ou à proximité immédiate de celle-ci, à l\'aide de techniques opérationnelles adaptées ou en mettant en oeuvre des matériels spécifiques', 100)
    ajout_mf('Pilotage', 'SSA TPC', 'TPC', 'Réaliser une action de sauvetage en tant que pilote d\'une embarcation motorisée', 100)

def initier_tests():
    ajout_test('Mise en oeuvre',
               'Rôle et mission',
               "met en œuvre les différentes missions du SSA littoral",
               FieldType.E_TestResField.value) 
    ajout_test('Rapport au responsable',
               'Rôle et mission',
               "rend compte à son responsable / autorité d'emploi",
               FieldType.E_TestResField.value) 
    ajout_test('Environnement et phénomènes naturels',
               'Analyse risques',
               "identifie les risques liés à l'environnement et aux phénomènes naturels",
               FieldType.E_TestResField.value) 
    ajout_test('Activités à risque',
               'Analyse risques',
               "identifie les risques d'une activité par rapport à l'environnement observé",
               FieldType.E_TestResField.value) 
    ajout_test('Météo sur tableau d\'information',
               'Actions prévention',
               "renseigne le tableau d'information à partir d'un bulletin météo",
               FieldType.E_TestResField.value) 
    ajout_test('Action de prévention adaptée',
               'Actions prévention',
               "réalise l'action de prévention adaptée",
               FieldType.E_TestResField.value) 
    ajout_test('Communication et message de prévention',
               'Actions prévention',
               "respecte les règles de communication et de construction du message de prévention",
               FieldType.E_TestResField.value) 
    ajout_test('Surveillance active et constante',
               'Dispositif surveillance',
               "réalise une surveillance active et constante en tenant compte des contraintes liées au milieu naturel",
               FieldType.E_TestResField.value) 
    ajout_test('Rôle et matériel dans un dispositif de surveillance',
               'Dispositif surveillance',
               "se positionne dans un dispositif de surveillance en respectant le rôle défini et en utilisant le matériel adapté si nécessaire",
               FieldType.E_TestResField.value) 
    ajout_test('Détection d\'une détresse',
               'Dispositif surveillance',
               "détecte les signes visibles d'une détresse",
               FieldType.E_TestResField.value) 
    ajout_test('Contraintes du milieu naturel dans premier secours',
               'Gestes PSA',
               "prend en compte les contraintes du milieu naturel dans les gestes de premier secours",
               FieldType.E_TestResField.value) 
    ajout_test('Respect référentiel SNSM',
               'Gestes PSA',
               "réalise les gestes adaptés conformément au référentiel technique SNSM",
               FieldType.E_TestResField.value) 
    ajout_test('Respect des procédures',
               'Action coordonnée',
               "applique les procédures en respectant les différentes étapes",
               FieldType.E_TestResField.value) 
    ajout_test('Sécurité',
               'Action coordonnée',
               "évolue en sécurité sur la plage et dans l'eau (à la nage et en planche de sauvetage)",
               FieldType.E_TestResField.value) 
    ajout_test('Action de sauvetage',
               'Action coordonnée',
               "réalise une action de sauvetage avec ou sans matériel",
               FieldType.E_TestResField.value) 
    ajout_test('Action coordonnée de sauvetage',
               'Action coordonnée',
               "participe à une action coordonnée de sauvetage",
               FieldType.E_TestResField.value) 
    ajout_test('Pilote sur embarcation',
               'Pilotage',
               "réalise une action de sauvetage en tant que pilote d'une embarcation motorisée (UNIQUEMENT POUR LA MENTION PILOTAGE)",
               FieldType.E_TestResField.value) 

def initier_ssa():
    initier_cours()
    initier_modules()
    initier_tests()
if __name__ == '__main__':
    initier_ssa()
