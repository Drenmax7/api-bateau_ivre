from rest_framework import serializers
from ..models import *

class ConnexionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connexion
        fields = '__all__'

class HistoriqueConnexionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoriqueConnexion
        fields = '__all__'
