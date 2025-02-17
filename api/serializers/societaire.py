from rest_framework import serializers
from ..models import *

class SocietaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Societaire
        fields = '__all__'