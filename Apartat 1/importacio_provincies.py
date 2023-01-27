import mysql.connector

path = "Documentació/02201904_MESA/07021904.DAT"
cnx = mysql.connector.connect(
    host='10.94.255.166',
    user="perepi",
    password="pastanaga",
    database="Grup2_eleccions"
)
cursor = cnx.cursor()
insert = ("INSERT INTO provincies"
          "(comunitat_aut_id,nom,codi_ine,num_escons)\n"
          "VALUES")
try:
    with open(path, "r") as fitxer:
        for linia in fitxer:
            if linia[11:13] != "99":
                comunitat_aut_id = cursor.execute(
                    f"SELECT comunitat_aut_id FROM comunitats_autonomes WHERE codi_ine = '{linia[9:11]}'")
                comunitat_aut_id = cursor.fetchone()
                nom = " ".join(linia[14:64].split())
                codi_ine = linia[11:13]
                escons = int(linia[149:155])
                insert += f'\t({comunitat_aut_id[0]},"{nom}","{codi_ine}",{escons}),\n'
except OSError as e:
    print("No s'ha pogut obrir el fitxer " + path)

insert = insert[:-2] + ";"
cursor.execute(insert)
cnx.commit()
cursor.close()
cnx.close()
