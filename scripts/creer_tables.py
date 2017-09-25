from models.Cours import *

database.create_tables([Cours, Eleve, Test, ModuleFormation, Lieu, Groupe, Groupe.participants.get_through_model(), Groupe.cours.get_through_model(), JourneeFormation, ModuleFormation, JourneeFormation.groupe_participants.get_through_model(), JourneeFormation.modules_vus.get_through_model(), Resultat], True)
