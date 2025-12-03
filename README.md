# Hackathon Météo France

Projet réalisé dans le cadre du Hackathon Météo France 2025 - Le climat en données 

## Défi

Visualisation des données : Représenter les données climatiques pour faciliter leur compréhension et leur appropriation

Il s’agira de proposer des formats pertinents de visualisation des données climatiques, seules ou croisées avec d’autres jeux de données non climatiques, pensés pour des publics comme des décideurs publics, des citoyens, des acteurs territoriaux, des professionnels, etc. Il faudra notamment veiller à intégrer visuellement l’incertitude climatique de manière lisible.


## Solution proposée 

Dans ce projet, nous souhaitons nous concentrer sur l'évolution de l'isotherme zéro dans la région alpine, ainsi que la fréquence d'apparition de nuits tropicales. 

### Zone d'étude 

La zone d'étude comprend les départements suivants:
* Alpes-de-Haute-Provence (04)
* Hautes-Alpes (05)
* Alpes-Maritimes (06)
* Drôme (26)
* Isère (38)
* Savoie (73)
* Haute-Savoie (74)
* Vaucluse (84)

### Approche adopée 

#### 1) Extraction et nettoyage des données
La première étape essentielle consiste à définir les données utilisées pour ce défi. Nous souhaitons nous concentrer sur les informations liées à la température dans la région alpine (définie ci-dessus) 
Nous utilisons donc le jeu de données ``pour le ESMS2-1 ALPX3 2,5km```. Le choix d'une telle résolution nous permet d'avoir une anlayse plus fine pour la région étudiée. 

#### 2) Calcul des indicateurs
Nous souhaitons mettre en avant deux indicateurs : l'isotherme zéro et la fréquence d'apparition de nuits tropicales. 
#### Isotherme zéro
Valeurs calculées : 
- Nombre de jours où la température moyenne est supérieure à 0 (Tmean > 0) par année et par hiver, avec hiver={décembre, janvier, février} pour les données de projection
- Moyenne, maximium et minimum du nombre de jours par plage de 20 ans pour les données de projection
- Nombre de jours où la température moyenne est supérieure à 0 (Tmean > 0) par année et par hiver, avec hiver={décembre, janvier, février} pour les données historiques
- Moyenne, maximium et minimum du nombre de jours par plage de 20 ans pour les données historiques 
- Différences entre valeurs calculées pour les données historiques (moyenne, maximum et minimum) et les valeurs calculées pour chaque horizons de temps des données de projection (moyenne, maximum, minimum) 

En calculant la moyenne, valeur minimale et valeur maximale on obtient trois scénarios : hiver moyen, hiver "chaud", et hiver "froid". 

#### Nuits tropicales

Une nuit tropicale est définie comme une nuit lors de laquelle la température ne descend pas en-dessous de 20°C.

Valeurs calculées : 
- Nombre de jours où la température minimale est supérieure à 20 (Tmin > 20) par année pour les données de projection
- Moyenne, maximium et minimum du nombre de jours où la température minimale est supérieure à 20 (Tmin < 20) sur toutes les années par plage de 20 ans pour les données de projection
- Nombre de jours où la température minimale est supérieure à 20 (Tmin > 20) par année pour les données historiques
- Moyenne, maximium et minimum du nombre de jours où la température minimale est supérieure à 20 (Tmin > 20) sur toutes les années par plage de 20 ans pour les données de projection 
- Différences entre valeurs calculées pour les données historiques (moyenne, maximum et minimum) et les valeurs calculées pour chaque horizons de temps des données de projection (moyenne, maximum, minimum) 

Nous nous basons sur la température minimale pour déterminer s'il y a présence de nuit tropicale ou non car la température minimale est souvent atteinte durant la nuit.
En calculant la moyenne, valeur minimale et valeur maximale on obtient trois scénarios à nouveau : moyenne, "chaud" et "froid". 


#### 3) Création du dashboard

Avec ce dashboard, nous souhaitons vulgariser les données afin de les rendre compréhensibles pour le plus grand nombre. 
Dessus, on peut retrouver : 
- la prévision de l'évolution de la fréquence de nuits tropicales
- la prévision de l'évolution de l'isotherme zéro dans le temps 


## Pré-requis
 TODO

## Installation

Cloner le dépôt à l'emplacement de votre choix: <br>
```git clone https://github.com/justinesommerlatt/Hackathon-Meteo-France``` <br>
```cd Hackathon-Meteo-France``` <br>

Installer les dépendances : <br>
```pip install -r requirements.txt```

## Démarrage

### Informations sur les défirents fichiers 
```cretes.py``` génère des sorties dans le dossier ```crete_animations```. Les sorties sont des schémas par intervalles de temps montrant la position de l'isotherme zéro dans une région donnée, ainsi qu'une vidéo d'animation montrant l'évolution. 

```cretes_plotly.py``` génère les mêmes sorties que ```cretes.py``` mais au format plotly, dans le dossier ```crete_animations_plotly```. Les sorties sont des schémas par intervalles de temps montrant la position de l'isotherme zéro dans une région donnée, ainsi qu'une vidéo d'animation montrant l'évolution. 


### Données utilisées 
TODO 

### Outils utilisés
TODO



### Auteurs

* Julien AVINÉE 
* Madeleine D'ARRENTIERES  
* Maëlle ABRAHAM 
* Etienne PAUTHENET  
* Lucio LURASCHI  
* Sandrine PARADOWSKI  
* Romuald WEIDMANN  
* Justine SOMMERLATT  

