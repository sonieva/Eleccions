# Apartat 1
## Estructura principal
Hem agafat el model d'eleccions d'abril de 2019 i l'hem descarregat, un cop descarregat en el mateix Workbench tenim l'opció d'exportar-lo a script i obtenir tota l'estructura, només resta canviar el nom de la base de dades.

## Modificació estructura
Hem hagut de modificar l'estructura creada anteriorment per adaptarla als diferents problemes que hem tingut a l'hora d'importar les dades.
Totes les modificacions realitzades estan a l'arxiu [BD_eleccions_v2](https://github.com/sonieva/Eleccions/blob/master/Apartat%201/BD_eleccions_v2.sql)

## Introducció de dades bàsiques
En aquest apartat hem introduït manualment la seguent sentencia SQL:<br>

```SQL 
INSERT INTO eleccions (eleccio_id, nom, data)
VALUES (1,"Eleccions Generals 2019", "2019-04-28")
```

I ha quedat aixi a la BD:<br>
![Captura taula "Eleccions"](https://github.com/sonieva/Eleccions/blob/master/Documentaci%C3%B3/Imatges/taula_eleccions.png)


# Consultes SQL Categoria 1
### Ex 1
#### Fes una consulta on Ens demani el codi_candidatura i el nom_llarg on el nom_curt sigui EB i ordena de forma descendent candidatura_id

```SQL 
SELECT codi_candidatura,nom_llarg FROM candidatures
Where nom_curt="EB"
ORDER BY candidatura_id DESC;
```

### Ex 2
### Mostra totes les persones que no tenen DNI assignat
```SQL 
SELECT nom,cog1,cog2,dni
    FROM persones
    WHERE dni IS NULL;
```

### EX 3 
## Cuantes candidatures té el PP?
```SQL
SELECT COUNT(*)
	FROM candidatures
    WHERE nom_curt = 'PP';
```

### Ex 4
## Busca per el municipi_id 2 cuants vots te cada candidatura _id per aquest municipi, i ordena de manera asc per vots
```SQL
SELECT candidatura_id,vots FROM vots_candidatures_mun
WHERE municipi_id=2
ORDER BY vots ASC;
```

## Ex 5
## Busca els candidats que siguin de tipus suplent S, nomes mostran el seu num_ordre i el candidat_id
```SQL
SELECT num_ordre, candidat_id FROM candidats
WHERE tipus="S";
```

## CATEGORIA 2
## DIGAM EL NOM COMPLERT DE TOTES LES PERSONES MES LA CANDIDATURA I EL NOM LLARG DE LA CANDIDATURA.
```SQL
SELECT p.nom, p.cog1, p.cog2, c.candidat_id, c1.nom_llarg
	FROM persones p
    INNER JOIN candidats c ON p.persona_id = c.persona_id
    INNER JOIN candidatures c1 ON c.candidatura_id = c1.candidatura_id
    ORDER BY p.nom;
```

## MOSTRA TOTES LES PROVINCIES I TOTS EL MUNICIPIS DE CATALUNYA(al nom de provincies li direm nom_pro i municipis nom_mun)
# |codi_ine|pronvincia_id|nom_pro|municipi_id|nom_mun|
```SQL
SELECT c.codi_ine, p.provincia_id, p.nom AS nom_pro, m.municipi_id, m.nom AS nom_mun
	FROM comunitats_autonomes c
    INNER JOIN provincies p ON c.comunitat_aut_id = p.comunitat_aut_id
    INNER JOIN municipis m ON p.provincia_id = m.provincia_id
    WHERE upper(c.nom) = 'CATALUNYA';
```

#### Fes una consulta on demani el nom de la provincia, el seu codi_ine, candidatura_id i els vots per cada candidatura, i ordena per quantitat de vots.
```SQL
SELECT p.nom,p.codi_ine,v.candidatura_id,v.vots FROM vots_candidatures_prov v
INNER JOIN provincies p ON p.provincia_id = v.provincia_id
ORDER BY vots;
```

## Per cada municipi volem saber el seu nom, a la provincia a la que pertany a mes volem saber el nom de les eleccions a mes de la seva data. També volem que ens filtri per municipis que tinguin mes de 4 cops vots valids que vots en blanc.
```SQL
SELECT m.nom as nom_municipi, p.nom as nom_provincia, e.nom as nom_eleccions, e.data as data_eleccions FROM municipis m
INNER JOIN provincies p ON m.provincia_id=p.provincia_id
INNER JOIN eleccions_municipis em ON em.municipi_id=m.municipi_id
INNER JOIN eleccions e ON e.eleccio_id=em.eleccio_id
WHERE vots_valids>4*vots_blanc;
```

### Per cada provincia volem saber el seu nom y el total de vots que ha obtingut cada provincia a mes volem saber el nom de la comunitat autonoma que pertanyen y que es filtri per comunitat_aut_id = 1 i 2
```SQL
SELECT p.nom as nom_provincia, sum(vcp.vots) as vots, ca.nom as nom_comunitat_autonoma from provincies p
INNER JOIN vots_candidatures_prov vcp ON p.provincia_id = vcp.provincia_id
INNER JOIN comunitats_autonomes ca ON ca.comunitat_aut_id = p.comunitat_aut_id
WHERE ca.comunitat_aut_id IN (1,2)
GROUP BY p.provincia_id
```

### CATEGORIA 3
## Busca les persones amb el seu nom, cognoms y el seu sexe que pertanyin al tipus T (Titular)
```SQL
SELECT nom, concat(cog1," ",cog2) as cognoms, sexe 
FROM persones
WHERE persona_id IN (SELECT persona_id FROM candidats
                        WHERE tipus="T")
```

## Mostra la provinvia_id, nom, codi_ine, num_escons on la comunitat autonoma sigui Barcelona.
```SQL
SELECT provincia_id, nom, codi_ine, num_escons
FROM provincies
WHERE comunitat_aut_id = (SELECT comunitat_aut_id FROM provincies WHERE nom = 'Barcelona');
```

## Mostra tots els municipis que sigui de catalunya ordenats pel nom;
## |municipi_id|nom|codi_ide|
```SQL
select  m.municipi_id, m.nom, m.codi_ine 
	FROM municipis m
    INNER JOIN provincies p ON p.provincia_id = m.provincia_id
    INNER JOIN comunitats_autonomes c ON c.comunitat_aut_id = p.comunitat_aut_id
	WHERE c.comunitat_aut_id = (SELECT comunitat_aut_id
									FROM comunitats_autonomes
                                    WHERE upper(nom) = 'CATALUÑA')
    ORDER BY nom;
```

## Mostra la candidatura_id, nom curt, el nom llarg, De una porvincia nomes sabent el aquest municipi_id '21901'.
## |candidatura_id|vots|nom_curt|nom_llarg|
```SQL
SELECT v.candidatura_id, p.nom, v.vots, c.nom_curt, c.nom_llarg
	FROM vots_candidatures_prov v
    INNER JOIN provincies p ON p.provincia_id = v.provincia_id
    INNER JOIN candidatures c ON c.candidatura_id = v.candidatura_id
	WHERE p.provincia_id = (SELECT provincia_id 
								FROM municipis
								WHERE municipi_id = 21901);
```

## Volem els nuemros emesos i de taules de cada municipi separats per cada demarcació, sabent que Navarcles es de Barcelona, Maçanet de la selva de Girona, Solsona de Lleida i Salou de Tarragona
```SQL
SELECT  DISTINCT m.nom, e.num_meses, e.vots_emesos
	FROM provincies p			
    INNER JOIN vots_candidatures_prov v ON p.provincia_id = v.provincia_id
    INNER JOIN municipis m ON m.provincia_id = v.provincia_id
    INNER JOIN eleccions_municipis e ON e.municipi_id = m.municipi_id
	WHERE p.provincia_id = (SELECT provincia_id
								FROM municipis
								WHERE lower(nom) = 'navarcles');
```

=======
### CATEGORIA 4  
## 1 pregunta utilitzant WINDOW FUNCTIONS o recursivitat 
```SQL
WITH RECURSIVE eleccions_totals AS (
  SELECT m.municipi_id, m.nom, m.codi_ine 
  FROM municipis m
  INNER JOIN provincies p ON p.provincia_id = m.provincia_id
  INNER JOIN comunitats_autonomes c ON c.comunitat_aut_id = p.comunitat_aut_id
  WHERE c.comunitat_aut_id = (SELECT comunitat_aut_id
                              FROM comunitats_autonomes
                              WHERE upper(nom) = 'CATALUÑA')
)
SELECT *
FROM eleccions_totals
ORDER BY nom;
```

