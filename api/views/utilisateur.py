from rest_framework.decorators import action, permission_classes
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


from ..models import Utilisateur
from ..serializers import UtilisateurSerializer

class UtilisateurAPIView(viewsets.ViewSet):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer

    
    
    @action(detail=False, methods=["get"], url_path="test")
    def getAllget(self, request):
        return Response("utilisateur")
    
    @action(detail=False, methods=["post"], url_path="testpost")
    def getAll(self, request):
        return Response("utilisateur")
    
    
    @action(detail=False, methods=["post"], authentication_classes = [])
    def login(self, request):
        mail = request.data.get("mail")
        password = request.data.get("password")

        user = authenticate(username=mail, password=password)
        if user:
            login(request, user)
            return Response("Connexion accepte",status=status.HTTP_200_OK)
        else:
            return Response("Connexion echoue", status=status.HTTP_401_UNAUTHORIZED)
