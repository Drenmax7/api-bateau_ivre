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

Il faut ensuite ajouter le **token** que welogin a fourni dans le fichier **token.tok** afin d'assurer la mise à jour de la base de données avec les eventuelles nouvelles informations que reçoit celle de welogin.

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

## 🧪 **Vérifier le bon fonctionnement**

Pour vérifier qu'il n'y a pas de problème de configuration et que l'api marche, vous pouvez lancer les tests fonctionnelles de l'application :
```bash
python -m manage test
```

## 🚀 **Démarrer le Serveur**

Pour lancer le serveur, utilisez cette commande :
```bash
python -m manage runserver
```

---

## 🧑‍🔬 **Remplir la Base de Données avec des Données de Test**

Une fois le serveur démarré, vous pouvez remplir la base de données avec des données de test via l'URL **`/api/populate`** en mode **POST**. Cela peut prendre quelques dizaines de secondes.
Pour pouvoir accéder à l'URL il faut obligatoirement que l'application soit en mode **debug**. Ce parametre est accessible dans le fichier **`bateau_ivre/settings.py`**, il faut trouver la variable nommé `DEBUG` et mettre sa valeur à `True`. Une fois la base de données rempli pensez bien à enlever le mode debug en remettant la valeur de la variable à `False`.

👉 Si la création des données est trop lente, vous pouvez réduire leur quantité en modifiant le fichier **`api/populate.py`** et en ajustant le nombre d'itérations dans certaines boucles `for`.

---

## 🧑‍🔬 **Importer les données de WeLogin**

Une fois le serveur démarré, vous pouvez importer les données de WeLogin via l'URL **`/api/import/importWeLogin`** en mode **POST**.
De la meme facon que precedemment, cette requete necessite que l'application soit en mode **debug**
La requete prend un long moment à etre executé notemment du à la recherche de la localisation des societaires. Cette recherche s'effectue via un service externe gratuit mais lent. Des delais sont present dans le code entre chaque requete et sont **necessaire** afin que le service ne renvoie pas d'erreur.
Les localisations trouvé sont placé dans un fichier cahce `cacheGeolocator.txt` afin de limiter au maximum les appels au service externe.
Les appels à l'api peuvent etre desactivé en utilisant cette URL **`/api/import/importWeLogin/?skipLocalisation=1`**.
Le fichier `geolocatorLog.txt` contient les adresses que le service externe n'a pas réussie à trouver. Cela peut etre du à des fautes de frappe, une ponctuation eronné etc. 

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
🔹 **URLS** : `/api/utilisateur/getUser/`, `/api/utilisateur/getCollege/`, `/api/societaire/getSocietaire/`, `/api/partSocial/getPartSocial/`, `/api/evenement/getEvenement/`, `/api/evenement/getReserve/`, `/api/chaloupe/getChaloupe/`, `/api/chaloupe/getRejoint/`, `/api/connexion/getConnexion/`, `/api/connexion/getHistorique/`  
🔹 **Accès** : 🔒 Requiert une connexion  (excepté **`/api/evenement/getEvenement/`**)  
🔹 **Méthode** : **GET**  
🔹 **Description** :  Permet de selectionner des entrées d'une table via des filtres et de les récuperer.
<details>
<summary><b>🔹Paramètres requis dans le header :</b></summary>

| Champ   | Type    | Description |
|---------|--------|-------------|
| `colonne` | `list[str]` | Liste des colonnes sur lesquelles appliquer les filtres |
| `filtre`  | `list[str]` | Liste des valeurs utilisées pour filtrer les résultats |
| `mode`    | `list[str]` | Méthode de filtrage appliquée |
| `geojson` (optionnel) | `bool` : 0 ou 1| Uniquement pour getUser, specifie si les utilisateurs renvoyé sont au format geojson ou non|

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
/api/utilisateur/getUser/?colonne=nom&colonne=ville&filtre=Duck&filtre=Paris&mode===&mode===

