from django.db import models

class Utilisateur(models.Model):
    id_utilisateur = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    mail = models.EmailField(max_length=100, unique=True)
    mot_de_passe = models.CharField(max_length=50)
    civilite = models.CharField(max_length=50)
    adresse = models.CharField(max_length=200)
    ville = models.CharField(max_length=50)
    pays = models.CharField(max_length=50)
    code_postal = models.CharField(max_length=6, blank=True, null=True)
    telephone = models.CharField(max_length=15)
    complement_adresse = models.CharField(max_length=100, blank=True, null=True)
    premiere_connexion = models.DateTimeField(blank=True, null=True)
    derniere_connexion = models.DateTimeField(blank=True, null=True)