USE Grup2_eleccions;

INSERT INTO eleccions (eleccio_id, nom, data)
VALUES (1,"Eleccions Generals 2019", "2019-04-28")

ALTER TABLE candidats 
DROP FOREIGN KEY fk_candidats_persones1;

ALTER TABLE persones
MODIFY COLUMN dni char(9) NULL,
MODIFY COLUMN persona_id INT UNSIGNED AUTO_INCREMENT;

ALTER TABLE candidats
ADD CONSTRAINT fk_candidats_persones1 FOREIGN KEY (persona_id)
    REFERENCES persones(persona_id);