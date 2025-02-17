from rest_framework.decorators import action, permission_classes
from rest_framework import viewsets
from rest_framework.response import Response

from ..models import Chaloupe
from ..serializers import ChaloupeSerializer

class ChaloupeAPIView(viewsets.ModelViewSet):
    queryset = Chaloupe.objects.all()
    serializer_class = ChaloupeSerializer

    @action(detail=False, methods=["get"], url_path="getAllIDs")
    def getAllIDs(self, request):
        return Response("chaloupe")