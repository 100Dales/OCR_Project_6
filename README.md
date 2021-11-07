# OCR Project 6

This automation script was developed with Python version 3.9.
Its objective is to automate the creation of OUs, users and groups on Windows Server OS from a CSV file.

## Install
`pip install -r requirements` 

## Run

Setup env vars
```
LDAP_SERVER
LDAP_USERNAME
LDAP_PASSWORD
```

If under linux run:
`set -o allexport; source .env; set +o allexport`

and run
`python main.py <users csv> dc1,dc2`

~~brre~~
**gras**
_italique_