import peewee

database = peewee.SqliteDatabase("snsm.db")

# Un eleve, c'est:
#   - un nom
#   - un prenom
#   - une date de naissance
#   - un statut ("benevole", "eleve")
#   - une date d'entree dans la SNSM
class Eleve(peewee.Model):
        nom = peewee.CharField(max_length=50, verbose_name="Nom de famille")
        prenom = peewee.CharField(max_length=50, verbose_name="Prénom")
        date_naissance = peewee.DateTimeField( verbose_name="Date de naissance")
        telephone = peewee.CharField(max_length=16, verbose_name="Numéro de téléphone")
        courriel = peewee.CharField(max_length=64, verbose_name="Adresse courrier électronique")
        is_formateur = peewee.BooleanField(null=False, default=False)
        date_entree = peewee.DateTimeField(verbose_name="Date de première adhésion")
        photo_path = peewee.CharField(max_length=256, verbose_name="Photo")
        class Meta:
                database = database
        def __str__(self):
            return self.nom
