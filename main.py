
import sys
import csv
import os
import os.path

from typing import List, Set, Tuple, Any, Optional, Dict
from dataclasses import dataclass
from pyad import pyad_setdefaults

from pyad.adobject import *


@dataclass
class User:
    nom: str
    prenom: str
    telephone: str
    adresse: str
    ville: str
    code_postal: int
    service: str

    def common_name(self) -> str:
        return f"{self.prenom.lower().strip()}.{self.nom.lower().strip()}" # Put in lowercase and without spaces


    def distinguished_name(self, dcs: List[str]) -> str:
        dn_fragment = f"cn={self.common_name()}, ou={self.service}"
        formatted_dcs: List[str] = [f"dc={dc}" for dc in dcs]
        dcs_fragment: str = ', '.join(formatted_dcs)
        return f"{dn_fragment}, {dcs_fragment}"


def get_credentials_from_env() -> Optional[Dict[str, str]]:
    connection_infos = {
        'ldap_server': os.getenv('LDAP_SERVER'),
        'username': os.getenv('LDAP_USERNAME'),
        'password': os.getenv('LDAP_PASSWORD')
    }
    connection_infos = {k: v for k, v in connection_infos.items() if v is not None}
    print(f"AD credentials: {connection_infos}")
    if len(connection_infos) != 3:
        return None

    # Note: if too long to wait for timeout, exit here
    if len(connection_infos) > 0:
        pyad_setdefaults(**connection_infos)
    return connection_infos


def connect_to_ad(connection_infos: Dict[str, str]) -> bool:
    # This runs a connection with the current user credentials
    print(f"Connecting to AD using: {connection_infos}")
    try:
        from pyad import pyad
        return True
    except Exception as e:
        print(f'Error while connecting to ad: {e}')
    return False


def create_organisational_units(organisational_units: List[str]) -> Tuple[bool, str]:
    # The PYAD documentation could be found : https: // zakird.github.io / pyad / pyad.html  # basic-object-manipulation
    from pyad import pyad
    is_success = True
    reason = ""
    formatted_dcs: List[str] = [f"DC={dc}" for dc in dcs]
    dcs_string = ','.join(formatted_dcs)
    for unit in organisational_units:
        organisational_unit = pyad.adcontainer.ADContainer.from_dn(
            f"ou={USERS_OU},{dcs_string}")
        try:
            # Create Organisational Units on AD
            print(f"Creating Organisational Unit : {unit}")
            pyad.adcontainer.ADContainer.create_container(organisational_unit, unit)
        except Exception as e:
            print(f"Something wrong happend for {organisational_unit} : {e}")
            print(f"Something wrong happend for {unit} : {e}")
            reason = str(e)
            is_success = False
    return is_success, reason


def load_csv(filename: str) -> List[User]:
    users = []
    # Open CSV file and read it as dictionnary
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            code_postal = int(row['Code Postal'])
            user = User(nom=row['Nom'], prenom=row['Prenom'], telephone=row['Telephone'], adresse=row['Adresse'],
                        ville=row['Ville'], code_postal=code_postal, service=row['Service'])
            users.append(user)  # Add the user after the others
    return users


def extract_services_from_users(users: List[User]) -> Set[str]:
    services_list = set(user.service for user in users)  # Have a set of services
    return services_list


def create_users(users: List[User], dcs: List[str]) -> Tuple[bool, str]:
    # The PYAD documentation could be found : https: // zakird.github.io / pyad / pyad.html  # basic-object-manipulation
    from pyad import pyad
    is_success = True
    reason = ""
    formatted_dcs: List[str] = [f"DC={dc}" for dc in dcs]
    dcs_string = ','.join(formatted_dcs)
    for user in users:
        organisational_unit = pyad.adcontainer.ADContainer.from_dn(
            f"OU={user.service},OU={USERS_OU},{dcs_string}")
        try:
            # Create User by service
            print(f"Creating user : {user.distinguished_name(dcs)}")
            ad_user = pyad.aduser.ADUser.create(user.common_name(), organisational_unit, password="P@ssw0rd!", enable=True)
            # Change password at the first connection
            # Best Practice : the password should be randomly generated, stored and sent to the user
            ad_user.force_pwd_change_on_login()
        except Exception as e:
            print(f"Something wrong happend for {organisational_unit} : {e}")
            print(f"Something wrong happend for {user} : {e}")
            reason = str(e)
            is_success = False
    return is_success, reason


def fail(error_message: str, code: int = 1):
    print(error_message)
    exit(code)


USERS_OU = "Utilisateurs"


if __name__ == '__main__':
    # Parse Command line arguments
    users_csv_filepath, dcs = None, None
    if len(sys.argv) > 1:
        # get the first argument passed to the script as being the csv file name
        users_csv_filepath = sys.argv[1]
        # sys.argv is a string which becomes a comma separated (split) string list
        dcs = sys.argv[2].split(',')
    else:
        fail(f"Error : the argument list must be at least size 2.")

    # Ensure that we can load and read the csv file
    if not os.path.exists(users_csv_filepath):
        fail(f"Error : the file path is not valid, please put the path of the csv file as the first argument.")
    if not os.access(users_csv_filepath, os.R_OK):
        fail(f"Error : the file is not readable.")

    # Setup AD connection
    ad_connection_infos = get_credentials_from_env()
    if ad_connection_infos is None:
        fail("Error : missing AD credentials (check your env vars)")

    # Connection to Active Directory
    is_connected = connect_to_ad(ad_connection_infos)
    if is_connected is None:
        fail("Unable to connect to AD")

    # Load users and services from external file
    users: List[User] = load_csv(users_csv_filepath)
    services: Set[str] = extract_services_from_users(users)

    # Create Organisation Units (OU) in Active Directory
    services_init_success, services_error_message = create_organisational_units(list(services))
    if services_init_success is False:
        fail(f"Error initializing services : {services_error_message} !")

    # Create users by OUs in Active Directory
    users_init_success, user_error_message = create_users(users, dcs)
    if services_init_success is False:
        fail(f"Error initializing users : {user_error_message} !")

    print("The script executed correctly ! =)")
    exit(0)
