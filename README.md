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

📚 Projet Bateau Ivre 🚤
🛠 Prérequis
Avant de démarrer, il est nécessaire d'installer les dépendances suivantes :

Django : pip install django
Django Rest Framework : pip install djangorestframework
⚙️ Configuration de la Base de Données
Les paramètres de la base de données peuvent être ajustés en modifiant le fichier bateau_ivre/settings.py.

Ouvrez le fichier et cherchez le dictionnaire DATABASES.
Modifiez-le pour qu'il corresponde à votre base de données locale.
Par défaut, ce projet utilise MariaDB, géré par XAMPP :

Nom de la base de données : bateauivre
Utilisateur : root
Mot de passe : Aucun
🧑‍💻 Configuration et Initialisation de la Base de Données
Créez la base de données bateauivre dans MariaDB si ce n'est pas déjà fait.
Exécutez la commande suivante pour préparer les tables de la base de données :
bash
Copy
Edit
python -m manage makemigrations
Ensuite, appliquez les migrations pour créer les tables :
bash
Copy
Edit
python -m manage migrate
🚀 Démarrer le Serveur
Pour lancer le serveur, utilisez cette commande :

bash
Copy
Edit
python -m manage runserver
🧑‍🔬 Remplir la Base de Données avec des Données de Test
Une fois le serveur démarré, vous pouvez remplir la base de données avec des données de test via l'URL /api/populate. Cela peut prendre quelques dizaines de secondes.

👉 Si la création des données est trop lente, vous pouvez réduire leur quantité en modifiant le fichier api/populate.py et en ajustant le nombre d'itérations dans certaines boucles for.

🔑 Création d'une Session Utilisateur
Pour créer une session utilisateur, utilisez l'URL suivante avec une méthode POST :

swift
Copy
Edit
POST /api/utilisateur/login/
Envoyez les paramètres suivants dans le corps de la requête :

mail : L'email de l'utilisateur.
username : Le nom d'utilisateur.
📑 Liste des URL pour la gestion des données
🔍 Récupérer des données :
[Liste des URLs de récupération] 👇
➕ Ajouter des données :
[Liste des URLs d'ajout] 👇
🔄 Mettre à jour des données :
[Liste des URLs de mise à jour] 👇
❌ Supprimer des données :
[Liste des URLs de suppression] 👇
🌐 Ressources Complémentaires
Django Documentation
Django Rest Framework Documentation
