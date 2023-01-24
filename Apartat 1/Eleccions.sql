USE Grup2_eleccions;
#Volem extreuer el fitxer 01

INSERT INTO eleccions (eleccio_id, nom, data)
VALUES (1,"Eleccions Generals 2019", "2019-04-28")

ALTER TABLE personas
MODIFY COLUMN dni char(10) NULL;
