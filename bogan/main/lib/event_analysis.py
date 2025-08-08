from bogan.utils import load_yaml, get_date, get_db_engine, DateFormat
import bogan.config as cfg

# To Remove?
from sqlalchemy.orm import Session
from bogan.db.models import Game, PlayerPos, Location

engine = get_db_engine()

events = load_yaml(cfg.EVENT_YAML)


def get_game_list(event_name: str, mode: str) -> list[dict]:

    event_dict = events[event_name]
    # Create Filter for all games
    location = event_dict.get("location")
    datum_start = get_date(event_dict.get("datum_start"), DateFormat.YAML)
    datum_ende = get_date(event_dict.get("datum_ende"), DateFormat.YAML)

    with Session(engine) as session:
        match_games = (
            session.query(Game)
            .join(PlayerPos)
            .join(Location)
            .filter(Game.datum >= datum_start, Game.datum <= datum_ende, Location.name == location)
            .all()
        )
        spiele_list = []
        for match in match_games:
            spiel_dict = {}
            spiel_dict["id"] = match.id  # Hinzugefügte Game ID
            spiel_dict["datum"] = match.datum
            spiel_dict["datum_fmt"] = match.datum.strftime("%d.%b %Y")
            spiel_dict["boardgame"] = match.boardgame.name
            spiel_dict["bgg_id"] = match.boardgame.bgg_id
            spiel_dict["playtime"] = match.playtime
            spiel_dict["game_bgg_id"] = match.game_bgg_id
            spiel_dict["img_small"] = match.boardgame.img_small
            
            # Verwende die neue get_sorted_players Methode
            players_data = match.get_sorted_players()
            
            # Filtere Spieler ohne Punkte heraus (falls gewünscht)
            players_with_points = [player for player in players_data if player["punkte"] is not None]
            
            if players_with_points:
                # TODO: wenn keine Playtime gesetzt, soll der Default Wert aus BGG genommen werden
                match_playtime = (
                    match.playtime / 60 if match.playtime > 10 else 0.5
                )  # wenn keine Match Playtime gesetzt wird 30min angenommen
                
                spiel_dict["players"] = create_ranking(
                    players_with_points, mode=mode, playtime_hours=match_playtime, complexity=match.boardgame.weight
                )
            else:
                spiel_dict["players"] = players_data

            spiele_list.append(spiel_dict)

        # Spiele nach Datum sortieren -> neuestes Spiel zuerst
        spiele_list = sorted(spiele_list, key=lambda x: x["datum"], reverse=True)

        return spiele_list


def create_ranking(players, mode='default', playtime_hours=1, complexity=1):
    """
    Erweitert jedes Player-Dictionary um "ranking_point".
    Die "position" ist bereits durch die Game.get_sorted_players() Methode gesetzt.
    
    Regeln:
      - Die 'mode'-Parameter bestimmt den Wertebereich für die Ranking-Punkte:
          * 'default':    +N bis -N       (N = Anzahl der Spieler)
          * 'playtime':   +(N*playtime) bis -(N*playtime)
          * 'complexity': +(N*complexity) bis -(N*complexity)
      - Ranking_Punkte sind linear verteilt und summieren sich über alle Spieler zu 0.
      - Bei Gleichstand: Mittelwert der Ranking_Punkte der betroffenen Ränge.
    """
    # Anzahl der Spieler
    n = len(players)
    
    # Bestimme den Maximalwert (Skalierung) nach Modus
    if mode == 'default':
        max_val = n
    elif mode == 'playtime':
        max_val = n * playtime_hours
    elif mode == 'complexity':
        max_val = n * complexity
    else:
        raise ValueError(f"Unbekannter Modus: {mode}")

    # Schrittweite berechnen
    if n > 1:
        step = (2 * max_val) / (n - 1)
    else:
        # Nur 1 Spieler => Ranking-Punkte = 0
        players[0]['ranking_point'] = 0
        return players

    # Basispunkte pro Rang (1-basiert)
    base_ranking_points = [
        (max_val - (rank - 1) * step) 
        for rank in range(1, n + 1)
    ]
    
    # Gruppiere Spieler nach Position für Gleichstand-Behandlung
    position_groups = {}
    for player in players:
        pos = player['position']
        if pos not in position_groups:
            position_groups[pos] = []
        position_groups[pos].append(player)
    
    # Ranking-Punkte basierend auf Position zuweisen
    for position, group in position_groups.items():
        group_size = len(group)
        
        # Indizes der Basispunkte für diese Gruppe
        start_index = position - 1
        end_index = start_index + group_size
        
        # Mittelwert über die entsprechenden Ränge
        if end_index <= len(base_ranking_points):
            ranks_to_average = base_ranking_points[start_index:end_index]
            avg_points = sum(ranks_to_average) / group_size
        else:
            # Fallback für den Fall, dass nicht genug Basispunkte vorhanden sind
            avg_points = base_ranking_points[start_index] if start_index < len(base_ranking_points) else 0
        
        # Jedem Spieler in der Gruppe die gleichen Punkte zuweisen
        for player_dict in group:
            player_dict['ranking_point'] = round(avg_points, 2)
    
    return players


