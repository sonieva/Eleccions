-- Mostra el nom complet de totes les persones, el seu candidat_id i el nom llarg de la candidatura on estan
SELECT c.candidat_id, p.nom, p.cog1, p.cog2, c1.nom_llarg
	FROM persones p
	INNER JOIN candidats c ON p.persona_id = c.persona_id
	INNER JOIN candidatures c1 ON c.candidatura_id = c1.candidatura_id
ORDER BY p.nom;

-- Mostra el codi_ine,provincia_id i el nom de totes les provincies com a nom_pro i el municipi_id i el nom de tots els municipis com a nom_mun de "Cataluña".
SELECT c.codi_ine, p.provincia_id,
		p.nom AS nom_pro, 
        m.municipi_id, 
        m.nom AS nom_mun
	FROM comunitats_autonomes c
    INNER JOIN provincies p ON c.comunitat_aut_id = p.comunitat_aut_id
    INNER JOIN municipis m ON p.provincia_id = m.provincia_id
    WHERE upper(c.nom) = 'CATALUÑA';

-- Fes una consulta per veure el nom de la provincia, codi_ine, candidatura_id i els vots per cada candidatura, ordena per numero de vots
SELECT p.nom,p.codi_ine,v.candidatura_id,v.vots 
	FROM vots_candidatures_prov v
	INNER JOIN provincies p ON p.provincia_id = v.provincia_id
ORDER BY vots;

-- Per cada municipi volem saber el seu nom, la provincia a la que pertany, el nom de les eleccions i la data. També volem que mostri municipis que tinguin 4 cops mes de vots valids que de vots en blanc
SELECT 	m.nom as nom_municipi,
		p.nom as nom_provincia, 
        e.nom as nom_eleccions, 
        e.data as data_eleccions 
	FROM municipis m
	INNER JOIN provincies p ON m.provincia_id = p.provincia_id
	INNER JOIN eleccions_municipis em ON em.municipi_id = m.municipi_id
	INNER JOIN eleccions e ON e.eleccio_id = em.eleccio_id
WHERE em.vots_valids>(4*em.vots_blanc);

-- Per cada provincia de la comunitat_aut_id = 1 i comunitat_aud_id = 2, volem saber el seu nom i el total de vots que ha obtingut cada provincia, a mes, volem saber el nom de la comunitat autonoma.
SELECT 	p.nom AS nom_provincia, 
		sum(vcp.vots) AS vots,
        ca.nom AS nom_comunitat_autonoma 
	FROM provincies p
	INNER JOIN vots_candidatures_prov vcp ON p.provincia_id = vcp.provincia_id
	INNER JOIN comunitats_autonomes ca ON ca.comunitat_aut_id = p.comunitat_aut_id
WHERE ca.comunitat_aut_id IN (1,2)
GROUP BY p.provincia_id