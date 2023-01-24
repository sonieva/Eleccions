import mysql.connector

path = "Documentació/02201904_MESA/04021904.DAT"
cnx = mysql.connector.connect(
    host='10.94.255.166',
    user='perepi',
    password='pastanaga',
    database='Grup2_eleccions')
cursor = cnx.cursor()

insert = ("INSERT INTO persones "
          "(nom,cog1,cog2,sexe,dni)\n"
          "VALUES")

try:
    with open(path, "r") as fitxer:
        for linia in fitxer:
            #codi = linia[8:14]
            pri_nom = " ".join(linia[25:49].split()).replace("'", '\\'+"'")
            pri_cog = " ".join(linia[50:74].split())
            seg_cog = " ".join(linia[75:99].split()).replace('"','\\'+'"')
            sexe = linia[100:101]
            dni =  " "" ".join(linia[109:119].split()).replace('','')
            insert += f"\t('{pri_nom}','{pri_cog}','{seg_cog}','{sexe}','{dni}') ,\n"
except OSError as e:
    print("No s'ha pogut obrir el fitxer " + path)

insert=insert.split(" ")
insert[-1] = ";"
insert=" ".join(insert)
#print(insert)
cursor.execute(insert)
cnx.commit()
cursor.close()
cnx.close()