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


LIMITE_PART = 1000000
ID_PRODUIT_PART_SOCIAL = 11

with open("token.tok","r") as f:
    token = f.read()

headers = {
    "Authorization": f"Bearer {token}"
}

def resetBDD():
    Utilisateur.objects.all().delete()
    Connexion.objects.all().delete()
    College.objects.all().delete()

"""Recupere les LIMITE_PART premieres part social de welogin et renvoie une liste contenant les informations pertinante de ces parts
Il est possible de passer une date en parametre afin de ne recuperer que des part social ayant été acheté apres cette date 
"""
def getPartSocial(dateDebut="1970-01-01"):
    #limité a un maximum de 100 par l'api
    limite = 100

    part = []

    offset = 0  
    endReached = False
    while offset < LIMITE_PART:
        url = f"https://weapi1.welogin.fr/commandes?id_produit={ID_PRODUIT_PART_SOCIAL}&date_debut={dateDebut}&limit={limite}&offset={offset}"
        print(url)  
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
                    "quantite" : i["lignes"][0]["quantite_produit"],
                    "id_client_welogin" : i["id_client"]
                    } for i in part]

    return partFormate

"""Recupere l'entiereté de la base d'utilisateur de welogin et renvoie une liste contenant les informations pertinante de ces utilisateurs
"""
def getUsers(dateDebutModification = "1970-01-01"):    
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
    
    url = f"https://weapi1.welogin.fr/clients?date_debut_modification={dateDebutModification}"#&limit=3000&offset=0"  
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        user = response.json()["data"]
        print(f"{len(user)} utilisateurs recu")
    else:
        return Response({"message": "Échec de l'import des utilisateurs","status":response.status_code,"url":url,"reponse":response})
    
    userFormate = []
    for i in user:
        pays = pycountry.countries.get(alpha_3=i["code_pays"])
        if (pays != None):
            nomPays = pays.name
        else:
            nomPays = i["code_pays"]

        userFormate.append({
            "id_client" : i["id_client"],
            "nom" : i["nom"],
            "prenom" : i["prenom"],
            "mail" : i["email"],
            "mot_de_passe" : "mot de passe inconnu",
            "civilite" : civiliteFormat.get(i["id_civilite_client"],"n/a"),
            "adresse" : i["adresse"].replace(","," "),
            "ville" : i["ville"],
            "pays" : nomPays,
            "complement_adresse" : i["adresse_complementaire"],
            "code_postal" : i["code_postal"],
            "telephone" : i["telephone"],
            "college" : i["categorie_client"],
            "organisation" : i["structure"],
        })

    return userFormate

def updateUsers(users):
    compte = 0
    for user in users:
        utilisateur = Utilisateur.objects.filter(id_client_welogin = user["id_client"])
        if len(utilisateur) == 0:
            continue

        societaire = Societaire.objects.filter(id_utilisateur = utilisateur[0])
        if len(societaire) == 0:
            continue

        societaire.update(organisation=user["organisation"])
        
        compte += 1
        del user["id_client"]
        del user['mot_de_passe']
        del user["organisation"]
        del user["college"]
        
        try:
            utilisateur.update(**user)
        except:
            del user["mail"]
            utilisateur.update(**user)

    
    print(f"{compte} utilisateur mis a jour")

"""Ajoute un utilisateur lambda, qui a pour vocation d'etre supprimé, permettant de designer un vrai utilisateur comme admin
"""
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
        id_client_welogin = 999999999,

        mail = "canard@gmail.com",
        college = College.objects.all()[0]
    )

    user.set_password("canard")
    user.save()

"""Repere tous les colleges existant a partir de la liste d'utilisateur et les ajoute a la bdd
"""
def addCollege(user):
    print("add college")
    listeCollege = [i.nom for i in College.objects.all()]
    nouveauxCollege = []
    for i in user:
        if not(str(i["college"]) in listeCollege) and not(str(i["college"]) in nouveauxCollege):
            nouveauxCollege.append(str(i["college"]))
    
    College.objects.bulk_create([College(nom=str(nom)) for nom in nouveauxCollege])

