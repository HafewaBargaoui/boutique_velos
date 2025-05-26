
# Boutique Vélos

Bienvenue dans le projet **Boutique Vélos** !  
Cette application web permet de gérer une boutique de vélos grâce à une interface simple et interactive.

## Description

Boutique Vélos est une application développée avec **Streamlit**, qui permet de consulter et gérer un catalogue de vélos.  
Elle offre une interface intuitive pour afficher les vélos disponibles et effectuer diverses opérations liées à la gestion du stock.

## Installation

1. Clonez ce dépôt :
```bash
git clone https://github.com/HafewaBargaoui/boutique_velos.git
cd boutique_velos
```

2. (Optionnel) Créez un environnement virtuel :
```bash
python -m venv env
source env/bin/activate  # Sur Windows : env\Scripts\activate
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Lancement de l'application

Pour démarrer l'application, lancez la commande suivante :

```bash
streamlit run main.py
```

Puis ouvrez votre navigateur à l'adresse indiquée (généralement `http://localhost:8501`).

# Structure du projet

Voici la structure principale du projet :

```
boutique_velos/
│
├── main.py                
├── requirements.txt       # Liste des dépendances Python
├── README.md              # Documentation du projet
├── databases              # Contient la base de données
├── assets/                # Contient les images pour enrichir le site
├── utils/                 # Contient le style à appliquer aux différentes pas de l'application
└── models                 # Contient les constructeurs des objets
└── pages                  # Contient les pages qui s'affichent en front
└── scripts                # Contient les scripts utiles au projet, comme la création de la bdd
└── services               # Contient les méthodes pour manipuler les objets
```

## Contribuer

Les contributions sont les bienvenues !  
N'hésitez pas à forker ce dépôt, faire vos modifications, puis proposer une Pull Request.

## Licence

Ce projet est sous licence **MIT**.  
Merci de contacter l'auteur pour plus d'informations.