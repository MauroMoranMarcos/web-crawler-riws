from elasticsearch import Elasticsearch

# Conexión con ElasticSearch en localhost
es = Elasticsearch(hosts=["http://localhost:9200"])

# Definimos la consulta de búsqueda. Esta consulta muestra por orden de relevancia.
simple_query = {
    "query": {
        "match": {
            "referee": "Jose"
        }
    }
}

# Ejecutar la búsqueda
res = es.search(index="partidos", body=simple_query)

# Imprimimos los resultados de la búsqueda
print("\n\nResultados de la búsqueda de partidos por árbitro 'Jose':\n")
for hit in res['hits']['hits']:
    print(hit["_source"])

# Definimos la búsqueda con filtros. Falta filter.
range_query = {
    "query": {
        "bool": {
            "must": [
                {"match": {"field": "Milladoiro"}}
            ],
        }
    }
}

# Ejecutar la búsqueda
res = es.search(index="partidos", body=range_query)

# Imprimimos los resultados de la búsqueda
print("\n\nResultados de la búsqueda de partidos jugados en 'Milladoiro':\n")
for hit in res['hits']['hits']:
    print(hit["_source"])