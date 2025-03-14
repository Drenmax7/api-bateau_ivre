from rest_framework.decorators import action, permission_classes
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser 

from api.models import *

from django.http import JsonResponse

import datetime
from time import time

LIMITE_UTILISATEUR = 100

class ImportWeLogin(viewsets.GenericViewSet):
    queryset = Utilisateur.objects.all()
    serializer_class = None

    @action(detail=False, methods=["post"], permission_classes = [IsAdminUser])
    def importWeLogin(self, request):
        #return Response({"message": "Cette requete est desactivé pour eviter la supression de la BDD. Si vous souhaitez vraiment l'utiliser vous devez modifier le fichier importWeLogin.py et mettre la ligne envoyant ce message en commentaire"})
    
        debut = time()
    

        return Response({"message": "Importation reussie en {}s".format(round(time()-debut,3))})

    def updateWeLogin(self):
        pass