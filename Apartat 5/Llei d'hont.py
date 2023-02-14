import mysql.connector
conexion = mysql.connector.connect(
    host='10.94.255.166',
    user="perepi",
    password="pastanaga",
    database="Grup2_eleccions"
)

x = input("Introdueix la provincia de la cual vols la informació? ").lower()
cursor = conexion.cursor()
cursor.execute(
    f"SELECT sum(vots) as vots from vots_candidatures_prov where provincia_id=(SELECT provincia_id FROM provincies WHERE lower(nom)='{x}')")
vots_totals = cursor.fetchone()
cursor.execute(
    f"SELECT sum(vots_blanc) as VotsBlancs FROM eleccions_municipis em INNER JOIN municipis m on m.municipi_id=em.municipi_id WHERE m.provincia_id=(SELECT provincia_id FROM provincies WHERE lower(nom)='{x}')")
vots_blancs = cursor.fetchone()
cursor.execute(
    f"SELECT sum(vots_nuls) as VotsNuls FROM eleccions_municipis em INNER JOIN municipis m on m.municipi_id=em.municipi_id WHERE m.provincia_id=(SELECT provincia_id FROM provincies WHERE lower(nom)='{x}')")
vots_nulls = cursor.fetchone()
cursor.execute(f"SELECT num_escons FROM provincies WHERE nom = '{x}';")
esconss = cursor.fetchone()
cursor.execute(
    f"Select  nom_curt, vp.vots  from provincies p INNER JOIN  vots_candidatures_prov vp on vp.provincia_id=p.provincia_id INNER JOIN candidatures c on c.candidatura_id = vp.candidatura_id where p.provincia_id=(SELECT provincia_id FROM provincies WHERE lower(nom) = '{x}') and vp.vots/(SELECT sum(vots) as vots FROM vots_candidatures_prov where provincia_id = (SELECT provincia_id FROM provincies WHERE lower(nom) = '{x}')) * 100 >= 3;")
partit_vots = cursor.fetchall()

llista = []
print(f"\nPROVINCIA DE {x.upper()}")
print("-"*30)
print(f"Vots: {vots_totals[0]}")
print(f"Vots Blanc: {vots_blancs[0]}")
print(f"Vots Nuls: {vots_nulls[0]}")
for partit, vots in partit_vots:
    for i in range(1, esconss[0]+1):
        element = f"{vots/i:15.3f},{partit}"
        llista.append(element)
llistaEscons = sorted(zip(llista), reverse=True)[:esconss[0]]
PartitsEscons = {}
for item in llistaEscons:
    nom = item[0].strip().split(',')[1]
    if nom in PartitsEscons:
        PartitsEscons[nom] += 1
    else:
        PartitsEscons[nom] = 1
for partit2, escons2 in PartitsEscons.items():
    print(f"{partit2} : {escons2}")
