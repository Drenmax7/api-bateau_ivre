# 📚 **Projet Bateau Ivre** 🚤

## 🛠 **Prérequis**

Avant de démarrer, il est nécessaire d'installer les dépendances du fichier requirements.txt :

```bash
pip install -r requirements.txt
```

## ⚙️ **Configuration de la Base de Données**

Les paramètres de la base de données peuvent être ajustés en modifiant le fichier **`bateau_ivre/settings.py`**.

1. Ouvrez le fichier et cherchez le dictionnaire `DATABASES`.
2. Modifiez-le pour qu'il corresponde à votre base de données locale.

Par défaut, ce projet utilise **MariaDB**, géré par **XAMPP** :
- **Nom de la base de données** : `bateauIvre`
- **Utilisateur** : `root`
- **Mot de passe** : Aucun

---

## 🧑‍💻 **Configuration et Initialisation de la Base de Données**

1. Créez la base de données **bateauivre** dans MariaDB si ce n'est pas déjà fait.
2. Exécutez la commande suivante pour préparer les tables de la base de données :

```bash
python -m manage makemigrations
```

3. Ensuite, appliquez les migrations pour créer les tables :
```bash
python -m manage migrate
```

## 🚀 **Démarrer le Serveur**

Pour lancer le serveur, utilisez cette commande :
```bash
python -m manage runserver
```

---

## 🧑‍🔬 **Remplir la Base de Données avec des Données de Test**

Une fois le serveur démarré, vous pouvez remplir la base de données avec des données de test via l'URL **`/api/populate/`**. Cela peut prendre quelques dizaines de secondes.

👉 Si la création des données est trop lente, vous pouvez réduire leur quantité en modifiant le fichier **`api/populate.py`** et en ajustant le nombre d'itérations dans certaines boucles `for`.

---

### 🔑 **Identifiants de Test Utilisateur**

Voici les identifiants d'un des utilisateurs créés lors du remplissage :

- **Mail** : `canard@gmail.com` 🦆  
- **Mot de passe** : `canard` 🔒

---

## 🔑 **Création d'une Session Utilisateur**

Pour créer une session utilisateur, utilisez l'URL suivante avec une méthode **POST** :  
**`/api/utilisateur/login/`**

Envoyez les paramètres suivants dans le corps de la requête :
- **`mail`** : L'email de l'utilisateur.
- **`password`** : Le mot de passe de l'utilisateur.

## **Important**

Lorsque vous interagissez avec l'API, il est essentiel de **récupérer le token CSRF** renvoyé dans la réponse de l'API, ainsi que le **session id**. 🦆

L'API Django utilise un système de sécurité basé sur des **tokens CSRF** (Cross-Site Request Forgery). Ce mécanisme est utilisé pour sécuriser les requêtes sensibles. En effet, chaque méthode **POST**, **PUT**, **PATCH** ou **DELETE** nécessite ce token pour être traitée.
Le **session id** peremt à l'api de lier une requete à une session active.

### Comment l'utiliser ?
- **Lors de l'envoi d'une requête** de type **POST**, **PUT**, **PATCH** ou **DELETE**, vous devez inclure dans **l'URL** de votre requête un champ nommé `csrftoken`.
- La **valeur** de ce champ doit être le **token CSRF** récupéré.
- De la même façon, lors de chaque requête **necessitant une connexion** il faut inclure dans **l'URL** de votre requête un champs nommé `sessionid` dont la valeur doit être **l'id recupéré** précedemment.

Assurez-vous de toujours envoyer ces tokens afin de garantir que vos requêtes seront **acceptées** par l'API.

💡 **Note** : Sans l'un de ces tokens, l'API rejettera la requête et vous recevrez une erreur de type **CSRF failed** ou bien **Unauthorized**.

---

## 📑 **Liste des URL pour la gestion des données** 


<details>
<summary><strong>🔍 Récupération des données :</strong></summary>

