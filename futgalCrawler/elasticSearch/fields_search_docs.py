from elasticsearch import Elasticsearch

# Conexión con ElasticSearch en localhost
es = Elasticsearch(hosts=["http://localhost:9200"])

# Definimos la consulta de búsqueda. Esta consulta muestra por orden de relevancia.
simple_query = {
    "query": {
        "match": {
            "type": "Tierra"
        }
    },
    "size": 1503
}

# Ejecutar la búsqueda
res = es.search(index="fields", body=simple_query)

# Imprimimos los resultados de la búsqueda
print("\n\nResultados de la búsqueda de campos de tierra:\n")
for hit in res['hits']['hits']:
    print(hit["_source"])

# Definimos la búsqueda con filtros. Falta filter.
range_query = {
    "query": {
        "bool": {
            "must": [
                {"match": {"name": "Sagrada"}}
            ],
        }
    }
}

# Ejecutar la búsqueda
res = es.search(index="fields", body=range_query)

# Imprimimos los resultados de la búsqueda
print("\n\nResultados de la búsqueda de campos que se llamen o sean de 'Sagrada':\n")
for hit in res['hits']['hits']:
    print(hit["_source"])