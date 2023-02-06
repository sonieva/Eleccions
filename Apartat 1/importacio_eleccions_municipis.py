import mysql.connector

path = "Documentació/02201904_MESA/05021904.DAT"
cnx = mysql.connector.connect(
    host='10.94.255.166',
    user="perepi",
    password="pastanaga",
    database="Grup2_eleccions"
)
cursor = cnx.cursor(buffered=True)
insert = ("INSERT INTO eleccions_municipis"
          "(eleccio_id,municipi_id,num_meses,cens,vots_emesos,vots_valids,vots_candidatures,vots_blanc,vots_nuls)\n"
          "VALUES")
try:
    with open(path, "r", encoding="utf-8") as fitxer:
        for linia in fitxer:
            if linia[16:18] == "99":
                municipi_id = cursor.execute(
                    f"SELECT municipi_id FROM municipis WHERE (codi_ine = '{linia[13:16]}') AND (provincia_id = (SELECT provincia_id FROM provincies WHERE codi_ine = '{linia[11:13]}'))")
                municipi_id = cursor.fetchone()
                num_meses = int(linia[136:141])
                cens = int(linia[157:165]) + int(linia[141:149])
                vots_emesos = int(linia[189:197]) + \
                    int(linia[197:205]) + int(linia[205:213])
                vots_valids = int(linia[205:213]) + int(linia[197:205])
                vots_candidatures = int(linia[205:213])
                vots_blanc = int(linia[189:197])
                vots_nuls = int(linia[197:205])
                insert += f"\t(1,{municipi_id[0]},{num_meses},{cens},{vots_emesos},{vots_valids},{vots_candidatures},{vots_blanc},{vots_nuls}),\n"

except OSError as e:
    print("No s'ha pogut obrir el fitxer " + path)

insert = insert[:-2] + ";"
cursor.execute(insert)
cnx.commit()
cursor.close()
cnx.close()
