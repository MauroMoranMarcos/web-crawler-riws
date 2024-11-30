from elasticsearch import Elasticsearch

# Conexión con ElasticSearch en localhost
es = Elasticsearch(hosts=["http://localhost:9200"])

# Nombre del íncice
index_name = "partidos"

# Define el mapeo de campos (estructura del documento)
mapping = {
    "mappings": {
        "properties": {
            "home_team": {"type": "text", "fields": {"suggest": {"type": "completion"}}},
            "home_team_goalscorer1_name": {"type": "text"},
            "home_team_goalscorer1_games_played": {"type": "float"},
            "home_team_goalscorer1_goals": {"type": "float"},
            "home_team_goalscorer1_goal_ratio": {"type": "float"},
            "home_team_goalscorer2_name": {"type": "text"},
            "home_team_goalscorer2_games_played": {"type": "float"},
            "home_team_goalscorer2_goals": {"type": "float"},
            "home_team_goalscorer2_goal_ratio": {"type": "float"},
            "home_team_goalscorer3_name": {"type": "text"},
            "home_team_goalscorer3_games_played": {"type": "float"},
            "home_team_goalscorer3_goals": {"type": "float"},
            "home_team_goalscorer3_goal_ratio": {"type": "float"},
            "away_team": {"type": "text", "fields": {"suggest": {"type": "completion"}}},
            "away_team_goalscorer1_name": {"type": "text"},
            "away_team_goalscorer1_games_played": {"type": "float"},
            "away_team_goalscorer1_goals": {"type": "float"},
            "away_team_goalscorer1_goal_ratio": {"type": "float"},
            "away_team_goalscorer2_name": {"type": "text"},
            "away_team_goalscorer2_games_played": {"type": "float"},
            "away_team_goalscorer2_goals": {"type": "float"},
            "away_team_goalscorer2_goal_ratio": {"type": "float"},
            "away_team_goalscorer3_name": {"type": "text"},
            "away_team_goalscorer3_games_played": {"type": "float"},
            "away_team_goalscorer3_goals": {"type": "float"},
            "away_team_goalscorer3_goal_ratio": {"type": "float"},
            "date": {"type": "date"},
            "time": {"type": "text"},
            "field": {"type": "text", "fields": {"suggest": {"type": "completion"}}},
            "field_type": {"type": "text"},
            "field_direction": {"type": "text"},
            "field_city": {"type": "keyword"},
            "referee": {"type": "text"},
            "season": {"type": "text"},
            "group": {"type": "text"},
            "match_week": {"type": "float"},
        }
    }
}

if es.indices.exists(index=index_name):
    confirm = input(f"El índice '{index_name}' ya existe. ¿Quieres eliminarlo y recrearlo? (y/n): ").strip().lower()
    if confirm == 'y':
        es.indices.delete(index=index_name)
        print(f"Índice '{index_name}' eliminado.")
        es.indices.create(index=index_name, body=mapping)
        print(f"Índice '{index_name}' creado nuevamente.")
    else:
        print("Operación cancelada. El índice no se ha modificado.")
else:
    # Crea el íncice
    es.indices.create(index=index_name, body=mapping)
    print(f"Indice '{index_name}' creado correctamente.")
