-- Fes una consulta on ens demani el codi_candidatura i el nom_llarg on el nom_curt sigui "EB" i ordena per candidatura_id de forma descendent.
SELECT codi_candidatura,nom_llarg 
	FROM candidatures
WHERE nom_curt = "EB"
ORDER BY candidatura_id DESC;

-- Mostra totes les persones que no tinguin el DNI posat a la base de dades.
SELECT nom,cog1,cog2,dni
	FROM persones
WHERE dni IS NULL;

-- Mostra quantes candidatures té el PP
SELECT COUNT(*)
	FROM candidatures
WHERE nom_curt = 'PP';

-- Mostra el municipi_id i la candidatura_id de les candidatures votades a nivell municipal que tinguin més de 5000 vots. Orderna per nombre de vots
SELECT candidatura_id,vots 
	FROM vots_candidatures_mun
WHERE vots > 5000
ORDER BY vots;

-- Mostra el nom i el cognom de les persones que es diguin igual que algun membre del grup
SELECT nom,cog1
	FROM persones
WHERE nom IN ("Jordi","Mark","Hemant","Santiago")
ORDER BY nom;
