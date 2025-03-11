from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from urllib.parse import urlencode

from api.models import Evenement, Utilisateur, Reserve, College

class EvenementTest_correctUse(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.college = College.objects.create(nom="Citoyen")
        self.user = Utilisateur.objects.create_user(mail="testuser", password="password", college=self.college)
        self.user.is_staff = True
        self.client.force_authenticate(user=self.user)

        self.data = {
            "place_disponible": 50,
            "date_evenement": "2025-06-15 14:00:00",
            "titre": "Concert de Rock",
            "description": "Un super concert en plein air !"
        }

    def test_add_evenement(self):
        url = "/api/evenement/addEvenement/"
        response = self.client.post(url, self.data, format="json")

        # requête traitée correctement
        self.assertEqual(response.status_code, 201)

        id_evenement = response.json()["id_evenement"]
        query = Evenement.objects.filter(id_evenement=id_evenement)

        # vérifie l'existence de l'événement
        self.assertEqual(len(query), 1)

        evenement = query[0]
        # vérifie que les valeurs sont les bonnes
        self.assertEqual(evenement.titre, self.data["titre"])
        self.assertEqual(evenement.description, self.data["description"])

    def test_delete_evenement(self):
        # crée un événement
        url = "/api/evenement/addEvenement/"
        response = self.client.post(url, self.data, format="json")
        id_evenement = response.json()["id_evenement"]

        url = "/api/evenement/deleteEvenement/"
        response = self.client.delete(url, {"id_evenement": id_evenement}, format="json")

        # requête traitée correctement
        self.assertEqual(response.status_code, 200)

        query = Evenement.objects.filter(id_evenement=id_evenement)
        # vérifie la suppression de l'événement
        self.assertEqual(len(query), 0)

    def test_update_evenement(self):
        # crée un événement
        url = "/api/evenement/addEvenement/"
        response = self.client.post(url, self.data, format="json")
        id_evenement = response.json()["id_evenement"]

        url = "/api/evenement/updateEvenement/"
        newData = {
            "id_evenement": id_evenement, 
            "colonne": ["titre", "description"], 
            "valeur": ["Nouveau titre", "Nouvelle description"]
        }
        response = self.client.put(url, newData, format="json")

        # requête traitée correctement
        self.assertEqual(response.status_code, 200)

        query = Evenement.objects.filter(id_evenement=id_evenement)
        evenement = query[0]
        # vérifie la modification de l'événement
        for i in range(len(newData["colonne"])):
            colonne = newData["colonne"][i]
            valeur = newData["valeur"][i]
            self.assertEqual(getattr(evenement, colonne), valeur)

    def test_get_evenement(self):
        # crée un événement
        url = "/api/evenement/addEvenement/"
        response = self.client.post(url, self.data, format="json")
        id_evenement = response.json()["id_evenement"]

        for i in range(5):
            self.client.post(url, {
                "place_disponible": 100,
                "date_evenement": "2025-06-20 18:00:00",
                "titre": f"Événement {i}",
                "description": "Description test"
            }, format="json")

        param = {"colonne": ["titre"], "filtre": ["Concert de Rock"], "mode": ["=="]}
        query_string = urlencode(param, doseq=True)
        url = f"/api/evenement/getEvenement/?{query_string}"
        response = self.client.get(url, format="json")

        # requête traitée correctement
        self.assertEqual(response.status_code, 200)

        # vérifie qu'une ligne est récupérée
        data = response.json()
        self.assertEqual(len(data), 1)

        # vérifie que la ligne récupérée est bien celle qui est cherchée
        id_recup = data[0]["id_evenement"]
        self.assertEqual(id_recup, id_evenement)


class ReserveTest_correctUse(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.college = College.objects.create(nom="Citoyen")
        self.user = Utilisateur.objects.create_user(mail="testuser", password="password", college=self.college)
        self.user.is_staff = True
        self.client.force_authenticate(user=self.user)

        self.utilisateur = Utilisateur.objects.create(
            mail="partsocial@test.com",
            nom="Doe",
            prenom="John",
            telephone="0123456789",
            college=self.college
        )

        self.evenement = Evenement.objects.create(
            place_disponible = 50,
            date_evenement = "2025-06-15 14:00:00",
            titre = "Concert de Rock",
            description = "Un super concert en plein air !"
        )
        
        self.data = {"nb_place": 3, "id_utilisateur":self.utilisateur.id_utilisateur,"id_evenement":self.evenement.id_evenement}


    def test_add(self):
        url = "/api/evenement/addReservation/"
        response = self.client.post(url, self.data, format="json")

        #requete traité correctement
        self.assertEqual(response.status_code, 201) 

        query = Reserve.objects.filter(id_utilisateur=self.data["id_utilisateur"], id_evenement=self.data["id_evenement"])
        
        #verifie l'existence de la reservation
        self.assertEqual(len(query), 1)

        entree = query[0]
        #verifie que les valeurs sont les bonnes
        self.assertEqual(entree.nb_place, self.data["nb_place"])

    def test_delete(self):
        #cree une chaloupe
        url = "/api/evenement/addReservation/"
        response = self.client.post(url, self.data, format="json")

        url = "/api/evenement/deleteReservation/"
        response = self.client.delete(url, {"id_utilisateur":self.data["id_utilisateur"], "id_evenement":self.data["id_evenement"]}, format="json")

        #requete traité correctement
        self.assertEqual(response.status_code, 200)

        query = Reserve.objects.filter(id_utilisateur=self.data["id_utilisateur"], id_evenement=self.data["id_evenement"])
        #verifie la supression de la reservation
        self.assertEqual(len(query), 0)

    def test_update(self):
        url = "/api/evenement/addReservation/"
        response = self.client.post(url, self.data, format="json")

        url = "/api/evenement/updateReservation/"
        newData = {"id_utilisateur":self.data["id_utilisateur"], "id_evenement":self.data["id_evenement"], "colonne": ["nb_place"], "valeur" : [10]}
        response = self.client.put(url, newData, format="json")

        #requete traité correctement
        self.assertEqual(response.status_code, 200)

        query = Reserve.objects.filter(id_utilisateur=self.data["id_utilisateur"], id_evenement=self.data["id_evenement"])
        entree = query[0]
        #verifie la modification de la chaloupe
        self.assertEqual(entree.nb_place, newData["valeur"][0])

    def test_get(self):
        #cree une chaloupe
        url = "/api/evenement/addReservation/"
        response = self.client.post(url, self.data, format="json")

        param = {"colonne": ["id_utilisateur", "id_evenement"], "filtre" : [self.data["id_utilisateur"], self.data["id_evenement"]], "mode":["==", "=="]}
        query_string = urlencode(param, doseq=True)
        url = f"/api/evenement/getReservation/?{query_string}"
        response = self.client.get(url, format="json")
        
        #requete traité correctement
        self.assertEqual(response.status_code, 200)
        
        #verifie qu'une ligne est récupéré
        data = response.json()
        self.assertEqual(len(data), 1)

        #verifie que la ligne récupéré est bien celle qui est cherché
        self.assertEqual(data[0]["id_utilisateur"], self.data["id_utilisateur"])
        self.assertEqual(data[0]["id_evenement"], self.data["id_evenement"])
        self.assertEqual(data[0]["nb_place"], self.data["nb_place"])

