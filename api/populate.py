from rest_framework.decorators import action, permission_classes
from rest_framework import viewsets
from rest_framework.response import Response

from api.models import *
from api.serializers import *

from django.http import JsonResponse

from random import normalvariate, randint, choice, getrandbits, expovariate, shuffle
import datetime
from time import time

def populate(request):
    debut = time()
    
    popUtilisateur()
    popSocietaire()

    popEvenement()
    popReservation()

    popChaloupe()
    popRejoint()

    popPartSocial()

    popConnexion()
    
    return JsonResponse({"message": "Importation reussie en {}s".format(round(time()-debut,3))})

def popUtilisateur():
    print('utilisateur')
    # Liste de 50 noms
    noms = [
        "Dupont", "Durand", "Lemoine", "Lemoine", "Lefevre", "Benoit", "Robert", "Martin", "Bernard", "Guerin",
        "Michaud", "Gauthier", "Chauvin", "Lemoine", "Caron", "Leblanc", "Germain", "Lemoine", "Hebert", "Donald",
        "Leclerc", "Bouvier", "Bouchet", "Lemoine", "Dumont", "Paquet", "Gosse", "Garin", "Marchand", "Caron",
        "Vivier", "Beaupré", "Morin", "Vasseur", "Baron", "Lemoine", "Lemaitre", "Nicolas", "Desjardins", "Blanchet",
        "Bertrand", "Desmarais", "Sauvage", "Roche", "Caron", "Lambert", "Tremblay", "Lemoine", "Gosselin", "Vallee"
    ]

    # Liste de 50 prénoms
    prenoms = [
        "Pierre", "Marie", "Jean", "Luc", "Sophie", "Michel", "Martine", "Alice", "François", "Anne",
        "Claire", "Paul", "Sébastien", "Camille", "Thierry", "Jacques", "Emilie", "Jacinthe", "Pauline", "Lucie",
        "David", "Pierre-Alexandre", "Julie", "Isabelle", "Charlotte", "Aurélie", "Dominique", "Bernadette", "Henri",
        "Aline", "Régis", "Valérie", "Frédéric", "Duck", "Caroline", "Sébastien", "Fabrice", "Léa", "Chloé",
        "Catherine", "Nicolas", "Delphine", "Patricia", "Sylvie", "Jean-Luc", "Franck", "Nathalie", "Mélanie", "Victor"
    ]

    # Liste de 20 formes de rue
    formes_de_rue = [
        "Allée", "Rue", "Avenue", "Boulevard", "Place", "Quai", "Impasse", "Chemin", "Route", "Esplanade",
        "Passage", "Cours", "Boulevard", "Promenade", "Mare", "Cité", "Hameau", "Voie", "Pont", "Périphérique"
    ]

    # Liste de 50 noms de rue
    noms_de_rue = [
        "Saint-Denis", "Victor Hugo", "République", "Montmartre", "Général de Gaulle", "Porte de Clignancourt", "Montaigne", "Voltaire", "Bastille", "Gambetta",
        "Gare de Lyon", "Clemenceau", "Foch", "Saint-Germain", "Austerlitz", "Le Marais", "Champs-Élysées", "De la Paix", "Jaurès", "Jean-Jaurès",
        "Belleville", "Gare Saint-Lazare", "Sébastopol", "Raspail", "Louvre", "Notre-Dame", "Concorde", "Parmentier", "Moulin Rouge",
        "Rue de la Paix", "Saint-Michel", "Château d'Eau", "Bastille", "Raspail", "des Canards", "des Martyrs", "Pasteur", "Baille", "Bourgogne", "Montparnasse",
        "Cochin", "Jules Ferry", "Voltaire", "Pelleport", "Marceau", "Opéra", "Saint-Antoine", "Orléans", "Vaugirard"
    ]

    # Liste de 10 pays
    liste_pays = [
        "Allemagne", "Italie", "Espagne", "Belgique", "Suisse", "Portugal", "Pays-Bas", "Canada", "Luxembourg"
    ]

    # Liste de 50 compléments d'adresse
    complements_d_adresse = [
        "Appartement 1", "Bâtiment A", "Lot 7", "Escalier 2", "Étage 3", "Boîte Postale", "Suite 11", "Appartement 4", "Résidence 2", "Tour B",
        "Bloc C", "Entrée principale", "N°2", "N°10", "Rez-de-chaussée", "Cave", "Garage", "Rez-de-jardin", "Sous-sol", "Box", 
        "Appartement 3", "Étages 2-5", "Immeuble A", "Tour 1", "Bloc E", "Entrée Sud", "Voie 5", "Quartier Nord", "N°9", "Appartement 8", 
        "Étages 1 à 4", "Boîte 25", "Secteur 2", "Immeuble E", "Lotissement 3", "N°6", "Villa 2", "Résidence des Lilas", "Chemin des Pins", 
        "Appart 18", "Quartier Central", "Bâtiment L", "Cottage 4", "Boulevard Est", "Lotissement 5", "Immeuble D", "Studio 7", "Château 3"
    ]

    # Dictionnaire associant 20 villes à leurs codes postaux
    villes_codes_postaux = {
        "Paris": "75000", "Marseille": "13000", "Lyon": "69000", "Toulouse": "31000", "Nice": "06000", 
        "Nantes": "44000", "Strasbourg": "67000", "Montpellier": "34000", "Bordeaux": "33000", "Lille": "59000", 
        "Rennes": "35000", "Reims": "51100", "Le Havre": "76600", "Saint-Étienne": "42000", "Toulon": "83000", 
        "Angers": "49000", "Dijon": "21000", "Brest": "29200", "Le Mans": "72000", "Aix-en-Provence": "13090"
    }

    Utilisateur.objects.all().delete()
    listeMail = []

    for batch in range(100):
        listeEntree = []
        for i in range(100):
            nom = choice(noms)
            prenom = choice(prenoms)
            
            premiereFois = True
            mail = ""
            while (mail in listeMail or premiereFois):
                premiereFois = False
                mail = f"{nom}{choice(["","."])}{prenom}{randint(0,20)}@{choice(["gmail","orange","outlook","canard"])}.com"
            listeMail.append(mail)

            mdp = getrandbits(128)
            civilite = choice(["M","Mme","Non binaire","N/a","Oiseau"])
            adresse = f"{randint(1,999)} {choice(formes_de_rue)} {choice(noms_de_rue)}"
            ville = choice(list(villes_codes_postaux))
            pays = "France"
            if (randint(0,9) == 0):
                pays = choice(liste_pays)
            codePostal = villes_codes_postaux[ville]
            tel = f"0{choice([6,7])}" + str(randint(0,10**8-1)).zfill(8)
            comp = choice(complements_d_adresse)

            premiere = None
            #chance qu'un utilisateur se soit un jour connecté
            if (randint(0,9) >= 2):
                premiere = datetime.datetime.now().replace(hour=randint(0,23), minute=randint(0,59),second=randint(0,59),microsecond=randint(0,999999)) - datetime.timedelta(days=expovariate(1/1000))
            
            derniere = premiere
            #chance qu'un utilisateur se soit connecté plusieurs fois
            if premiere != None and randint(0,9) >= 3:
                ecart = (datetime.datetime.now() - premiere).days
                if ecart >= 2:
                    derniere = premiere.replace(hour=randint(0,23), minute=randint(0,59),second=randint(0,59),microsecond=randint(0,999999)) + datetime.timedelta(days=randint(1,ecart-1))
            
            listeEntree.append(Utilisateur(
                nom = nom,
                prenom = prenom,
                mail = mail,
                mot_de_passe = mdp,
                civilite = civilite,
                adresse = adresse,
                ville = ville,
                pays = pays,
                code_postal = codePostal,
                telephone = tel,
                complement_adresse = comp,
                premiere_connexion = premiere,
                derniere_connexion = derniere
            ))

        Utilisateur.objects.bulk_create(listeEntree)

