original_string = "022019041502970200010400000049000"

# Posiciones de los caracteres a separar
separator_positions = [2, 6, 8, 9, 11, 14, 16, 22, 30]

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
