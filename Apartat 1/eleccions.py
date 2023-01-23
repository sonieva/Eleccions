import sys
import mysql.connector

path = "Documentació/02201904_MESA/01021904.DAT"
cnx = mysql.connector.connect(
    host='10.94.255.166',
    user='perepi',
    password='pastanaga',
    database='Grup2_eleccions')
cursor = cnx.cursor()

try:
    with open(path, "r") as fitxer:
        for linia in fitxer:
            nom = "Eleccions Generals " + linia[2:6]
            anny = linia[2:6]
            mes = linia[6:8]
            
except OSError as e:
    print("No s'ha pogut obrir el fitxer " + path)
