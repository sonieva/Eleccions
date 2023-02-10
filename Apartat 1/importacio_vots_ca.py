import mysql.connector
path= "Documentació/02201904_MESA/08021904.DAT"
conexion = mysql.connector.connect(
    host= '10.94.255.166',
    user="perepi",
    password="pastanaga",
    database="Grup2_eleccions"
)
cursor=conexion.cursor()
insert=("INSERT INTO vots_candidatures_ca"
        "(comunitat_autonoma_id,candidatura_id,vots)\n" 
        "VALUES")
try :
    with open(path, "r") as fitxer:
        for linia in fitxer:
            if linia[9:11] != "99":
                candidatura_id= cursor.execute(
                    f"SELECT candidatura_id FROM candidatures WHERE codi_candidatura = '{linia[14:20]}'"
                )
                candidatura_id = cursor.fetchone()
                comunitat_autonoma_id = cursor.execute(
                        f"SELECT comunitat_aut_id FROM comunitats_autonomes WHERE codi_ine = '{linia[9:11]}'")
                comunitat_autonoma_id = cursor.fetchone()
                vots=int(linia[21:28])
                insert += f'\t({comunitat_autonoma_id[0]},{candidatura_id[0]},{vots}) ,\n'
except OSError as e:
    print("No s'ha pogut obrir el fitxer " + path)

insert=insert.split(" ")
insert[-1] = ";"
insert=" ".join(insert)
cursor.execute(insert)
conexion.commit()
cursor.close()
conexion.close()