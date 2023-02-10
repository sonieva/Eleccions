import mysql.connector

path= "Documentació/02201904_MESA/07021904.DAT"
cnx = mysql.connector.connect(
    host='10.94.255.166',
    user="perepi",
    password="pastanaga",
    database="Grup2_eleccions"
)
cursor=cnx.cursor()
insert=("INSERT INTO comunitats_autonomes"
        "(codi_ine,nom)\n" 
        "VALUES")
try :
    with open(path, "r") as fitxer:
        for linia in fitxer:
            if linia[11:13] == "99":
                if linia[9:11] != "99":
                    codi_ine = linia[9:11]
                    nom = " ".join(linia[14:64].split())
                    insert += f'\t("{codi_ine}","{nom}") ,\n'
except OSError as e:
    print("No s'ha pogut obrir el fitxer " + path)

insert = insert[:-2] + ";"
cursor.execute(insert)
cnx.commit()
cursor.close()
cnx.close()
