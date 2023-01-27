# Apartat 1
## Estructura principal
Hem agafat el model d'eleccions de l'abril el 2019 i l'hem descarregat, un cop descarregat el model hem obert en el workbench el model,
en el workbench tenim l'opció d'exportar-lo en DML i obtenir totes les sentències, un cop exportat hem canviat alguns paràmetres per
adequar a la pràctica.

## Modificació estructura
Hem hagut de modificar l'estructura creada anteriorment per adaptarla als diferents errors que hem a anant trobant.
Totes les sentencies utilitzades estan a l'arxiu [BD_eleccions_v2.sql](https://github.com/sonieva/Eleccions/blob/master/Apartat%201/BD_eleccions_v2.sql)

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
SELECT codi_candidatura,nom_llarg FROM candidatures
Where nom_curt="EB"
ORDER BY candidatura_id DESC;
### Ex 2
### Mostra totes les persones que no tenen DNI assignat
SELECT nom,cog1,cog2,dni
    FROM persones
    WHERE dni IS NULL;

### EX 3 
## Cuantes candidatures té el PP?
SELECT COUNT(*)
	FROM candidatures
    WHERE nom_curt = 'PP';
### Ex 4
## Busca per el municipi_id 2 cuants vots te cada candidatura _id per aquest municipi, i ordena de manera asc per vots
SELECT candidatura_id,vots FROM vots_candidatures_mun
WHERE municipi_id=2
ORDER BY vots ASC;

## Ex 5
## Busca els candidats que siguin de tipus suplent S, nomes mostran el seu num_ordre i el candidat_id
SELECT num_ordre, candidat_id FROM candidats
WHERE tipus="S";

<<<<<<< HEAD
## Categoria 2
### Ex 1
#### Fes una consulta on demani el nom de la provincia, el seu codi_ine, candidatura_id i els vots per cada candidatura, i ordena per quantitat de vots.
SELECT p.nom,p.codi_ine,v.candidatura_id,v.vots FROM vots_candidatures_prov v
INNER JOIN provincies p ON p.provincia_id = v.provincia_id
ORDER BY vots;
=======

## CATEGORIA 2
## DIGAM EL NOM COMPLERT DE TOTES LES PERSONES MES LA CANDIDATURA I EL NOM LLARG DE LA CANDIDATURA.
SELECT p.nom, p.cog1, p.cog2, c.candidat_id, c1.nom_llarg
	FROM persones p
    INNER JOIN candidats c ON p.persona_id = c.persona_id
    INNER JOIN candidatures c1 ON c.candidatura_id = c1.candidatura_id
    ORDER BY p.nom;

## MOSTRA TOTES LES PROVINCIES I TOTS EL MUNICIPIS DE CATALUNYA(al nom de provincies li direm nom_pro i municipis nom_mun)
# |codi_ine|pronvincia_id|nom_pro|municipi_id|nom_mun|
SELECT c.codi_ine, p.provincia_id, p.nom AS nom_pro, m.municipi_id, m.nom AS nom_mun
	FROM comunitats_autonomes c
    INNER JOIN provincies p ON c.comunitat_aut_id = p.comunitat_aut_id
    INNER JOIN municipis m ON p.provincia_id = m.provincia_id
    WHERE upper(c.nom) = 'CATALUNYA';
>>>>>>> 765ff6e9c8165b4748c00b2ed7c0c704dd84d226
