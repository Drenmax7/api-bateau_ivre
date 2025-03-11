from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from urllib.parse import urlencode
from api.models import PartSocial, Societaire, Utilisateur, College
from datetime import datetime

class PartSocialTest_correctUse(APITestCase):
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

        self.college = College.objects.create(nom="College Test")

        self.societaire = Societaire.objects.create(
            organisation="Organisation Test",
            numero_societaire="12345",
            id_utilisateur=self.utilisateur
        )

        self.data = {
            "date_achat": datetime.now().isoformat(),
            "quantite": 10,
            "num_facture": "FACT123",
            "id_societaire": self.societaire.id_societaire
        }

    def test_add_part_social(self):
        url = "/api/partSocial/addPartSocial/"
        response = self.client.post(url, self.data, format="json")

        # requête traitée correctement
        self.assertEqual(response.status_code, 201)

        id_achat = response.json()["id_achat"]
        query = PartSocial.objects.filter(id_achat=id_achat)

        # vérifie l'existence de la part sociale
        self.assertEqual(len(query), 1)

        part_social = query[0]
        # vérifie que les valeurs sont les bonnes
        self.assertEqual(part_social.quantite, self.data["quantite"])
        self.assertEqual(part_social.numero_achat, 1)
        self.assertEqual(part_social.num_facture, self.data["num_facture"])

    def test_delete_part_social(self):
        # crée une part sociale
        url = "/api/partSocial/addPartSocial/"
        response = self.client.post(url, self.data, format="json")
        id_achat = response.json()["id_achat"]

        url = "/api/partSocial/deletePartSocial/"
        response = self.client.delete(url, {"id_achat": id_achat}, format="json")

        # requête traitée correctement
        self.assertEqual(response.status_code, 200)

        query = PartSocial.objects.filter(id_achat=id_achat)
        # vérifie la suppression de la part sociale
        self.assertEqual(len(query), 0)

    def test_update_part_social(self):
        # crée une part sociale
        url = "/api/partSocial/addPartSocial/"
        response = self.client.post(url, self.data, format="json")
        id_achat = response.json()["id_achat"]

        url = "/api/partSocial/updatePartSocial/"
        newData = {
            "id_achat": id_achat, 
            "colonne": ["quantite", "num_facture"], 
            "valeur": [20, "FACT999"]
        }
        response = self.client.put(url, newData, format="json")

        # requête traitée correctement
        self.assertEqual(response.status_code, 200)

        query = PartSocial.objects.filter(id_achat=id_achat)
        part_social = query[0]
        # vérifie la modification de la part sociale
        for i in range(len(newData["colonne"])):
            colonne = newData["colonne"][i]
            valeur = newData["valeur"][i]
            self.assertEqual(getattr(part_social, colonne), valeur)

    def test_get_part_social(self):
        # crée une part sociale
        url = "/api/partSocial/addPartSocial/"
        response = self.client.post(url, self.data, format="json")
        id_achat = response.json()["id_achat"]

        for i in range(5):
            self.client.post(url, {
                "date_achat": datetime.now().isoformat(),
                "quantite": i + 5,
                "numero_achat": i + 1,
                "num_facture": f"FACT{i}",
                "id_societaire": self.societaire.id_societaire
            }, format="json")

        param = {"colonne": ["num_facture"], "filtre": ["FACT123"], "mode": ["=="]}
        query_string = urlencode(param, doseq=True)
        url = f"/api/partSocial/getPartSocial/?{query_string}"
        response = self.client.get(url, format="json")

        # requête traitée correctement
        self.assertEqual(response.status_code, 200)

        # vérifie qu'une ligne est récupérée
        data = response.json()
        self.assertEqual(len(data), 1)

        # vérifie que la ligne récupérée est bien celle qui est cherchée
        id_recup = data[0]["id_achat"]
        self.assertEqual(id_recup, id_achat)
