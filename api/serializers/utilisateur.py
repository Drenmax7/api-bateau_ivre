from rest_framework import serializers
from ..models import *

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        #tout sauf mdp
        fields = ["id_utilisateur","last_login","nom","prenom","civilite","adresse","ville",
                  "pays","code_postal","telephone","complement_adresse","premiere_connexion",
                  "derniere_connexion","mail","is_active","is_staff"]