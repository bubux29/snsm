#!/usr/bin/env python3
from models.dbDefs import FieldType
from scripts.poplib import ajout_mf, ajout_cours, ajout_test, modict, tesresdict

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
    tesresdict('Dégagement d\'urgence' , MOD1, 'Dégagement d\'urgence' ),
    # MOD2
    tesresdict('Équipement en moyen de protection contre les agents infectieux', MOD2, 'Équipement en moyen de protection contre les agents infectieux'),
    tesresdict('Lavage des mains', MOD2, 'Lavage des mains'),
    tesresdict('Friction des mains', MOD2, 'Friction des mains'),
    tesresdict('Retrait de gants à usage unique', MOD2, 'Retrait de gants à usage unique'),
    tesresdict('Utilisation des emballages à élimination de déchets', MOD2, 'Utilisation des emballages à élimination de déchets'),
    # MOD3
    tesresdict('Recherche d\'une détresse vitale', MOD3, 'Recherche d\'une détresse vitale'),
    tesresdict('Mesure de la saturation pulsatile en oxygène', MOD3, 'Mesure de la saturation pulsatile en oxygène'),
    tesresdict('Mesure de la pression artérielle', MOD3, 'Mesure de la pression artérielle'),
    tesresdict('Interrogatoire de la victime', MOD3, 'Interrogatoire de la victime'),
    tesresdict('Gestes complémentaires d\'examen', MOD3, 'Gestes complémentaires d\'examen'),
    tesresdict('Mesure de la température', MOD3, 'Mesure de la température'),
    # MOD4
    tesresdict('Utilisation d\'une bouteille d\'oxygène', MOD4, 'Utilisation d\'une bouteille d\'oxygène'),
    tesresdict('Administration d\'oxygène par inhalation', MOD4, 'Administration d\'oxygène par inhalation'),
    tesresdict('Désobstruction par la méthode des claques dans le dos', MOD4, 'Désobstruction par la méthode des claques dans le dos'),
    tesresdict('Désobstruction par la méthode des compressions abdominales', MOD4, 'Désobstruction par la méthode des compressions abdominales'),
    tesresdict('Désobstruction par la méthode des compressions thoraciques', MOD4, 'Désobstruction par la méthode des compressions thoraciques'),
    tesresdict('Compression manuelle', MOD4, 'Compression manuelle'),
    tesresdict('Pansement compressif', MOD4, 'Pansement compressif'),
    tesresdict('Garrot', MOD4, 'Garrot'),
    tesresdict('Libération des voies aériennes chez une victime non traumatisée', MOD4, 'Libération des voies aériennes chez une victime non traumatisée'),
    tesresdict('Aspiration de mucosités', MOD4, 'Aspiration de mucosités'),
    tesresdict('Utilisation d\'un défibrillateur automatisé externe', MOD4, 'Utilisation d\'un défibrillateur automatisé externe'),
    tesresdict('Compression thoraciques', MOD4, 'Compression thoraciques'),
    tesresdict('Administration d\'oxygène par insufflation', MOD4, 'Administration d\'oxygène par insufflation'),
    tesresdict('Ventilation artificielle par un insufflateur manuel', MOD4, 'Ventilation artificielle par un insufflateur manuel'),
    tesresdict('Ventilation artificielle par une méthode orale', MOD4, 'Ventilation artificielle par une méthode orale'),
    tesresdict('Mise en place de la canule oro-pharyngée', MOD4, 'Mise en place de la canule oro-pharyngée'),
    tesresdict('Libération des voies aériennes chez une victime traumatisée', MOD4, 'Libération des voies aériennes chez une victime traumatisée'),
    # MOD5
    tesresdict('Utilisation d\'un Lot Membre Arrache ou Sectionné', MOD5, 'Utilisation d\'un Lot Membre Arrache ou Sectionné'),
    tesresdict('Aide à la prise de médicament', MOD5, 'Aide à la prise de médicament'),
    tesresdict('Application de froid', MOD5, 'Application de froid'),
    tesresdict('Emballage au moyen d\'un pansement stérile', MOD5, 'Emballage au moyen d\'un pansement stérile'),
    tesresdict('Pansement', MOD5, 'Pansement'),
    tesresdict('Maintien d\'un pansement', MOD5, 'Maintien d\'un pansement'),
    # MOD6
    tesresdict('Positions d\'attente et de transport', MOD6, 'Positions d\'attente et de transport'),
    tesresdict('Position latéral de sécurité à un sauveteur', MOD6, 'Position latéral de sécurité à un sauveteur'),
    tesresdict('Position latéral de sécurité à deux sauveteurs', MOD6, 'Position latéral de sécurité à deux sauveteurs'),
    # MOD7
    tesresdict('Maintien de la tête en position neutre chez une victime allongée', MOD7, 'Maintien de la tête en position neutre chez une victime allongée'),
    tesresdict('Pose d\'un collier cervical chez une victime allongée', MOD7, 'Pose d\'un collier cervical chez une victime allongée'),
    tesresdict('Réalignement d\'un membre', MOD7, 'Réalignement d\'un membre'),
    tesresdict('Immobilisation d\'un membre supérieur au moyen d\'écharpes', MOD7, 'Immobilisation d\'un membre supérieur au moyen d\'écharpes'),
    tesresdict('Immobilisation d\'un membre au moyen d\'une attelle modulable', MOD7, 'Immobilisation d\'un membre au moyen d\'une attelle modulable'),
    tesresdict('Immobilisation d\'un membre au moyen d\'une attelle à dépression', MOD7, 'Immobilisation d\'un membre au moyen d\'une attelle à dépression'),
    # MOD8
    tesresdict('Retournement d\'urgence à un sauveteur', MOD8, 'Retournement d\'urgence à un sauveteur'),
    tesresdict('Retournement en urgence à deux sauveteurs', MOD8, 'Retournement en urgence à deux sauveteurs'),
    tesresdict('Retrait d\'un casque de protection', MOD8, 'Retrait d\'un casque de protection'),
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
