#!/usr/bin/env python3
from models.dbDefs import FieldType
from scripts.poplib import ajout_mf, ajout_cours, ajout_test, modict, tesdic, tesresdict

NOM_COURS='PSE1 Technicités'
DETAILS_COURS='Technicités'
MOD1='Protection et sécurité'
MOD2='Gestes d\'hygiène et asepsie'
MOD3='Gestes d\'examen'
MOD4='Gestes d\'urgence vitale'
MOD5='Gestes de soins'
MOD6='Positions d\'attente'
MOD7='Immobilisations'
MOD8='Relevages et brancardages'

MODULES=[
   modict(MOD1, 'Protection et sécurité', 160),
   modict(MOD2, MOD2, 180),
   modict(MOD3, MOD3, 140),
   modict(MOD4, MOD4, 170),
   modict(MOD5, MOD5, 150),
   modict(MOD6, MOD6, 170),
   modict(MOD7, MOD7, 140),
   modict(MOD8, MOD8, 180),
]

TESTS=[
    # MOD1
    tesresdict('Dégagement d\'urgence' , MOD1, ''),
    # MOD2
    tesresdict('Équipement en moyen de protection contre les agents infectieux', MOD2, ''),
    tesresdict("Lavage des mains", MOD2, ''),
    tesresdict("Friction des mains", MOD2, ''),
    tesresdict("Retrait de gants à usage unique", MOD2, ''),
    tesresdict("Utilisation des emballages à élimination de déchets", MOD2, ''),
    # MOD3
    tesresdict("Recherche d'une détresse vitale", MOD3, ''),
    tesresdict("Mesure de la saturation pulsatile en oxygène", MOD3, ''),
    tesresdict("Mesure de la pression artérielle", MOD3, ''),
    tesresdict("Interrogatoire de la victime", MOD3, ''),
    tesresdict("Gestes complémentaires d'examen", MOD3, ''),
    tesresdict("Mesure de la température", MOD3, ''),
    # MOD4
    tesresdict("Utilisation d'une bouteille d 'oxygène", MOD4, ''),
    tesresdict("Administration d'oxygène par inhalation", MOD4, ''),
    tesresdict("Désobstruction par la méthode des claques dans le dos", MOD4, ''),
    tesresdict("Désobstruction par la méthode des compressions abdominales", MOD4, ''),
    tesresdict("Désobstruction par la méthode des compressions thoraciques", MOD4, ''),
    tesresdict("Compression manuelle", MOD4, ''),
    tesresdict("Pansement compressif", MOD4, ''),
    tesresdict("Garrot", MOD4, ''),
    tesresdict("Libération des voies aériennes chez une victime non traumatisée", MOD4, ''),
    tesresdict("Aspiration de mucosités", MOD4, ''),
    tesresdict("Utilisation d'un défibrillateur automatisé externe", MOD4, ''),
    tesresdict("Compression thoraciques", MOD4, ''),
    tesresdict("Administration d'oxygène par insufflation", MOD4, ''),
    tesresdict("Ventilation artificielle par un insufflateur manuel", MOD4, ''),
    tesresdict("Ventilation artificielle par une méthode orale", MOD4, ''),
    tesresdict("Mise en place de la canule oro-pharyngée", MOD4, ''),
    tesresdict("Libération des voies aériennes chez une victime traumatisée", MOD4, ''),
    # MOD5
    tesresdict("Utilisation d'un Lot Membre Arrache ou Sectionné", MOD5, ''),
    tesresdict("Aide à la prise de médicament", MOD5, ''),
    tesresdict("Application de froid", MOD5, ''),
    tesresdict("Emballage au moyen d'un pansement stérile", MOD5, ''),
    tesresdict("Pansement", MOD5, ''),
    tesresdict("Maintien d'un pansement", MOD5, ''),
    # MOD6
    tesresdict("Positions d'attente et de transport", MOD6, ''),
    tesresdict("Position latéral de sécurité à un sauveteur", MOD6, ''),
    tesresdict("Position latéral de sécurité à deux sauveteurs", MOD6, ''),
    # MOD7
    tesresdict("Maintien de la tête en position neutre chez une victime allongée", MOD7, ''),
    tesresdict("Pose d'un collier cervical chez une victime allongée", MOD7, ''),
    tesresdict("Réalignement d'un membre", MOD7, ''),
    tesresdict("Immobilisation d'un membre supérieur au moyen d'écharpes", MOD7, ''),
    tesresdict("Immobilisation d'un membre au moyen d'une attelle modulable", MOD7, ''),
    tesresdict("Immobilisation d'un membre au moyen d'une attelle à dépression", MOD7, ''),
    # MOD8
    tesresdict("Retournement d'urgence à un sauveteur", MOD8, ''),
    tesresdict("Retournement en urgence à deux sauveteurs", MOD8, ''),
    tesresdict("Retrait d'un casque de protection", MOD8, ''),
]

def initier_cours():
    ajout_cours(NOM_COURS)

def initier_modules():
    for modic in MODULES:
        ajout_mf(modic['nom'], NOM_COURS, DETAILS_COURS, modic['desc'], modic['width'])

def initier_tests():
    for tesdic in TESTS:
        ajout_test(tesdic['nom'], tesdic['module'], tesdic['desc'], tesdic['type'])

def initier_pse1_tech():
    initier_cours()
    initier_modules()
    initier_tests()

if __name__ == '__main__':
    initier_pse1_tech()
