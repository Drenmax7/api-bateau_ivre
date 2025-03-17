from rest_framework.decorators import action, permission_classes
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser 
from rest_framework.decorators import api_view

from api.models import *

from django.http import JsonResponse

import requests
import datetime
from time import time

LIMITE_UTILISATEUR = 100
ID_PRODUIT_PART_SOCIAL = 11

with open("token","r") as f:
    TOKEN = f.read()

@api_view(['POST'])
def importWeLogin(request):
    #return Response({"message": "Cette requete est desactivé pour eviter la supression de la BDD. Si vous souhaitez vraiment l'utiliser vous devez modifier le fichier importWeLogin.py et mettre la ligne envoyant ce message en commentaire"})

    debut = time()

    limite = 100
    offset = 0
    url = f"https://weapi1.welogin.fr/commandes?id_produit={ID_PRODUIT_PART_SOCIAL}&limit={limite}&offset={offset}"  
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
    else:
        return Response({"message": "Échec de l'import des utilisateurs","status":response.status_code,"url":url,"reponse":response})

    print(data)


    return Response({"message": "Importation reussie en {}s".format(round(time()-debut,3))})

def updateWeLogin(request):
    pass