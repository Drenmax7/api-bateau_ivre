from django.db import models

class Chaloupe(models.Model):
    id_chaloupe = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, blank=True, null=True)


class Rejoint(models.Model):
    id_utilisateur = models.ForeignKey('Utilisateur', on_delete=models.CASCADE)
    id_chaloupe = models.ForeignKey('Chaloupe', on_delete=models.CASCADE)
    dirige = models.BooleanField()

    class Meta:
        unique_together = ('id_utilisateur', 'id_chaloupe')