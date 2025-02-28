from rest_framework import serializers
from ..models import *

class SocietaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Societaire
        fields = '__all__'

class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = '__all__'