def popSocietaire():
    print("societaire")
    Societaire.objects.all().delete()

    organisations = [
        "CanardTech", "PlumesInnovantes", "DuckSolutions", "AilesDigitale", "PlumerieModerne",
        "DucksCorp", "TechnoPlume", "CanardIndustries", "Ailes&Co", "WebDuck",
        "Plumetronix", "DuckLabs", "SplashInnovations", "CyberPlume", "AilésCréatifs",
        "CanardConception", "DigiCanard", "QuackSystems", "PlumeTech", "AilesNetworking",
        "Duckify", "QuackLabs", "BecDigital", "PlumeFutur", "TechDuckers",
        "AilesSolutions", "DuckEmpire", "PlumerieMobile", "TechnoCanard", "DuckWorks",
        "PlumeConnect", "DigitalFeather", "SplashTech", "CanardFusion"
    ]

    listeEntrees = []

    users = list(Utilisateur.objects.all())
    for user in users:
        if (randint(1,20) != 20):
            continue
        
        choixOrga = "N/a"
        if randint(1,10) == 10:
            choixOrga = choice(organisations)

        listeEntrees.append(Societaire(
            produit = "Je ne sais pas ce que c'est",
            organisation = choixOrga,
            id_utilisateur = user
        ))


    Societaire.objects.bulk_create(listeEntrees)

