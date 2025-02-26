from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser 

from django.core import exceptions
from django.db.utils import DataError

from .generalFunctions import filtreTable, updateTable
from ..models import Societaire, Utilisateur
from ..serializers import SocietaireSerializer

class SocietaireAPIView(viewsets.GenericViewSet):
    queryset = Societaire.objects.all()
    serializer_class = SocietaireSerializer

    """Permet à un utilisateur disposant des permissions necessaire de recuperer les informations concernant des societaires
    Le body de la requete doit contenir les champs 'colonne', 'filtre' et 'mode'.
    'colonne' contient les colonnes sur lesquelles les filtres seront appliqué,
    'filtre' contient les filtres qui seront appliqué sur les colonnes,
    'mode' contient la façon d'appliquer le filtre. Les modes possibles sont '==', '>', '>=', '<', '<=', '^'
    """
    @action(detail=False, methods=["get"], permission_classes = [IsAuthenticated])
    def getSocietaire(self, request):
        try :
            utilisateurs = Societaire.objects.filter(**filtreTable(request))
            serializer = self.get_serializer(utilisateurs, many=True)
            return Response(serializer.data)

        except exceptions.FieldError as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response(str(e),status=status.HTTP_403_FORBIDDEN)
    
    """Permet à un utilisateur disposant des permissions necessaire de modifier les informations concernant un societaire
    Le body de la requete doit contenir les champs 'id_societaire', 'colonne', 'valeur'.
    'id_societaire' correspond à l'id du societaire dont on veut modifier les informations, 
    'colonne' aux champs à modifier,
    'valeur' est la valeur qui sera placé dans le champs
    """
    @action(detail=False, methods=["put"], permission_classes = [IsAdminUser])
    def updateSocietaire(self, request):
        table_id = request.data.get("id_societaire")
        if not table_id:
            return Response({"message": "id_societaire est un parametre obligatoire"}, status=status.HTTP_400_BAD_REQUEST)

        entry = Societaire.objects.filter(id_societaire=table_id)
        if len(entry) == 0:
            return Response({"message": "Aucun societaire n'a cette id"}, status=status.HTTP_404_NOT_FOUND)

        try:
            entry.update(**updateTable(request))
            return Response({"message": "Changement effectue"}, status=status.HTTP_200_OK)
        except exceptions.FieldDoesNotExist as e:
            return Response({"message":f"{e} Les colonnes possible sont {Societaire._meta.get_fields()}."},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    """Permet à un utilisateur disposant des permissions necessaire de supprimer un societaire
    Le body de la requete doit contenir le champs 'id_societaire' qui correspond à l'id du societaire qu'on veut supprimer.
    """
    @action(detail=False, methods=["delete"], permission_classes = [IsAdminUser])
    def deleteSocietaire(self, request):
        table_id = request.data.get("id_societaire")
        if not table_id:
            return Response({"message": "id_societaire est un parametre obligatoire"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            entry = Societaire.objects.get(id_societaire=table_id)
            entry.delete()
            return Response({"message": "Societaire supprime"}, status=status.HTTP_200_OK)
        except Societaire.DoesNotExist:
            return Response({"message": "Aucun societaire n'a cette id"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    """Permet à un utilisateur disposant des permissions necessaire d'ajouter un societaire
    Le body de la requete doit contenir tous les champs non nulle de la table, avec les valeurs qui doivent etre mise sur ces champs
    L'id de l'utilisateur doit exister et ne pas deja etre utiliser dans une autre entrée de societaire
    Renvoie l'id du societaire ainsi crée
    """
    @action(detail=False, methods=["post"], permission_classes = [IsAdminUser])
    def addSocietaire(self, request):
        id_utilisateur = request.data.get("id_utilisateur")
        organisation = request.data.get("organisation")
        
        if not all([id_utilisateur, organisation]):
            return Response({"message": "Certains champs ne sont pas remplis. Voici les champs necessaire : id_utilisateur, organisation"}, 
                            status=status.HTTP_400_BAD_REQUEST)

        if Societaire.objects.filter(id_utilisateur=id_utilisateur).exists():
            return Response({"message": "Cet utilisateur est deja societaire"}, status=status.HTTP_400_BAD_REQUEST)

        query = Utilisateur.objects.filter(id_utilisateur=id_utilisateur)
        if len(query) == 0:
            return Response({"message": "Aucun utilisateur n'a cette id"}, status=status.HTTP_400_BAD_REQUEST)
        utilisateur = query[0]

        try:
            societaire = Societaire(
                id_utilisateur=utilisateur,
                organisation=organisation
            )
            societaire.save()

            return Response({"message": "Societaire cree", "id_societaire": societaire.id_societaire}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    
    