import mysql.connector


def CrearSchema(cursor, nom):
    cursor.execute(
        f"DROP SCHEMA IF EXISTS {nom};\n"
        f"CREATE SCHEMA {nom} DEFAULT CHARACTER SET utf8;\n"
        f"USE {nom};")


def CrearTaules(cursor, nom):
    cursor.execute(f"CREATE TABLE {nom}.comunitats_autonomes (\n"
                   "comunitat_aut_id TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,\n"
                   "nom VARCHAR(45) NULL,\n"
                   "codi_ine CHAR(2) NOT NULL,\n"
                   "PRIMARY KEY(comunitat_aut_id),\n"
                   "UNIQUE INDEX uk_com_aut_id(codi_ine ASC) VISIBLE)\n"
                   "ENGINE=InnoDB;")

    cursor.execute(f"CREATE TABLE {nom}.provincies (\n"
                   "provincia_id TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,\n"
                   "comunitat_aut_id TINYINT UNSIGNED NOT NULL,\n"
                   "nom VARCHAR(45) NULL,\n"
                   "codi_ine CHAR(2) NOT NULL,\n"
                   "num_escons TINYINT UNSIGNED NULL COMMENT 'Numero escons que li pertoquen a aquella provincia',\n"
                   "PRIMARY KEY(provincia_id),\n"
                   "UNIQUE INDEX uk_provincies_codi_ine(codi_ine ASC) VISIBLE,\n"
                   "INDEX idx_fk_provincies_comunitats_autonomes(comunitat_aut_id ASC) VISIBLE,\n"
                   "CONSTRAINT fk_provincies_comunitats_autonomes\n"
                   "FOREIGN KEY(comunitat_aut_id)\n"
                   f"REFERENCES {nom}.comunitats_autonomes(comunitat_aut_id)\n"
                   "ON DELETE NO ACTION\n"
                   "ON UPDATE NO ACTION)\n"
                   "ENGINE=InnoDB;")

    cursor.execute(f"CREATE TABLE {nom}.municipis (\n"
                   "municipi_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,\n"
                   "nom VARCHAR(100) NULL,\n"
                   "codi_ine CHAR(3) NOT NULL,\n"
                   "provincia_id TINYINT UNSIGNED NOT NULL,\n"
                   "districte CHAR(2) NULL COMMENT 'Número de districte municipal , sinó el seu valor serà 99. Per exemple aquí municiís com Blanes el seu valor serà 99, però en ciutats com Barcelona hi haurà el número de districte',\n"
                   "PRIMARY KEY(municipi_id),"
                   "UNIQUE INDEX uk_municipis_codi_ine(codi_ine ASC) VISIBLE,\n"
                   "INDEX idx_fk_municipis_provincies1(provincia_id ASC) VISIBLE,\n"
                   "CONSTRAINT fk_municipis_provincies\n"
                   "FOREIGN KEY(provincia_id)\n"
                   f"REFERENCES {nom}.provincies(provincia_id)\n"
                   "ON DELETE NO ACTION\n"
                   "ON UPDATE NO ACTION)\n"
                   "ENGINE=InnoDB;")

    cursor.execute(f"CREATE TABLE {nom}.eleccions (\n"
                   "eleccio_id TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,\n"
                   "nom VARCHAR(45) NULL,"
                   "data DATE NOT NULL COMMENT 'Data (dia mes i any) de quan shan celebrat les eleccions',\n"
                   "any YEAR GENERATED ALWAYS AS(YEAR(data))  COMMENT 'any el qual han celebrat les eleccions',\n"
                   "mes TINYINT GENERATED ALWAYS AS(MONTH(data)) STORED COMMENT 'El mes que han celebrat les eleccions',\n"
                   "PRIMARY KEY(eleccio_id),\n"
                   "UNIQUE INDEX uk_eleccions_any_mes(any ASC, mes ASC) VISIBLE,\n"
                   "UNIQUE INDEX uk_eleccions_data(data ASC) VISIBLE)\n"
                   "ENGINE=InnoDB;")

    cursor.execute(f"CREATE TABLE {nom}.eleccions_municipis (\n"
                   "eleccio_id TINYINT UNSIGNED NOT NULL,\n"
                   "municipi_id SMALLINT UNSIGNED NOT NULL,\n"
                   "num_meses SMALLINT UNSIGNED NULL,\n"
                   "cens INT UNSIGNED NULL,\n"
                   "vots_emesos INT UNSIGNED NULL COMMENT 'Número total de vots realitzats en el municipi',\n"
                   "vots_valids INT UNSIGNED NULL COMMENT 'Número de vots es que tindran en compte: vots a candidatures + vots nuls',\n"
                   "vots_candidatures INT UNSIGNED NULL COMMENT 'Total de vots a les candidatures'\n,"
                   "vots_blanc INT UNSIGNED NULL,\n"
                   "vots_nuls INT UNSIGNED NULL,\n"
                   "INDEX idx_fk_eleccions_municipis_eleccions(eleccio_id ASC) VISIBLE,\n"
                   "INDEX fk_eleccions_municipis_municipis(municipi_id ASC) VISIBLE,\n"
                   "UNIQUE INDEX uk_eleccions_municipis(eleccio_id ASC, municipi_id ASC) VISIBLE,\n"
                   "PRIMARY KEY(eleccio_id, municipi_id),\n"
                   "CONSTRAINT fk_eleccions_municipis_municipis\n"
                   "FOREIGN KEY(municipi_id)\n"
                   f"REFERENCES {nom}.municipis(municipi_id)\n"
                   "ON DELETE NO ACTION\n"
                   "ON UPDATE NO ACTION,\n"
                   "CONSTRAINT fk_eleccions_municipis_eleccions\n"
                   "FOREIGN KEY(eleccio_id)\n"
                   f"REFERENCES {nom}.eleccions(eleccio_id)\n"
                   "ON DELETE NO ACTION\n"
                   "ON UPDATE NO ACTION)\n"
                   "ENGINE=InnoDB;")

    cursor.execute(f"CREATE TABLE {nom}.candidatures (\n"
                   "candidatura_id INT UNSIGNED NOT NULL AUTO_INCREMENT,\n"
                   "eleccio_id TINYINT UNSIGNED NOT NULL,\n"
                   "codi_candidatura CHAR(6) NULL,\n"
                   "nom_curt VARCHAR(50) NULL COMMENT 'Sigles de la candidatura', \n"
                   "nom_llarg VARCHAR(150) NULL COMMENT 'Nom llarg de la candidatura (denominació)',\n"
                   "codi_acumulacio_provincia CHAR(6) NULL COMMENT 'Codi de la candidatura acumulació a nivell provincial.',\n"
                   "codi_acumulacio_ca CHAR(6) NULL COMMENT 'Codi de la candidatura acumulació a nivell de comunitat autònoma',\n"
                   "codi_acumulario_nacional CHAR(6) NULL,\n"
                   "PRIMARY KEY(candidatura_id),\n"
                   "INDEX idx_fk_eleccions_partits_eleccions(eleccio_id ASC) VISIBLE,\n"
                   "UNIQUE INDEX uk_eleccions_partits(eleccio_id ASC, codi_candidatura ASC) VISIBLE,\n"
                   "CONSTRAINT fk_eleccions_partits_eleccions\n"
                   "FOREIGN KEY(eleccio_id)\n"
                   f"REFERENCES {nom}.eleccions(eleccio_id)\n"
                   "ON DELETE NO ACTION\n"
                   "ON UPDATE NO ACTION)\n"
                   "ENGINE=InnoDB;")

    cursor.execute(f"CREATE TABLE {nom}.persones (\n"
                   "persona_id INT UNSIGNED NOT NULL,\n"
                   "nom VARCHAR(30) NULL,\n"
                   "cog1 VARCHAR(30) NULL,\n"
                   "cog2 VARCHAR(30) NULL,\n"
                   "sexe ENUM('M', 'F') NULL COMMENT 'M=Masculí, F=Femení',\n"
                   "data_naixement DATE NULL,\n"
                   "dni CHAR(10) NOT NULL,\n"
                   "PRIMARY KEY(persona_id),\n"
                   "UNIQUE INDEX uk_candidats_dni(dni ASC) VISIBLE)\n"
                   "ENGINE=InnoDB")

    cursor.execute(f"CREATE TABLE {nom}.candidats (\n"
                   "candidat_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,\n"
                   "candidatura_id INT UNSIGNED NOT NULL,\n"
                   "persona_id INT UNSIGNED NOT NULL,\n"
                   "provincia_id TINYINT UNSIGNED NOT NULL,\n"
                   "num_ordre TINYINT NULL COMMENT 'Num ordre del candidatdins la llista del partit dins de la circumpscripció que es presenta.',\n"
                   "tipus ENUM('T', 'S') NULL COMMENT 'T=Titular, S=Suplent',\n"
                   "PRIMARY KEY(candidat_id),\n"
                   "INDEX fk_candidats_provincies1_idx(provincia_id ASC) VISIBLE,\n"
                   "INDEX fk_candidats_persones1_idx(persona_id ASC) VISIBLE,\n"
                   "INDEX fk_candidats_candidatures1_idx(candidatura_id ASC) VISIBLE,\n"
                   "UNIQUE INDEX uk_candidats_persona_cand(candidatura_id ASC, persona_id ASC) VISIBLE,\n"
                   "CONSTRAINT fk_candidats_provincies1\n"
                   "FOREIGN KEY(provincia_id)\n"
                   f"REFERENCES {nom}.provincies(provincia_id)\n"
                   "ON DELETE NO ACTION\n"
                   "ON UPDATE NO ACTION,\n"
                   "CONSTRAINT fk_candidats_persones1\n"
                   "FOREIGN KEY(persona_id)\n"
                   f"REFERENCES {nom}.persones(persona_id)\n"
                   "ON DELETE NO ACTION\n"
                   "ON UPDATE NO ACTION,\n"
                   "CONSTRAINT fk_candidats_candidatures1\n"
                   "FOREIGN KEY(candidatura_id)\n"
                   f"REFERENCES {nom}.candidatures(candidatura_id)\n"
                   "ON DELETE NO ACTION\n"
                   "ON UPDATE NO ACTION)\n"
                   "ENGINE=InnoDB;")

    cursor.execute(f"CREATE TABLE {nom}.vots_candidatures_mun (\n"
                   "eleccio_id TINYINT UNSIGNED NOT NULL,\n"
                   "municipi_id SMALLINT UNSIGNED NOT NULL,\n"
                   "candidatura_id INT UNSIGNED NOT NULL,\n"
                   "vots INT UNSIGNED NULL COMMENT 'Número de vots obtinguts per la candidatura',\n"
                   "PRIMARY KEY(eleccio_id, municipi_id, candidatura_id),\n"
                   "INDEX fk_candidatures_municipis_candidatures1_idx(candidatura_id ASC) VISIBLE,\n"
                   "INDEX fk_candidatures_municipis_eleccions_municipis1_idx(eleccio_id ASC, municipi_id ASC) VISIBLE,\n"
                   "CONSTRAINT fk_candidatures_municipis_candidatures1\n"
                   "FOREIGN KEY(candidatura_id)\n"
                   f"REFERENCES {nom}.candidatures(candidatura_id)\n"
                   "ON DELETE NO ACTION\n"
                   "ON UPDATE NO ACTION,\n"
                   "CONSTRAINT fk_candidatures_municipis_eleccions_municipis1\n"
                   "FOREIGN KEY(eleccio_id, municipi_id)\n"
                   f"REFERENCES {nom}.eleccions_municipis(eleccio_id, municipi_id)\n"
                   "ON DELETE NO ACTION\n"
                   "ON UPDATE NO ACTION)\n"
                   "ENGINE=InnoDB;")

    cursor.execute(f"CREATE TABLE {nom}.vots_candidatures_prov (\n"
                   "provincia_id TINYINT UNSIGNED NOT NULL,\n"
                   "candidatura_id INT UNSIGNED NOT NULL,\n"
                   "vots INT UNSIGNED NULL COMMENT 'Número de vots obtinguts per la candidatura',\n"
                   "candidats_obtinguts SMALLINT UNSIGNED NULL COMMENT 'Número de candidats obtinguts per la candidatura',\n"
                   "PRIMARY KEY(provincia_id, candidatura_id),\n"
                   "INDEX fk_candidatures_provincies_candidatures1_idx(candidatura_id ASC) VISIBLE,\n"
                   "CONSTRAINT fk_candidatures_provincies_provincies1\n"
                   "FOREIGN KEY(provincia_id)\n"
                   f"REFERENCES {nom}.provincies(provincia_id)\n"
                   "ON DELETE NO ACTION\n"
                   "ON UPDATE NO ACTION,\n"
                   "CONSTRAINT fk_candidatures_provincies_candidatures1\n"
                   "FOREIGN KEY(candidatura_id)\n"
                   f"REFERENCES {nom}.candidatures(candidatura_id)\n"
                   "ON DELETE NO ACTION\n"
                   "ON UPDATE NO ACTION)\n"
                   "ENGINE=InnoDB;")

    cursor.execute(f"CREATE TABLE {nom}.vots_candidatures_ca (\n"
                   "comunitat_autonoma_id TINYINT UNSIGNED NOT NULL,\n"
                   "candidatura_id INT UNSIGNED NOT NULL,\n"
                   "vots INT UNSIGNED NULL,\n"
                   "PRIMARY KEY(comunitat_autonoma_id, candidatura_id),\n"
                   "INDEX fk_comunitats_autonomes_has_candidatures_candidatures1_idx(candidatura_id ASC) VISIBLE,\n"
                   "INDEX fk_comunitats_autonomes_has_candidatures_comunitats_autonom_idx(comunitat_autonoma_id ASC) VISIBLE,\n"
                   "CONSTRAINT fk_comunitats_autonomes_has_candidatures_comunitats_autonomes1\n"
                   "FOREIGN KEY(comunitat_autonoma_id)\n"
                   f"REFERENCES {nom}.comunitats_autonomes(comunitat_aut_id)\n"
                   "ON DELETE NO ACTION\n"
                   "ON UPDATE NO ACTION,\n"
                   "CONSTRAINT fk_comunitats_autonomes_has_candidatures_candidatures1\n"
                   "FOREIGN KEY(candidatura_id)\n"
                   f"REFERENCES {nom}.candidatures(candidatura_id)\n"
                   "ON DELETE NO ACTION\n"
                   "ON UPDATE NO ACTION)\n"
                   "ENGINE=InnoDB;")


