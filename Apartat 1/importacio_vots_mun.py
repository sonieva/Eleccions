import mysql.connector
path = "Documentació/02201904_MESA/06021904.DAT"
conexion = mysql.connector.connect(
    host='10.94.255.166',
    user="perepi",
    password="pastanaga",
    database="Grup2_eleccions"
)
cursor = conexion.cursor()
insert = ("INSERT INTO vots_candidatures_mun"
          "(eleccio_id,municipi_id,candidatura_id,vots)\n"
          "VALUES")
try:
    with open(path, "r") as fitxer:
        for linia in fitxer:
            if linia[16:22] in ("000003","000004","000006","000009","000010","000011","000012","000013","000015","000016","000017","000018","000019","000020","000021","000022","000023","000024","000025","000026","000027","000028","000029","000030","000032","000033","000034","000035","000036","000037","000038","000039","000040","000041","000042","000043","000044","000045","000047","000049","000050","000052","000053","000054","000055","000056","000057","000058","000060","000061","000063","000064","000065","000066","000067","000068","000069","000072","000073","000074","000075","000076","000077","000078","000079","000080","000081","000082","000083","000084","000085","000086","000088","000089","000090","000091","000092","000093","000094","000096","000097","000098","000100","000101","000103","000104","000105","000106","000107","000108","000109","000110","000112","000116","000117"):
                candidatura_id = cursor.execute(
                    f"SELECT candidatura_id FROM candidatures WHERE codi_candidatura = '{linia[16:22]}'")
                candidatura_id = cursor.fetchone()
                municipi_id = cursor.execute(
                    "SELECT municipi_id FROM municipis m "
                    "INNER JOIN provincies p ON p.provincia_id = m.provincia_id " 
                    f"WHERE m.codi_ine = '{linia[11:14]}' " 
                    f"AND p.codi_ine = '{linia[9:11]}'")
                municipi_id = cursor.fetchone()
                vots = int(linia[22:30])
                insert += f'\t(1,{municipi_id[0]},{candidatura_id[0]},{vots}),\n'
except OSError as e:
    print("No s'ha pogut obrir el fitxer " + path)

insert = insert[:-2] + ";"
print(insert)