```

</details>

---

#### 📊 **Compter le nombre de connexion effectué par des utilisateurs**  
🔹 **URL** : `api/connexion/compteConnexion/`
🔹 **Accès** : 🔒 Requiert une connexion
🔹 **Méthode** : **GET**  
🔹 **Description** :  Permet de recuperer le nombre de connexion unique enregistré dans la BDD

<details>
<summary><b>🔹Paramètres optionnel dans le header :</b></summary>

| Champ   | Type    | Description |
|---------|--------|-------------|
| `mode` | `str : "jour" ou "mois"` | Indique si les connexions doivent regroupé par jour ou par mois |
| `college`  | `bool : 0 ou 1` | Indique si le nombre de connexion doit distingué les diffents colleges ou tous les regrouper |

</details>


---

</details>

<details>
<summary><strong>➕ Ajouter des données :</strong></summary>

#### 📕**Ajouter des données dans une table**
🔹 **URLS** : `api/utilisateur/addUser/`, `api/utilisateur/addCollege/`, `api/societaire/addSocietaire/`, `api/partSocial/addPartSocial/`, `api/evenement/addEvenement/`, `api/evenement/addReservation/`, `api/connexion/addConnexion/`, `api/chaloupe/addChaloupe/`, `api/chaloupe/addRejoint/`  
🔹 **Accès** : 🔒 Requiert d'être administrateur
🔹 **Méthode** : **POST**  
🔹 **Description** :  Permet d'ajouter des entrées dans une table, nécessite de mettre les informations de la donnée qu'on veut ajouter dans le body

<details>
<summary><b>🔹Paramètres requis dans le body :</b></summary>

Les paramètres requis varient selon l'URL car les informations à renseigner ne sont pas les mêmes selon la table :

| URL   | Paramètres |
|---------|------------|
| `api/utilisateur/addUser/` | `nom`, `prenom`, `civilite`, `adresse`, `ville`, `pays`, `code_postal`, `telephone`, `complement_adresse`, `mail`, `password`, `college`, `is_staff` |
| `api/utilisateur/addCollege/` | `nom` |
| `api/societaire/addSocietaire/` | `id_utilisateur`, `organisation`, `numero_societaire` |
| `api/partSocial/addPartSocial/` | `date_achat`, `quantite`, `num_facture`, `id_societaire` |
| `api/evenement/addEvenement/` | `place_disponible`, `date_evenement`, `titre`, `description` |
| `api/evenement/addReservation/` | `id_utilisateur`, `id_evenement`, `nb_place` |
| `api/connexion/addConnexion/` | `id_utilisateur`, `id_evenement`, `nb_place` |
| `api/chaloupe/addChaloupe/` | `nom`, `description` |
| `api/chaloupe/addRejoint/` | `id_utilisateur`, `id_chaloupe`, `dirige` |

✅ **Exemple d'utilisation** :  
Si tu veux ajouter une chaloupe dont le nom est **CoinCoinTech** et la description est **Start-up innovante développant des gadgets pour améliorer la vie des canards connectés.**, il faut utiliser l'URL suivant :  
```json
/api/chaloupe/addChaloupe/
```

Puis dans le body :

```json
{
    "nom": "CoinCoinTech",
    "description": "Start-up innovante développant des gadgets pour améliorer la vie des canards connectés."
}
```
</details>

---

</details>

<details>
<summary><strong>🔄 Mettre à jour des données :</strong></summary>

#### 📕**Modifier les informations d'une donnée dans une table**
🔹 **URLS** : `api/utilisateur/updateUserPassword/`, `api/utilisateur/updateUser/`, `api/utilisateur/fusionneUsers/`, `api/utilisateur/updateCollege/`, `api/societaire/updateSocietaire/`, `api/partSocial/updatePartSocial/`, `api/evenement/updateEvenement/`, `api/evenement/updateReservation/`, `api/chaloupe/updateChaloupe/`, `api/chaloupe/updateRejoint/`  
🔹 **Accès** : 🔒 Requiert d'être administrateur  
🔹 **Méthode** : **PUT**  
🔹 **Description** :  Permet de modifier des données dans une table, nécessite de connaître l'**ID** de la donnée qu'on veut modifier

<details>

<summary><b>🔹Paramètres requis dans le body :</b></summary>

#### 👍**Le cas "normal"**

| Champ   | Type    | Description |
|---------|--------|-------------|
| `id` | `int` | l'ID de l'élément à modifier dans la table, le nom dépend évidemment de l'URL, exemple : id_utilisateur |
| `colonne`  | `list[str]` | Liste des colonnes à modifier |
| `valeur`    | `list[str]` | Liste des nouvelles valeurs des colonnes (les indices de colonne et valeur doivent correspondre) |

#### ⚠️**Les exceptions**

🔹 `api/utilisateur/updateUserPassword/` : dans le body, on met seulement `id_utilisateur` et le nouveau mot de passe dans `password`  
🔹 `api/utilisateur/fusionneUsers/` : dans le body, on met seulement `dissout`, l'ID de l'utilisateur qu'on veut supprimer, et `recipient` l'ID de l'utilisateur qui récupère les données  
🔹 `api/evenement/updateReservation/` : en guise d'ID, on utilise `id_evenement` **ET** `id_utilisateur`, de même pour `api/chaloupe/updateRejoint/` qui utilise `id_chaloupe` **ET** `id_utilisateur`  

✅ **Exemples d'utilisation** :

Si tu veux que l'utilisateur d'ID **9** ait maintenant pour `nom` **Picsou** et que sa `ville` soit **DonaldVille**, il faut utiliser l'URL suivant :
```json
api/utilisateur/updateUser/
```

Puis dans le body :
```json
{
    "id_utilisateur": 9,
    "colonne": ["nom", "ville"],
    "valeur": ["Picsou", "DonaldVille"]
}
```

❌ Erreur à ne pas faire :
```json
{
    "id_utilisateur": 9,
    "colonne": ["nom", "ville"],
    "valeur": ["DonaldVille", "Picsou"]
}
```

**Autre exemple :** Si tu veux que ce même utilisateur (ID **9**), qui est actuellement membre de la chaloupe d'ID **3**, `dirige` maintenant cette chaloupe, il faut utiliser l'URL suivant :
```json
api/chaloupe/updateRejoint/
```

Puis dans le body :
```json
{
    "id_chaloupe": 3,
    "id_utilisateur": 9,
    "colonne": ["dirige"],
    "valeur": ["true"]
}
```

</details>

---

</details>

<details>
<summary><strong>❌ Supprimer des données :</strong></summary>

#### 📕**Supprimer une donnée dans une table**
🔹 **URLS** : `api/utilisateur/deleteUser/`, `api/utilisateur/deleteCollege/`, `api/societaire/deleteSocietaire/`, `api/partSocial/deletePartSocial/`, `api/evenement/deleteEvenement/`, `api/evenement/deleteReservation/`, `api/connexion/deleteConnexion/`, `api/chaloupe/deleteChaloupe/`, `api/chaloupe/deleteRejoint/`  
🔹 **Accès** : 🔒 Requiert d'être administrateur  
🔹 **Méthode** : **DELETE**  
🔹 **Description** :  Permet de supprimer une donnée dans une table, nécessite de connaître l'**ID** de la donnée qu'on veut supprimer

<details>

<summary><b>🔹Paramètres requis dans le body :</b></summary>

#### 👍**Le cas "normal"**

| Champ   | Type    | Description |
|---------|--------|-------------|
| `id` | `int` | l'ID de l'élément à supprimer dans la table, le nom dépend évidemment de l'URL, exemple : id_utilisateur |

... et c'est tout !

#### ⚠️**Les exceptions**

🔹 `api/evenement/deleteReservation/` : en guise d'ID, on utilise `id_evenement` **ET** `id_utilisateur`, de même pour `api/chaloupe/deleteRejoint/` qui utilise `id_chaloupe` **ET** `id_utilisateur`  
🔹 `api/connexion/deleteConnexion/` : en plus de l'ID (qui correspond à `id_utilisateur`), on a un paramètre `jour` obligatoire qui correspond au jour de la connexion  

✅ **Exemples d'utilisation** :

Si tu veux que l'utilisateur d'ID **9** soit supprimé de la base de données, il faut utiliser l'URL suivant :
```json
api/utilisateur/deleteUser/
```

Puis dans le body :
```json
{
    "id_utilisateur": 9
}
```

**Autre exemple :** Si tu veux que l'utilisateur d'ID **6** n'appartienne plus à la chaloupe d'ID **3**, il faut utiliser l'URL suivant :
```json
api/chaloupe/deleteRejoint/
```

Puis dans le body :
```json
{
    "id_chaloupe": 3,
    "id_utilisateur": 6
}
```

</details>

---

</details>

---

## 🌐 **Ressources Complémentaires**

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Rest Framework Documentation](https://www.django-rest-framework.org/)

