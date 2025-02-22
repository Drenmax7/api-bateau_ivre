from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.core import exceptions
from django.contrib.auth import authenticate, login

from .generalFunctions import filtreTable
from ..models import Utilisateur
from ..serializers import UtilisateurSerializer

class UtilisateurAPIView(viewsets.GenericViewSet):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer 
    
    @action(detail=False, methods=["post"], authentication_classes = [])
    def login(self, request):
        mail = request.data.get("mail")
        password = request.data.get("password")

        user = authenticate(username=mail, password=password)
        if user:
            login(request, user)
            request.session.save()
            sessionid = request.session.session_key
            return Response({"message":"Connexion reussie","sessionid":sessionid},status=status.HTTP_200_OK)
        else:
            return Response({"message":"Connexion echoue","sessionid":""}, status=status.HTTP_401_UNAUTHORIZED)


    @action(detail=False, methods=["get"], permission_classes = [IsAuthenticated])
    def getLoginUser(self, request):     
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    

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