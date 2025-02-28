from django.db import models

class Societaire(models.Model):
    id_societaire = models.AutoField(primary_key=True)
    organisation = models.CharField(max_length=50, blank=True, null=True)
    numero_societaire = models.CharField(max_length=50)
    id_utilisateur = models.OneToOneField('Utilisateur', on_delete=models.CASCADE)
    college = models.ForeignKey('College', on_delete=models.CASCADE)

class College(models.Model):
    nom = models.CharField(max_length=50, primary_key=True)