def popEvenement():
    print("evenement")
    Evenement.objects.all().delete()

    nomDescription = {
        "Le Ballet des Plumes": "Un spectacle de danse synchronisée sur l'eau, où les canards réalisent des figures élégantes.",
        "CoinCoin Symphonie": "Un concert où les canards sifflent et coincoinent en harmonie avec un orchestre aquatique.",
        "Plumes en Feu": "Un show pyrotechnique où les flammes se reflètent sur l'eau, mettant en scène des canards acrobates.",
        "La Parade des Marais": "Un défilé majestueux de canards costumés, accompagné de musique festive.",
        "Les Ailes du Vent": "Un spectacle de voltige où les canards réalisent des loopings et figures aériennes impressionnantes.",
        "Mare Mystique": "Une pièce de théâtre racontant la légende d'un canard légendaire aux pouvoirs magiques.",
        "Sifflets et Mélodies": "Un concours de chant mettant en avant les plus belles voix des canards du marais.",
        "Danse des Nénuphars": "Une chorégraphie aquatique synchronisée avec des lumières colorées et des effets d'eau.",
        "Canard Magicien": "Un spectacle de magie où un canard illusionniste fait disparaître et réapparaître des objets sous l'eau.",
        "Le Carnaval des Plumes": "Une fête haute en couleur avec des costumes extravagants et des danses folkloriques.",
        "Opéra CoinCoin": "Un opéra majestueux où les canards interprètent des grands classiques avec des variations coin-coin.",
        "Marais en Lumière": "Un spectacle nocturne combinant jeux de lumières, musique et reflets sur l'eau.",
        "La Légende du Grand Lac": "Une fresque théâtrale racontant l'histoire des ancêtres des canards et leurs aventures.",
        "Cirque des Ondes": "Un cirque aquatique avec des acrobaties sur l'eau et des plongeons spectaculaires.",
        "L'Épopée des Ailes": "Un conte épique mettant en scène des héros canards affrontant les dangers de la migration.",
        "Canard Broadway": "Un spectacle musical inspiré des plus grands classiques de Broadway, version canard.",
        "Plume en Fusion": "Un spectacle de danse et de musique électronique pour une ambiance festive.",
        "Le Lac aux Canards": "Une réinterprétation du célèbre ballet Le Lac des Cygnes, mais avec des canards.",
        "Comédie du Marais": "Un spectacle humoristique basé sur la vie quotidienne des canards et leurs mésaventures.",
        "Plumes d'Or": "Un concours de talents où les canards montrent leurs meilleures performances artistiques.",
        "Le Secret du Marais": "Un spectacle de suspense où un détective canard mène une enquête palpitante.",
        "Fête des Ondes": "Un festival en plein air avec des performances musicales et des danses aquatiques.",
        "La Symphonie des Roseaux": "Un concert de musique classique joué avec des instruments fabriqués à partir de roseaux.",
        "Le Grand Cabaret CoinCoin": "Un cabaret mettant en scène des numéros de chant, de danse et de jonglage.",
        "Le Rire du Marais": "Un one-duck-show avec des sketches humoristiques et des imitations d'autres animaux.",
        "Murmures du Lac": "Une performance poétique avec des récits, des chants et des lumières projetées sur l'eau.",
        "AcroPlume": "Un spectacle d'acrobaties aériennes où les canards enchaînent figures et pirouettes.",
        "Le Magicien des Plumes": "Un show d'illusionnisme où un canard mystérieux défie la réalité.",
        "Les Fantômes du Marais": "Une pièce de théâtre fantastique où des esprits de canards racontent leurs histoires.",
        "Opéra des Ailes": "Un grand opéra en plein air où les canards chantent et racontent leur voyage migratoire."
    }
    nomDescriptionListe = [[key,nomDescription[key]] for key in nomDescription]

    listeEntrees = [
        Evenement(titre=nomDescriptionListe[i%len(nomDescriptionListe)][0], 
                 description=nomDescriptionListe[i%len(nomDescriptionListe)][1],
                 place_disponible = normalvariate(200,50),
                 date_evenement = datetime.datetime.now().replace(hour=randint(18,21), minute=30*randint(0,1), second=0, microsecond=0) - datetime.timedelta(days=round(i/5*7))

        ) for i in range(250)        
    ]

    Evenement.objects.bulk_create(listeEntrees)

