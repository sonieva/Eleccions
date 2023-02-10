USE Grup2_eleccions;

INSERT INTO eleccions (eleccio_id, nom, data)
VALUES (1,"Eleccions Generals 2019", "2019-04-28");

ALTER TABLE candidats 
DROP FOREIGN KEY fk_candidats_persones1;

ALTER TABLE persones
MODIFY COLUMN dni char(10) NULL,
MODIFY COLUMN persona_id INT UNSIGNED AUTO_INCREMENT;

ALTER TABLE candidats
ADD CONSTRAINT fk_candidats_persones1 FOREIGN KEY (persona_id)
    REFERENCES persones(persona_id);

ALTER TABLE municipis
DROP CONSTRAINT uk_municipis_codi_ine,
ADD CONSTRAINT uk_municipis_codi_ine_districte_provincia_id UNIQUE (codi_ine,districte,provincia_id);

ALTER TABLE vots_candidatures_mun
DROP CONSTRAINT fk_candidatures_municipis_eleccions_municipis1,
ADD CONSTRAINT fk_eleccions_municipis_municipis FOREIGN KEY (municipi_id)
    REFERENCES municipis(municipi_id),
ADD CONSTRAINT fk_eleccions_municipis_eleccions FOREIGN KEY (eleccio_id)
    REFERENCES eleccions(eleccio_id);