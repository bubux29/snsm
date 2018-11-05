#!/usr/bin/env python3
from scripts.poplib import modict, tesresdict
from scripts.poplib import SNSMCours

class SSATech(SNSMCours):
    NOM_COURS='SSA Technicités'
    DETAILS_COURS='Technicités'
    MOD1='Sans matériel'
    MOD2='Rescue Tube'
    MOD3='Planche de sauvetage'
    MOD4='Communication'
    MOD5='Montage et préparation'
    MOD6='Vérifications pré-opérationnelles'
    MOD7='Manoeuvres d\'urgence'
    MOD8='Mise en oeuvre'
    MOD9='Récupération de victime'

    MODULES=[
        modict(MOD1, MOD1, 140),
        modict(MOD2, MOD2, 140),
        modict(MOD3, MOD3, 150),
        modict(MOD4, MOD4, 140),
        modict(MOD5, MOD5, 160),
        modict(MOD6, MOD6, 180),
        modict(MOD7, MOD7, 160),
        modict(MOD8, MOD8, 150),
        modict(MOD9, MOD9, 180),
    ]

    TESTS=[
        tesresdict('Evoluer dans l\'eau', MOD1, ''),
        tesresdict('Aborder une victime consciente dans l\'eau', MOD1, ''),
        tesresdict('Remorquer une victime', MOD1, ''),
        tesresdict('Sortir de l\'eau une victime consciente seule', MOD1, ''),
        tesresdict('Aborder une vicitme inconsciente dans l\'eau', MOD1, ''),
        tesresdict('Sortir de l\'eau et déposer une victime inconsciente seul', MOD1, ''),
        tesresdict('Sortir de l\'eau et déposer une victime inconsciente à 2 sauveteurs positionnés à la tête', MOD1, ''),
        tesresdict('Sortir de l\'eau et déposer une victime inconsciente à 2 sauveteurs positionnés aux jambes', MOD1, ''),
        tesresdict('Aborder une victime avec suspicion de traumatisme du rachis dans l\'eau', MOD1, ''),
        tesresdict('Sortir de l\'eau et déposer une victime avec suspicion de traumatisme du rachis seul', MOD1, ''),
        tesresdict('Sortir de l\'eau et déposer une victime avec suspicion de traumatisme du rachis à 2 sauveteurs positionnés à la tête', MOD1, ''),
        tesresdict('Sortir de l\'eau et déposer une victime avec suspicion de traumatisme du rachis à 2 sauveteurs positionnés aux jambes', MOD1, ''),
        tesresdict('Sortir de l\'eau une victime selon la technique d\'urgence et la déposer à 2 sauveteurs', MOD1, ''),
        # MOD2
        tesresdict('Evoluer dans l\'eau', MOD2, ''),
        tesresdict('Aborder une victime consciente dans l\'eau', MOD2, ''),
        tesresdict('Aborder une victime inconsciente dans l\'eau', MOD2, ''),
        tesresdict('Remorquer une victime seul en "corps à corps"', MOD2, ''),
        tesresdict('Remorquer une victime seul selon la technique de tractage', MOD2, ''),
        tesresdict('Remorquer une victime à 2 sauveteurs selon la technique de tractage', MOD2, ''),
        tesresdict('Retirer le rescue tube lors d\'une dépose de victime inconsciente ou avec suspicion de traumatisme du rachis', MOD2, ''),
        tesresdict('Sortir de l\'eau une victime selon la technique d\'urgence', MOD2, ''),
        tesresdict('Sécuriser de multiples victimes', MOD2, ''),
        # MOD3
        tesresdict('Effectuer une mise à l\'eau', MOD3, ''),
        tesresdict('Evoluer dans l\'eau', MOD3, ''),
        tesresdict('Aborder une victime consciente dans l\'eau', MOD3, ''),
        tesresdict('Aborder une victime inconsciente dans l\'eau', MOD3, ''),
        tesresdict('Evoluer avec une victime sur la planche de sauvetage', MOD3, ''),
        tesresdict('Sortir de l\'eau une victime inconsciente depuis une planche de sauvetage', MOD3, ''),
        tesresdict('Utiliser la planche de sauvetage comme moyen de brancardage', MOD3, ''),
        # MOD4
        tesresdict('Réaliser les signaux de communication gestuels depuis la plage', MOD4, ''),
        tesresdict('Réaliser les signaux de communication gestuels depuis l\'eau', MOD4, ''),
        tesresdict('Appliquer les signaux sonores', MOD4, ''),
        tesresdict('Utiliser la VHF', MOD4, ''),
        # MOD5
        tesresdict('Monter et réparer une embarcation pneumatique', MOD5, ''),
        tesresdict('Préparer le moteur et l\'ensemble d\'alimentation en carburant d\'une embarcation pneumatique', MOD5, ''),
        # MOD6
        tesresdict('Vérifier l\'embarcation pneumatique', MOD6, ''),
        tesresdict('Vérifier le moteur et l\'alimentation en carburant', MOD6, ''),
        tesresdict('Vérifier l\'armement d\'une embarcation pneumatique', MOD6, ''),
        # MOD7
        tesresdict('Réaliser un arrêt d\'urgence', MOD7, ''),
        tesresdict('Réaliser une manoeuvre d\'évitement en cas de chute d\'équipier', MOD7, ''),
        tesresdict('Réaliser un drainage', MOD7, ''),
        tesresdict('Réaliser un retournement de pneumatique en cas de dessalage', MOD7, ''),
        # MOD8
        tesresdict('S\'équiper des équipements de protection individuels (EPI)', MOD8, ''),
        tesresdict('S\'équiper du coupe-circuit en tant que pilote', MOD8, ''),
        tesresdict('Evoluer à 2 sauveteurs en tant que pilote', MOD8, ''),
        tesresdict('Evoluer à 2 sauveteurs en tant qu\'équipier', MOD8, ''),
        tesresdict('Evoluer seul', MOD8, ''),
        tesresdict('Réaliser un départ de plage à 2 sauveteurs en tant que pilote', MOD8, ''),
        tesresdict('Réaliser un départ de plage à 2 sauveteurs en tant qu\'équipier', MOD8, ''),
        tesresdict('Réaliser un départ de plage à 1 sauveteur', MOD8, ''),
        tesresdict('Réaliser une arrivée de plage en Beach', MOD8, ''),
        tesresdict('Réaliser une arrivée de plage en demi-tour', MOD8, ''),
        # MOD9
        tesresdict('Récupérer une victime consciente en tant que pilote', MOD9, ''),
        tesresdict('Récupérer une victime consciente en tant qu\'équipier', MOD9, ''),
        tesresdict('Récupérer une victime inconsciente en tant que pilote', MOD9, ''),
        tesresdict('Récupérer une victime inconsciente en tant qu\'équipier', MOD9, ''),
        tesresdict('Récupérer une victime avec un rescue tube en tant que pilote', MOD9, ''),
        tesresdict('Récupérer une victime avec un rescue tube en tant qu\'équipier', MOD9, ''),
        tesresdict('Sortir une victime inconsciente d\'un pneumatique en tant que pilote', MOD9, ''),
        tesresdict('Sortir une victime inconsciente d\'un pneumatique en tant qu\'équipier', MOD9, '')
    ]

