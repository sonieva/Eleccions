import mysql.connector
path = "Documentació/02201904_MESA/06021904.DAT"
cnx = mysql.connector.connect(
    host='10.94.255.166',
    user="perepi",
    password="pastanaga",
    database="Grup2_eleccions"
)
cursor = cnx.cursor(buffered=True)
insert = ("INSERT INTO vots_candidatures_mun"
          "(eleccio_id,municipi_id,candidatura_id,vots)\n"
          "VALUES (%s,%s,%s,%s)")
try:
    with open(path, "r") as fitxer:
        for linia in fitxer:
            if linia[14:16] != "99":
                candidatura_id = cursor.execute(
                    f"SELECT candidatura_id FROM candidatures WHERE codi_candidatura = '{linia[16:22]}'")
                candidatura_id = cursor.fetchone()
                municipi_id = cursor.execute(
                    f"SELECT municipi_id FROM municipis WHERE (codi_ine = '{linia[11:14]}') AND (districte = '{linia[14:16]}') AND (provincia_id =  (SELECT provincia_id FROM provincies WHERE codi_ine = '{linia[9:11]}'))")
                municipi_id = cursor.fetchone()
                vots = int(linia[22:30])
                cursor.execute(insert,(1,municipi_id[0],candidatura_id[0],vots))
except OSError as e:
    print("No s'ha pogut obrir el fitxer " + path)

insert = insert[:-2] + ";"
cnx.commit()
cursor.close()
cnx.close()
