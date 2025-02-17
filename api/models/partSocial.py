from django.db import models

class PartSocial(models.Model):
    id_achat = models.AutoField(primary_key=True)
    date_achat = models.DateTimeField()
    quantite = models.SmallIntegerField()
    num_facture = models.CharField(max_length=50)
    id_societaire = models.ForeignKey('Societaire', on_delete=models.CASCADE)