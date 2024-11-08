from elasticsearch import Elasticsearch
import json
from datetime import datetime

# Conexión con ElasticSearch en localhost
es = Elasticsearch(hosts=["http://localhost:9200"])

# Variables para crear secuencialmente doc1, doc2, doc3...

variables = {}
base_name = "doc"

# Documentos a indexar

# Importamos quotes.json

with open('../futgalCrawler/quotes.json', 'r', encoding='utf-8') as file:
    quotes_data = json.load(file)

# Transformar e insertar cada documento en Elasticsearch
for i, quote in enumerate(quotes_data, start=1):
    # Convertir el formato de la fecha a yyyy-MM-dd
    date_str = quote.get("date")
    formatted_date = None
    if date_str:
        try:
            formatted_date = datetime.strptime(date_str.strip(), '%d-%m-%Y').strftime('%Y-%m-%d')
        except ValueError:
            print(f"Fecha inválida en el documento {i}: {date_str}")
            continue  # Saltar este documento si el formato de fecha es incorrecto

    # Comprobar si los campos existen y no son None; de lo contrario, asignar una cadena vacía
    home_team_value = (quote.get("home_team") or "").strip()
    away_team_value = (quote.get("away_team") or "").strip()
    time_value = (quote.get("time") or "").strip()
    field_value = (quote.get("field") or "").strip()
    field_type_value = (quote.get("field_type") or "").strip()
    referee_value = (quote.get("referee") or "").strip()

    # Crear un documento con los campos necesarios
    doc = {
        "home_team": home_team_value,
        "away_team": away_team_value,
        "date": formatted_date,
        "time": time_value,
        "field": field_value,
        "field_type": field_type_value,
        "referee": referee_value,
        "season": quote.get("season", "").strip(),
        "group": quote.get("group", ""),
        "match_week": quote.get("match_week", "")
    }

    if formatted_date:
        doc["date"]: formatted_date
    
    # Insertar el documento en Elasticsearch
    es.index(index="partidos", id=i, body=doc)
    print(f"Documento {i} insertado")

print(f"\nTodos los documentos insertados correctamente.")    
