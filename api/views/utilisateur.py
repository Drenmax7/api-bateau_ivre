from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser 

from django.core import exceptions
from django.contrib.auth import authenticate, login
from django.middleware.csrf import get_token
from django.db.utils import DataError

from .generalFunctions import filtreTable, updateTable
from ..models import Utilisateur, Connexion, HistoriqueConnexion
from ..serializers import UtilisateurSerializer

import datetime

class UtilisateurAPIView(viewsets.GenericViewSet):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer 
    
    """Permet à un utilisateur de se connecter et d'acceder aux requetes sensibles
    Le body de la requete doit contenir les champs 'mail' et 'password' dont les valeurs correspondent aux mail et mot de passe de l'utilisateur
    Renvoie un token permettant d'identifier la session actuelle, et un deuxieme permettant de passer la verification csrf.
    Ces 2 tokens sont a passer dans l'url de chaque requete envoyé par la suite à l'api
    """
    @action(detail=False, methods=["post"], authentication_classes = [])
    def login(self, request):
        mail = request.data.get("mail")
        password = request.data.get("password")

        user = authenticate(username=mail, password=password)    
        if user:
            if user.premiere_connexion == None:
                user.premiere_connexion = datetime.datetime.now()
            user.derniere_connexion = datetime.datetime.now()
            user.save()
            
            jour = datetime.datetime.now().strftime("%Y-%m-%d")
            query = Connexion.objects.filter(jour=jour)
            if len(query) == 0:
                connexion = Connexion(
                    jour=jour
                )
                connexion.save()
            else:
                connexion = query[0]
            
            query = HistoriqueConnexion.objects.filter(jour=connexion,id_utilisateur=user)
            if len(query) == 0:
                historique = HistoriqueConnexion(
                    jour=connexion,
                    id_utilisateur=user
                )
                historique.save()

            login(request, user)
            request.session.save()
            sessionid = request.session.session_key
            csrftoken = get_token(request)
            return Response({"message":"Connexion reussie","sessionid":sessionid,"csrftoken":csrftoken},status=status.HTTP_200_OK)
        else:
            return Response({"message":"Connexion echoue","sessionid":"", "csrftoken":""}, status=status.HTTP_401_UNAUTHORIZED)

    """Permet à un utilisateur connecté de recuperer les informations le concernant
    """
    @action(detail=False, methods=["get"], permission_classes = [IsAuthenticated])
    def getLoginUser(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    """Permet à un utilisateur conneecté de modifier son mot de passe
    Le body de la requete doit contenir le champs 'password' qui correspont au nouveau mot de passe
    """
    @action(detail=False, methods=["put"], permission_classes = [IsAuthenticated])
    def updateSelfPassword(self, request):
        password = request.data.get("password")
        if not password:
            return Response({"message": "password est un parametre obligatoire"}, status=status.HTTP_400_BAD_REQUEST)

        request.user.set_password(password)
        request.user.save()

        return Response({"message": "Changement effectue"}, status=status.HTTP_200_OK)
    
    """Permet à un utilisateur disposant des permissions necessaire de modifier le mot de passe d'un utilisateur
    Le body de la requete doit contenir les champss 'id_utilisateur' et 'password' qui correspondent à 
    l'id de l'utilisateur dont on veut modifier le mot de passe, et au nouveau mot de passe
    """
    @action(detail=False, methods=["put"], permission_classes = [IsAdminUser])
    def updateUserPassword(self, request):
        table_id = request.data.get("id_utilisateur")
        if not table_id:
            return Response({"message": "id_utilisateur est un parametre obligatoire"}, status=status.HTTP_400_BAD_REQUEST)
        
        password = request.data.get("password")
        if not password:
            return Response({"message": "password est un parametre obligatoire"}, status=status.HTTP_400_BAD_REQUEST)

        user = Utilisateur.objects.get(id_utilisateur=table_id)
        user.set_password(password)
        user.save()

        return Response({"message": "Changement effectue"}, status=status.HTTP_200_OK)

    """Permet à un utilisateur disposant des permissions necessaire de recuperer les informations concernant d'autres utilisateurs
    Le body de la requete doit contenir les champs 'colonne', 'filtre' et 'mode'.
    'colonne' contient les colonnes sur lesquelles les filtres seront appliqué,
    'filtre' contient les filtres qui seront appliqué sur les colonnes,
    'mode' contient la façon d'appliquer le filtre. Les modes possibles sont '==', '>', '>=', '<', '<=', '^'
    """
    @action(detail=False, methods=["get"], permission_classes = [IsAuthenticated])
    def getUser(self, request):
        try :
            utilisateurs = Utilisateur.objects.filter(**filtreTable(request))
            serializer = self.get_serializer(utilisateurs, many=True)
            return Response(serializer.data)

        except exceptions.FieldError as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response(str(e),status=status.HTTP_403_FORBIDDEN)
    
    """Permet à un utilisateur disposant des permissions necessaire de modifier les informations concernant un autre utilisateur
    Le body de la requete doit contenir les champs 'id_utilisateur', 'colonne', 'valeur'.
    'id_utilisateur' correspond à l'id de l'utilisateur dont on veut modifier les informations, 
    'colonne' aux champs à modifier,
    'valeur' est la valeur qui sera placé dans le champs
    """
    @action(detail=False, methods=["put"], permission_classes = [IsAdminUser])
    def updateUser(self, request):
        table_id = request.data.get("id_utilisateur")
        if not table_id:
            return Response({"message": "id_utilisateur est un parametre obligatoire"}, status=status.HTTP_400_BAD_REQUEST)

        entry = Utilisateur.objects.filter(id_utilisateur=table_id)
        if len(entry) == 0:
            return Response({"message": "Aucun utilisateur n'a cette id"}, status=status.HTTP_404_NOT_FOUND)

        try:
            entry.update(**updateTable(request))
            return Response({"message": "Changement effectue"}, status=status.HTTP_200_OK)
        except exceptions.FieldDoesNotExist as e:
            return Response({"message":f"{e} Les colonnes possible sont {Utilisateur._meta.get_fields()}."},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    """Permet à un utilisateur disposant des permissions necessaire de supprimer un autre utilisateur
    Le body de la requete doit contenir le champs 'id_utilisateur' qui correspond à l'id de l'utilisateur 
    qu'on veut supprimer.
    """
    @action(detail=False, methods=["delete"], permission_classes = [IsAdminUser])
    def deleteUser(self, request):
        table_id = request.data.get("id_utilisateur")
        if not table_id:
            return Response({"message": "id_utilisateur est un parametre obligatoire"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            entry = Utilisateur.objects.get(id_utilisateur=table_id)
            entry.delete()
            return Response({"message": "Utilisateur supprime"}, status=status.HTTP_200_OK)
        except Utilisateur.DoesNotExist:
            return Response({"message": "Aucun utilisateur n'a cette id"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    """Permet à un utilisateur disposant des permissions necessaire d'ajouter un autre utilisateur
    Le body de la requete doit contenir tous les champs non nulle de la table, avec les valeurs qui doivent etre mise sur ces champs
    Le mail doit etre unique
    Renvoie l'id de l'utilisateur ainsi crée
    """
    @action(detail=False, methods=["post"], permission_classes = []) #pas de permissions pour que quelqu'un puisse creer son compte par lui meme
    def addUser(self, request):
        nom = request.data.get("nom")
        prenom = request.data.get("prenom")
        civilite = request.data.get("civilite")
        adresse = request.data.get("adresse")
        ville = request.data.get("ville")
        pays = request.data.get("pays")
        code_postal = request.data.get("code_postal")
        telephone = request.data.get("telephone")
        complement_adresse = request.data.get("complement_adresse")
        mail = request.data.get("mail")
        password = request.data.get("password")
        
        if not all([nom, prenom, civilite, adresse, ville, pays, code_postal, telephone, complement_adresse, mail, password]):
            return Response({"message": "Certains champs ne sont pas remplis. Voici les champs necessaire : nom, prenom, civilite, adresse, ville, pays, code_postal, telephone, complement_adresse, mail, password"}, 
                            status=status.HTTP_400_BAD_REQUEST)

        if Utilisateur.objects.filter(mail=mail).exists():
            return Response({"message": "Ce mail est deja pris"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = Utilisateur(
                nom = nom,
                prenom = prenom,
                civilite = civilite,
                adresse = adresse,
                ville = ville,
                pays = pays,
                code_postal = code_postal,
                telephone = telephone,
                complement_adresse = complement_adresse,
                premiere_connexion = None,
                derniere_connexion = None,
                longitude = None,
                latitude = None,

                mail = mail,
            )

            user.set_password(password)
            user.save()

            return Response({"message": "Utilisateur cree", "id_utilisateur": user.id_utilisateur}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    
    