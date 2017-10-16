from models.Cours import *

database.create_tables([
    Cours,
    Eleve,
    Test,
    ModuleFormation,
    Lieu,
    Groupe,
    Groupe.participants.get_through_model(),
    Eleve.fait_partie.get_through_model(),
    Cours.groupes_attaches.get_through_model(),
    Groupe.cours.get_through_model(),
    JourneeFormation,
    JourneeFormation.groupe_participants.get_through_model(),
    Groupe.a_participe_le.get_through_model(),
    JourneeFormation.modules_vus.get_through_model(),
    ModuleFormation,
    ModuleFormation.etudie_le.get_through_model(),
    Resultat],
    safe=True)
