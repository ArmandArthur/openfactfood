# openfoodfacts
# Programme - Echange avec une base de données - PYTHON

Installer les modules et dépendances avec les commandes suivantes :
- pip install requests
- pip install mysql-connector-python
- pip install colorama

Le fichier "database.py" contient les informations de connexion à la base de données.
Vous devez saisir correctement vos paramètres de connexion pour que le programme puisse installer la base de données sur votre local.

Le fichier "setup.py" et plus précisément la méthode "database_set_values" contient les URLS des catégories de l'API Openfactfoodk, catégories qui seront ajoutées à la BDD  lors de l'exécution du programme.

Pour lancer le programme, effectuer un "py Main.py"
