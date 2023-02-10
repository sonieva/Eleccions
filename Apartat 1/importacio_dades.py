import mysql.connector


def ImportarComunitatsAutonomes(cursor):
    path = "Documentació/02201904_MESA/07021904.DAT"
    insert = ("INSERT INTO comunitats_autonomes (codi_ine,nom) VALUES (%s,%s)")
    with open(path, "r") as fitxer:
        for linia in fitxer:
            if linia[11:13] == "99":
                if linia[9:11] != "99":
                    codi_ine = linia[9:11]
                    nom = linia[14:64].strip()
                    cursor.execute(insert, (codi_ine, nom))


def ImportarProvincies(cursor):
    path = "Documentació/02201904_MESA/07021904.DAT"
    insert = (
        "INSERT INTO provincies (comunitat_aut_id,nom,codi_ine,num_escons) VALUES (%s,%s,%s,%s)")
    with open(path, "r") as fitxer:
        for linia in fitxer:
            if linia[11:13] != "99":
                comunitat_aut_id = cursor.execute(
                    f"SELECT comunitat_aut_id FROM comunitats_autonomes WHERE codi_ine = '{linia[9:11]}'")
                comunitat_aut_id = cursor.fetchone()
                nom = linia[14:64].strip()
                codi_ine = linia[11:13]
                escons = int(linia[149:155])
                cursor.execute(
                    insert, (comunitat_aut_id[0], nom, codi_ine, escons))


def ImportarMunicipis(cursor):
    path = "Documentació/02201904_MESA/05021904.DAT"
    insert = (
        "INSERT INTO municipis (codi_ine,nom,provincia_id,districte) VALUES (%s,%s,%s,%s)")
    with open(path, "r") as fitxer:
        for linia in fitxer:
            provincia_id = cursor.execute(
                f"SELECT provincia_id FROM provincies WHERE codi_ine = '{linia[11:13]}'")
            provincia_id = cursor.fetchone()
            nom = linia[18:118].strip()
            codi_ine = linia[13:16]
            districte = linia[16:18]
            cursor.execute(insert, (codi_ine, nom, provincia_id[0], districte))


def ImportarEleccionsMunicipis(cursor):
    path = "Documentació/02201904_MESA/05021904.DAT"
    insert = ("INSERT INTO eleccions_municipis (eleccio_id,municipi_id,num_meses,cens,vots_emesos,vots_valids,vots_candidatures,vots_blanc,vots_nuls) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)")
    with open(path, "r") as fitxer:
        for linia in fitxer:
            if linia[16:18] == "99":
                municipi_id = cursor.execute(
                    f"SELECT municipi_id FROM municipis WHERE (codi_ine='{linia[13:16]}') AND (districte = '{linia[16:18]}') AND (provincia_id = (SELECT provincia_id FROM provincies WHERE codi_ine='{linia[11:13]}'))")
                municipi_id = cursor.fetchone()
                num_meses = int(linia[136:141])
                cens = int(linia[157:165]) + int(linia[141:149])
                vots_emesos = int(linia[189:197]) + \
                    int(linia[197:205]) + int(linia[205:213])
                vots_valids = int(linia[205:213]) + int(linia[197:205])
                vots_candidatures = int(linia[205:213])
                vots_blanc = int(linia[189:197])
                vots_nuls = int(linia[197:205])
                cursor.execute(insert, (1, municipi_id[0], num_meses, cens, vots_emesos,
                               vots_valids, vots_candidatures, vots_blanc, vots_nuls))


def ImportarCandidatures(cursor):
    path = "Documentació/02201904_MESA/03021904.DAT"
    insert = ("INSERT INTO candidatures (eleccio_id,codi_candidatura,nom_curt,nom_llarg,codi_acumulacio_provincia,codi_acumulacio_ca,codi_acumulario_nacional) VALUES (%s,%s,%s,%s,%s,%s,%s)")
    with open(path, "r") as fitxer:
        for linia in fitxer:
            codi = linia[8:14]
            nomCurt = linia[14:64].strip()
            nomLlarg = linia[64:214].strip().replace("'", '\\'+"'")
            codiProvincial = linia[214:220]
            codiAutonomic = linia[220:226]
            codiNacional = linia[226:232]
            cursor.execute(insert, (1, codi, nomCurt, nomLlarg,
                           codiProvincial, codiAutonomic, codiNacional))


def ImportarPersones(cursor):
    path = "Documentació/02201904_MESA/04021904.DAT"
    insert = (
        "INSERT INTO persones (nom,cog1,cog2,sexe,dni) VALUES (%s,%s,%s,%s,%s)")
    with open(path, "r") as fitxer:
        for linia in fitxer:
            #codi = linia[8:14]
            pri_nom = linia[25:50].strip()
            pri_cog = linia[50:75].strip()
            seg_cog = linia[75:100].strip()
            sexe = linia[100:101]
            dni = linia[109:119].strip()
            if dni == "":
                cursor.execute(insert, (pri_nom, pri_cog, seg_cog, sexe, None))
            else:
                cursor.execute(insert, (pri_nom, pri_cog, seg_cog, sexe, dni))


