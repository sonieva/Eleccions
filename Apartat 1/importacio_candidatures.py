import mysql.connector

path = "Documentaci√≥/02201904_MESA/03021904.DAT"
cnx = mysql.connector.connect(
    host='10.94.255.166',
    user='perepi',
    password='pastanaga',
    database='Grup2_eleccions')
cursor = cnx.cursor()

insert = ("INSERT INTO candidatures "
          "(eleccio_id,codi_candidatura,nom_curt,nom_llarg,codi_acumulacio_provincia,codi_acumulacio_ca,codi_acumulario_nacional)\n"
          "VALUES ")

try:
    with open(path, "r") as fitxer:
        for linia in fitxer:
            codi = linia[8:14]
            nomCurt = linia[14:64].strip()
            nomLlarg = linia[64:214].strip().replace("'", '\\'+"'")
            codiProvincial = linia[214:220]
            codiAutonomic = linia[220:226]
            codiNacional = linia[226:232]
            insert += f"\t(1,'{codi}','{nomCurt}','{nomLlarg}','{codiProvincial}','{codiAutonomic}','{codiNacional}') ,\n"
except OSError as e:
    print("No s'ha pogut obrir el fitxer " + path)

insert=insert[:-1] + ";"
cursor.execute(insert)
cnx.commit()
cursor.close()
cnx.close()
