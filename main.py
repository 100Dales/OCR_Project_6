"""
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
Créer les comptes AD pour chaque utilisateurs
Créer un MDP Générique : P@ssw0rd!
Changer le mdp à la première connexion
"""

import sys
import csv
import os
import os.path
# import pypiwin32

from typing import List, Set, Tuple, Any
from dataclasses import dataclass
from dotenv import load_dotenv
from pyad import *
from pyad.adobject import *

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
        distinguished_name_composition = [self.nom, self.service] + dcs
        return ', '.join(distinguished_name_composition)

# TODO Installer le package python-dotenv mais bug de python package
def get_credentials_from_env() -> str: # valider les entrées de .env
    load_dotenv()
    AD_LDAP_SERVER = os.getenv(MY_AD_LDAP_SERVER)
    AD_USERNAME = os.getenv(MY_USERNAME)
    AD_PASSWORD = os.getenv(MY_PASSWORD)

    if load_dotenv() is False:
        AD_LDAP_SERVER = input("Quel est votre nom de serveur AD(FQDN) ?")
        AD_USERNAME = input("Quel est votre nom de compte AD ?")
        AD_PASSWORD = input("Quel est votre mot de passe ?")

    credentials_name_composition = f"ldap_server={AD_LDAP_SERVER}, username={AD_USERNAME}, password={AD_PASSWORD}"
    return credentials_name_composition


def connect_to_ad(ad_credentials) -> bool:
    # The PYAD documentation could be found : https: // zakird.github.io / pyad / pyad.html  # basic-object-manipulation
    connection = pyad.set_defaults(ad_credentials)
    return connection


def setup(ad_connection, default_ous) -> Tuple[bool, str]: # Pb je dois me référer à une OU de base mais je ne connais pas son nom
    create_ou_user = pyad.adcontainer.ADContainer.create_container(ou, Utilisateurs)
    create_ou_workstation = pyad.adcontainer.ADContainer.create_container(ou, Ordinateurs)
    return True, 'Le setup des OUs a été réalisé


def load_csv(filename: str) -> List[User]:  # La fonction load_csv s'attend à ce que l'argument filename soit de type str et le type de retour sune liste utilisateur décrit comme dans le dataclass
    users = []
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)  # lit les lignes dans un format de dictionnaire
        for row in csv_reader:
            code_postal = int(row['Code Postal'])
            user = User(nom=row['Nom'], prenom=row['Prenom'], telephone=row['Telephone'], adresse=row['Adresse'],
                        ville=row['Ville'], code_postal=code_postal, service=row['Service'])
            users.append(user)  # Ajoute les utilisateurs les uns à la suite des autres
    return users


def extract_services_from_users(users: List[User]) -> Set[str]:
    services_list = set(user.service for user in users)  # Permet d'avoir un set de services
    return services_list


def init_services(ad_connection, services: Set[str]) -> bool:
    return services_list


def init_users(ad_connection, users: List[User]) -> bool:
    return False


# TODO GOOGLE LE IF name == main
if __name__ == '__main__':

    if len(sys.argv) > 1:
        csv_user_file = sys.argv[1] # récupérer le premier argument passé au script comme étant le nom de fichier du csv
        dcs = sys.argv[2].split(',') # sys.argv est une string qui devient une liste de string séparé (split) par des virgules
    else:
        print(f"Erreur : la liste d'arguement doit être au moins de taille 2.")
        exit(1)
    if os.path.exists(csv_user_file) is False:
        print(f"Erreur : le chemin du fichier n'est pas valide, veuillez mettre en premier argument le chemin du fichier csv.")
        exit(1)
    if os.access(csv_user_file, os.R_OK) is False:
        print(f"Erreur : le fichier n'est pas accessible en lecture.")
        exit(1)

    ad_credentials = get_credentials_from_env()
    ad_connection = connect_to_ad(ad_credentials)

    default_ous = ["Ordinateurs", "Utilisateurs"]
    setup_success, failure_reason = setup(ad_connection, default_ous)
    if setup_success is False:
        print(f"Erreur lors du setup : {failure_reason}")
        exit(1)

    filename = "resources/Fichier utilisateurs AD - Données.csv"
    users: List[User] = load_csv(filename) # A revoir

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
