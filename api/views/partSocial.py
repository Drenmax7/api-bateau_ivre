from rest_framework.decorators import action, permission_classes
from rest_framework import viewsets
from rest_framework.response import Response

from ..models import PartSocial
from ..serializers import PartSocialSerializer

class PartSocialAPIView(viewsets.ModelViewSet):
    queryset = PartSocial.objects.all()
    serializer_class = PartSocialSerializer

    @action(detail=False, methods=["get"], url_path="test")
    def getAll(self, request):
        return Response("part social")