"""Ajoute tous les utilisateurs qui ont acheté une ou plusieurs part social, et ajoute ces parts social dans la bdd
"""
def addUsers(user, part):
    print("add user")
    listeSocietaire = set([i["id_client"] for i in part])

    compteUser = 0
    for i in user:
        if not(i["id_client"] in listeSocietaire):
            continue
    
        if compteUser%100 == 0:
            print(f"{compteUser} utilisateurs ajoutés")
        compteUser += 1

        if len(i["mail"]) < 2:
            i["mail"] = f"pas de mail {compteUser}"
        else:
            duplicatMail = Utilisateur.objects.filter(mail__icontains=i["mail"])
            if len(duplicatMail) > 0:
                i["mail"] += f" erreur duplicat {len(duplicatMail)}"
                print(i["mail"])

        if len(Utilisateur.objects.filter(id_client_welogin=i["id_client"])) > 0:
            continue

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
            college = College.objects.get(nom=str(i["college"])),
            id_client_welogin = i["id_client"]
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
            compteAchat += 1
            j.numero_achat = compteAchat
            j.save()

"""Tente de trouver une localisation pour chacun des utilisateurs
Si skipLocalisation est a true, ne regarde que le cache contenu dans cacheGeolocator.txt
Si il y a une erreur lors de la recherche de l'adresse la fonction ajoute cette erreur au fichier log geolocatorLog.txt
"""
def trouveCoordonneeUsers(skipLocalisation):
    users = Utilisateur.objects.all()
    compte = 0
    for user in users:
        compte += 1
        print(f"{compte}/{len(users)} localisation cherché")

        erreur = trouveCoordonnee(user, skipLocalisation)
        if erreur != "":
            with open("geolocatorLog.txt","a") as f:
                f.write(f"{erreur}")

            print(erreur)

"""Detruit toutes les données de la BDD à l'exception des tables evenements et chaloupes
Importe ensuite les parts social acheté ainsi que les utilisateurs correspondant depuis welogin
Il est necessaire d'avoir mis le token welogin dans le fichier token.tok sans quoi la connexion ne pourra pas s'effectuer
Il est possible de passer le parametre skipLocalisation dans le header avec la valeur 1 afin de ne pas faire d'appel au service permettant de 
trouver les localisations des utilisateurs
"""
@api_view(['POST'])
def importWeLogin(request):

    #return Response({"message": "Cette requete est desactivé pour eviter la supression de la BDD. Si vous souhaitez vraiment l'utiliser vous devez modifier le fichier importWeLogin.py et mettre la ligne envoyant ce message en commentaire"})

    skipLocalisation = request.GET.get("skipLocalisation") == "1"


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
    
    trouveCoordonneeUsers(skipLocalisation)
    
    addBaseUser()

    with open("detailImport.txt","w") as f:
        now = datetime.now().strftime("%Y-%m-%d")
        f.write(now)

    return Response({"message": "Importation reussie en {}s".format(round(time()-debut,3))})

"""Enleve toutes les parts social qui serait deja presente dans la BDD
Cette verification s'effectue en fonction de l'id client et de la date d'achat
"""
def supprimeDoublon(part):
    nouveau = []

    for i in part:
        user = Utilisateur.objects.filter(id_client_welogin=i["id_client_welogin"])
        if len(user) == 0:
            nouveau.append(i)
            continue
        user = user[0]

        societaire = Societaire.objects.filter(id_utilisateur=user)
        if len(societaire) == 0:
            nouveau.append(i)
            continue
        societaire = societaire[0]

        partSocial = PartSocial.objects.filter(id_societaire=societaire, date_achat=datetime.strptime(i["date_achat"].replace("T"," ").split("+")[0], "%Y-%m-%d %H:%M:%S"))
        if len(partSocial) == 0:
            nouveau.append(i)

    return nouveau

"""Recupere toutes les informations ayant ete ajouté dans la bdd de welogin depuis la derniere maj ou import
Inclut les nouveaux utilisateurs, achat de part social et modification des données d'utilisateur
"""
@api_view(['POST'])
def updateWeLogin(request):
    skipLocalisation = request.GET.get("skipLocalisation") == "1"

    debut = time()

    with open("detailImport.txt","r") as f:
        dernierImport = f.read()

    #part social apres dernierImport
    part = getPartSocial(dernierImport)
    if type(part) != list:
        return part
    #eviter les doublons
    part = supprimeDoublon(part)

    #user apres dernierImport
    user = getUsers()
    if type(user) != list:
        return user
    
    #verif si nouveaux college et ajout si il y en a
    addCollege(user)
    #ajouter les users qui correspondent a des parts social
    addUsers(user, part)

    user = getUsers(dernierImport)
    if type(user) != list:
        return user
    #application des modifications des utilisateurs
    updateUsers(user)
    
    #calul coordonnés des nouveaux users
    trouveCoordonneeUsers(skipLocalisation)

    with open("detailImport.txt","w") as f:
        now = datetime.now().strftime("%Y-%m-%d")
        f.write(now)


    return Response({"message": "Importation reussie en {}s".format(round(time()-debut,3))})
