from elasticsearch import Elasticsearch
import json
from datetime import datetime

# Conexión con ElasticSearch en localhost
es = Elasticsearch(hosts=["http://localhost:9200"])

# Variables para crear secuencialmente doc1, doc2, doc3...

variables = {}
base_name = "doc"

# Método auxiliar para eliminar el caracter de los equipos 'B'
def clean_team_name(team_name):
    return team_name.replace(' "B"', '').strip()

# Documentos a indexar

# Importamos quotes.json

with open('../futgalCrawler/combined_matches.json', 'r', encoding='utf-8') as matches_file:
    matches_data = json.load(matches_file)

# Transformar e insertar cada documento en Elasticsearch
for i, match in enumerate(matches_data, start=1):

    # Convertir el formato de la fecha a yyyy-MM-dd
    date_str = match.get("date")
    formatted_date = None
    if date_str:
        try:
            formatted_date = datetime.strptime(date_str.strip(), '%d-%m-%Y').strftime('%Y-%m-%d')
        except ValueError:
            print(f"Fecha inválida en el documento {i}: {date_str}")
            continue  # Saltar este documento si el formato de fecha es incorrecto

    # Comprobar si los campos existen y no son None; de lo contrario, asignar una cadena vacía
    home_team_value = clean_team_name((match.get("home_team") or ""))
    away_team_value = clean_team_name((match.get("away_team") or ""))
    time_value = (match.get("time") or "").strip()
    field_value = (match.get("field") or "").strip()
    referee_value = (match.get("referee") or "").strip()
    category_value = (match.get("category") or "").strip()

    # Buscamos la información asociada al campo de juego en el fichero fields_spider.json
    with open('../futgalCrawler/fields_spider.json', 'r', encoding='utf-8') as fields_file:
        fields_data = json.load(fields_file)

    field = next((item for item in fields_data if item["name"] == field_value), None)

    field_type_value = field["type"] if field else None
    field_direction_value = field["direction"] if field else None
    field_city_value = field["city"] if field else None

    # Buscamos la información asociada a los tres máximos goleadores de cada equipo en el fichero goalscorers_spider.json
    with open('../futgalCrawler/goalscorers_spider.json', 'r', encoding='utf-8') as goalscorers_file:
        goalscorers_data = json.load(goalscorers_file)

    goalscorers_home_team = [doc for doc in goalscorers_data if clean_team_name(doc["team"]) == home_team_value][:3]

    goalscorer1_home_team_name = goalscorers_home_team[0]["name"] if home_team_value and goalscorers_home_team and (len(goalscorers_home_team) >= 1) else None
    goalscorer1_home_team_games_played = goalscorers_home_team[0]["games_played"] if home_team_value and goalscorers_home_team and (len(goalscorers_home_team) >= 1) else None
    goalscorer1_home_team_goals = goalscorers_home_team[0]["goals"] if home_team_value and goalscorers_home_team and (len(goalscorers_home_team) >= 1) else None
    goalscorer1_home_team_goal_ratio = float(goalscorers_home_team[0]["goal_ratio"].replace(',', '.')) if home_team_value and goalscorers_home_team and (len(goalscorers_home_team) >= 1) else None
    goalscorer2_home_team_name = goalscorers_home_team[1]["name"] if home_team_value and goalscorers_home_team and (len(goalscorers_home_team) >= 2) else None
    goalscorer2_home_team_games_played = goalscorers_home_team[1]["games_played"] if home_team_value and goalscorers_home_team and (len(goalscorers_home_team) >= 2) else None
    goalscorer2_home_team_goals = goalscorers_home_team[1]["goals"] if home_team_value and goalscorers_home_team and (len(goalscorers_home_team) >= 2) else None
    goalscorer2_home_team_goal_ratio = float(goalscorers_home_team[1]["goal_ratio"].replace(',', '.')) if home_team_value and goalscorers_home_team and (len(goalscorers_home_team) >= 2) else None
    goalscorer3_home_team_name = goalscorers_home_team[2]["name"] if home_team_value and goalscorers_home_team and (len(goalscorers_home_team) >= 3) else None
    goalscorer3_home_team_games_played = goalscorers_home_team[2]["games_played"] if home_team_value and goalscorers_home_team and (len(goalscorers_home_team) >= 3) else None
    goalscorer3_home_team_goals = goalscorers_home_team[2]["goals"] if home_team_value and goalscorers_home_team and (len(goalscorers_home_team) >= 3) else None
    goalscorer3_home_team_goal_ratio = float(goalscorers_home_team[2]["goal_ratio"].replace(',', '.')) if home_team_value and goalscorers_home_team and (len(goalscorers_home_team) >= 3) else None

    goalscorers_away_team = [doc for doc in goalscorers_data if clean_team_name(doc["team"]) == away_team_value][:3]

    goalscorer1_away_team_name = goalscorers_away_team[0]["name"] if away_team_value and goalscorers_away_team and (len(goalscorers_away_team) >= 1) else None
    goalscorer1_away_team_games_played = goalscorers_away_team[0]["games_played"] if away_team_value and goalscorers_away_team and (len(goalscorers_away_team) >= 1) else None
    goalscorer1_away_team_goals = goalscorers_away_team[0]["goals"] if away_team_value and goalscorers_away_team and (len(goalscorers_away_team) >= 1) else None
    goalscorer1_away_team_goal_ratio = float(goalscorers_away_team[0]["goal_ratio"].replace(',', '.')) if away_team_value and goalscorers_away_team and (len(goalscorers_away_team) >= 1) else None
    goalscorer2_away_team_name = goalscorers_away_team[1]["name"] if away_team_value and goalscorers_away_team and (len(goalscorers_away_team) >= 2) else None
    goalscorer2_away_team_games_played = goalscorers_away_team[1]["games_played"] if away_team_value and goalscorers_away_team and (len(goalscorers_away_team) >= 2) else None
    goalscorer2_away_team_goals = goalscorers_away_team[1]["goals"] if away_team_value and goalscorers_away_team and (len(goalscorers_away_team) >= 2) else None
    goalscorer2_away_team_goal_ratio = float(goalscorers_away_team[1]["goal_ratio"].replace(',', '.')) if away_team_value and goalscorers_away_team and (len(goalscorers_away_team) >= 2) else None
    goalscorer3_away_team_name = goalscorers_away_team[2]["name"] if away_team_value and goalscorers_away_team and (len(goalscorers_away_team) >= 3) else None
    goalscorer3_away_team_games_played = goalscorers_away_team[2]["games_played"] if away_team_value and goalscorers_away_team and (len(goalscorers_away_team) >= 3) else None
    goalscorer3_away_team_goals = goalscorers_away_team[2]["goals"] if away_team_value and goalscorers_away_team and (len(goalscorers_away_team) >= 3) else None
    goalscorer3_away_team_goal_ratio = float(goalscorers_away_team[2]["goal_ratio"].replace(',', '.')) if away_team_value and goalscorers_away_team and (len(goalscorers_away_team) >= 3) else None

    # Crear un documento con los campos necesarios
    doc = {
        "home_team": home_team_value,
        "home_team_goalscorer1_name": goalscorer1_home_team_name,
        "home_team_goalscorer1_games_played": goalscorer1_home_team_games_played,
        "home_team_goalscorer1_goals": goalscorer1_home_team_goals,
        "home_team_goalscorer1_goal_ratio": goalscorer1_home_team_goal_ratio,
        "home_team_goalscorer2_name": goalscorer2_home_team_name,
        "home_team_goalscorer2_games_played": goalscorer2_home_team_games_played,
        "home_team_goalscorer2_goals": goalscorer2_home_team_goals,
        "home_team_goalscorer2_goal_ratio": goalscorer2_home_team_goal_ratio,
        "home_team_goalscorer3_name": goalscorer3_home_team_name,
        "home_team_goalscorer3_games_played": goalscorer3_home_team_games_played,
        "home_team_goalscorer3_goals": goalscorer3_home_team_goals,
        "home_team_goalscorer3_goal_ratio": goalscorer3_home_team_goal_ratio,
        "away_team": away_team_value,
        "away_team_goalscorer1_name": goalscorer1_away_team_name,
        "away_team_goalscorer1_games_played": goalscorer1_away_team_games_played,
        "away_team_goalscorer1_goals": goalscorer1_away_team_goals,
        "away_team_goalscorer1_goal_ratio": goalscorer1_away_team_goal_ratio,
        "away_team_goalscorer2_name": goalscorer2_away_team_name,
        "away_team_goalscorer2_games_played": goalscorer2_away_team_games_played,
        "away_team_goalscorer2_goals": goalscorer2_away_team_goals,
        "away_team_goalscorer2_goal_ratio": goalscorer2_away_team_goal_ratio,
        "away_team_goalscorer3_name": goalscorer3_away_team_name,
        "away_team_goalscorer3_games_played": goalscorer3_away_team_games_played,
        "away_team_goalscorer3_goals": goalscorer3_away_team_goals,
        "away_team_goalscorer3_goal_ratio": goalscorer3_away_team_goal_ratio,
        "date": formatted_date,
        "time": time_value,
        "field": field_value,
        "field_type": field_type_value,
        "field_direction": field_direction_value,
        "field_city": field_city_value,
        "referee": referee_value,
        "category": category_value,
        "season": match.get("season", "").strip(),
        "group": match.get("group", ""),
        "match_week": match.get("match_week", "")
    }

    if formatted_date:
        doc["date"]: formatted_date
    
    # Insertar el documento en Elasticsearch
    body = json.dumps(doc, ensure_ascii=False)
    es.index(index="partidos", id=i, body=body)
    print(f"Documento {i} insertado")

print(f"\nTodos los documentos insertados correctamente.")    