def popReservation():
    print("reservation")
    Reserve.objects.all().delete()

    users = list(Utilisateur.objects.all())
    events = list(Evenement.objects.all())

    for event in events:
        listeEntrees = []

        ajoutPlace = randint(1,3)
        totalPlace = ajoutPlace + expovariate(1/100) #enleve des places, qui seront donc vide
        dejaFait = []
        while totalPlace <= event.place_disponible:
            premiereFois = True
            while (premiereFois or randomUser.id_utilisateur in dejaFait):
                premiereFois = False
                randomUser = choice(users)
            dejaFait.append(randomUser.id_utilisateur)

            listeEntrees.append(Reserve(
                id_utilisateur = randomUser,
                id_evenement = event,
                nb_place = ajoutPlace
            ))

            ajoutPlace = randint(1,3)
            totalPlace += ajoutPlace
        
        Reserve.objects.bulk_create(listeEntrees)
            
def popChaloupe():
    print("chaloupe")
    Chaloupe.objects.all().delete()

    nomDescription = {
        "CanardExplorateur": "Regroupe les canards aventuriers explorant marais et rivières à la recherche de nouvelles terres.",
        "Plum'Art": "Communauté d'artistes canards spécialisés en peinture aquatique et sculptures en roseaux.",
        "CoinCoinTech": "Start-up innovante développant des gadgets pour améliorer la vie des canards connectés.",
        "AquaPlouf": "Club de plongeon synchronisé pour canards adeptes des sauts artistiques.",
        "FlotteursGourmets": "Réseau de restaurants flottants spécialisés en algues gastronomiques et insectes bio.",
        "DuckEnergy": "Recherche et développement sur les énergies renouvelables adaptées aux habitats aquatiques.",
        "MaraisZen": "Centre de bien-être et méditation pour canards stressés par la migration.",
        "CanardExpress": "Service de messagerie ultra-rapide assuré par les meilleurs nageurs de la mare.",
        "Plume&Plongeon": "Académie de natation pour jeunes canetons souhaitant améliorer leur technique.",
        "CoinBusiness": "Incubateur de start-ups aquatiques spécialisées dans les solutions pour volatiles.",
        "DuckFashion": "Haute couture pour canards avec des accessoires élégants comme chapeaux et nœuds-papillons.",
        "CanardRieur": "Troupe de théâtre et de spectacles humoristiques pour divertir les canards du marais.",
        "Ailes&Vent": "Club de vol synchronisé pour les migrations en formation optimisée.",
        "CoinNews": "Agence de presse diffusant les actualités importantes du marais et des alentours.",
        "PondSecurity": "Brigade de sécurité pour surveiller les prédateurs et assurer la tranquillité des nids.",
        "BioCanard": "Filière spécialisée en agriculture bio pour produire des graines et algues de qualité.",
        "DuckCinema": "Industrie du cinéma produisant des films et documentaires sur la vie aquatique.",
        "MareConnect": "Réseau social dédié aux canards pour partager photos, conseils et itinéraires de migration.",
        "CoinFestival": "Organisation d'événements festifs comme la Fête de la Grenouille et la Parade des Plumes.",
        "DuckTrek": "Tour-opérateur proposant des circuits migratoires sécurisés et optimisés.",
        "CanardEcolo": "Collectif engagé dans la préservation des milieux humides et la protection des habitats.",
        "PaddleMasters": "Groupe de compétition de nage et courses en eau libre.",
        "PlumeRadio": "Station de radio locale animée par des canards pour des infos et musiques aquatiques.",
        "BecGourmand": "Confrérie des fins gastronomes spécialisés en dégustation d'insectes rares.",
        "NestDesign": "Architectes spécialisés en conception et aménagement de nids modernes et écologiques.",
        "CoinGames": "Compétitions sportives entre canards incluant nage, plongeon et course sur l'eau.",
        "DuckInvest": "Fonds d'investissement pour projets innovants dans le monde aquatique.",
        "OndulationRecords": "Label musical promouvant les talents de sifflements et coin-coin mélodieux.",
        "CanardSciences": "Centre de recherche sur l'aérodynamisme et les comportements migratoires.",
        "MarePharm": "Pharmacie spécialisée en soins et remèdes naturels pour canards et volatiles."
    }

    listeEntrees = [
        Chaloupe(nom=key, description=nomDescription[key]) for key in nomDescription
    ]

    Chaloupe.objects.bulk_create(listeEntrees)
            