def AplicarCanvis(cursor, nom):
    cursor.execute(f"USE {nom}")
    cursor.execute(
        "INSERT INTO eleccions(eleccio_id, nom, data) VALUES (1, 'Eleccions Generals 2019', '2019-04-28')")
    cursor.execute(
        "ALTER TABLE candidats DROP FOREIGN KEY fk_candidats_persones1")
    cursor.execute(
        "ALTER TABLE persones MODIFY COLUMN persona_id INT UNSIGNED AUTO_INCREMENT, MODIFY COLUMN dni CHAR(10) NULL")
    cursor.execute(
        "ALTER TABLE candidats ADD CONSTRAINT fk_candidats_persones1 FOREIGN KEY(persona_id) REFERENCES persones(persona_id)")
    cursor.execute("ALTER TABLE municipis\n"
                   "DROP CONSTRAINT uk_municipis_codi_ine,\n"
                   "ADD CONSTRAINT uk_municipis_codi_ine_districte_provincia_id UNIQUE(codi_ine, districte, provincia_id)")
    cursor.execute("ALTER TABLE vots_candidatures_mun\n"
                   "DROP CONSTRAINT fk_candidatures_municipis_eleccions_municipis1,\n"
                   "ADD CONSTRAINT fk_candidatures_mun_municipis FOREIGN KEY(municipi_id)\n"
                   "REFERENCES municipis(municipi_id),\n"
                   "ADD CONSTRAINT fk_candidatures_mun_eleccions FOREIGN KEY(eleccio_id)\n"
                   "REFERENCES eleccions(eleccio_id)")


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


