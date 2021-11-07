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

from typing import List, Set, Tuple, Any, Optional
from dataclasses import dataclass


# from pyad import *
# from pyad.adobject import *


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

    def common_name(self) -> str:
        return f"{self.prenom.lower().strip()}.{self.nom.lower().strip()}"

    def distinguished_name(self, dcs: List[str]) -> str:
        dn_fragment = f"cn={self.common_name()}, ou={self.service}"
        formatted_dcs: List[str] = [f"dc={dc}" for dc in dcs]
        dcs_fragment: str = ', '.join(formatted_dcs)
        return f"{dn_fragment}, {dcs_fragment}"


# TODO Installer le package python-dotenv mais bug de python package
def get_credentials_from_env() -> Optional[str]:  # valider les entrées de .env
    server = os.getenv('LDAP_SERVER')
    username = os.getenv('LDAP_USERNAME')
    password = os.getenv('LDAP_PASSWORD')

    # Test if any of the username, password or server value is missing or empty
    # If any value is invalid, then do not connect and return None
    is_value_invalid = lambda value: value is None or value == ''
    if any(is_value_invalid(value) for value in [server, username, password]):
        return None
    else:
        connection_string = f"ldap_server={server}, username={username}, password={password}"
        print(f"Found AD credentials: {connection_string}")
        return connection_string


def connect_to_ad(connection_string) -> bool:
    # The PYAD documentation could be found : https: // zakird.github.io / pyad / pyad.html  # basic-object-manipulation
    # connection = pyad.set_defaults(ad_credentials)
    is_success = True
    try:
        print(f"Connecting to AD using: {connection_string}")
    except Exception as e:
        print(f"Unable to connect to AD: {e}")
        is_success = False
    return is_success


def create_organisational_units(ad_connection,
                                organisational_units: List[str],
                                parent: Optional[str] = None) -> Tuple[bool, str]:
    # Pb je dois me référer à une OU de base mais je ne connais pas son nom
    is_success = True
    reason = ""
    print(f"Creating Organisational Units: {', '.join(organisational_units)}")
    if parent is not None:
        print(f"Under the parent={parent}")

    for unit in organisational_units:
        if parent is not None:
            unit_name = f"{parent}/{unit}"
        else:
            unit_name = unit
        # Pour ton information, la meme chose version Ternaire (ternary expression)
        # unit_name = f"{parent}/{unit}" if parent is not None else unit
        try:
            # Create UNIT on AD
            # create_ou_workstation = pyad.adcontainer.ADContainer.create_container(ou, Ordinateurs)
            print(f"\tCreating unit={unit_name}")  # Modifier avec PYAD
        except Exception as e:
            print(f"Something bad happened: {e}")
            reason = str(e)
            is_success = False
    return is_success, reason


# La fonction load_csv s'attend à ce que l'argument filename soit de type str et le type de retour sune liste utilisateur décrit comme dans le dataclass
def load_csv(filename: str) -> List[User]:
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


def create_users(ad_connection, users: List[User], dcs: List[str]) -> Tuple[bool, str]:
    is_success = True
    reason = ""
    for user in users:
        try:
            # Create User
            # created_user = pyad.adcontainer.ADContainer.create_container(ou, Ordinateurs) TODO Replace me
            print(f"Creating user: {user.distinguished_name(dcs)}")
        except Exception as e:
            print(f"Something bad happend for {user}: {e}")
            reason = str(e)
            is_success = False
    return is_success, reason


USERS_OU = "Utilisateurs"
DEVICES_OU = "Ordinateurs"
DEFAULT_OUS = [DEVICES_OU, USERS_OU]


def fail(error_message: str, code: int = 1):
    print(error_message)
    print("Usage : ...")
    exit(code)


# TODO GOOGLE LE IF name == main
if __name__ == '__main__':
    # Parse Command line arguments
    users_csv_filepath, dcs = None, None
    if len(sys.argv) > 1:
        # récupérer le premier argument passé au script comme étant le nom de fichier du csv
        users_csv_filepath = sys.argv[1]
        # sys.argv est une string qui devient une liste de string séparé (split) par des virgules
        dcs = sys.argv[2].split(',')
    else:
        fail(f"Erreur : la liste d'arguement doit être au moins de taille 2.")

    # Ensure that we can load the users file
    if not os.path.exists(users_csv_filepath):
        fail(f"Erreur : le chemin du fichier n'est pas valide, "
             f"veuillez mettre en premier argument le chemin du fichier csv.")
    if not os.access(users_csv_filepath, os.R_OK):
        fail(f"Erreur : le fichier n'est pas accessible en lecture.")

    # Setup AD connection
    ad_connection_string = get_credentials_from_env()
    if ad_connection_string is None:
        fail("Error : missing AD credentials (check your env vars)")

    # if connection fails, what do???
    ad_connection = connect_to_ad(ad_connection_string)

    # Create Organisation Units (OU)
    setup_success, failure_reason = create_organisational_units(ad_connection, DEFAULT_OUS)
    if setup_success is False:
        fail(f"Erreur lors du setup : {failure_reason}")

    # Load users and services from external file
    users: List[User] = load_csv(users_csv_filepath)  # A revoir
    services: Set[str] = extract_services_from_users(users)

    # Create entities in AD
    services_init_success, services_error_message = create_organisational_units(
        ad_connection, list(services), parent=USERS_OU
    )
    if services_init_success is False:
        fail(f"Erreur lors de l'initialisation des services: {services_error_message} !")

    users_init_success, user_error_message = create_users(ad_connection, users, dcs)
    if services_init_success is False:
        fail(f"Erreur lors de l'initialisation des utilisateurs: {user_error_message} !")

    print("Le script s'est executé correctement ! =)")
    exit(0)
