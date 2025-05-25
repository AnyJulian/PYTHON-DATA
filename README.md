# Dashboard de suivi de production et de consommation

Ce projet est une application **Dash** permettant de visualiser et d’analyser différentes données industrielles : ventes, niveaux de silos, températures d’air frais, mouvements de stock, blocages/déblocages, etc.  
L’objectif est de fournir un outil interactif pour le suivi de la production, la gestion des stocks et l’optimisation énergétique.

## Fonctionnalités principales

- **Visualisation des ventes** : Histogrammes et séries temporelles des quantités vendues par article.
- **Suivi des niveaux de silos** : Graphiques d’évolution des niveaux de différents silos.
- **Analyse de l’air frais** : Affichage de la température de l’air frais et prédiction du coût énergétique associé.
- **Mouvements de stock** : Visualisation des entrées/sorties de stock par article, avec filtrage par unité (SAC/TO).
- **Blocages et déblocages** : Graphique des mouvements de blocage/déblocage par article et type de mouvement.

## Structure du projet

- `app.py` : Point d’entrée principal, initialise l’application et charge les données.
- `data/` : Traitement et nettoyage des données, connexion à la base.
- `layouts/` : Construction des layouts et des graphiques Plotly.
- `callbacks/` : Callbacks Dash pour l’interactivité.
- `utils/` : Constantes et mappings utiles.

## Librairies principales et justification

- **Dash** : Framework web Python pour créer des dashboards interactifs facilement.
- **Plotly** : Génération de graphiques interactifs et personnalisés.
- **pandas** : Manipulation, nettoyage et agrégation des données tabulaires.
- **scikit-learn** : Modélisation prédictive (régression linéaire pour estimer le coût énergétique en fonction de l’air frais).
    - *Pourquoi ?* Simple à utiliser, efficace pour la régression, bien adapté à des jeux de données industriels.
- **holidays** : Gestion des jours fériés pour exclure ces dates des analyses de séries temporelles.
- **dash-bootstrap-components** : Pour un design moderne et responsive du dashboard.

## Lancement

1. Installer les dépendances
2. Lancer l’application :
3. Ouvrir le navigateur à l’adresse indiquée dans la console (généralement `http://127.0.0.1:8050`).
