from rest_framework.decorators import action, permission_classes
from rest_framework import viewsets
from rest_framework.response import Response

from ..models import Connexion
from ..serializers import ConnexionSerializer

class ConnexionAPIView(viewsets.ViewSet):
    queryset = Connexion.objects.all()
    serializer_class = ConnexionSerializer

    @action(detail=False, methods=["get"], url_path="test")
    def getAll(self, request):
        return Response("connexion")