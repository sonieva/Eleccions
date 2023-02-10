import mysql.connector

path = "Documentació/02201904_MESA/08021904.DAT"
conexion = mysql.connector.connect(
    host='10.94.255.166',
    user="perepi",
    password="pastanaga",
    database="Grup2_eleccions"
)
cursor = conexion.cursor()
insert = ("INSERT INTO vots_candidatures_prov"
          "(provincia_id,candidatura_id,vots,candidats_obtinguts)\n"
          "VALUES ")
try:
    with open(path, "r") as fitxer:
        for linia in fitxer:
            if linia[11:13] != "99":
                candidatura_id = cursor.execute(
                    f"SELECT candidatura_id FROM candidatures WHERE codi_candidatura = '{linia[14:20]}'")
                candidatura_id = cursor.fetchone()
                provincia_id = cursor.execute(
                    f"SELECT provincia_id FROM provincies WHERE codi_ine = '{linia[11:13]}'")
                provincia_id = cursor.fetchone()
                vots = int(linia[20:28])
                candidats_obtinguts = int(linia[28:33])
                insert += f'\t({provincia_id[0]},{candidatura_id[0]},{vots},{candidats_obtinguts}),\n'
except OSError as e:
    print("No s'ha pogut obrir el fitxer " + path)

insert = insert[:-2] + ";"
cursor.execute(insert)
conexion.commit()
cursor.close()
conexion.close()
