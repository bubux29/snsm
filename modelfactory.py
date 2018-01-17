from diplomes import ssa_model, pse1_model


_MODELS = [
        {'Piscine', None},
        {'SSA TPC', ssa_model.populate_file},
        {'PSE TPC', pse1_model.populate_file}
        ]

def print_resultat(nom_cours, nom_eleve, bilans_modules, resultats_tests):
    pass
