from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from ..models import Chaloupe, Utilisateur, College, Societaire, Rejoint

from urllib.parse import urlencode


class ChaloupeTest_correctUse(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.college = College.objects.create(nom="Citoyen")
        self.user = Utilisateur.objects.create_user(mail="testuser", password="password", college=self.college)
        self.user.is_staff = True
        self.client.force_authenticate(user=self.user)

        self.data = {"nom": "nom chaloupe", "description": "description chaloupe"}


    def test_add(self):
        url = "/api/chaloupe/addChaloupe/"
        response = self.client.post(url, self.data, format="json")

        #requete traité correctement
        self.assertEqual(response.status_code, 201) 

        id_entree = response.json()["id_chaloupe"]
        query = Chaloupe.objects.filter(id_chaloupe=id_entree)
        
        #verifie l'existence de la chaloupe
        self.assertEqual(len(query), 1)

        entree = query[0]
        #verifie que les valeurs sont les bonnes
        self.assertEqual(entree.nom, self.data["nom"])
        self.assertEqual(entree.description, self.data["description"])

    def test_delete(self):
        #cree une chaloupe
        url = "/api/chaloupe/addChaloupe/"
        response = self.client.post(url, self.data, format="json")
        id_entree = response.json()["id_chaloupe"]

        url = "/api/chaloupe/deleteChaloupe/"
        response = self.client.delete(url, {"id_chaloupe":id_entree}, format="json")

        #requete traité correctement
        self.assertEqual(response.status_code, 200)

        query = Chaloupe.objects.filter(id_chaloupe=id_entree)
        #verifie la supression de la chaloupe
        self.assertEqual(len(query), 0)

    def test_update(self):
        #cree une chaloupe
        url = "/api/chaloupe/addChaloupe/"
        response = self.client.post(url, self.data, format="json")
        id_entree = response.json()["id_chaloupe"]

        url = "/api/chaloupe/updateChaloupe/"
        newData = {"id_chaloupe":id_entree, "colonne": ["nom","description"], "valeur" : ["nouveau nom chaloupe", "nouveau description chaloupe"]}
        response = self.client.put(url, newData, format="json")

        #requete traité correctement
        self.assertEqual(response.status_code, 200)

        query = Chaloupe.objects.filter(id_chaloupe=id_entree)
        entree = query[0]
        #verifie la modification de la chaloupe
        for i in range(len(newData["colonne"])):
            colonne = newData["colonne"][i]
            valeur = newData["valeur"][i]            
            self.assertEqual(getattr(entree, colonne) , valeur)

    def test_get(self):
        #cree une chaloupe
        url = "/api/chaloupe/addChaloupe/"
        response = self.client.post(url, self.data, format="json")
        id_entree = response.json()["id_chaloupe"]
        
        for i in range(10):
            self.client.post(url, {"nom":"test nom","description":"test description"}, format="json")


        param = {"colonne": ["nom", "description"], "filtre" : ["nom chaloupe", "description chaloupe"], "mode":["==", "=="]}
        query_string = urlencode(param, doseq=True)
        url = f"/api/chaloupe/getChaloupe/?{query_string}"
        response = self.client.get(url, format="json")
        
        #requete traité correctement
        self.assertEqual(response.status_code, 200)
        
        #verifie qu'une ligne est récupéré
        data = response.json()
        self.assertEqual(len(data), 1)

        #verifie que la ligne récupéré est bien celle qui est cherché
        id_recup = data[0]["id_chaloupe"]
        self.assertEqual(id_recup, id_entree)


class RejointTest_correctUse(APITestCase):
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

        self.chaloupe = Chaloupe.objects.create(
            nom = "nom chaloupe",
            description = "description chaloupe"
        )
        
        self.data = {"dirige": True, "id_utilisateur":self.utilisateur.id_utilisateur,"id_chaloupe":self.chaloupe.id_chaloupe}


    def test_add(self):
        url = "/api/chaloupe/addRejoint/"
        response = self.client.post(url, self.data, format="json")

        #requete traité correctement
        self.assertEqual(response.status_code, 201) 

        query = Rejoint.objects.filter(id_chaloupe=self.data["id_chaloupe"], id_utilisateur=self.data["id_utilisateur"])
        
        #verifie l'existence de la chaloupe
        self.assertEqual(len(query), 1)

        entree = query[0]
        #verifie que les valeurs sont les bonnes
        self.assertEqual(entree.dirige, self.data["dirige"])

    def test_delete(self):
        #cree une chaloupe
        url = "/api/chaloupe/addRejoint/"
        response = self.client.post(url, self.data, format="json")

        url = "/api/chaloupe/deleteRejoint/"
        response = self.client.delete(url, {"id_chaloupe":self.data["id_chaloupe"], "id_utilisateur":self.data["id_utilisateur"]}, format="json")

        #requete traité correctement
        self.assertEqual(response.status_code, 200)

        query = Rejoint.objects.filter(id_chaloupe=self.data["id_chaloupe"], id_utilisateur=self.data["id_utilisateur"])
        #verifie la supression de la chaloupe
        self.assertEqual(len(query), 0)

    def test_update(self):
        #cree une chaloupe
        url = "/api/chaloupe/addRejoint/"
        response = self.client.post(url, self.data, format="json")

        url = "/api/chaloupe/updateRejoint/"
        newData = {"id_chaloupe":self.data["id_chaloupe"], "id_utilisateur":self.data["id_utilisateur"], "colonne": ["dirige"], "valeur" : [False]}
        response = self.client.put(url, newData, format="json")

        #requete traité correctement
        self.assertEqual(response.status_code, 200)

        query = Rejoint.objects.filter(id_chaloupe=self.data["id_chaloupe"], id_utilisateur=self.data["id_utilisateur"])
        entree = query[0]
        #verifie la modification de la chaloupe
        self.assertEqual(entree.dirige, False)

    def test_get(self):
        #cree une chaloupe
        url = "/api/chaloupe/addRejoint/"
        response = self.client.post(url, self.data, format="json")

        param = {"colonne": ["id_chaloupe", "id_utilisateur"], "filtre" : [self.data["id_chaloupe"], self.data["id_utilisateur"]], "mode":["==", "=="]}
        query_string = urlencode(param, doseq=True)
        url = f"/api/chaloupe/getRejoint/?{query_string}"
        response = self.client.get(url, format="json")
        
        #requete traité correctement
        self.assertEqual(response.status_code, 200)
        
        #verifie qu'une ligne est récupéré
        data = response.json()
        self.assertEqual(len(data), 1)

        #verifie que la ligne récupéré est bien celle qui est cherché
        id_recup = data[0]["id_chaloupe"]
        self.assertEqual(id_recup, self.data["id_chaloupe"])
        id_recup = data[0]["id_utilisateur"]
        self.assertEqual(id_recup, self.data["id_utilisateur"])

