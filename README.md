Necessité d'installer django et django rest

Les parametres de la base de données peuvent etre changé en modifiant le fichier bateau_ivre/setings.py.
Modifier le dictionnaire DATABASES afin de convenir à la BDD local.
De base il s'agit d'une BDD MariaDB géré par Xamp, le nom de la BDD est bateauivre, le user est root et pas de mdp.

Une fois la BDD crée executer la commande 'python -m manage makemigrations' afin de préparer les tables de la BDD puis 'python -m manage migrate' pour les créer.
Le server se lance quant à lui avec 'python -m manage runserver'.
La BDD peut ensuite être rempli de donnée de test via l'URL /api/populate.
Cela devrait prendre quelques dizaines de seconde.
Si la creation des données est trop longue, il est possible de réduire leur quantité en modifiant le fichier api/populate.py en reduisant le nombre d'iterations de certaines boucles for.

Creation d'une session utilisateur :
  /api/utilisateur/login/ POST {mail, username}
  
Ci dessous la liste des urls permettant de recuperer des données :

Ci dessous la liste des urls permettant d'ajouter des données :

Ci dessous la liste des urls permettant de mettre à jour des données :

Ci dessous la liste des urls permettant de supprimer des données :

# 📚 **Projet Bateau Ivre** 🚤

## 🛠 **Prérequis**

Avant de démarrer, il est nécessaire d'installer les dépendances suivantes :

- **Django** : `pip install django`
- **Django Rest Framework** : `pip install djangorestframework`

## ⚙️ **Configuration de la Base de Données**

Les paramètres de la base de données peuvent être ajustés en modifiant le fichier **`bateau_ivre/settings.py`**.

1. Ouvrez le fichier et cherchez le dictionnaire `DATABASES`.
2. Modifiez-le pour qu'il corresponde à votre base de données locale.

Par défaut, ce projet utilise **MariaDB**, géré par **XAMPP** :
- **Nom de la base de données** : `bateauivre`
- **Utilisateur** : `root`
- **Mot de passe** : Aucun

---

## 🧑‍💻 **Configuration et Initialisation de la Base de Données**

1. Créez la base de données **bateauivre** dans MariaDB si ce n'est pas déjà fait.
2. Exécutez la commande suivante pour préparer les tables de la base de données :

```bash
python -m manage makemigrations
