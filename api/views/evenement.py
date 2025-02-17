from rest_framework.decorators import action, permission_classes
from rest_framework import viewsets
from rest_framework.response import Response

from ..models import Evenement
from ..serializers import EvenementSerializer

class EvenementAPIView(viewsets.ViewSet):
    queryset = Evenement.objects.all()
    serializer_class = EvenementSerializer

    @action(detail=False, methods=["get"], url_path="test")
    def getAll(self, request):
        return Response("evenement")