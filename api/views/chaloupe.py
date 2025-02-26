from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.core import exceptions

from .generalFunctions import filtreTable, updateTable
from ..models import Chaloupe, Rejoint, Societaire
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
        
    """Permet à un utilisateur disposant des permissions necessaire de modifier les informations concernant une chaloupe
    Le body de la requete doit contenir les champs 'id_chaloupe', 'colonne', 'valeur'.
    'id_chaloupe' correspond à l'id de la chaloupe dont on veut modifier les informations, 
    'colonne' aux champs à modifier,
    'valeur' est la valeur qui sera placé dans le champs
    """
    @action(detail=False, methods=["put"], permission_classes = [IsAdminUser])
    def updateChaloupe(self, request):
        table_id = request.data.get("id_chaloupe")
        if not table_id:
            return Response({"message": "id_chaloupe est un parametre obligatoire"}, status=status.HTTP_400_BAD_REQUEST)

        entry = Chaloupe.objects.filter(id_chaloupe=table_id)
        if len(entry) == 0:
            return Response({"message": "Aucune chaloupe n'a cette id"}, status=status.HTTP_404_NOT_FOUND)

        try:
            entry.update(**updateTable(request))
            return Response({"message": "Changement effectue"}, status=status.HTTP_200_OK)
        except exceptions.FieldDoesNotExist as e:
            return Response({"message":f"{e} Les colonnes possible sont {Chaloupe._meta.get_fields()}."},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    """Permet à un utilisateur disposant des permissions necessaire de supprimer une chaloupe
    Le body de la requete doit contenir le champs 'id_chaloupe' qui correspond à l'id de la chaloupe que l'on veut supprimer
    """
    @action(detail=False, methods=["delete"], permission_classes = [IsAdminUser])
    def deleteChaloupe(self, request):
        table_id = request.data.get("id_chaloupe")
        if not table_id:
            return Response({"message": "id_chaloupe est un parametre obligatoire"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            entry = Chaloupe.objects.get(id_chaloupe=table_id)
            entry.delete()
            return Response({"message": "Chaloupe supprime"}, status=status.HTTP_200_OK)
        except Chaloupe.DoesNotExist:
            return Response({"message": "Aucune chaloupe n'a cette id"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    """Permet à un utilisateur disposant des permissions necessaire d'ajouter une chaloupe
    Le body de la requete doit contenir tous les champs non nulle de la table, avec les valeurs qui doivent etre mise sur ces champs
    Renvoie l'id de chaloupe ainsi crée
    """
    @action(detail=False, methods=["post"], permission_classes = [IsAdminUser])
    def addChaloupe(self, request):
        nom = request.data.get("nom")
        description = request.data.get("description")
        
        if not all([nom, description]):
            return Response({"message": "Certains champs ne sont pas remplis. Voici les champs necessaire : nom, description"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        try:
            chaloupe = Chaloupe(
                nom = nom,
                description = description
            )
            chaloupe.save()

            return Response({"message": "Chaloupe cree", "id_chaloupe": chaloupe.id_chaloupe}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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

    """Permet à un utilisateur disposant des permissions necessaire de modifier la participation d'un societaire a une chaloupe
    Le body de la requete doit contenir les champs 'id_societaire', 'id_chaloupe', 'colonne', 'valeur'.
    'id_societaire' et 'id_chaloupe' identifient la participation dont on veut modifier les informations, 
    'colonne' aux champs à modifier,
    'valeur' est la valeur qui sera placé dans le champs
    """
    @action(detail=False, methods=["put"], permission_classes = [IsAdminUser])
    def updateRejoint(self, request):
        id_chaloupe = request.data.get("id_chaloupe")
        if not id_chaloupe:
            return Response({"message": "id_chaloupe est un parametre obligatoire"}, status=status.HTTP_400_BAD_REQUEST)
        
        id_societaire = request.data.get("id_societaire")
        if not id_societaire:
            return Response({"message": "id_societaire est un parametre obligatoire"}, status=status.HTTP_400_BAD_REQUEST)

        entry = Rejoint.objects.filter(id_societaire=id_societaire, id_chaloupe=id_chaloupe)
        if len(entry) == 0:
            return Response({"message": "Aucune participation correspondant à ces id n'a été trouvé"}, status=status.HTTP_404_NOT_FOUND)

        try:
            entry.update(**updateTable(request))
            return Response({"message": "Changement effectue"}, status=status.HTTP_200_OK)
        except exceptions.FieldDoesNotExist as e:
            return Response({"message":f"{e} Les colonnes possible sont {Chaloupe._meta.get_fields()}."},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    """Permet à un utilisateur disposant des permissions necessaire de supprimer la participation d'un utilisateur à une chaloupe
    Le body de la requete doit contenir le champs 'id_societaire' et 'id_chaloupe' qui identifient la participation que l'on veut supprimer
    """
    @action(detail=False, methods=["delete"], permission_classes = [IsAdminUser])
    def deleteRejoint(self, request):
        print("delete rejoin\n\n\n")
        id_chaloupe = request.data.get("id_chaloupe")
        if not id_chaloupe:
            return Response({"message": "id_chaloupe est un parametre obligatoire"}, status=status.HTTP_400_BAD_REQUEST)
        
        id_societaire = request.data.get("id_societaire")
        if not id_societaire:
            return Response({"message": "id_societaire est un parametre obligatoire"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            entry = Rejoint.objects.get(id_chaloupe=id_chaloupe, id_societaire=id_societaire)
            entry.delete()
            return Response({"message": "Participation supprime"}, status=status.HTTP_200_OK)
        except Rejoint.DoesNotExist:
            return Response({"message": "Aucune participation n'a ces id"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    """Permet à un utilisateur disposant des permissions necessaire d'ajouter une participation d'un utilisateur à une chaloupe
    Le body de la requete doit contenir tous les champs non nulle de la table, avec les valeurs qui doivent etre mise sur ces champs
    Renvoie l'id de chaloupe ainsi crée
    """
    @action(detail=False, methods=["post"], permission_classes = [IsAdminUser])
    def addRejoint(self, request):
        id_societaire = request.data.get("id_societaire")
        id_chaloupe = request.data.get("id_chaloupe")
        dirige = request.data.get("dirige")
        
        if not all([id_societaire, id_chaloupe, dirige]):
            return Response({"message": "Certains champs ne sont pas remplis. Voici les champs necessaire : id_societaire, id_chaloupe, dirige"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        query = Societaire.objects.filter(id_societaire=id_societaire)
        if len(query) == 0:
            return Response({"message": "Aucun societaire n'a cette id"}, status=status.HTTP_400_BAD_REQUEST)
        societaire = query[0]

        query = Chaloupe.objects.filter(id_chaloupe=id_chaloupe)
        if len(query) == 0:
            return Response({"message": "Aucune chaloupe n'a cette id"}, status=status.HTTP_400_BAD_REQUEST)
        chaloupe = query[0]

        try:
            rejoint = Rejoint(
                id_societaire = societaire,
                id_chaloupe = chaloupe,
                dirige = dirige
            )
            rejoint.save()

            return Response({"message": "Participation cree"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#delete self participation, add self participation