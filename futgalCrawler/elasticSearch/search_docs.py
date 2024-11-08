from elasticsearch import Elasticsearch

# Conexión con ElasticSearch en localhost
es = Elasticsearch(hosts=["http://localhost:9200"])

# Definimos la consulta de búsqueda
simple_query = {
    "query": {
        "match": {
            "home_team": "Santa Marta"
        }
    }
}

# Ejecutar la búsqueda
res = es.search(index="partidos", body=simple_query)

# Imprimimos los resultados de la búsqueda
print("Resultados de la búsqueda de partidos:")
for hit in res['hits']['hits']:
    print(hit["_source"])

# Definimos la búsqueda con filtros. Falta filter
range_query = {
    "query": {
        "bool": {
            "must": [
                {"match": {"match_week": 10}}
            ],
        }
    }
}

# Ejecutar la búsqueda
res = es.search(index="partidos", body=range_query)

# Imprimimos los resultados de la búsqueda
print("Resultados de la búsqueda de partidos:")
for hit in res['hits']['hits']:
    print(hit["_source"])