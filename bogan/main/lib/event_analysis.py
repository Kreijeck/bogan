import itertools

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
            spiel_dict["datum"] = match.datum
            spiel_dict["datum_fmt"] = match.datum.strftime("%d.%b %Y")
            spiel_dict["name"] = match.boardgame.name
            spiel_dict["playtime"] = match.playtime
            spiel_dict["game_bgg_id"] = match.game_bgg_id
            spiel_dict["img_small"] = match.boardgame.img_small
            # Get Players and sort
            players_tmp = []
            for player in match.player_pos:
                players_tmp.append({"name": player.player.name, "punkte": player.points})

            # Sortiere nach Punkten, wenn vorhanden, ansonsten wird die Reihenfolge beibehalten
            players_tmp = [player for player in players_tmp if player["punkte"] is not None]
            if players_tmp:
                players_tmp = sorted(players_tmp, key=lambda x: x["punkte"], reverse=True)
                # TODO: wenn keine Playtime gesetzt, soll der Default Wert aus BGG genommen werden
                match_playtime = (
                    match.playtime / 60 if match.playtime > 10 else 0.5
                )  # wenn keine Match Playtime gesetzt wird 30min angenommen
                spiel_dict["players"] = create_ranking(
                    players_tmp, mode=mode, playtime_hours=match_playtime, complexity=match.boardgame.weight
                )
            else:
                spiel_dict["players"] = players_tmp

            spiele_list.append(spiel_dict)

        # Spiele nach Datum sortieren -> neuestes Spiel zuerst
        spiele_list = sorted(spiele_list, key=lambda x: x["datum"], reverse=True)

        return spiele_list


def create_ranking(players, mode='default', playtime_hours=1, complexity=1):
    """
    Erweitert jedes Player-Dictionary um:
        - "position"
        - "ranking_point"
    
    Regeln:
      - Sortierung absteigend nach 'punkte'.
      - Gleiche Punktzahl => gleiche Position (Standard Competition Ranking).
      - Die 'mode'-Parameter bestimmt den Wertebereich für die Ranking-Punkte:
          * 'default':    +N bis -N       (N = Anzahl der Spieler)
          * 'playtime':   +(N*playtime) bis -(N*playtime)
          * 'complexity': +(N*complexity) bis -(N*complexity)
      - Ranking_Punkte sind linear verteilt und summieren sich über alle Spieler zu 0.
      - Bei Gleichstand: Mittelwert der Ranking_Punkte der betroffenen Ränge.
      - playtime und complexity werden einmal pro Spiel global verwendet.
    """
    # Anzahl der Spieler
    n = len(players)
    
    # 1. Spieler nach Punkten absteigend sortieren
    sorted_players = sorted(players, key=lambda x: x['punkte'], reverse=True)
    
    # 2. Gruppieren nach gleicher Punktzahl
    groups = []
    for points, group in itertools.groupby(sorted_players, key=lambda x: x['punkte']):
        groups.append(list(group))

    # 3. Bestimme den Maximalwert (Skalierung) nach Modus
    if mode == 'default':
        max_val = n
    elif mode == 'playtime':
        max_val = n * playtime_hours
    elif mode == 'complexity':
        max_val = n * complexity
    else:
        raise ValueError(f"Unbekannter Modus: {mode}")

    # 4. Schrittweite berechnen
    #    Wir verteilen von +max_val bis -max_val => Gesamtbreite = 2*max_val
    #    Auf N Positionen => (N - 1) Zwischenräume
    if n > 1:
        step = (2 * max_val) / (n - 1)
    else:
        # Nur 1 Spieler => Ranking-Punkte = 0
        step = 0

    # 5. Basispunkte pro Rang (1-basiert)
    base_ranking_points = [
        (max_val - (rank - 1) * step) 
        for rank in range(1, n + 1)
    ]
    
    # 6. Rangzuweisung unter Berücksichtigung von Gleichständen
    current_rank = 1
    for group in groups:
        group_size = len(group)
        
        # Indizes der Basispunkte für diese Gruppe
        start_index = current_rank - 1
        end_index   = start_index + group_size
        
        # Mittelwert über die entsprechenden Ränge (z.B. [2,3] bei group_size=2)
        ranks_to_average = base_ranking_points[start_index:end_index]
        avg_points = sum(ranks_to_average) / group_size
        
        # Jedem Spieler in der Gruppe den gleichen Rang & gleiche Punkte
        for player_dict in group:
            player_dict['position'] = current_rank
            player_dict['ranking_point'] = round(avg_points, 2)
        
        # Überspringen bei Gleichständen:
        # z.B. wenn 2 Spieler auf Rang 2 stehen, bekommt der nächste den Rang 4
        current_rank += group_size
    
    return sorted_players


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
                    "game": game["name"],
                    "position": player["position"],
                    "points": player["ranking_point"],
                    "datum": game["datum_fmt"],
                }
            )

    # Sortiere die Spieler nach Gesamtpunkten absteigend
    sorted_ranking = sorted(ranking.items(), key=lambda x: x[1]["total"], reverse=True)
    return sorted_ranking


if __name__ == "__main__":
    for game in get_game_list("Mittwochsrunde 2025"):
        print(game)
