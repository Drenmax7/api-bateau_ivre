from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.core import exceptions
from django.db.models import Count
from django.db.models.functions import TruncMonth

from .generalFunctions import filtreTable
from ..models import Connexion, HistoriqueConnexion
from ..serializers import ConnexionSerializer, HistoriqueConnexionSerializer

class ConnexionAPIView(viewsets.GenericViewSet):
    queryset = Connexion.objects.all()
    serializer_class = ConnexionSerializer

    """Permet à un utilisateur disposant des permissions necessaire de recuperer les jours durant lesquelles des utilisateurs se sont connecté
    Le body de la requete doit contenir les champs 'colonne', 'filtre' et 'mode'.
    'colonne' contient les colonnes sur lesquelles les filtres seront appliqué,
    'filtre' contient les filtres qui seront appliqué sur les colonnes,
    'mode' contient la façon d'appliquer le filtre. Les modes possibles sont '==', '>', '>=', '<', '<=', '^'
    """
    @action(detail=False, methods=["get"], permission_classes = [IsAuthenticated])
    def getConnexion(self, request):
        try :
            utilisateurs = Connexion.objects.filter(**filtreTable(request))
            serializer = self.get_serializer(utilisateurs, many=True)
            return Response(serializer.data)

        except exceptions.FieldError as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response(str(e),status=status.HTTP_403_FORBIDDEN)
    
    """Permet à un utilisateur disposant des permissions necessaire de recuperer les jours de connexion des utilisateurs
    Le body de la requete doit contenir les champs 'colonne', 'filtre' et 'mode'.
    'colonne' contient les colonnes sur lesquelles les filtres seront appliqué,
    'filtre' contient les filtres qui seront appliqué sur les colonnes,
    'mode' contient la façon d'appliquer le filtre. Les modes possibles sont '==', '>', '>=', '<', '<=', '^'
    """
    @action(detail=False, methods=["get"], permission_classes = [IsAuthenticated])
    def getHistorique(self, request):
        try :
            utilisateurs = HistoriqueConnexion.objects.filter(**filtreTable(request))
            serializer = HistoriqueConnexionSerializer(utilisateurs, many=True)
            return Response(serializer.data)

        except exceptions.FieldError as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response(str(e),status=status.HTTP_403_FORBIDDEN)
    
    """Permet à un utilisateur disposant des permissions necessaire de recuperer le nombre de connexion pour chaque jour ou mois
    Le header de la requete peut contenir le champs 'mode' avec la valeur 'jour' ou 'mois', afin de preciser le format de la réponse
    La valeur 'jour' renverra un dictionnaire donnant le nombre de connexion pour chauqe jour, tandis que la valeur 'mois' renverra un dictionnaire
    comptant le nombre de connexion par mois. Sans ce champs, le dictionnaire renvoyé est celui de la valeur 'mois'.
    """
    @action(detail=False, methods=["get"], permission_classes = [IsAuthenticated])
    def compteConnexion(self, request):
        mode = request.GET.get("mode","mois")
        
        if mode != "jour":
            mode = "mois"
        
        if mode == "jour":
            statJour = HistoriqueConnexion.objects.values("jour").annotate(nb_utilisateurs=Count("id_utilisateur"))
            return Response(statJour,status=status.HTTP_200_OK)
    
        if mode == "mois":
            statMois = HistoriqueConnexion.objects.annotate(mois=TruncMonth("jour")).values("mois").annotate(nb_utilisateurs=Count("id_utilisateur")).order_by("mois")
            return Response(statMois,status=status.HTTP_200_OK)

        