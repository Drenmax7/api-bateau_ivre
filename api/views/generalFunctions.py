from rest_framework.response import Response
from django.core import exceptions
from rest_framework import status

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
