-- Fes una consulta on ens demani el codi_candidatura i el nom_llarg on el nom_curt sigui "EB" i ordena per candidatura_id de forma descendent.
SELECT codi_candidatura,nom_llarg 
	FROM candidatures
WHERE nom_curt="EB"
ORDER BY candidatura_id DESC;

-- Mostra totes les persones que no tinguin el DNI posat a la base de dades.
SELECT nom,cog1,cog2,dni
	FROM persones
WHERE dni IS NULL;

-- Mostra quantes candidatures té el PP?
SELECT COUNT(*)
	FROM candidatures
WHERE nom_curt = 'PP';

-- Busca per el municipi_id = 650 cuants vots te cada candidatura per aquest municipi, mostra la candidatura_id i el nombre de vots, ordena per vots de manera ASC.
SELECT candidatura_id,vots 
	FROM vots_candidatures_mun
WHERE municipi_id = 650
ORDER BY vots ASC;

-- Mostra el nom i el cognom de les persones que s'anomenin igual que algun membre del grup
SELECT nom,cog1 
	FROM persones
WHERE nom IN ("Jordi","Marc","Hemant","Santiago")
ORDER BY nom;
