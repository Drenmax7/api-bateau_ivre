from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.core import exceptions
from django.db.models import Count
from django.db.models.functions import TruncMonth

from .generalFunctions import filtreTable, updateTable
from ..models import Connexion, HistoriqueConnexion, Utilisateur
from ..serializers import ConnexionSerializer, HistoriqueConnexionSerializer

class ConnexionAPIView(viewsets.GenericViewSet):
    queryset = Connexion.objects.all()
    serializer_class = ConnexionSerializer

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
    

    """Permet à un utilisateur disposant des permissions necessaire de supprimer la connexion d'un utilisateur d'un jour donné
    Le body de la requete doit contenir le champs 'id_utilisateur' et 'jour' qui identifient la connexion que l'on veut supprimer
    """
    @action(detail=False, methods=["delete"], permission_classes = [IsAdminUser])
    def deleteConnexion(self, request):
        id_utilisateur = request.data.get("id_utilisateur")
        if not id_utilisateur:
            return Response({"message": "id_utilisateur est un parametre obligatoire"}, status=status.HTTP_400_BAD_REQUEST)
        
        jour = request.data.get("jour")
        if not jour:
            return Response({"message": "jour est un parametre obligatoire"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            entry = HistoriqueConnexion.objects.get(id_utilisateur=id_utilisateur, jour=jour)
            entry.delete()
            return Response({"message": "Connexion supprime"}, status=status.HTTP_200_OK)
        except HistoriqueConnexion.DoesNotExist:
            return Response({"message": "Aucune connexion de cette utilisateur ce jour la"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

    """Permet à un utilisateur disposant des permissions necessaire d'ajouter une connexion d'un utilisateur à un jour donné
    Le body de la requete doit contenir tous les champs non nulle de la table, avec les valeurs qui doivent etre mise sur ces champs
    L'id de l'utilisateur doit exister
    Renvoie l'id de l'achat de part social ainsi crée
    """
    @action(detail=False, methods=["post"], permission_classes = [IsAdminUser])
    def addConnexion(self, request):
        id_utilisateur = request.data.get("id_utilisateur")
        jour = request.data.get("jour")
        
        if not all([i != None for i in [id_utilisateur, jour]]):
            return Response({"message": "Certains champs ne sont pas remplis. Voici les champs necessaire : id_utilisateur, jour"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        query = Utilisateur.objects.filter(id_utilisateur=id_utilisateur)
        if len(query) == 0:
            return Response({"message": "Aucun utilisateur n'a cette id"}, status=status.HTTP_400_BAD_REQUEST)
        utilisateur = query[0]

        query = Connexion.objects.filter(jour=jour)
        if len(query) == 0:
            connexion = Connexion(
                jour = jour
            )
        else:
            connexion = query[0]

        try:
            historique = HistoriqueConnexion(
                jour = connexion,
                id_utilisateur = utilisateur
            )
            historique.save()

            return Response({"message": "Enregistrement de la connexion effectué"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)