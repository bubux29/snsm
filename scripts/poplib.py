from models.Cours import Cours, Lieu, Groupe, BilanModule, ModuleFormation, Resultat, Test, JourneeFormation
from models.Trombi import Eleve

import formation_db

def ajout_cours(nom):
    try:
        c = Cours.create(nom=nom)
        c.save()
        print('Ajout cours', nom, ': OK')
        return c
    except Exception as e:
        print('Ajout cours:', nom, 'impossib:', e)
        return None

def retrait_cours(nom):
    try:
        c = Cours.get(Cours.nom==nom)
        mf=ModuleFormation.select().where(ModuleFormation.cours == c)
        database.drop_tables(mf)
    except:
        pass

    try:
        c = Cours.get(Cours.nom==nom)
        formation_db.database.drop_table(c)
    except Exception as e:
        print('Retrait de', nom, 'impossib:', e)

def ajout_jf(**kwargs):
    try:
        #j,_ = JourneeFormation.get_or_create(**kwargs)
        j = JourneeFormation.create(**kwargs)
        j.save()
        return j
    except Exception as e:
        print('Creation JournéeFormation impossib:', e)

def ajout_lieu(**kwargs):
    try:
        l = Lieu.create(**kwargs)
        print('Ajout lieu', kwargs['nom'], ': OK')
        return l
    except Exception as e:
        print('Ajout lieu:', kwargs['nom'], 'impossib:', e)
        return

def ajout_eleve(nom, prenom, naissance, tel, courriel, statut, entree, photo, nom_cfi=''):
   try:
     pp=Eleve.create(nom=nom, prenom=prenom, date_naissance=naissance, telephone=tel, courriel=courriel, statut=statut, date_entree=entree, photo_path=photo, nom_cfi=nom_cfi)
     pp.save()
     print("Ajout élève", prenom, nom, ": OK")
     return pp
   except Exception as e:
     print("Ajout élève", prenom, nom, " impossib:", e)
     return None

def ajout_groupe(nom_groupe, cours):
    try:
        groupe, _ = Groupe.get_or_create(nom=nom_groupe)
        groupe.save()
        for c in cours:
            try:
                cc=Cours.get(nom=c)
                groupe.cours.add(cc)
                print('Ajout', nom_groupe, 'dans: ', cc.__str__())
            except Exception as e:
                print('Groupe', nom_groupe, 'non rajouté dans :', c, 'car :', e)
        return groupe
    except Exception as e:
        #e = sys.exc_info()[0]
        print(nom_groupe, 'existe déjà (', e,')')

def ajout_mf(nom, nom_cours, categorie, description, largeur_min):
    try:
        cc=Cours.get(Cours.nom==nom_cours)
        mf=ModuleFormation(nom=nom, cours=cc, categorie=categorie, description=description, largeur_cellule_min=largeur_min)
        mf.save()
        print('Ajout', nom, 'dans', nom_cours, ' : OK')
        return mf
    except Exception as e:
        print('Ajout', nom, 'dans', nom_cours, ' impossib:', e)
        return None

def ajout_bilan(**kwargs):
    module = kwargs['module']
    eleve = kwargs['eleve']
    print('Bilan pour:', module.nom, 'de', eleve.__str__())
    try:
        bil=BilanModule.create(**kwargs)
        bil.save()
        print('Ajout', bil.module.nom, 'pour', bil.eleve.__str__(),
              'fait (' + bil.statut + ')')
        return bil
    except Exception as e:
        print('Ajout', module.nom, 'impossible (', e, ')')
        return

def ajout_res(**kwargs):
    test = kwargs['test']
    eleve = kwargs['eleve']
    try:
        res=Resultat(**kwargs)
        res.save()
        print('Ajout', test.nom, 'pour', eleve.__str__(), 'fait')
        return res
    except Exception as e:
        print('Ajout', test.nom, 'pour', eleve.__str__(), 'impossible (' + e + ')')
        return

def ajout_test(nom, nom_mf, description, mode):
    try:
        mf=ModuleFormation.get(ModuleFormation.nom==nom_mf)
        test=Test(nom=nom, module=mf, description=description, mode=mode)
        test.save()
        print('Ajout', nom, 'dans le module', nom_mf, ' : OK')
        return test
    except Exception as e:
        print('Ajout', nom, 'dans le module', nom_mf, 'impossib:', e)
        return None

def ajout_element(classe, **kwargs):
    try:
        elm = classe.create(**kwargs)
        elm.save()
    except Exception as e:
        if 'nom' in kwargs:
            nom = kwargs['nom']
        else:
            nom = 'machin'
        print('Ajout de', kwargs['nom'], 'dans', classe, ': impossib')
        return None

def creer_tables():
    formation_db.database.create_tables([Eleve], safe=True)
    formation_db.database.create_tables([Cours], safe=True)
    formation_db.database.create_tables([Test], safe=True)
    formation_db.database.create_tables([ModuleFormation], safe=True)
    formation_db.database.create_tables([Lieu], safe=True)
    formation_db.database.create_tables([Groupe], safe=True)
    formation_db.database.create_tables([Groupe.participants.get_through_model()], safe=True)
    formation_db.database.create_tables([Eleve.fait_partie.get_through_model()], safe=True)
    formation_db.database.create_tables([Cours.groupes_attaches.get_through_model()], safe=True)
    formation_db.database.create_tables([Groupe.cours.get_through_model()], safe=True)
    formation_db.database.create_tables([JourneeFormation], safe=True)
    formation_db.database.create_tables([BilanModule], safe=True)
    formation_db.database.create_tables([Resultat], safe=True)

def initier_bilans():
    formation_db.database.create_table(BilanModule, safe=True)

    liste_modules=formation_db.liste_modules_all()[:]
    liste_eleves=formation_db.liste_eleves_all()[:]

    for t in liste_modules:
        for e in liste_eleves:
            ajout_bilan(t,e)

def initier_resultats():
    liste_tests=formation_db.liste_tests_all()[:]
    liste_eleves=formation_db.liste_eleves_all()[:]

    for t in liste_tests:
        for e in liste_eleves:
            ajout_res(t,e)
