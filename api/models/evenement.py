from django.db import models

class Evenement(models.Model):
    id_evenement = models.AutoField(primary_key=True)
    place_disponible = models.IntegerField()
    date_evenement = models.DateTimeField()
    titre = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)


class Reserve(models.Model):
    id_utilisateur = models.ForeignKey('Utilisateur', on_delete=models.CASCADE)
    id_evenement = models.ForeignKey('Evenement', on_delete=models.CASCADE)
    nb_place = models.SmallIntegerField()

    class Meta:
        unique_together = ('id_utilisateur', 'id_evenement')