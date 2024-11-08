from elasticsearch import Elasticsearch

# Conexión con ElasticSearch en localhost
es = Elasticsearch(hosts=["http://localhost:9200"])

# Nombre del íncice
index_name = "partidos"

# Define el mapeo de campos (estructura del documento)
mapping = {
    "mappings": {
        "properties": {
            "home_team": {"type": "text"},
            "away_team": {"type": "text"},
            "date": {"type": "date"},
            "time": {"type": "text"},
            "field": {"type": "text"},
            "field_type": {"type": "text"},
            "referee": {"type": "text"},
            "season": {"type": "text"},
            "group": {"type": "text"},
            "match_week": {"type": "float"},
        }
    }
}

# Crea el íncice
es.indices.create(index=index_name, body=mapping)
print(f"Indice '{index_name}' creado correctamente.")