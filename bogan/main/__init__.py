from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy.orm import Session

from bogan.main.lib.event_analysis import prepare_all_rankings
from bogan.main.lib.fetch_db import get_boardgame_by, get_games_by, get_all_boardgames, engine
from bogan.main.lib.boardgame_ranking import calculate_player_ranking, get_boardgame_stats
from bogan.main.lib.player_stats import get_player_stats, get_all_players
from bogan.main.lib.game_detail import get_game_detail_data
from bogan.db.models import Game, Boardgame, Location
from bogan.utils import load_yaml
import bogan.config as cfg
from datetime import datetime

main = Blueprint("main", __name__, template_folder="templates")


@main.route("/")
def index():
    # Hole die letzten 10 Spiele für die Statistik-Sektion
    with Session(engine) as session:
        latest_games = (
            session.query(Game)
            .join(Boardgame)
            .join(Location)
            .order_by(Game.datum.desc())
            .limit(10)
            .all()
        )
        
        # Konvertiere zu Dictionary für Template
        games_data = []
        for game in latest_games:
            # Hole die sortierten Spieler
            sorted_players = game.get_sorted_players()
            winner = sorted_players[0] if sorted_players else None
            
            games_data.append({
                'datum': game.datum,
                'datum_fmt': game.datum.strftime('%d.%m.%Y') if game.datum else '',
                'boardgame_name': game.boardgame.name,
                'boardgame_id': game.boardgame.bgg_id,
                'img_small': game.boardgame.img_small,
                'location': game.location.name,
                'player_count': len(game.player_pos),
                'winner': winner['name'] if winner else 'Unbekannt',
                'playtime': game.playtime
            })
    
    # Lade Events aus der YAML-Datei
    events = load_yaml(cfg.EVENT_YAML)
    events_data = []
    for event_name, event_info in events.items():
        # Parse Datumsangaben
        try:
            start_date = datetime.strptime(event_info['datum_start'], '%d.%m.%Y')
            end_date = datetime.strptime(event_info['datum_ende'], '%d.%m.%Y')
            
            events_data.append({
                'name': event_name,
                'location': event_info['location'],
                'start_date': start_date,
                'end_date': end_date,
                'start_date_fmt': start_date.strftime('%d.%m.%Y'),
                'end_date_fmt': end_date.strftime('%d.%m.%Y'),
                'is_future': start_date > datetime.now(),
                'is_current': start_date <= datetime.now() <= end_date
            })
        except (ValueError, KeyError):
            # Überspringe Events mit ungültigen Daten
            continue
    
    # Sortiere Events nach Startdatum (neueste zuerst)
    events_data.sort(key=lambda x: x['start_date'], reverse=True)
    
    # Erstelle zusätzlich eine nach Namen sortierte Liste für die Navigation
    events_nav = sorted(events_data, key=lambda x: x['name'])
    
    return render_template("index.html", latest_games=games_data, events=events_nav)


@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html", name=current_user.name)


@main.route("/search")
def search():
    return render_template("search.html")


@main.route("/add_game", methods=["POST"])
def add_game():
    pass

@main.route("/event/<path:event>", methods=["GET"])
def show_event(event: str):
    # Alle Rankings und Daten auf einmal berechnen
    event_data = prepare_all_rankings(event)
    
    return render_template(
        "event.html",
        games=event_data["games"],
        max_positions=event_data["max_positions"],
        ranking_default=event_data["ranking_default"],
        ranking_playtime=event_data["ranking_playtime"],
        ranking_complexity=event_data["ranking_complexity"],
    )

@main.route("/boardgame/<path:boardgame_id>", methods=["GET"])
def show_boardgame(boardgame_id: str):
    with Session(engine) as session:
        boardgame = get_boardgame_by(boardgame_id, session)
        games = get_games_by(boardgame_id, session)
        
        # Berechne Spieler-Rankings für dieses Brettspiel
        ranking_data = calculate_player_ranking(games)
        
        # Berechne allgemeine Spielstatistiken
        game_stats = get_boardgame_stats(games)
        
        return render_template("boardgame_detail.html", 
                             boardgame=boardgame, 
                             games=games, 
                             player_ranking=ranking_data,
                             game_stats=game_stats)

@main.route("/boardgames", methods=["GET"])    
def show_all_boardgames():
    with Session(engine) as session:
        boardgames = get_all_boardgames(session)

        return render_template("boardgames_overview.html", boardgames=boardgames)


@main.route("/players", methods=["GET"])
def show_all_players():
    with Session(engine) as session:
        players = get_all_players(session)
        return render_template("players_overview.html", players=players)


@main.route("/player/<path:player_name>", methods=["GET"])
def show_player(player_name: str):
    with Session(engine) as session:
        player_data = get_player_stats(player_name, session)
        return render_template("player_detail.html", 
                             player_name=player_name, 
                             player_data=player_data)


@main.route("/game/<int:game_id>", methods=["GET"])
def show_game(game_id: int):
    """
    Zeigt Details einer einzelnen gespielten Partie.
    
    Args:
        game_id: Die eindeutige ID der Partie in der Datenbank
    """
    with Session(engine) as session:
        try:
            game_data = get_game_detail_data(game_id, session)
            return render_template("game_detail.html", game=game_data)
        except ValueError as e:
            # Wenn Spiel nicht gefunden wird, zur Übersicht weiterleiten
            return render_template("error.html", 
                                 error_message=str(e), 
                                 error_code=404), 404


@main.route("/game", methods=["GET"])
def show_game_legacy():
    """Legacy route - leitet zur Spieleübersicht weiter"""
    return render_template("boardgames_overview.html")




