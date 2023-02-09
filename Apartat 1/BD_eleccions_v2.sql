USE Grup2_eleccions;

INSERT INTO eleccions (eleccio_id, nom, data)
VALUES (1,"Eleccions Generals 2019", "2019-04-28"); 
-- Introduccio dades elecció actual

ALTER TABLE candidats 
DROP FOREIGN KEY fk_candidats_persones1; 
-- Eliminem temporalment aquesta clau forana per poder cambiar al camp al que fa referencia

ALTER TABLE persones
MODIFY COLUMN persona_id INT UNSIGNED AUTO_INCREMENT,
MODIFY COLUMN dni CHAR(10) NULL;
-- Modifiquem el camp persona_id per que sigui auto incremental i el camp dni per que pugui tenir valors NULL

ALTER TABLE candidats
ADD CONSTRAINT fk_candidats_persones1 FOREIGN KEY (persona_id)
    REFERENCES persones(persona_id);
-- Tornem a crear la clau forana que vam eliminar previament

ALTER TABLE municipis
DROP CONSTRAINT uk_municipis_codi_ine,
ADD CONSTRAINT uk_municipis_codi_ine_districte_provincia_id UNIQUE (codi_ine,districte,provincia_id);
-- Canviem la restriccio unique per que tambe hi agafi el camp 'districte'

ALTER TABLE vots_candidatures_mun
DROP CONSTRAINT fk_candidatures_municipis_eleccions_municipis1,
ADD CONSTRAINT fk_candidatures_mun_municipis FOREIGN KEY (municipi_id)
    REFERENCES municipis(municipi_id),
ADD CONSTRAINT fk_candidatures_mun_eleccions FOREIGN KEY (eleccio_id)
    REFERENCES eleccions(eleccio_id);
-- Eliminem una clau forana per afegir dues noves que apuntin a les 'taules principals' dels camps corresponents