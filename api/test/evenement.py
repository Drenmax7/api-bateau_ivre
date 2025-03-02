from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from urllib.parse import urlencode

from api.models import Evenement, Utilisateur

class EvenementTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Utilisateur.objects.create_user(mail="testuser", password="password")
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
