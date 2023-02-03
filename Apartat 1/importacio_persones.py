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
          "VALUES (%s,%s,%s,%s,%s)")

try:
    with open(path, "r") as fitxer:
        for linia in fitxer:
            #codi = linia[8:14]
            pri_nom = linia[25:49].strip()
            pri_cog = linia[50:74].strip()
            seg_cog = linia[75:99].strip()
            sexe = linia[100:101]
            dni =  linia[109:119].strip()
            if dni == "":
                cursor.execute(insert,(pri_nom,pri_cog,seg_cog,sexe,None))
            else:
                cursor.execute(insert,(pri_nom,pri_cog,seg_cog,sexe,dni))
except OSError as e:
    print("No s'ha pogut obrir el fitxer " + path)

cnx.commit()
cursor.close()
cnx.close()