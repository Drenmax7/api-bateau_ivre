from django.db import models

class Connexion(models.Model):
    jour = models.DateField(primary_key=True)

class HistoriqueConnexion(models.Model):
    id_utilisateur = models.ForeignKey('Utilisateur', on_delete=models.CASCADE)
    jour = models.ForeignKey('Connexion', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('id_utilisateur', 'jour')