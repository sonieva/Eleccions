import mysql.connector

path = "Documentació/02201904_MESA/05021904.DAT"
cnx = mysql.connector.connect(
    host='10.94.255.166',
    user="perepi",
    password="pastanaga",
    database="Grup2_eleccions"
)
cursor = cnx.cursor()
insert = ("INSERT INTO municipis"
          "(codi_ine,districte,nom,provincia_id)\n"
          "VALUES")
try:
    with open(path, "r") as fitxer:
        for linia in fitxer:
            provincia_id = cursor.execute(f"SELECT provincia_id FROM provincies WHERE codi_ine = '{linia[11:13]}'")
            provincia_id = cursor.fetchone()
            codi_ine = linia[13:16]
            if linia[16:18] == "99":
                nom = " ".join(linia[18:118].split())
                insert += f'\t("{codi_ine}","{nom}",{provincia_id[0]}) ,\n'
            else:
                districte = " ".join(linia[18:118].split())
                insert += f'\t("{codi_ine}","{districte}",{provincia_id[0]}) ,\n'
            
except OSError as e:
    print("No s'ha pogut obrir el fitxer " + path)

insert = insert[:-2] + ";"
print(insert)