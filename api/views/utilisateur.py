from rest_framework.decorators import action, permission_classes
from rest_framework import viewsets
from rest_framework.response import Response

from ..models import Utilisateur
from ..serializers import UtilisateurSerializer

class UtilisateurAPIView(viewsets.ModelViewSet):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer

    @action(detail=False, methods=["get"], url_path="test")
    def getAll(self, request):
        return Response("utilisateur")