"""
Script d'automatisation réalisé sur Python

1ère étape :
(???) Installer un package pour avoir des fonctionnalités liées à Windows Server (???)
Générer un fichier requirements.txt

ouvrir le fichier :
    fichier = open("chemin du fichier", mode d'ouverture)
        différents modes d'ouverture :
            r (lire)
            w (écrire/écraser)
            a (continuer d'écrire)
            r+ (lire et écrire/écraser)


2ème étape :

Lister les Services présents dans le CSV
Créer les OU nécessaires :
    Direction
    Service Ressources Humaines
    Service Comptable
    Service Commercial
    Service Client
    Service IT
    Service Marketing
    Service Logistique
    Service Qualité
    Service Production


4ème étape :
Créer les comptes AD sous forme de [prénom.nom]
option : si doublon que faire ? [prénom1.nom] [prénom2.nom]

5ème étape :
Créer un MDP Générique : P@ssw0rd!
Changer le mdp à la première connexion

"""

import csv

with open(r'C:\Users\latri\Documents\Fichier utilisateurs AD - Données.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file)  # lit les lignes dans un format de dictionnaire
    next(csv_reader)  # Permet d'enlever le header du CSV


def create_ou(): # On définit la fonction créer une OU
    with open(r'C:\Users\latri\Documents\Fichier utilisateurs AD - Données.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)  # lit les lignes dans un format de dictionnaire
        next(csv_reader)  # Permet d'enlever le header du CSV
        for row in csv_reader:
            service = row['Service']
            # Sinon j'avais pensé à faire " pour chaque service présent dans la colonne "service", créer une OU. Si OU déjà créée alors ne rien faire.
            if service = "Direction"
                # create OU
            elif service = "Service Client"
                # create OU
            elif service = "Service Commercial"
                # create OU
            elif service = "Service Comptable"
            elif service = "Service IT"
            elif service = "Service Logistique"
            elif service = "Service Marketing"
            elif service = "Service Production"
            elif service = "Service Qualite"
            elif service = "Service Ressources Humaines"
                print(service)
    pass

def create_user(): # création user + mdp à changer à la première connexion
    with open(r'C:\Users\latri\Documents\Fichier utilisateurs AD - Données.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)  # lit les lignes dans un format de dictionnaire
        next(csv_reader)  # Permet d'enlever le header du CSV
        for row in csv_reader:
            nom = row['Nom']
            prenom = row['Prenom']
            telephone = row['Telephone']
            adresse = row['Adresse']
            ville = row['Ville']
            code_postal = row['Code Postal']
    pass


#csv = open_csv()
open_services = import_service()
