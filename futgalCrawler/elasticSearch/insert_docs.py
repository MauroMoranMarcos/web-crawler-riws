from elasticsearch import Elasticsearch

# Conexión con ElasticSearch en localhost
es = Elasticsearch(hosts=["http://localhost:9200"])

# Documentos a indexar

doc1 = {
    "home_team": "Santa Marta",
    "away_team": "Sporting Santiago",
    "date": "2024-11-10",
    "time": "18:00",
    "field": "Conxo",
    "field_type": "Hierba artificial",
    "referee": "Manolo el del bombo",
    "season": "2024-25",
    "group": "Tercara futgal grupo 3",
    "match_week": 9
}

doc2 = {
    "home_team": "Santa Marta",
    "away_team": "Resmon",
    "date": "2024-11-17",
    "time": "12:00",
    "field": "USC",
    "field_type": "Hierba artificial",
    "referee": "Manolo el del bombo",
    "season": "2024-25",
    "group": "Tercara futgal grupo 3",
    "match_week": 10
}

doc3 = {
    "home_team": "Sporting Santiago",
    "away_team": "Fatima",
    "date": "2024-11-17",
    "time": "18:00",
    "field": "Conxo",
    "field_type": "Hierba artificial",
    "referee": "Julio",
    "season": "2024-25",
    "group": "Tercara futgal grupo 3",
    "match_week": 10
}

es.index(index="partidos", id=1, body=doc1)
es.index(index="partidos", id=2, body=doc2)
es.index(index="partidos", id=3, body=doc3)