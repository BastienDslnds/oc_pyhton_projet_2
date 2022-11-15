# Titre du projet

Programme permettant la gestion de tournois d'échecs suisses.

## Description

Le projet a pour but de :
* gérer le déroulement d'un tournoi
* générer des rapports
* sauvegarder/charger les données d'un tournoi

Le déroulement d'un tournoi est le suivant:
* Créer un nouveau tournoi
* Ajouter huit joueurs
* Générer des paires de joueurs chaque tour
* Lorsque le tour est terminé, saisir les résultats
* Répéter jusquà la fin du tournoi

Les rapports sont:
* Liste de tous les acteurs :
    * par ordre alphabétique ;
    * par classement.
* Liste de tous les joueurs d'un tournoi :
    * par ordre alphabétique ;
    * par classement.
* Liste de tous les tournois.
* Liste de tous les tours d'un tournoi.
* Liste de tous les matchs d'un tournoi.


## Se préparer à commencer

### Dépendances

* installer Windows, version 10.0.19043
* installer Python 3.10

### Installation

* git clone https://github.com/BastienDslnds/oc_python_projet_4.git
* Créer et activer l'environnement virtuel 
  * 1- ouvrir l'application "invite de commande"
  * 2- se positionner dans le dossier "oc_python_projet_4" contenant le fichier requirements.txt
  * 3- créer l'environnement virtuel avec: "python -m venv env"
  * 4- Activer l'environnement virtuel:
    * se positionner dans le dosser Scripts: "cd env/Scripts"
    * activer l'environnement: "source activate"
  * 5- utiliser la commande suivante pour installer les packages: "pip install -r requirements.txt"

### Executer le programme

* Se positionner dans le dossier "oc_python_projet_4"
* Utiliser la commande "python main.py"
* Un menu d'actions possibles va s'afficher

### Générer un nouveau fichier flake8-html

* Se positionner dans le dossier "oc_python_projet_4"
* Utiliser la commande "flake8 --format=html --htmldir=flake-report --exclude=env --max-line-length=119"
* Un dossier flake-report sera généré avec un fichier "index.html"

## Auteurs

Bastien Deslandes

bastien.deslandes@free.fr