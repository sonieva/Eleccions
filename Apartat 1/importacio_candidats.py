import mysql.connector
import sys
path= "Documentació/02201904_MESA/04021904.DAT"
conexion = mysql.connector.connect(
    host='10.94.255.166',
    user="perepi",
    password="pastanaga",
    database="Grup2_eleccions"
)
cursor=conexion.cursor()
insert=("INSERT INTO candidats"
        "(candidatura_id,num_ordre,tipus)\n" 
        "VALUES")
try :
    with open(path, "r") as fitxer:
        for linia in fitxer:
            candidatura_id=linia[15:21]
            num_ordre=linia[21:24]
            tipus=linia[24:25]
            insert += f'\t({candidatura_id},{num_ordre},"{tipus}") ,\n'
except OSError as e:
    print("No s'ha pogut obrir el fitxer " + path)

insert=insert.split(" ")
insert[-1] = ";"
insert=" ".join(insert)
cursor.execute(insert)
conexion.commit()
cursor.close()
conexion.close()