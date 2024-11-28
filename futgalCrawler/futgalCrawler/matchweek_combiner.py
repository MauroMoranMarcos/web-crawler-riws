import json
import os

# Nombre de la carpeta donde están los archivos JSON
input_folder = "./"  # Asegúrate de que sea el directorio donde están los archivos JSON
output_file = "combined_matches.json"

all_matches = []

# Recorre todos los archivos en la carpeta
for filename in sorted(os.listdir(input_folder)):
    if filename.startswith("quotes_mw") and filename.endswith(".json"):
        file_path = os.path.join(input_folder, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                matches = json.load(file)  # Carga los partidos del archivo actual
                all_matches.extend(matches)  # Añade los partidos a la lista global
        except Exception as e:
            print(f"Error leyendo el archivo {filename}: {e}")

# Escribe todos los partidos en un único archivo JSON
with open(output_file, 'w', encoding='utf-8') as outfile:
    json.dump(all_matches, outfile, ensure_ascii=False, indent=4)

print(f"Archivo combinado generado: {output_file}")