import mysql.connector
import sys

path = "Documentació/02201904_MESA/04021904.DAT"
conexion = mysql.connector.connect(
    host='10.94.255.166',
    user="perepi",
    password="pastanaga",
    database="Grup2_eleccions"
)
cursor = conexion.cursor()
insert = ("INSERT INTO candidats"
          "(candidatura_id,persona_id,provincia_id,num_ordre,tipus)\n"
          "VALUES")
noms = []
try:
    with open(path, "r") as fitxer:
        for linia in fitxer:
            if linia[9:11] != "99":
                provincia_id = cursor.execute(
                    f"SELECT provincia_id FROM provincies WHERE codi_ine = '{linia[9:11]}'"
                )
                provincia_id = cursor.fetchone()
                candidatura_id = cursor.execute(
                    f"SELECT candidatura_id FROM candidatures WHERE codi_candidatura = '{linia[15:21]}'"
                )
                candidatura_id = cursor.fetchone()
                nom = linia[25:50].strip()
                cog1 = linia[50:75].strip()
                cog2 = linia[75:100].strip()
                nom_complet = f"{nom} {cog1} {cog2}"
                noms.append(nom_complet)
                if noms.count(nom_complet) >= 2:
                    desc = 'SELECT persona_id FROM persones WHERE (nom = %s) AND (cog1 = %s) AND (cog2 = %s) ORDER BY persona_id DESC LIMIT 1'
                    persona_id = cursor.execute(desc,(nom,cog1,cog2))
                else:
                    asc = 'SELECT persona_id FROM persones WHERE (nom = %s) AND (cog1 = %s) AND (cog2 = %s) ORDER BY persona_id ASC LIMIT 1'
                    persona_id = cursor.execute(asc, (nom, cog1, cog2))
                persona_id = cursor.fetchone()
                num_ordre = int(linia[21:24])
                tipus = linia[24:25]
                insert += f"\t({candidatura_id[0]},{persona_id[0]},{provincia_id[0]},{num_ordre},'{tipus}'),\n"
except OSError as e:
    print("No s'ha pogut obrir el fitxer " + path)

insert = insert[:-2] + ";"
cursor.execute(insert)
conexion.commit()
cursor.close()
conexion.close()
