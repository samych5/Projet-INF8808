# Application de visualisation de données

Ce projet est une application de visualisation interactive développée avec Dash et Plotly.

## Description générale

L’application utilise **Plotly** pour générer les différents graphiques affichés dans l’interface.
Afin de rendre les transitions plus fluides lors de la navigation, les graphiques non interactifs générés avec Plotly sont convertis en images, puis affichés sous cette forme dans l’application.

Cette approche permet d’éviter de recalculer ou de redessiner les graphiques Plotly à chaque changement d’étape, ce qui améliore la fluidité de l’expérience utilisateur.

## Dépendances

Les dépendances nécessaires au projet se trouvent dans le fichier : `requirements.txt`

Pour les installer :

`pip install -r requirements.txt`

## Lancement de l’application

Le script principal pour lancer l’application en local est :

`python app.py`

L’application est ensuite accessible sur `http://localhost:8050`.

## Génération des images

La génération des images est indépendante du lancement de l’application.

Le script responsable de générer les images est :

`python generate_images.py`

Si un graphique est modifié, il faut relancer ce script afin de régénérer les images utilisées par l’application.

## Structure du projet

Chaque graphique possède son propre dossier dans le dossier `graphs`.

Chaque dossier de graphique gère l’affichage et la génération du graphique correspondant. Il contient au minimum :

- `template.py` : définit la structure d’affichage du graphique dans l’application
- `graph.py` : contient le code responsable de générer le graphique avec Plotly

Le fichier `template.py` principal de l’application appelle les différents fichiers `template.py` présents dans les dossiers de graphiques.
