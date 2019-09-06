# VD-SerVis
Application HTML CSS JS pour le cours "Visualisation de données"

# Indications
Télécharger tous les fichiers présents dans le répertoire VD-SerVis.
Il est possible de lancer l'application sur l'hôte local (localhost:5000) en tapant dans l'invite de commande :

`Scripts\actiate.bat'`

pour activer l'environnement virtuel et

`python app.py`

# Description

VD-SerVis est une application permettant de visualiser l'accessibilité aux services publics et de constater et quantifier les inégalités spatiales qui en résultent. La version actuelle ne comprend pour l'instant qu'un prototype de service implémenté : les établissements secondaires scolaires. Dans les prochaines mises à jours, d'autres services publics y seront rajoutés, notamment dans le domaine de la santé, des secours et des urgences médicales. Les contraintes d'accessibilité et les temps de trajets sont des éléments notables dans la géographie de l'urgence, ce qui rend l'utilisation de VD-SerVis particulièrement intéressante.

# Divers

Les données relatives aux temps de trajet ont été extraites directement depuis le serveur d'OTP (Open Trip Planner https://www.opentripplanner.org/) grâce aux requêtes formulées dans le script python joint `script.py`.

Les données relatives à la population sont issues du recensement démographique sur la population et les ménages mené par l'Office Fédéral de la Statistique en 2015 et publié en 2016 : https://www.bfs.admin.ch/bfs/fr/home/actualites/quoi-de-neuf.assetdetail.1442443.html. Ces données sont disponibles à l'hectomètre, ce qui est à ce jour le plus fin niveau d'analyse qui puisse être mis à disposition.

![alt text](https://github.com/nmonach2/VD-SerVis/blob/master/CaptureAppli.JPG)

Copyright © 2019 - Nicolas Monachon
