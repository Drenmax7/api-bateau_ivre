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

Une fois le serveur démarré, vous pouvez remplir la base de données avec des données de test via l'URL **`/api/populate`**. Cela peut prendre quelques dizaines de secondes.

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

Lorsque vous interagissez avec l'API, il est essentiel de **récupérer le token CSRF** renvoyé dans la réponse de l'API. 🦆

L'API Django utilise un système de sécurité basé sur des **tokens CSRF** (Cross-Site Request Forgery). Ce mécanisme est utilisé pour sécuriser les requêtes sensibles. En effet, chaque méthode **POST**, **PUT**, **PATCH** ou **DELETE** nécessite ce token pour être traitée.

### Comment l'utiliser ?
- **Lors de l'envoi d'une requête** de type **POST**, **PUT**, **PATCH** ou **DELETE**, vous devez inclure dans le **header** de votre requête un champ nommé `X-CSRFToken`.
- La **valeur** de ce champ doit être le **token CSRF** récupéré.

Assurez-vous de toujours envoyer ce token afin de garantir que vos requêtes seront **acceptées** par l'API.

💡 **Note** : Sans ce token, l'API rejettera la requête et vous recevrez une erreur de type **CSRF failed**.

---

## 📑 **Liste des URL pour la gestion des données**

### 🔍 **Récupérer des données** :

- [Liste des URLs de récupération] 👇

### ➕ **Ajouter des données** :

- [Liste des URLs d'ajout] 👇

### 🔄 **Mettre à jour des données** :

- [Liste des URLs de mise à jour] 👇

### ❌ **Supprimer des données** :

- [Liste des URLs de suppression] 👇

---

## 🌐 **Ressources Complémentaires**

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Rest Framework Documentation](https://www.django-rest-framework.org/)

---

✨ **Bonne chance et bon développement !** 🦆💻🚀

