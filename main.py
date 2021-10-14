"""
Script d'automatisation réalisé sur Python

1ère étape :
- OU : Ordinateurs
- OU : Utilisateurs
    - Services...
    - Services
- Groupes

2ème étape :

Lister les Services présents dans le CSV
Créer les OU nécessaires :
    Direction
    Service resources Humaines
    Service Comptable
    Service Commercial
    Service Client
    Service IT
    Service Marketing
    Service Logistique
    Service Qualité
    Service Production


3ème étape :
Créer les comptes AD sous forme de [prénom.nom]
option : si doublon que faire ? [prénom1.nom] [prénom2.nom]
Créer un MDP Générique : P@ssw0rd!
Changer le mdp à la première connexion

"""

import csv

# TODO lire un peu la partie typage et hints
from typing import List, Set, Tuple
from dataclasses import dataclass


# from pyad import *

# TODO lire plus a propos des decorateurs en python
@dataclass  # Qu'est ce que c'est ?
class User:
    nom: str
    prenom: str
    telephone: str
    adresse: str
    ville: str
    code_postal: int
    service: str

    def distinguished_name(self, dcs: List[str]) -> str:
        # TODO Finir l'implémentation, utiliser str.join (exemple: ''.join(quelquechoses))
        return f"cn={self.nom}, ou={self.service}, dc"


def get_credentials_from_env():
    # regarderr comment recuperer des env var en python
    # username = ...
    # server = ...
    # password = ...
    return None


def connect_to_ad(credentials):
    # # Connexion au DC_01 du domaine monentreprise.lan
    # pyad.set_defaults(ldap_server="DC_01.monentreprise.lan", username="adm_b.latrille", password="P@ssw0rd!")
    # connection = pyad.set_defaults()
    pass


def setup(ad_connection, default_ous) -> Tuple[bool, str]:
    return False, 'Not implemented'


def extract_services_from_users(users: List[User]) -> Set[str]:
    return set(user.service for user in users)


def init_services(ad_connection, services: Set[str]) -> bool:
    return False


def load_csv(filename: str) -> List[User]:  # La fonction load_csv s'attend à ce que l'argument filename soit de type str et le type de retour sune liste utilisateur décrit comme dans le dataclass
    users = []
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)  # lit les lignes dans un format de dictionnaire
        for row in csv_reader:
            code_postal = int(row['Code Postal'])
            user = User(nom=row['Nom'], prenom=row['Prenom'], telephone=row['Telephone'], adresse=row['Adresse'],
                        ville=row['Ville'], code_postal=code_postal, service=row['Service'])
            users.append(user)  # Ajoute les utilisateurs à la suite
    return users


def init_users(ad_connection, users: List[User]) -> bool:
    return False


# def create_user(user: User) -> bool:  # création user + mdp à changer à la première connexion
#    return False


# services_uniques = set(user.service for user in users) # Permet d'avoir un set de services

# TODO GOOGLE LE IF name == main
if __name__ == '__main__':
    # récupérer le premier argument passé au script comme étant le nom de fichier du csv
    # exemple: python main.py C:\data\user.csv
    # tester que le fichier existe et au'on peut le lire. Sinon, fail fast -> quitter l'execution directement

    ad_credentials = get_credentials_from_env()
    ad_connection = connect_to_ad(ad_credentials)

    default_ous = ["Ordinateurs", "Utilisateurs"]
    setup_success, failure_reason = setup(ad_connection, default_ous)
    if setup_success is False:
        print(f"Erreur lors du setup : {failure_reason}")
        exit(1)

    filename = "resources/Fichier utilisateurs AD - Données.csv"
    users: List[User] = load_csv(filename)

    services: Set[str] = extract_services_from_users(users)
    services_init_success = init_services(ad_connection, services)
    if services_init_success is False:
        print(f"Erreur lors de l'initialisation des services !")
        exit(1)

    users_init_success = init_users(ad_connection, users)
    if services_init_success is False:
        print(f"Erreur lors de l'initialisation des utilisateurs !")
        exit(1)

    print("Le script s'est executé correctement ! =)")
    exit(0)
