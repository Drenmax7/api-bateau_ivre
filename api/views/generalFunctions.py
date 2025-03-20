from rest_framework.response import Response
from django.core import exceptions
from rest_framework import status

from geopy.geocoders import Nominatim
import time

"""Cette fonction est appelé par les views recuperant des données dans les tables
"""
def filtreTable(request):
    colonne = request.GET.getlist('colonne',[])
    filtre = request.GET.getlist('filtre',[])
    mode = request.GET.getlist("mode",[])

    if "password" in colonne:
        raise ValueError("Cannot filter by password for security reason")

    taille = min(len(colonne),len(filtre))

    colonne = colonne[:taille]
    filtre = filtre[:taille]
    while len(mode) < taille:
        mode.append(">=")


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
    
    return filtre_dict

"""Cette fonction est appelé par les view mettant a jour les tables
"""
def updateTable(request):
    colonne = request.data.get('colonne',[])
    valeur = request.data.get('valeur',[])

    if "password" in colonne:
        raise ValueError("Veuillez utiliser la requete specifique au changement de mot de passe pour le changer")

    taille = min(len(colonne),len(valeur))

    colonne = colonne[:taille]
    valeur = valeur[:taille]

    filtre_dict = {}
    for i in range(len(colonne)):
        col = colonne[i]        
        filtre_dict[col] = valeur[i]
    
    return filtre_dict

geolocator = Nominatim(user_agent="geo_duck")
with open("cacheGeolocator.txt","r", encoding="utf-8") as f:
    cache = eval(f.read())

"""Apelle un service externe afin de trouver les coordonnées gps de l'utilisateur
Attribue automatiquement les coordonnées à l'utilisateur
Les coordonnées peuvent etre calculé de plusieurs facons differentes
La fonction essaie d'abord de les trouver grace à l'adresse, la ville et le pays de l'utilisateur
Si le service ne trouve pas ou qu'une de ces infos n'est pas renseigné alors on essaie avec seulement la ville et le pays
Si le service ne trouve pas ou qu'une de ces infos n'est pas renseigné alors on essaie avec le code postal et le pays
Si le service ne trouve toujours pas ou qu'une de ces infos n'est pas renseigné alors la fonction abandonne et aucune coordonnées n'est attribué
Le service auquel fait appel la fonction est gratuite mais tres limité
Pour eviter d'y faire trop d'appel toutes les coordonnées sont mis en cache dans un fichier cacheGeolocator.txt
Si la fonction trouve une correspondance dans le cache alors elle prendra les coordonnées associé sans rien essayer d'autre, meme si les coordonnées sont erroné
Ce fichier peut potentiellement devenir volumineux mais sa supression entrainera de nouveaux des appels à l'api, qui prennent 2s par appel
Cette fonction comprend des time.sleep(2) et sont necessaire afin que le service externe ne rejette pas les requetes qui serait envoyé trop rapidement
"""
def trouveCoordonnee(user, skipLocalisation=False):
    erreur = ""

    location = None
    if location == None and user.ville and user.pays and user.adresse:
        cacheAdresse = cache["adresse"].get(f"{user.adresse.lower()}-{user.ville.lower()}-{user.pays.lower()}",None)
        if cacheAdresse != None:
            user.latitude = cacheAdresse[0]
            user.longitude = cacheAdresse[1]
            user.save()
            return erreur
        else:
            try:
                if skipLocalisation:
                    location = None
                else:
                    location = geolocator.geocode(f"{user.adresse}, {user.ville}, {user.pays}")
                    time.sleep(2)

                if location != None:
                    cache["adresse"][f"{user.adresse.lower()}-{user.ville.lower()}-{user.pays.lower()}"] = (location.latitude,location.longitude)
                    with open("cacheGeolocator.txt","w", encoding="utf-8") as f:
                        f.write(str(cache))

                elif not(skipLocalisation):
                    erreur += f"adresse non trouvé : {user.adresse}, {user.ville}, {user.pays}\n"
            except:
                erreur += f"recherche api echoué : {user.adresse}, {user.ville}, {user.pays}\n"

    if location == None and user.ville and user.pays:
        cacheVille = cache["ville"].get(f"{user.ville.lower()}-{user.pays.lower()}",None)
        if cacheVille != None:
            user.latitude = cacheVille[0]
            user.longitude = cacheVille[1]
            user.save()
            return erreur
        else:
            try:
                if skipLocalisation:
                    location = None
                else:
                    location = geolocator.geocode(f"{user.ville}, {user.pays}")
                    time.sleep(2)
                
                if location != None:
                    cache["ville"][f"{user.ville.lower()}-{user.pays.lower()}"] = (location.latitude,location.longitude)
                    with open("cacheGeolocator.txt","w", encoding="utf-8") as f:
                        f.write(str(cache))
                
                elif not(skipLocalisation):
                    erreur += f"ville non trouvé : {user.ville}, {user.pays}\n"
            except:
                erreur += f"recherche api echoué : {user.ville}, {user.pays}\n"

    if location == None and user.code_postal and user.pays:
        cachePostal = cache["postal"].get(f"{user.code_postal}-{user.pays.lower()}",None)
        if cachePostal != None:
            user.latitude = cachePostal[0]
            user.longitude = cachePostal[1]
            user.save()
            return erreur
        else:
            try:
                if skipLocalisation:
                    location = None
                else:
                    location = geolocator.geocode(f"{user.code_postal}, {user.pays}")
                    time.sleep(2)

                if location != None:
                    cache["postal"][f"{user.code_postal}-{user.pays.lower()}"] = (location.latitude,location.longitude)
                    with open("cacheGeolocator.txt","w", encoding="utf-8") as f:
                        f.write(str(cache))
                
                elif not(skipLocalisation):
                    erreur += f"code postal non trouvé : {user.code_postal}, {user.pays}\n"
            
            except:
                erreur += f"recherche echoué : {user.code_postal}, {user.pays}\n"
    
    if location != None:
        user.latitude = location.latitude
        user.longitude = location.longitude
        user.save()
    
    return erreur