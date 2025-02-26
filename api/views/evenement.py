from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser 

from django.core import exceptions

from .generalFunctions import filtreTable, updateTable
from ..models import Evenement, Reserve, Utilisateur
from ..serializers import EvenementSerializer, ReserveSerializer

class EvenementAPIView(viewsets.GenericViewSet):
    queryset = Evenement.objects.all()
    serializer_class = EvenementSerializer

    """Permet de recuperer les informations concernant les evenements
    Le body de la requete doit contenir les champs 'colonne', 'filtre' et 'mode'.
    'colonne' contient les colonnes sur lesquelles les filtres seront appliqué,
    'filtre' contient les filtres qui seront appliqué sur les colonnes,
    'mode' contient la façon d'appliquer le filtre. Les modes possibles sont '==', '>', '>=', '<', '<=', '^'
    """
    @action(detail=False, methods=["get"])
    def getEvenement(self, request):
        try :
            utilisateurs = Evenement.objects.filter(**filtreTable(request))
            serializer = self.get_serializer(utilisateurs, many=True)
            return Response(serializer.data)

        except exceptions.FieldError as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response(str(e),status=status.HTTP_403_FORBIDDEN)
    
    """Permet à un utilisateur disposant des permissions necessaire de modifier les informations concernant un evenement
    Le body de la requete doit contenir les champs 'id_evenement', 'colonne', 'valeur'.
    'id_evenement' correspond à l'id de l'evenement dont on veut modifier les informations, 
    'colonne' aux champs à modifier,
    'valeur' est la valeur qui sera placé dans le champs
    """
    @action(detail=False, methods=["put"], permission_classes = [IsAdminUser])
    def updateEvenement(self, request):
        table_id = request.data.get("id_evenement")
        if not table_id:
            return Response({"message": "id_evenement est un parametre obligatoire"}, status=status.HTTP_400_BAD_REQUEST)

        entry = Evenement.objects.filter(id_evenement=table_id)
        if len(entry) == 0:
            return Response({"message": "Aucun evenement n'a cette id"}, status=status.HTTP_404_NOT_FOUND)

        try:
            entry.update(**updateTable(request))
            return Response({"message": "Changement effectue"}, status=status.HTTP_200_OK)
        except exceptions.FieldDoesNotExist as e:
            return Response({"message":f"{e} Les colonnes possible sont {Evenement._meta.get_fields()}."},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    """Permet à un utilisateur disposant des permissions necessaire de supprimer un evenement
    Le body de la requete doit contenir le champs 'id_evenement' qui correspond à l'id de l'evenement que l'on veut supprimer
    """
    @action(detail=False, methods=["delete"], permission_classes = [IsAdminUser])
    def deleteEvenement(self, request):
        table_id = request.data.get("id_evenement")
        if not table_id:
            return Response({"message": "id_evenement est un parametre obligatoire"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            entry = Evenement.objects.get(id_evenement=table_id)
            entry.delete()
            return Response({"message": "Evenement supprime"}, status=status.HTTP_200_OK)
        except Evenement.DoesNotExist:
            return Response({"message": "Aucun evenement n'a cette id"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    """Permet à un utilisateur disposant des permissions necessaire d'ajouter un evenement
    Le body de la requete doit contenir tous les champs non nulle de la table, avec les valeurs qui doivent etre mise sur ces champs
    Renvoie l'id de l'evenement ainsi crée
    """
    @action(detail=False, methods=["post"], permission_classes = [IsAdminUser])
    def addEvenement(self, request):
        place_disponible = request.data.get("place_disponible")
        date_evenement = request.data.get("date_evenement")
        titre = request.data.get("titre")
        description = request.data.get("description")
        
        if not all([place_disponible, date_evenement, titre, description]):
            return Response({"message": "Certains champs ne sont pas remplis. Voici les champs necessaire : place_disponible, date_evenement, titre, description"}, 
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            evenement = Evenement(
                place_disponible = place_disponible,
                date_evenement = date_evenement,
                titre = titre,
                description = description
            )
            evenement.save()

            return Response({"message": "Evenement cree", "id_evenement": evenement.id_evenement}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        
    """Permet à un utilisateur disposant des permissions necessaire de recuperer les informations concernant les reservations des evenements
    Le body de la requete doit contenir les champs 'colonne', 'filtre' et 'mode'.
    'colonne' contient les colonnes sur lesquelles les filtres seront appliqué,
    'filtre' contient les filtres qui seront appliqué sur les colonnes,
    'mode' contient la façon d'appliquer le filtre. Les modes possibles sont '==', '>', '>=', '<', '<=', '^'
    """
    @action(detail=False, methods=["get"], permission_classes = [IsAuthenticated])
    def getReserve(self, request):
        try :
            utilisateurs = Reserve.objects.filter(**filtreTable(request))
            serializer = ReserveSerializer(utilisateurs, many=True)
            return Response(serializer.data)

        except exceptions.FieldError as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response(str(e),status=status.HTTP_403_FORBIDDEN)

    """Permet à un utilisateur disposant des permissions necessaire de modifier les informations concernant une reservation
    Le body de la requete doit contenir les champs 'id_utilisateur', 'id_evenement', 'colonne', 'valeur'.
    'id_evenement' et 'id_utilisateur' determinent la reservation dont on veut modifier les informations, 
    'colonne' aux champs à modifier,
    'valeur' est la valeur qui sera placé dans le champs
    """
    @action(detail=False, methods=["put"], permission_classes = [IsAdminUser])
    def updateReservation(self, request):
        id_evenement = request.data.get("id_evenement")
        if not id_evenement:
            return Response({"message": "id_evenement est un parametre obligatoire"}, status=status.HTTP_400_BAD_REQUEST)
        
        id_utilisateur = request.data.get("id_utilisateur")
        if not id_utilisateur:
            return Response({"message": "id_utilisateur est un parametre obligatoire"}, status=status.HTTP_400_BAD_REQUEST)


        entry = Reserve.objects.filter(id_evenement=id_evenement, id_utilisateur=id_utilisateur)
        if len(entry) == 0:
            return Response({"message": "Aucun reservation correspondant à ces id n'a été trouvé"}, status=status.HTTP_404_NOT_FOUND)

        try:
            entry.update(**updateTable(request))
            return Response({"message": "Changement effectue"}, status=status.HTTP_200_OK)
        except exceptions.FieldDoesNotExist as e:
            return Response({"message":f"{e} Les colonnes possible sont {Evenement._meta.get_fields()}."},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    """Permet à un utilisateur disposant des permissions necessaire de supprimer une reservation
    Le body de la requete doit contenir le champs 'id_evenement' et 'id_utilisateur' qui determinent la reservation que l'on veut supprimer
    """
    @action(detail=False, methods=["delete"], permission_classes = [IsAdminUser])
    def deleteReservation(self, request):
        id_evenement = request.data.get("id_evenement")
        if not id_evenement:
            return Response({"message": "id_evenement est un parametre obligatoire"}, status=status.HTTP_400_BAD_REQUEST)
        
        id_utilisateur = request.data.get("id_utilisateur")
        if not id_utilisateur:
            return Response({"message": "id_utilisateur est un parametre obligatoire"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            entry = Reserve.objects.filter(id_evenement=id_evenement, id_utilisateur=id_utilisateur)
            entry.delete()
            return Response({"message": "Reservation supprime"}, status=status.HTTP_200_OK)
        except Evenement.DoesNotExist:
            return Response({"message": "Aucun reservation correspondant à ces id n'a été trouvé"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    """Permet à un utilisateur disposant des permissions necessaire d'ajouter une reservation
    Le body de la requete doit contenir tous les champs non nulle de la table, avec les valeurs qui doivent etre mise sur ces champs
    Renvoie l'id de l'evenement ainsi crée
    """
    @action(detail=False, methods=["post"], permission_classes = [IsAdminUser])
    def addReservation(self, request):
        id_utilisateur = request.data.get("id_utilisateur")
        id_evenement = request.data.get("id_evenement")
        nb_place = request.data.get("nb_place")
        
        if not all([id_utilisateur, id_evenement, nb_place]):
            return Response({"message": "Certains champs ne sont pas remplis. Voici les champs necessaire : id_utilisateur, id_evenement, nb_place"}, 
                            status=status.HTTP_400_BAD_REQUEST)

        query = Utilisateur.objects.filter(id_utilisateur=id_utilisateur)
        if len(query) == 0:
            return Response({"message": "Aucun utilisateur n'a cette id"}, status=status.HTTP_400_BAD_REQUEST)
        utilisateur = query[0]

        query = Evenement.objects.filter(id_evenement=id_evenement)
        if len(query) == 0:
            return Response({"message": "Aucun evenement n'a cette id"}, status=status.HTTP_400_BAD_REQUEST)
        evenement = query[0]

        try:
            reservation = Reserve(
                id_utilisateur = utilisateur,
                id_evenement = evenement,
                nb_place = nb_place
            )
            reservation.save()

            return Response({"message": "Reservation cree"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)