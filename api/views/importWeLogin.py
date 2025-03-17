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

with open("token.tok","r") as f:
    TOKEN = f.read()

@api_view(['POST'])
def importWeLogin(request):
    #return Response({"message": "Cette requete est desactivé pour eviter la supression de la BDD. Si vous souhaitez vraiment l'utiliser vous devez modifier le fichier importWeLogin.py et mettre la ligne envoyant ce message en commentaire"})

    debut = time()

    Utilisateur.objects.all().delete()
  
    #limité a un maximum de 100 par l'api
    limite = 100
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }

    part = []

    offset = 0  
    endReached = False
    while offset < LIMITE_UTILISATEUR:
        url = f"https://weapi1.welogin.fr/commandes?id_produit={ID_PRODUIT_PART_SOCIAL}&limit={limite}&offset={offset}"  
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()["data"]
            part += data

            if len(part) != limite and endReached:
                return Response({"message": "Probleme au niveau de la limite, l'api n'a pas renvoyé autant d'entrée que prévu","limite":limite,"url":url,"taille reponse":len(data)})
            elif len(part) != limite:
                endReached = True
                
        elif response.status_code == 422:
            #le offset est plus grand que le nombre d'entrée de l'api, on a recupéré toutes les entrées
            break
        else:
            return Response({"message": "Échec de l'import des utilisateurs","status":response.status_code,"url":url,"reponse":response})
        
        offset += limite

    print(part)


    return Response({"message": "Importation reussie en {}s".format(round(time()-debut,3))})

def updateWeLogin(request):
    pass