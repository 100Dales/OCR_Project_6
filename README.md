# OCR Project 6

This automation script was developed with Python version 3.9.7.

Its objective is to automate the creation of OUs and users on Windows Server OS (2016 and more) from a CSV file.

The spreadsheet need to be like this (you've got an example with randoms 150 users in _resources_ folder) :
[![Image](https://i.goopics.net/2pm8xm.png)](https://goopics.net/i/2pm8xm)

Fields "Nom", "Prenom", "Telephone", "Adresse", "Ville" and "Service" are _strings_.

Field "Code Postal" is an _integer_.

**WARNING** : If your spreadsheet is different, you have to change the source code !

## Install
Lauch your terminal command (_as administrator_).

To install requirements on your terminal command : `pip install -r requirements.txt` 


## Setup and activate environment variables
Setup env vars :
```
LDAP_SERVER
LDAP_USERNAME
LDAP_PASSWORD
```

To load environment if you are under Windows, run on your terminal command (_as administrator_) :
`loadenv.bat` in the folder `Scripts`

To load environment if you are under Linux, run on your terminal command :
`set -o allexport; source .env; set +o allexport`

## Run

To run the main.py follow this sentence :
`python main.py "my/file/path.csv" dc1,dc2`