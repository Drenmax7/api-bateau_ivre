from rest_framework.decorators import action, permission_classes
from rest_framework import viewsets
from rest_framework.response import Response

from ..models import Societaire
from ..serializers import SocietaireSerializer

class SocietaireAPIView(viewsets.ModelViewSet):
    queryset = Societaire.objects.all()
    serializer_class = SocietaireSerializer

    @action(detail=False, methods=["get"], url_path="test")
    def getAll(self, request):
        return Response("societaire")