from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.core import exceptions

from .generalFunctions import filtreTable
from ..models import Chaloupe, Rejoint
from ..serializers import ChaloupeSerializer, RejointSerializer

class ChaloupeAPIView(viewsets.GenericViewSet):
    queryset = Chaloupe.objects.all()
    serializer_class = ChaloupeSerializer

    """Permet à un utilisateur disposant des permissions necessaire de recuperer les informations concernant des chaloupes
    Le body de la requete doit contenir les champs 'colonne', 'filtre' et 'mode'.
    'colonne' contient les colonnes sur lesquelles les filtres seront appliqué,
    'filtre' contient les filtres qui seront appliqué sur les colonnes,
    'mode' contient la façon d'appliquer le filtre. Les modes possibles sont '==', '>', '>=', '<', '<=', '^'
    """
    @action(detail=False, methods=["get"], permission_classes = [IsAuthenticated])
    def getChaloupe(self, request):
        try :
            utilisateurs = Chaloupe.objects.filter(**filtreTable(request))
            serializer = self.get_serializer(utilisateurs, many=True)
            return Response(serializer.data)

        except exceptions.FieldError as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response(str(e),status=status.HTTP_403_FORBIDDEN)
        
    """Permet à un utilisateur disposant des permissions necessaire de recuperer les societaires appartenant a une chaloupe
    Le body de la requete doit contenir les champs 'colonne', 'filtre' et 'mode'.
    'colonne' contient les colonnes sur lesquelles les filtres seront appliqué,
    'filtre' contient les filtres qui seront appliqué sur les colonnes,
    'mode' contient la façon d'appliquer le filtre. Les modes possibles sont '==', '>', '>=', '<', '<=', '^'
    """
    @action(detail=False, methods=["get"], permission_classes = [IsAuthenticated])
    def getRejoint(self, request):
        try :
            utilisateurs = Rejoint.objects.filter(**filtreTable(request))
            serializer = RejointSerializer(utilisateurs, many=True)
            return Response(serializer.data)

        except exceptions.FieldError as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response(str(e),status=status.HTTP_403_FORBIDDEN)