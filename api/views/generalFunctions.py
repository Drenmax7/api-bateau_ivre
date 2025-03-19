from rest_framework.response import Response
from django.core import exceptions
from rest_framework import status

from geopy.geocoders import Nominatim
import time


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