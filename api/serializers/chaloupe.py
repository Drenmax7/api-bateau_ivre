from rest_framework import serializers
from ..models import *

class ChaloupeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chaloupe
        fields = '__all__'

class RejointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rejoint
        fields = '__all__'