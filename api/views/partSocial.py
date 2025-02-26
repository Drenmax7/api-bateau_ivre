from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser 

from django.core import exceptions
from django.db.utils import DataError

from .generalFunctions import filtreTable, updateTable
from ..models import PartSocial,Societaire
from ..serializers import PartSocialSerializer

class PartSocialAPIView(viewsets.GenericViewSet):
    queryset = PartSocial.objects.all()
    serializer_class = PartSocialSerializer

    """Permet à un utilisateur disposant des permissions necessaire de recuperer les informations concernant les parts social des societaires
    Le body de la requete doit contenir les champs 'colonne', 'filtre' et 'mode'.
    'colonne' contient les colonnes sur lesquelles les filtres seront appliqué,
    'filtre' contient les filtres qui seront appliqué sur les colonnes,
    'mode' contient la façon d'appliquer le filtre. Les modes possibles sont '==', '>', '>=', '<', '<=', '^'
    """
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
    
    """Permet à un utilisateur disposant des permissions necessaire de modifier les informations concernant l'achat de part social
    Le body de la requete doit contenir les champs 'id_achat', 'colonne', 'valeur'.
    'id_achat' correspond à l'id de l'achat de part dont on veut modifier les informations, 
    'colonne' aux champs à modifier,
    'valeur' est la valeur qui sera placé dans le champs
    """
    @action(detail=False, methods=["put"], permission_classes = [IsAdminUser])
    def updatePartSocial(self, request):
        table_id = request.data.get("id_achat")
        if not table_id:
            return Response({"message": "id_achat est un parametre obligatoire"}, status=status.HTTP_400_BAD_REQUEST)

        entry = PartSocial.objects.filter(id_achat=table_id)
        if len(entry) == 0:
            return Response({"message": "Aucun achat de part social n'a cette id"}, status=status.HTTP_404_NOT_FOUND)

        try:
            entry.update(**updateTable(request))
            return Response({"message": "Changement effectue"}, status=status.HTTP_200_OK)
        except exceptions.FieldDoesNotExist as e:
            return Response({"message":f"{e} Les colonnes possible sont {PartSocial._meta.get_fields()}."},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    """Permet à un utilisateur disposant des permissions necessaire de supprimer un achat de part social
    Le body de la requete doit contenir le champs 'id_achat' qui correspond à l'id de l'achat de part que l'on veut supprimer
    """
    @action(detail=False, methods=["delete"], permission_classes = [IsAdminUser])
    def deletePartSocial(self, request):
        table_id = request.data.get("id_achat")
        if not table_id:
            return Response({"message": "id_achat est un parametre obligatoire"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            entry = PartSocial.objects.get(id_achat=table_id)
            entry.delete()
            return Response({"message": "Achat de part social supprime"}, status=status.HTTP_200_OK)
        except PartSocial.DoesNotExist:
            return Response({"message": "Aucun achat de part social n'a cette id"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    """Permet à un utilisateur disposant des permissions necessaire d'ajouter un achat de part social
    Le body de la requete doit contenir tous les champs non nulle de la table, avec les valeurs qui doivent etre mise sur ces champs
    L'id de societaire doit exister
    Renvoie l'id de l'achat de part social ainsi crée
    """
    @action(detail=False, methods=["post"], permission_classes = [IsAdminUser])
    def addPartSocial(self, request):
        date_achat = request.data.get("date_achat")
        quantite = request.data.get("quantite")
        num_facture = request.data.get("num_facture")
        id_societaire = request.data.get("id_societaire")
        
        if not all([date_achat, quantite, num_facture, id_societaire]):
            return Response({"message": "Certains champs ne sont pas remplis. Voici les champs necessaire : date_achat, quantite, num_facture, id_societaire"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        query = Societaire.objects.filter(id_societaire=id_societaire)
        if len(query) == 0:
            return Response({"message": "Aucun societaire n'a cette id"}, status=status.HTTP_400_BAD_REQUEST)
        societaire = query[0]

        try:
            part = PartSocial(
                date_achat = date_achat,
                quantite = quantite,
                num_facture = num_facture,
                id_societaire = societaire
            )
            part.save()

            return Response({"message": "Achat de part social cree", "id_achat": part.id_achat}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    
    