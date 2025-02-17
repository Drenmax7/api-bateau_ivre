Necessité d'installer django et django rest

Les parametres de la base de données peuvent etre changé en modifiant le fichier bateau_ivre/setings.py.
Modifier le dictionnaire DATABASES afin de convenir à la BDD local
De base il s'agit d'une BDD MariaDB géré par Xamp, le nom de la BDD est bateauivre, le user est root et pas de mdp

Une fois la BDD crée executer la commande 'python -m manage makemigrations' afin de préparer les tables de la BDD puis 'python -m manage migrate' pour les créer
La BDD peut ensuite être rempli de donnée de test via l'URL /api/populate
Cela devrait prendre quelques dizaines de seconde
Si la creation des données est trop longue, il est possible de réduire leur quantité en modifiant le fichier api/populate.py en reduisant le nombre d'iterations de certaines boucles for

Ci dessous la liste des urls permettant de recuperer des données :

Ci dessous la liste des urls permettant d'ajouter des données :

Ci dessous la liste des urls permettant de mettre à jour des données :

Ci dessous la liste des urls permettant de supprimer des données :
