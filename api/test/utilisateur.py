from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from urllib.parse import urlencode

from api.models import Utilisateur, College, Societaire, PartSocial, Reserve, Connexion, HistoriqueConnexion, Rejoint, Chaloupe, Evenement

class UtilisateurTest_correctUse(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.college = College.objects.create(nom="Citoyen")
        self.user = Utilisateur.objects.create_user(mail="testuser", password="password", college=self.college)
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
            "password":"password",
            "college": "Citoyen"
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


class CollegeTest_correctUse(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.college = College.objects.create(nom="Citoyen")
        self.user = Utilisateur.objects.create_user(mail="testuser", password="password", college=self.college)
        self.user.is_staff = True
        self.client.force_authenticate(user=self.user)
                
        self.data = {"nom": "nom college"}


    def test_add(self):
        url = "/api/utilisateur/addCollege/"
        response = self.client.post(url, self.data, format="json")

        #requete traité correctement
        self.assertEqual(response.status_code, 201) 

        nom = response.json()["nom"]
        query = College.objects.filter(nom=nom)
        
        #verifie l'existence de la chaloupe
        self.assertEqual(len(query), 1)

        entree = query[0]
        #verifie que les valeurs sont les bonnes
        self.assertEqual(entree.nom, self.data["nom"])

    def test_delete(self):
        #cree une chaloupe
        url = "/api/utilisateur/addCollege/"
        response = self.client.post(url, self.data, format="json")
        id_entree = response.json()["nom"]

        url = "/api/utilisateur/deleteCollege/"
        response = self.client.delete(url, {"college":id_entree}, format="json")

        #requete traité correctement
        self.assertEqual(response.status_code, 200)

        query = College.objects.filter(nom=id_entree)
        #verifie la supression de la chaloupe
        self.assertEqual(len(query), 0)

    def test_update(self):
        #cree une chaloupe
        url = "/api/utilisateur/addCollege/"
        response = self.client.post(url, self.data, format="json")
        id_entree = response.json()["nom"]

        url = "/api/utilisateur/updateCollege/"
        newData = {"college":id_entree, "colonne": ["nom"], "valeur" : ["nouveau nom college"]}
        response = self.client.put(url, newData, format="json")

        #requete traité correctement
        self.assertEqual(response.status_code, 200)
        
        query = College.objects.filter(nom=newData["valeur"][newData["colonne"].index("nom")])
        entree = query[0]
        #verifie la modification de la chaloupe
        for i in range(len(newData["colonne"])):
            colonne = newData["colonne"][i]
            valeur = newData["valeur"][i]            
            self.assertEqual(getattr(entree, colonne) , valeur)

    def test_get(self):
        #cree une chaloupe
        url = "/api/utilisateur/addCollege/"
        response = self.client.post(url, self.data, format="json")
        id_entree = response.json()["nom"]
        
        for i in range(10):
            self.client.post(url, {"nom":f"test nom college{i}"}, format="json")


        param = {"colonne": ["nom"], "filtre" : ["nom college"], "mode":["=="]}
        query_string = urlencode(param, doseq=True)
        url = f"/api/utilisateur/getCollege/?{query_string}"
        response = self.client.get(url, format="json")
        
        #requete traité correctement
        self.assertEqual(response.status_code, 200)
        
        #verifie qu'une ligne est récupéré
        data = response.json()
        self.assertEqual(len(data), 1)

        #verifie que la ligne récupéré est bien celle qui est cherché
        id_recup = data[0]["nom"]
        self.assertEqual(id_recup, id_entree)
    
class FusionneUsersTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.college = College.objects.create(nom="Test college")
        self.recipient = Utilisateur.objects.create(nom="Recipient", prenom="User", mail="recipient@example.com", college=self.college)
        self.dissout = Utilisateur.objects.create(nom="Dissout", prenom="User", mail="dissout@example.com", college=self.college)

        self.admin = Utilisateur.objects.create_user(nom="Admin", prenom="User", mail="admin@example.com", password="admin", college=self.college)
        self.admin.is_staff = True
        self.client.force_authenticate(user=self.admin)

        self.url = "/api/utilisateur/fusionneUsers/"

    def test_fusion_succes(self):
        response = self.client.post(self.url, {"recipient": self.recipient.id_utilisateur, "dissout": self.dissout.id_utilisateur}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Utilisateur.objects.filter(id_utilisateur=self.dissout.id_utilisateur).exists())
        self.assertTrue(Utilisateur.objects.filter(id_utilisateur=self.recipient.id_utilisateur).exists())
    
    def test_fusion_recipient_non_existant(self):
        response = self.client.post(self.url, {"recipient": 9999, "dissout": self.dissout.id_utilisateur}, format="json")
        self.assertEqual(response.status_code, 400)
    
    def test_fusion_dissout_non_existant(self):
        response = self.client.post(self.url, {"recipient": self.recipient.id_utilisateur, "dissout": 9999}, format="json")
        self.assertEqual(response.status_code, 400)
    
    def test_fusion_champs_vide_rempli(self):
        self.recipient.telephone = ""
        self.recipient.save()
        self.dissout.telephone = "0606060606"
        self.dissout.save()
        
        self.client.post(self.url, {"recipient": self.recipient.id_utilisateur, "dissout": self.dissout.id_utilisateur}, format="json")
        self.recipient.refresh_from_db()
        self.assertEqual(self.recipient.telephone, "0606060606")
    
    def test_fusion_evenements(self):
        evenement = Evenement.objects.create(titre="Event Test", place_disponible=10,date_evenement="2024-08-30")
        evenement2 = Evenement.objects.create(titre="Event Test2", place_disponible=10,date_evenement="2024-08-30")
        Reserve.objects.create(id_utilisateur=self.dissout, id_evenement=evenement, nb_place=2)
        Reserve.objects.create(id_utilisateur=self.dissout, id_evenement=evenement2, nb_place=2)
        Reserve.objects.create(id_utilisateur=self.recipient, id_evenement=evenement, nb_place=3)
        
        self.client.post(self.url, {"recipient": self.recipient.id_utilisateur, "dissout": self.dissout.id_utilisateur}, format="json")

        reservation = Reserve.objects.get(id_utilisateur=self.recipient, id_evenement=evenement)
        self.assertEqual(reservation.nb_place, 5)

        self.assertTrue(Reserve.objects.filter(id_utilisateur=self.recipient, id_evenement=evenement2).exists())
    
    def test_fusion_chaloupes(self):
        chaloupe = Chaloupe.objects.create(nom="Chaloupe Test")
        Rejoint.objects.create(id_utilisateur=self.dissout, id_chaloupe=chaloupe, dirige=True)
        
        self.client.post(self.url, {"recipient": self.recipient.id_utilisateur, "dissout": self.dissout.id_utilisateur}, format="json")
        rejoint = Rejoint.objects.get(id_utilisateur=self.recipient, id_chaloupe=chaloupe)
        self.assertTrue(rejoint.dirige)
    
    def test_fusion_societaire(self):
        societaire_dissout = Societaire.objects.create(id_utilisateur=self.dissout, numero_societaire="123")
        PartSocial.objects.create(id_societaire=societaire_dissout, quantite=10, numero_achat=1, num_facture="FACT123", date_achat = "2025-03-11")
        
        self.client.post(self.url, {"recipient": self.recipient.id_utilisateur, "dissout": self.dissout.id_utilisateur}, format="json")
        societaire_recipient = Societaire.objects.get(id_utilisateur=self.recipient)
        self.assertEqual(societaire_recipient.numero_societaire, "123")
        self.assertTrue(PartSocial.objects.filter(id_societaire=societaire_recipient).exists())