#### 🧑‍💻 **Obtenir les informations de l'utilisateur connecté**  
🔹 **URL** : `/api/utilisateur/getLoginUser/`  
🔹 **Accès** : 🔒 Requiert une connexion  
🔹 **Méthode** : **GET**  
🔹 **Description** :  Permet de récupérer les informations de base sur l'utilisateur actuellement connecté, telles que :  **Nom, prénom, ville, etc.**  

---

#### 🎯 **Rechercher dans une table avec filtres avancés**  
🔹 **URLS** : `/api/utilisateur/getUser/`, `/api/societaire/getSocietaire/`, `/api/partSocial/getPartSocial/`, `/api/evenement/getEvenement/`, `/api/evenement/getReserve/`, `/api/chaloupe/getChaloupe/`, `/api/chaloupe/getRejoint/`, `/api/connexion/getConnexion/`, `/api/connexion/getHistorique/`  
🔹 **Accès** : 🔒 Requiert une connexion  (excepté **`/api/evenement/getEvenement/`**)  
🔹 **Méthode** : **GET**  
🔹 **Description** :  Permet de selectionner des entrées d'une table via des filtres et de les récuperer.
<details>
<summary><b>🔹Paramètres requis dans le body :</b></summary>

| Champ   | Type    | Description |
|---------|--------|-------------|
| `colonne` | `list[str]` | Liste des colonnes sur lesquelles appliquer les filtres |
| `filtre`  | `list[str]` | Liste des valeurs utilisées pour filtrer les résultats |
| `mode`    | `list[str]` | Méthode de filtrage appliquée |

🔹 **Modes de filtrage disponibles** :  
| Mode | Signification |
|------|--------------|
| `==`  | Égal à |
| `<=`  | Inférieur ou égal |
| `<`   | Strictement inférieur |
| `>=`  | Supérieur ou égal |
| `>`   | Strictement supérieur |
| `^`   | Contient |

✅ **Exemple d'utilisation** :  
Si tu veux récupérer tous les utilisateurs **nommés "Duck"** qui habitent **à Paris**, en **mode strictement égal** :  
```json
URL : "/api/utilisateur/getUser/"

body : {
  "colonne": ["nom", "ville"],
  "filtre": ["Duck", "Paris"],
  "mode": ["==", "=="]
}
```

</details>

---

- `api/connexion/compteConnexion`

</details>

<details>
<summary><strong>➕ Ajouter des données :</strong></summary>

- [Liste des URLs d'ajout] 👇
- `api/utilisateur/addUser/`
- `api/societaire/addSocietaire/`
- `api/partSocial/addPartSocial/`
- `api/evenement/addEvenement/`
- `api/evenement/addReservation/`
- `api/connexion/addConnexion/`
- `api/chaloupe/addChaloupe/`
- `api/chaloupe/addRejoint/`
- `api/chaloupe/addSelfRejoint/`

</details>

<details>
<summary><strong>🔄 Mettre à jour des données :</strong></summary>

- [Liste des URLs de maj] 👇
- `api/utilisateur/updateSelfPassword/`
- `api/utilisateur/updateUserPassword/`
- `api/utilisateur/updateUser/`
- `api/societaire/updateSocietaire/`
- `api/partSocial/updatePartSocial/`
- `api/evenement/updateEvenement/`
- `api/evenement/updateReservation/`
- `api/chaloupe/updateChaloupe/`
- `api/chaloupe/updateRejoint/`



</details>

<details>
<summary><strong>❌ Supprimer des données :</strong></summary>

- [Liste des URLs de supression] 👇
- `api/utilisateur/deleteUser/`
- `api/societaire/deleteSocietaire/`
- `api/partSocial/deletePartSocial/`
- `api/evenement/deleteEvenement/`
- `api/evenement/deleteReservation/`
- `api/connexion/deleteConnexion/`
- `api/chaloupe/deleteChaloupe/`
- `api/chaloupe/deleteRejoint/`
- `api/chaloupe/deleteSelfRejoint/`


</details>

---

## 🌐 **Ressources Complémentaires**

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Rest Framework Documentation](https://www.django-rest-framework.org/)