class SSATPC(SNSMCours):
    NOM_COURS='SSA TPC'
    DETAILS_COURS='SSA Théoriques, Pratiques et comportementales'
    MOD1='Rôle et mission'
    MOD2='Analyse risques'
    MOD3='Actions prévention'
    MOD4='Dispositif surveillance'
    MOD5='Gestes PSA'
    MOD6='Action coordonnée'
    MOD7='Pilotage'

    MODULES=[
        modict(MOD1, 'situer son rôle et sa mission au sein d\'un dispositif évolutif et adaptable aux conditions du moment', 140),
        modict(MOD2, 'effectuer une analyse des risques particuliers présents sur sa zone', 140),
        modict(MOD3, 'développer des actions de prévention adaptées aux risques et pratiques sur zone', 140),
        modict(MOD4, 'Participer à un dispositif de surveillance en mettant en oeuvre des techniques opérationnelles adaptées et mettant éventuellement en oeuvre des moyens spécifiques', 160),
        modict(MOD5, 'Réaliser des gestes de premier secours adaptés', 100),
        modict(MOD6, 'Participer à une action coordonnée de sauvetage, dans sa zone, ou à proximité immédiate de celle-ci, à l\'aide de techniques opérationnelles adaptées ou en mettant en oeuvre des matériels spécifiques', 140),
        modict(MOD7, 'Réaliser une action de sauvetage en tant que pilote d\'une embarcation motorisée', 100)
    ]

    TESTS=[
        tesresdict('Mise en oeuvre',
               MOD1,
               "met en œuvre les différentes missions du SSA littoral"),
        tesresdict('Rapport au responsable',
               MOD1,
               "rend compte à son responsable / autorité d'emploi"),
        tesresdict('Environnement et phénomènes naturels',
               MOD2,
               "identifie les risques liés à l'environnement et aux phénomènes naturels"),
        tesresdict('Activités à risque',
               MOD2,
               "identifie les risques d'une activité par rapport à l'environnement observé"),
        tesresdict('Météo sur tableau d\'information',
               MOD3,
               "renseigne le tableau d'information à partir d'un bulletin météo"),
        tesresdict('Action de prévention adaptée',
               MOD3,
               "réalise l'action de prévention adaptée"),
        tesresdict('Communication et message de prévention',
               MOD3,
               "respecte les règles de communication et de construction du message de prévention"),
        tesresdict('Surveillance active et constante',
               MOD4,
               "réalise une surveillance active et constante en tenant compte des contraintes liées au milieu naturel"),
        tesresdict('Rôle et matériel dans un dispositif de surveillance',
               MOD4,
               "se positionne dans un dispositif de surveillance en respectant le rôle défini et en utilisant le matériel adapté si nécessaire"),
        tesresdict('Détection d\'une détresse',
               MOD4,
               "détecte les signes visibles d'une détresse"),
        tesresdict('Contraintes du milieu naturel dans premier secours',
               MOD5,
               "prend en compte les contraintes du milieu naturel dans les gestes de premier secours"),
        tesresdict('Respect référentiel SNSM',
               MOD5,
               "réalise les gestes adaptés conformément au référentiel technique SNSM"),
        tesresdict('Respect des procédures',
               MOD6,
               "applique les procédures en respectant les différentes étapes"),
        tesresdict('Sécurité',
               MOD6,
               "évolue en sécurité sur la plage et dans l'eau (à la nage et en planche de sauvetage)"),
        tesresdict('Action de sauvetage',
               MOD6,
               "réalise une action de sauvetage avec ou sans matériel"),
        tesresdict('Action coordonnée de sauvetage',
               MOD6,
               "participe à une action coordonnée de sauvetage"),
        tesresdict('Pilote sur embarcation',
               MOD7,
               "réalise une action de sauvetage en tant que pilote d'une embarcation motorisée (UNIQUEMENT POUR LA MENTION PILOTAGE)"),
    ]

if __name__ == '__main__':
    initier_ssa()
