from elasticsearch import Elasticsearch

# Conexión con ElasticSearch en localhost
es = Elasticsearch(hosts=["http://localhost:9200"])

# Nombre del íncice
index_name = "fields"

# Define el mapeo de campos (estructura del documento)
mapping = {
    "mappings": {
        "properties": {
            "name": {"type": "text"},
            "direction": {"type": "text"},
            "city": {"type": "text"},
            "type": {"type": "text"},
        }
    }
}

# Crea el íncice
es.indices.create(index=index_name, body=mapping)
print(f"Indice '{index_name}' creado correctamente.")