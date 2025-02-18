from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.core import exceptions

from .generalFunctions import filtreTable
from ..models import PartSocial
from ..serializers import PartSocialSerializer

class PartSocialAPIView(viewsets.GenericViewSet):
    queryset = PartSocial.objects.all()
    serializer_class = PartSocialSerializer

    @action(detail=False, methods=["get"], permission_classes = [IsAuthenticated])
    def getPartSocial(self, request):
        try :
            utilisateurs = PartSocial.objects.filter(**filtreTable(request))
            serializer = self.get_serializer(utilisateurs, many=True)
            return Response(serializer.data)

        except exceptions.FieldError as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response(str(e),status=status.HTTP_403_FORBIDDEN)