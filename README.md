# Apartat 1
## Importació de dades bàsiques
Hem agafat el model d'eleccions de l'abril el 2019 i l'hem descarregat, un cop descarregat el model hem obert en el workbench el model,
 en el workbench tenim l'opció d'exportar-lo en DML i obtenir totes les sentències, un cop exportat hem canviat alguns paràmetres per
  adequar a la pràctica.

original_string = "Este es un ejemplo de una cadena de texto"

# Posiciones de los caracteres a separar
separator_positions = [2, 3, 6, 7, 8, 9, 11, 12, 14, 15, 16, 17, 22, 23, 30, 31]

# Crea una lista vacía para almacenar los caracteres separados
separated_chars = []

# Itera sobre cada carácter en la cadena original
for i, char in enumerate(original_string):
    # Si el índice del carácter actual está en la lista de posiciones de separadores
    if i in separator_positions:
        # Agrega una coma antes del carácter actual
        separated_chars.append(",")
    # Agrega el carácter actual a la lista de caracteres separados
    separated_chars.append(char)

# Concatena todos los caracteres en la lista separados y almacena en una nueva cadena
separated_string = "".join(separated_chars)
print(separated_string)
