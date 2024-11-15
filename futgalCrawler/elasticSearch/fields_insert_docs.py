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

with open('../futgalCrawler/fields.json', 'r', encoding='utf-8') as file:
    fields_data = json.load(file)

# Transformar e insertar cada documento en Elasticsearch
for i, field in enumerate(fields_data, start=1):
    # Comprobar si los campos existen y no son None; de lo contrario, asignar una cadena vacía
    name_value = (field.get("name") or "").strip()
    direction_value = (field.get("direction") or "").strip()
    city_value = (field.get("city") or "").strip()
    type_value = (field.get("type") or "").strip()

    # Crear un documento con los campos necesarios
    doc = {
        "name": name_value,
        "direction": direction_value,
        "city": city_value,
        "type": type_value,
    }
    
    # Insertar el documento en Elasticsearch
    es.index(index="fields", id=i, body=doc)
    print(f"Documento {i} insertado")

print(f"\nTodos los documentos insertados correctamente.")    
