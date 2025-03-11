from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from urllib.parse import urlencode
from api.models import Societaire, Utilisateur, College

class SocietaireTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.college = College.objects.create(nom="Citoyen")
        self.user = Utilisateur.objects.create_user(mail="testuser", password="password", college=self.college)
        self.user.is_staff = True
        self.client.force_authenticate(user=self.user)
        
        self.utilisateur = Utilisateur.objects.create(
            mail="societaire@test.com",
            nom="Doe",
            prenom="John",
            telephone="0123456789",
            college=self.college
        )

        self.data = {
            "organisation": "Organisation Test",
            "numero_societaire": "12345",
            "id_utilisateur": self.utilisateur.id_utilisateur
        }

    def test_add_societaire(self):
        url = "/api/societaire/addSocietaire/"
        response = self.client.post(url, self.data, format="json")

        # requête traitée correctement
        self.assertEqual(response.status_code, 201)

        id_societaire = response.json()["id_societaire"]
        query = Societaire.objects.filter(id_societaire=id_societaire)

        # vérifie l'existence du sociétaire
        self.assertEqual(len(query), 1)

        societaire = query[0]
        # vérifie que les valeurs sont les bonnes
        self.assertEqual(societaire.organisation, self.data["organisation"])
        self.assertEqual(societaire.numero_societaire, self.data["numero_societaire"])

    def test_delete_societaire(self):
        # crée un sociétaire
        url = "/api/societaire/addSocietaire/"
        response = self.client.post(url, self.data, format="json")
        id_societaire = response.json()["id_societaire"]

        url = "/api/societaire/deleteSocietaire/"
        response = self.client.delete(url, {"id_societaire": id_societaire}, format="json")

        # requête traitée correctement
        self.assertEqual(response.status_code, 200)

        query = Societaire.objects.filter(id_societaire=id_societaire)
        # vérifie la suppression du sociétaire
        self.assertEqual(len(query), 0)

    def test_update_societaire(self):
        # crée un sociétaire
        url = "/api/societaire/addSocietaire/"
        response = self.client.post(url, self.data, format="json")
        id_societaire = response.json()["id_societaire"]

        url = "/api/societaire/updateSocietaire/"
        newData = {
            "id_societaire": id_societaire, 
            "colonne": ["organisation", "numero_societaire"], 
            "valeur": ["Nouvelle Organisation", "67890"]
        }
        response = self.client.put(url, newData, format="json")

        # requête traitée correctement
        self.assertEqual(response.status_code, 200)

        query = Societaire.objects.filter(id_societaire=id_societaire)
        societaire = query[0]
        # vérifie la modification du sociétaire
        for i in range(len(newData["colonne"])):
            colonne = newData["colonne"][i]
            valeur = newData["valeur"][i]
            self.assertEqual(getattr(societaire, colonne), valeur)

    def test_get_societaire(self):
        # crée un sociétaire
        url = "/api/societaire/addSocietaire/"
        response = self.client.post(url, self.data, format="json")
        id_societaire = response.json()["id_societaire"]

        for i in range(5):
            self.client.post(url, {
                "organisation": f"Organisation {i}",
                "numero_societaire": f"Num-{i}",
                "id_utilisateur": self.utilisateur.id_utilisateur,
                "college": self.college.nom
            }, format="json")

        param = {"colonne": ["organisation"], "filtre": ["Organisation Test"], "mode": ["=="]}
        query_string = urlencode(param, doseq=True)
        url = f"/api/societaire/getSocietaire/?{query_string}"
        response = self.client.get(url, format="json")

        # requête traitée correctement
        self.assertEqual(response.status_code, 200)

        # vérifie qu'une ligne est récupérée
        data = response.json()
        self.assertEqual(len(data), 1)

        # vérifie que la ligne récupérée est bien celle qui est cherchée
        id_recup = data[0]["id_societaire"]
        self.assertEqual(id_recup, id_societaire)