def ProgramaPrincipalN(host, user, pasw, nom):
    conexion = mysql.connector.connect(
        host=host,
        user=user,
        password=pasw)
    cursor = conexion.cursor()
    CrearSchema(cursor, nom)
    conexion = mysql.connector.connect(
        host=host,
        user=user,
        password=pasw,
        database=nom)
    cursor = conexion.cursor()
    CrearTaules(cursor, nom)
    AplicarCanvis(cursor, nom)
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


def ProgramaPrincipalS(host, user, pasw):
    conexion = mysql.connector.connect(
        host=host,
        user=user,
        password=pasw,
        database="Grup2_eleccions")
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


print("Benvingut al programa d'importació de dades de les eleccions del dia 2 d'Abril del 2019\n")
opcio = input("Esta la BD Grup2_eleccions ja creada? (S,N)? ")

if opcio.upper() == "N":
    nom = input("Introdueix el nom per la BD: ")
    host = input("Introdueix el host (X.X.X.X): ")
    user = input("Introdueix l'usuari: ")
    pasw = input("Introdueix la contrasenya: ")
    ProgramaPrincipalN(host, user, pasw, nom)
    print(f"\nLes dades s'han importat correctament a {nom}\n")
elif opcio.upper() == "S":
    host = input("Introdueix el host (X.X.X.X): ")
    user = input("Introdueix l'usuari: ")
    pasw = input("Introdueix la contrasenya: ")
    ProgramaPrincipalS(host, user, pasw)
    print(f"\nLes dades s'han importat correctament a Grup2_eleccions\n")
else:
    print("Opció introduida incorrecte, tancant programa")
