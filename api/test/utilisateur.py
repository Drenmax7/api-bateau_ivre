from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from urllib.parse import urlencode
from api.models import Utilisateur

class UtilisateurTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Utilisateur.objects.create_user(mail="admin@test.com", password="password")
        self.user.is_staff = True
        self.client.force_authenticate(user=self.user)

        self.data = {
            "nom": "Doe", 
            "prenom": "John", 
            "civilite": "Monsieur", 
            "adresse": "123 rue Exemple", 
            "ville": "Paris", 
            "pays": "France", 
            "code_postal": "75000", 
            "telephone": "0123456789", 
            "complement_adresse": "Apt 2B",
            "mail": "johndoe@test.com",
            "password":"password"
        }

    def test_add_user(self):
        url = "/api/utilisateur/addUser/"
        response = self.client.post(url, self.data, format="json")

        # Vérifie que la requête a bien été traitée
        self.assertEqual(response.status_code, 201)

        id_utilisateur = response.json()["id_utilisateur"]
        query = Utilisateur.objects.filter(id_utilisateur=id_utilisateur)
        
        # Vérifie l'existence de l'utilisateur
        self.assertEqual(len(query), 1)

        utilisateur = query[0]
        # Vérifie que les valeurs sont correctes
        self.assertEqual(utilisateur.nom, self.data["nom"])
        self.assertEqual(utilisateur.mail, self.data["mail"])

    def test_delete_user(self):
        # Crée un utilisateur
        url = "/api/utilisateur/addUser/"
        response = self.client.post(url, self.data, format="json")
        print(response.json())
        id_utilisateur = response.json()["id_utilisateur"]

        # Supprime l'utilisateur
        url = "/api/utilisateur/deleteUser/"
        response = self.client.delete(url, {"id_utilisateur": id_utilisateur}, format="json")

        # Vérifie que la requête a bien été traitée
        self.assertEqual(response.status_code, 200)

        query = Utilisateur.objects.filter(id_utilisateur=id_utilisateur)
        # Vérifie la suppression de l'utilisateur
        self.assertEqual(len(query), 0)

    def test_update_user(self):
        # Crée un utilisateur
        url = "/api/utilisateur/addUser/"
        response = self.client.post(url, self.data, format="json")
        id_utilisateur = response.json()["id_utilisateur"]

        # Mets à jour l'utilisateur
        newData = {
            "id_utilisateur": id_utilisateur, 
            "colonne": ["nom", "prenom"], 
            "valeur": ["NouveauNom", "NouveauPrenom"]
        }
        url = "/api/utilisateur/updateUser/"
        response = self.client.put(url, newData, format="json")

        # Vérifie que la requête a bien été traitée
        self.assertEqual(response.status_code, 200)

        query = Utilisateur.objects.filter(id_utilisateur=id_utilisateur)
        utilisateur = query[0]
        # Vérifie la mise à jour des champs
        for i in range(len(newData["colonne"])):
            colonne = newData["colonne"][i]
            valeur = newData["valeur"][i]
            self.assertEqual(getattr(utilisateur, colonne), valeur)

    def test_get_user(self):
        # Crée un utilisateur
        url = "/api/utilisateur/addUser/"
        response = self.client.post(url, self.data, format="json")
        id_utilisateur = response.json()["id_utilisateur"]
        
        # Crée plusieurs utilisateurs
        for i in range(5):
            self.client.post(url, {
                "nom": f"Nom{i}", "prenom": f"Prenom{i}", "mail": f"user{i}@test.com", 
                "adresse": "Adresse Exemple", "telephone": "0123456789", "civilite":"na","ville":"ville", "pays":"pays","code_postal":"35","complement_adresse":"na", "password":"password"
            }, format="json")

        # Recherche un utilisateur spécifique
        param = {"colonne": ["nom", "mail"], "filtre": ["Doe", "johndoe@test.com"], "mode": ["==", "=="]}
        query_string = urlencode(param, doseq=True)
        url = f"/api/utilisateur/getUser/?{query_string}"
        response = self.client.get(url, format="json")
        
        # Vérifie que la requête a bien été traitée
        self.assertEqual(response.status_code, 200)
        
        # Vérifie qu'un utilisateur est récupéré
        data = response.json()
        self.assertEqual(len(data), 1)

        # Vérifie que l'utilisateur récupéré est bien celui qui a été cherché
        id_recup = data[0]["id_utilisateur"]
        self.assertEqual(id_recup, id_utilisateur)