def prepare_ranking_table(game_list, event_name):
    """
    Bereitet die Ranking-Daten basierend auf der Spielerliste und ignorierten Spielern vor.

    :param game_list: Liste der Spiele mit Spieler- und Punktedaten
    :param ignored_players: Liste der zu ignorierenden Spieler
    :return: Sortiertes Ranking-Dictionary
    """
    ignored_players = events[event_name]["ignored_player"]
    ranking = {}
    for game in game_list:
        for player in game.get("players", []):
            name = player["name"]
            if name in ignored_players:
                continue  # Ignoriere diesen Spieler
            if name not in ranking:
                ranking[name] = {
                    "total": 0,  # Gesamtpunkte
                    "points": [0] * len(game_list),  # Punkte pro Spiel
                    "details": [],  # Details zu jedem Spiel
                }
            # Addiere Ranking-Punkte zur Gesamtpunktzahl
            ranking[name]["total"] += player["ranking_point"]
            # Füge die Punkte des aktuellen Spiels hinzu
            game_index = game_list.index(game)
            ranking[name]["points"][game_index] = player["ranking_point"]
            # Details für dieses Spiel
            ranking[name]["details"].append(
                {
                    "game": game["boardgame"],
                    "position": player["position"],
                    "points": player["ranking_point"],
                    "datum": game["datum_fmt"],
                }
            )

    # Sortiere die Spieler nach Gesamtpunkten absteigend
    sorted_ranking = sorted(ranking.items(), key=lambda x: x[1]["total"], reverse=True)
    return sorted_ranking


def prepare_all_rankings(event_name: str) -> dict:
    """
    Bereitet alle drei Rankings (default, playtime, complexity) auf einmal vor.
    
    :param event_name: Name des Events
    :return: Dictionary mit allen Rankings und Game-Listen
    """
    # Alle drei Game-Listen auf einmal holen
    game_list_default = get_game_list(event_name, mode="default")
    game_list_playtime = get_game_list(event_name, mode="playtime")
    game_list_complexity = get_game_list(event_name, mode="complexity")
    
    # Max Positions berechnen
    max_positions = max(
        (len(game['players']) for game in game_list_default 
         if isinstance(game.get('players'), list)), 
        default=0
    )
    
    # Alle Rankings berechnen
    ranking_default = prepare_ranking_table(game_list_default, event_name)
    ranking_playtime = prepare_ranking_table(game_list_playtime, event_name)
    ranking_complexity = prepare_ranking_table(game_list_complexity, event_name)
    
    return {
        "games": game_list_default,
        "max_positions": max_positions,
        "ranking_default": ranking_default,
        "ranking_playtime": ranking_playtime,
        "ranking_complexity": ranking_complexity
    }


if __name__ == "__main__":
    for game in get_game_list("Mittwochsrunde 2025"):
        print(game)
