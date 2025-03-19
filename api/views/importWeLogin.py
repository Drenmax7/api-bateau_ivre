from rest_framework.decorators import action, permission_classes
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser 
from rest_framework.decorators import api_view

from api.models import *
from .generalFunctions import trouveCoordonnee

from django.http import JsonResponse

import requests
from datetime import datetime
from time import time
import pycountry


LIMITE_PART = 100
ID_PRODUIT_PART_SOCIAL = 11

with open("token.tok","r") as f:
    TOKEN = f.read()
headers = {
    "Authorization": f"Bearer {TOKEN}"
}

def resetBDD():
    Utilisateur.objects.all().delete()
    Connexion.objects.all().delete()
    College.objects.all().delete()

def getPartSocial():
    #limité a un maximum de 100 par l'api
    limite = 100

    part = []

    offset = 0  
    endReached = False
    while offset < LIMITE_PART:
        url = f"https://weapi1.welogin.fr/commandes?id_produit={ID_PRODUIT_PART_SOCIAL}&limit={limite}&offset={offset}"  
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()["data"]
            part += data

            print(f"{len(part)}/... parts social recupéré")

            if len(data) != limite and endReached:
                return Response({"message": "Probleme au niveau de la limite, l'api n'a pas renvoyé autant d'entrée que prévu","limite":limite,"url":url,"taille reponse":len(data)})
            elif len(data) != limite:
                endReached = True
                
        elif response.status_code == 422:
            #le offset est plus grand que le nombre d'entrée de l'api, on a recupéré toutes les entrées
            break
        else:
            return Response({"message": "Échec de l'import des part social","status":response.status_code,"url":url,"reponse":response})
        
        offset += limite

    print(f"{len(part)} parts social recupéré")

    for i in part:
        if len(i["lignes"]) > 1:
            return Response({"message": "Le programme part du principe que un seul article est acheté par part social, mais plusieurs lignes d'achat ont ete trouvé",
                             "status":response.status_code,"url":url,"part":i})

    partFormate = [{"date_achat": i["date_heure"],
                    "id_client" : i["id_client"],
                    "num_facture" : i["no_commande"],
                    "quantite" : i["lignes"][0]["quantite_produit"]
                    } for i in part]

    return partFormate

def getUsers():    
    url = f"https://weapi1.welogin.fr/clients/civilites"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        civilite = response.json()["data"]
        print("civilites recu")
    else:
        return Response({"message": "Échec de l'import des civilites","status":response.status_code,"url":url,"reponse":response})

    civiliteFormat = {
        i["id_civilite"]:i["libelle"] for i in civilite
    }
    
    url = f"https://weapi1.welogin.fr/clients?limit=3000&offset=0"  
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        user = response.json()["data"]
        print(f"{len(user)} utilisateurs recu")
    else:
        return Response({"message": "Échec de l'import des utilisateurs","status":response.status_code,"url":url,"reponse":response})

    userFormate = [
        {
            "id_client" : i["id_client"],
            "nom" : i["nom"],
            "prenom" : i["prenom"],
            "mail" : i["email"],
            "mot_de_passe" : "mot de passe inconnu",
            "civilite" : civiliteFormat.get(i["id_civilite_client"],"n/a"),
            "adresse" : i["adresse"].replace(","," "),
            "ville" : i["ville"],
            "pays" : pycountry.countries.get(alpha_3=i["code_pays"]).name,
            "complement_adresse" : i["adresse_complementaire"],
            "code_postal" : i["code_postal"],
            "telephone" : i["telephone"],
            "college" : i["categorie_client"],
            "organisation" : i["structure"]
        }
        for i in user
    ]

    return userFormate

def addBaseUser():
    #base user
    user = Utilisateur(
        nom = "Duck",
        prenom = "Donald",
        civilite = "n/a",
        adresse = "Tour Eiffel",
        ville = "Paris",
        pays = "France",
        code_postal = "70123",
        telephone = "0612345678",
        complement_adresse = "au sommet",
        longitude = 2.3512712112122625,
        latitude = 48.86363566675727,
        premiere_connexion = datetime.now(),
        derniere_connexion = datetime.now(),
        is_staff=True,

        mail = "canard@gmail.com",
        college = College.objects.all()[0]
    )

    user.set_password("canard")
    user.save()

def addCollege(user):
    print("add college")
    listeCollege = []
    for i in user:
        if not(i["college"] in listeCollege):
            listeCollege.append(i["college"])
    
    College.objects.bulk_create([College(nom=str(nom)) for nom in listeCollege])

def addUsers(user, part):
    print("add user")
    listeSocietaire = set([i["id_client"] for i in part])

    compteUser = 0
    for i in user:
        if not(i["id_client"] in listeSocietaire):
            continue
    
        if compteUser%100 == 0:
            print(f"{compteUser}/{len(user)} utilisateurs ajoutés")
        compteUser += 1

        utilisateur = Utilisateur(
            nom = i["nom"],
            prenom = i["prenom"],
            civilite = i["civilite"],
            adresse = i["adresse"],
            ville = i["ville"],
            pays = i["pays"],
            code_postal = i["code_postal"],
            telephone = i["telephone"],
            complement_adresse = i["complement_adresse"],
            mail = i["mail"],
            password = i["mot_de_passe"],
            college = College.objects.get(nom=str(i["college"]))
        )
        utilisateur.save()

        societaire = Societaire(
            organisation = i["organisation"],
            numero_societaire = i["id_client"], #todo a verifier si c'est bien ça
            id_utilisateur = utilisateur
        )
        societaire.save()

        listePart = []
        for j in part:
            if j["id_client"] != i["id_client"]:
                continue

            listePart.append(PartSocial(
                date_achat = datetime.strptime(j["date_achat"].replace("T"," ").split("+")[0], "%Y-%m-%d %H:%M:%S"),
                quantite = abs(j["quantite"]),
                num_facture = j["num_facture"],
                id_societaire = societaire,
                numero_achat = 0,
            ))

        listePart.sort(key=lambda c: c.date_achat)
        
        compteAchat = 0
        for j in listePart:
            j.numero_achat = compteAchat
            compteAchat += 1
            j.save()

def trouveCoordonneeUsers():
    users = Utilisateur.objects.all()
    compte = 0
    for user in users:
        compte += 1
        print(f"{compte}/{len(users)} localisation cherché")

        erreur = trouveCoordonnee(user)
        if erreur != "":
            with open("geolocatorLog.txt","a") as f:
                f.write(f"{erreur}")

            print(erreur)

        
@api_view(['POST'])
def importWeLogin(request):
    #return Response({"message": "Cette requete est desactivé pour eviter la supression de la BDD. Si vous souhaitez vraiment l'utiliser vous devez modifier le fichier importWeLogin.py et mettre la ligne envoyant ce message en commentaire"})

    debut = time()

    resetBDD()

    part = getPartSocial()
    if type(part) != list:
        return part

    user = getUsers()
    if type(user) != list:
        return user

    addCollege(user)
    addUsers(user, part)
    
    trouveCoordonneeUsers()
    
    addBaseUser()

    return Response({"message": "Importation reussie en {}s".format(round(time()-debut,3))})

def updateWeLogin(request):
    pass