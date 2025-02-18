from rest_framework.decorators import action, permission_classes
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from django.views.decorators.csrf import csrf_exempt
from django.core import exceptions

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


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
            return Response("Connexion accepte",status=status.HTTP_200_OK)
        else:
            return Response("Connexion echoue", status=status.HTTP_401_UNAUTHORIZED)


    @action(detail=False, methods=["get"], permission_classes = [IsAuthenticated])
    def getLoginUser(self, request):        
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=["get"], permission_classes = [IsAuthenticated])
    def getUser(self, request):
        colonne = request.data.get('colonne',[])
        filtre = request.data.get('filtre',[])
        mode = request.data.get("mode",[])

        if "password" in colonne:
            return Response("Cannot filter by password for security reason",status=status.HTTP_403_FORBIDDEN)

        taille = min(len(colonne),len(filtre))

        colonne = colonne[:taille]
        filtre = filtre[:taille]
        while len(mode) < taille:
            mode.append(0)


        filtre_dict = {}
        for i in range(len(colonne)):
            col = colonne[i]
            
            if mode[i] == "<":
                action = "lt"
            elif mode[i] == "<=":
                action = "lte"
            elif mode[i] == ">":
                action = "gt"
            elif mode[i] == ">=":
                action = "gte"
            elif mode[i] == "==":
                action = "exact"
            elif mode[i] == "^":
                action = "icontains"
            else:
                action = "exact"
            
            filtre_dict[f"{col}__{action}"] = filtre[i]

        try :
            utilisateurs = Utilisateur.objects.filter(**filtre_dict)
            serializer = self.get_serializer(utilisateurs, many=True)
            return Response(serializer.data)

        except exceptions.FieldError as e:
            return Response(str(e))
