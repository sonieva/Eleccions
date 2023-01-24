import mysql.connector
import sys
path= "Documentació/02201904_MESA/06021904.DAT"
conexion = mysql.connector.connect(
    host= '10.94.255.166',
    user="perepi",
    password="pastanaga",
    database="Grup2_eleccions"
)
cursor=conexion.cursor()
insert=("INSERT INTO vots_candidatures_mun"
        "(eleccio_id,vots)\n" 
        "VALUES")
try :
    with open(path, "r") as fitxer:
        for linia in fitxer:
            vots=linia[22:30]
            insert += f'\t(1,{vots}) ,\n'
except OSError as e:
    print("No s'ha pogut obrir el fitxer " + path)

insert=insert.split(" ")
insert[-1] = ";"
insert=" ".join(insert)
cursor.execute(insert)
conexion.commit()
cursor.close()
conexion.close()