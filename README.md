# OCR Project 6

This automation script was developed with Python version 3.9.7.

Its objective is to automate the creation of OUs and users on Windows Server OS (2016 and more) from a CSV file.

## Install

Install requirements on CMD : `pip install -r requirements.txt` 

## Run

Setup env vars
```
LDAP_SERVER
LDAP_USERNAME
LDAP_PASSWORD
```

To load environment if you are under Windows, run:
`set -o allexport; source .env; set +o allexport`

and run
`python main.py "resources\Fichier utilisateurs AD - Donnees.csv" dc1,dc2`

~~brre~~
**gras**
_italique_