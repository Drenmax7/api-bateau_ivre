from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser 

from django.core import exceptions
from django.contrib.auth import authenticate, login
from django.middleware.csrf import get_token
from django.db.utils import DataError

from .generalFunctions import filtreTable, updateTable
from ..models import Utilisateur, Connexion, HistoriqueConnexion, College, Reserve, Rejoint, Societaire, PartSocial
from ..serializers import UtilisateurSerializer, CollegeSerializer

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
            return Response({"message":f"{e} Les colonnes possible sont {[field.name for field in Utilisateur._meta.concrete_fields]}."},status=status.HTTP_400_BAD_REQUEST)
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
        college = request.data.get("college")
        
        if not all([i != None for i in [nom, prenom, civilite, adresse, ville, pays, code_postal, telephone, complement_adresse, mail, password, college]]):
            return Response({"message": "Certains champs ne sont pas remplis. Voici les champs necessaire : nom, prenom, civilite, \
                             adresse, ville, pays, code_postal, telephone, complement_adresse, mail, password, college"}, 
                            status=status.HTTP_400_BAD_REQUEST)

        if Utilisateur.objects.filter(mail=mail).exists():
            return Response({"message": "Ce mail est deja pris"}, status=status.HTTP_400_BAD_REQUEST)
        
        query = College.objects.filter(nom=college)
        if len(query) == 0:
            return Response({"message": f"Aucun college n'a ce nom. Voici la liste des colleges : {CollegeSerializer(College.objects.all()).data}"}, status=status.HTTP_400_BAD_REQUEST)
        college = query[0]

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
                college = college,

                mail = mail,
            )

            user.set_password(password)
            user.save()

            return Response({"message": "Utilisateur cree", "id_utilisateur": user.id_utilisateur}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    """Permet de fusionner 2 utilisateurs
    Le body de la requete doit contenir les champs "recipient", "dissout" qui sont des id d'utilisateur
    Les informations de l'utilisateur dissout vont etre transféré à l'utilisateur recipient de la facon suivante
    Tous les champs vide de recipient sont rempli avec les champs de dissout si rempli
    Recipient recupere toutes les participations à des evenements de dissout, et si les 2 ont participé au meme evenement, additionne le nombre de place
    Recipient recupere toutes les connexion de dissout, et ignore les connexions en commun
    Recipient recupere toutes les chaloupes rejointe de dissout, et ignore celles en commun, et le booleen dirige est mis à vrai si celui de dissout l'est
    Si dissout est societaire mais pas recipient, alors recipient recupere l'aspect societaire
    Si recipient et dissout sont societaire alors on fusionne societaire recipient avec societaire dissout de la maniere suivante
        Tous les champs vide de societaire recipient sont rempli avec les champs de societaire dissout si rempli
        Toutes les parts sociale que societaire dissout a acheté sont transféré à societaire recipient tel quel
    """
    @action(detail=False, methods=["post"], permission_classes = [IsAdminUser])
    def fusionneUsers(self, request):
        recipientID = request.data.get("recipient")
        if not recipientID:
            return Response({"message": "recipient est un parametre obligatoire"}, status=status.HTTP_400_BAD_REQUEST)
        
        query = Utilisateur.objects.filter(id_utilisateur=recipientID)
        if len(query) == 0:
            return Response({"message": "Aucun utilisateur n'a l'id de recipient"}, status=status.HTTP_400_BAD_REQUEST)
        recipient = query[0]
    
        dissoutID = request.data.get("dissout")
        if not dissoutID:
            return Response({"message": "dissout est un parametre obligatoire"}, status=status.HTTP_400_BAD_REQUEST)
        
        query = Utilisateur.objects.filter(id_utilisateur=dissoutID)
        if len(query) == 0:
            return Response({"message": "Aucun utilisateur n'a l'id de dissout"}, status=status.HTTP_400_BAD_REQUEST)
        dissout = query[0]
        
        #Tous les champs vide de recipient sont rempli avec les champs de dissout si rempli
        for field in recipient._meta.fields:
            if getattr(recipient, field.name) in [None, "", []]:  
                setattr(recipient, field.name, getattr(dissout, field.name))
    
        #Recipient recupere toutes les participations à des evenements de dissout
        for reservation in Reserve.objects.filter(id_utilisateur=dissout):
            existing = Reserve.objects.filter(id_utilisateur=recipient, id_evenement=reservation.id_evenement).first()
            if existing:
                existing.nb_place += reservation.nb_place
                existing.save()
            else:
                reservation.id_utilisateur = recipient
                reservation.save()
        
        #Recipient recupere toutes les connexion de dissout
        HistoriqueConnexion.objects.filter(id_utilisateur=dissout).exclude(jour__in=HistoriqueConnexion.objects.filter(id_utilisateur=recipient).values("jour")).update(id_utilisateur=recipient)
        
        #Recipient recupere toutes les chaloupes rejointe de dissout
        for rejoint in Rejoint.objects.filter(id_utilisateur=dissout):
            existing = Rejoint.objects.filter(id_utilisateur=recipient, id_chaloupe=rejoint.id_chaloupe).first()
            if not existing:
                rejoint.id_utilisateur = recipient
                rejoint.save()
            elif rejoint.dirige:
                existing.dirige = True
                existing.save()
        
        societaire_dissout = Societaire.objects.filter(id_utilisateur=dissout).first()
        societaire_recipient = Societaire.objects.filter(id_utilisateur=recipient).first()
        
        if societaire_dissout:
            # Si dissout est societaire mais pas recipient, alors recipient recupere l'aspect societaire
            if not societaire_recipient:
                societaire_dissout.id_utilisateur = recipient
                societaire_dissout.save()
            else:
                #Tous les champs vide de societaire recipient sont rempli avec les champs de societaire dissout si rempli
                for field in societaire_recipient._meta.fields:
                    if getattr(societaire_recipient, field.name) in [None, "", []]:
                        setattr(societaire_recipient, field.name, getattr(societaire_dissout, field.name))

                #Toutes les parts sociale que societaire dissout a acheté sont transféré à societaire recipient tel quel
                PartSocial.objects.filter(id_societaire=societaire_dissout).update(id_societaire=societaire_recipient)
                societaire_recipient.save()
                societaire_dissout.delete()

        recipient.save()
        dissout.delete()
        return Response({"message": "Fusion efectué"}, status=status.HTTP_200_OK)
    

    """Permet à un utilisateur disposant des permissions necessaire de recuperer les informations concernant des colleges
    Le body de la requete doit contenir les champs 'colonne', 'filtre' et 'mode'.
    'colonne' contient les colonnes sur lesquelles les filtres seront appliqué,
    'filtre' contient les filtres qui seront appliqué sur les colonnes,
    'mode' contient la façon d'appliquer le filtre. Les modes possibles sont '==', '>', '>=', '<', '<=', '^'
    """
    @action(detail=False, methods=["get"], permission_classes = [IsAuthenticated])
    def getCollege(self, request):
        try :
            utilisateurs = College.objects.filter(**filtreTable(request))
            serializer = CollegeSerializer(utilisateurs, many=True)
            return Response(serializer.data)

        except exceptions.FieldError as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response(str(e),status=status.HTTP_403_FORBIDDEN)
        
    """Permet à un utilisateur disposant des permissions necessaire de modifier les informations concernant un college
    Le body de la requete doit contenir les champs 'college', 'colonne', 'valeur'.
    'college' correspond au nom du college dont on veut modifier les informations, 
    'colonne' aux champs à modifier,
    'valeur' est la valeur qui sera placé dans le champs
    """
    @action(detail=False, methods=["put"], permission_classes = [IsAdminUser])
    def updateCollege(self, request):
        table_id = request.data.get("college")
        if not table_id:
            return Response({"message": "college est un parametre obligatoire"}, status=status.HTTP_400_BAD_REQUEST)

        entry = College.objects.filter(nom=table_id)
        if len(entry) == 0:
            return Response({"message": "Aucun college n'a ce nom"}, status=status.HTTP_404_NOT_FOUND)

        try:
            entry.update(**updateTable(request))
            return Response({"message": "Changement effectue"}, status=status.HTTP_200_OK)
        except exceptions.FieldDoesNotExist as e:
            return Response({"message":f"{e} Les colonnes possible sont {[field.name for field in College._meta.concrete_fields]}."},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    """Permet à un utilisateur disposant des permissions necessaire de supprimer un college
    Le body de la requete doit contenir le champs 'college' qui correspond au nom du college que l'on veut supprimer
    """
    @action(detail=False, methods=["delete"], permission_classes = [IsAdminUser])
    def deleteCollege(self, request):
        table_id = request.data.get("college")
        if not table_id:
            return Response({"message": "college est un parametre obligatoire"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            entry = College.objects.get(nom=table_id)
            entry.delete()
            return Response({"message": "College supprime"}, status=status.HTTP_200_OK)
        except College.DoesNotExist:
            return Response({"message": "Aucun college n'a ce nom"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    """Permet à un utilisateur disposant des permissions necessaire d'ajouter un college
    Le body de la requete doit contenir tous les champs non nulle de la table, avec les valeurs qui doivent etre mise sur ces champs
    Renvoie le nom du college ainsi crée
    """
    @action(detail=False, methods=["post"], permission_classes = [IsAdminUser])
    def addCollege(self, request):
        nom = request.data.get("nom")
        
        if not all([i != None for i in [nom]]):
            return Response({"message": "Certains champs ne sont pas remplis. Voici les champs necessaire : nom"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        try:
            chaloupe = College(
                nom = nom
            )
            chaloupe.save()

            return Response({"message": "Chaloupe cree", "nom": chaloupe.nom}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)