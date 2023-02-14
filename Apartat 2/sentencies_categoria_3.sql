-- Mostra el sexe, cognoms i nom de les persones que pertanyin al tipus "T" (Titular)
SELECT nom, concat(cog1," ",cog2) as cognoms, sexe 
	FROM persones
WHERE persona_id IN (	SELECT persona_id 
							FROM candidats
						WHERE tipus = "T"	);
                        
-- Mostra el nom de la comunitat autonoma amb el major numero de vots per la candidatura_id = 95
SELECT nom
	FROM comunitats_autonomes ca
    INNER JOIN vots_candidatures_ca vca ON vca.comunitat_autonoma_id = ca.comunitat_aut_id
    INNER JOIN candidatures c ON c.candidatura_id = vca.candidatura_id
WHERE c.candidatura_id = 95 AND vca.vots = (SELECT MAX(vots) FROM vots_candidatures_ca WHERE candidatura_id = 95);

-- Mostra tots els municipis de "Cataluña" ordenats pel nom;
SELECT  m.municipi_id, m.nom, m.codi_ine 
	FROM municipis m
    INNER JOIN provincies p ON p.provincia_id = m.provincia_id
    INNER JOIN comunitats_autonomes c ON c.comunitat_aut_id = p.comunitat_aut_id
WHERE c.comunitat_aut_id = (	SELECT comunitat_aut_id
									FROM comunitats_autonomes
								WHERE upper(nom) = 'CATALUÑA'	)
ORDER BY nom;

-- Mostra el nom llarg com nom_partit i el numero de vots de les candidatures votades a nivell provincial de la provincia del municipi de Purchena. Ordena per numero de vots de forma descendent
SELECT c.nom_llarg AS nom_partit, v.vots 
	FROM vots_candidatures_prov v
    INNER JOIN provincies p ON p.provincia_id = v.provincia_id
    INNER JOIN candidatures c ON c.candidatura_id = v.candidatura_id
WHERE p.provincia_id = (	SELECT provincia_id 
								FROM municipis
							WHERE nom = 'Purchena'	)
ORDER BY v.vots DESC;

-- Mostra la provincia_id, el nom de la provincia, el nom curt i el nom llarg de la candidatura i els vots de les candidatures que tinguin un numero de vots superior a les candidatures votades a nivell provincial. Ordena per numero de vots
SELECT p.provincia_id, p.nom, c.nom_curt, c.nom_llarg, v.vots
	FROM candidatures c
    INNER JOIN vots_candidatures_prov v ON v.candidatura_id = c.candidatura_id
    INNER JOIN provincies p ON p.provincia_id = v.provincia_id
WHERE v.vots > (SELECT ROUND(AVG(vots),0) FROM vots_candidatures_prov)
ORDER BY v.vots;