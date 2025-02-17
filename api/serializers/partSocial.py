from rest_framework import serializers
from ..models import *

class PartSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartSocial
        fields = '__all__'