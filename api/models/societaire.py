from django.db import models

class Societaire(models.Model):
    id_societaire = models.AutoField(primary_key=True)
    produit = models.CharField(max_length=50)
    organisation = models.CharField(max_length=50, blank=True, null=True)
    id_utilisateur = models.OneToOneField('Utilisateur', on_delete=models.CASCADE)