def ImportarCandidats(cursor):
    path = "Documentació/02201904_MESA/04021904.DAT"
    insert = ("INSERT INTO candidats (candidatura_id,persona_id,provincia_id,num_ordre,tipus) VALUES (%s,%s,%s,%s,%s)")
    noms = []
    with open(path, "r") as fitxer:
        for linia in fitxer:
            if linia[9:11] != "99":
                provincia_id = cursor.execute(
                    f"SELECT provincia_id FROM provincies WHERE codi_ine = '{linia[9:11]}'")
                provincia_id = cursor.fetchone()
                candidatura_id = cursor.execute(
                    f"SELECT candidatura_id FROM candidatures WHERE codi_candidatura = '{linia[15:21]}'")
                candidatura_id = cursor.fetchone()
                nom = linia[25:50].strip()
                cog1 = linia[50:75].strip()
                cog2 = linia[75:100].strip()
                nom_complet = f"{nom} {cog1} {cog2}"
                noms.append(nom_complet)
                if noms.count(nom_complet) >= 2:
                    desc = 'SELECT persona_id FROM persones WHERE (nom = %s) AND (cog1 = %s) AND (cog2 = %s) ORDER BY persona_id DESC LIMIT 1'
                    persona_id = cursor.execute(desc, (nom, cog1, cog2))
                else:
                    asc = 'SELECT persona_id FROM persones WHERE (nom = %s) AND (cog1 = %s) AND (cog2 = %s) ORDER BY persona_id ASC LIMIT 1'
                    persona_id = cursor.execute(asc, (nom, cog1, cog2))
                persona_id = cursor.fetchone()
                num_ordre = int(linia[21:24])
                tipus = linia[24:25]
                cursor.execute(
                    insert, (candidatura_id[0], persona_id[0], provincia_id[0], num_ordre, tipus))


def ImportarVotsMunicipal(cursor):
    path = "Documentació/02201904_MESA/06021904.DAT"
    insert = ("INSERT INTO vots_candidatures_mun (eleccio_id,municipi_id,candidatura_id,vots) VALUES (%s,%s,%s,%s)")
    with open(path, "r") as fitxer:
        for linia in fitxer:
            if linia[14:16] != "99":
                candidatura_id = cursor.execute(
                    f"SELECT candidatura_id FROM candidatures WHERE codi_candidatura = '{linia[16:22]}'")
                candidatura_id = cursor.fetchone()
                municipi_id = cursor.execute(
                    f"SELECT municipi_id FROM municipis WHERE (codi_ine = '{linia[11:14]}') AND (districte = '{linia[14:16]}') AND (provincia_id =  (SELECT provincia_id FROM provincies WHERE codi_ine = '{linia[9:11]}'))")
                municipi_id = cursor.fetchone()
                vots = int(linia[22:30])
                cursor.execute(
                    insert, (1, municipi_id[0], candidatura_id[0], vots))


def ImportarVotsProvincial(cursor):
    path = "Documentació/02201904_MESA/08021904.DAT"
    insert = ("INSERT INTO vots_candidatures_prov (provincia_id,candidatura_id,vots,candidats_obtinguts) VALUES (%s,%s,%s,%s)")
    with open(path, "r") as fitxer:
        for linia in fitxer:
            if linia[11:13] != "99":
                candidatura_id = cursor.execute(
                    f"SELECT candidatura_id FROM candidatures WHERE codi_candidatura = '{linia[14:20]}'")
                candidatura_id = cursor.fetchone()
                provincia_id = cursor.execute(
                    f"SELECT provincia_id FROM provincies WHERE codi_ine = '{linia[11:13]}'")
                provincia_id = cursor.fetchone()
                vots = int(linia[20:28])
                candidats_obtinguts = int(linia[28:33])
                cursor.execute(
                    insert, (provincia_id[0], candidatura_id[0], vots, candidats_obtinguts))


def ImportarVotsAutonomic(cursor):
    path = "Documentació/02201904_MESA/08021904.DAT"
    insert = (
        "INSERT INTO vots_candidatures_ca (comunitat_autonoma_id,candidatura_id,vots) VALUES (%s,%s,%s)")
    with open(path, "r") as fitxer:
        for linia in fitxer:
            if linia[11:13] == "99" and linia[9:11] != "99":
                comunitat_autonoma_id = cursor.execute(
                    f"SELECT comunitat_aut_id FROM comunitats_autonomes WHERE codi_ine = '{linia[9:11]}'")
                comunitat_autonoma_id = cursor.fetchone()
                candidatura_id = cursor.execute(
                    f"SELECT candidatura_id FROM candidatures WHERE codi_candidatura = '{linia[14:20]}'")
                candidatura_id = cursor.fetchone()
                vots = int(linia[21:28])
                cursor.execute(
                    insert, (comunitat_autonoma_id[0], candidatura_id[0], vots))


def ProgramaPrincipal(host, user, pasw, bd):
    conexion = mysql.connector.connect(
        host=host,
        user=user,
        password=pasw,
        database=bd)
    cursor = conexion.cursor()
    ImportarComunitatsAutonomes(cursor)
    ImportarProvincies(cursor)
    ImportarMunicipis(cursor)
    ImportarEleccionsMunicipis(cursor)
    ImportarCandidatures(cursor)
    ImportarPersones(cursor)
    ImportarCandidats(cursor)
    ImportarVotsMunicipal(cursor)
    ImportarVotsProvincial(cursor)
    ImportarVotsAutonomic(cursor)
    conexion.commit()
    cursor.close()
    conexion.close()

print("Benvingut al programa d'importació de dades de les eleccions d'abril de 2019\n")
host = input("Introdueix el host (X.X.X.X): ")
user = input("Introdueix l'usuari: ")
pasw = input("Introdueix la contrasenya: ")
bd = input("Introdueix la base de dades: ")
ProgramaPrincipal(host, user, pasw, bd)
print("\nLes dades s'han importat correctament!\n")
