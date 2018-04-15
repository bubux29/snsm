
class ResultatTestDesc(Object):
    description = None
    details = None
    resultat = None

    def __init__(self, description, details, resultat):
        self.description = description
        self.details = details
        self.resultat = resultat

class BilanModuleDesc(Object):
    titre = None
    desclist = None

    def __init__(self, titre, bilan, resultatstestslist):
        self.titre = titre
        self.bilan = bilan
        self.resultats_tests = resultatstestslist