def popRejoint():
    print("rejoint")
    Rejoint.objects.all().delete()

    listeEntrees = []

    chaloupes = list(Chaloupe.objects.all())
    users = list(Societaire.objects.all())

    for chaloupe in chaloupes:
        nbPersonne = int(max(1,normalvariate(20,5)))

        present = []
        for i in range(nbPersonne):
            premiereFois = True
            while (premiereFois or user.id_utilisateur in present):
                premiereFois = False
                user = choice(users)
            
            present.append(user.id_utilisateur)

            listeEntrees.append(Rejoint(
                id_societaire = user,
                id_chaloupe = chaloupe,
                dirige = i==0,
            ))



    Rejoint.objects.bulk_create(listeEntrees)

def popPartSocial():
    print("part social")
    PartSocial.objects.all().delete()

    users = list(Societaire.objects.all())

    listeEntrees = []
    for user in users:
        listeEntrees.append(PartSocial(
            date_achat = datetime.datetime.now().replace(hour=randint(0,23), minute=randint(0,59),second=randint(0,59),microsecond=randint(0,999999)) - datetime.timedelta(days=1+expovariate(1/1000)),
            quantite = expovariate(1/3) +1 ,
            num_facture = "FAC-{}-SOC".format(format(randint(0, 16**6-1), 'x')),
            id_societaire = user,
        ))


    PartSocial.objects.bulk_create(listeEntrees)

def popConnexion():
    print("connexion")
    Connexion.objects.all().delete()
    HistoriqueConnexion.objects.all().delete()

    users = list(Societaire.objects.all())
    currentDate = datetime.datetime.now()
    for i in range(1000):
        jour = Connexion(jour = currentDate - datetime.timedelta(days=i))
        jour.save()

        nbPersonne = round(expovariate(5/(1000-i)))

        shuffle(users)
        subSet = users[:nbPersonne]

        listeEntrees = []
        for user in subSet:
            listeEntrees.append(HistoriqueConnexion(
                id_societaire = user,
                jour = jour
            ))
        HistoriqueConnexion.objects.bulk_create(listeEntrees)


