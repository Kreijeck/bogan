"""
Game Detail Processing Library

This module contains functions for processing and formatting game detail data
for display in the game detail template.
"""

from typing import Dict, Any, List
from sqlalchemy.orm import Session
from bogan.db.models import Game


def get_game_detail_data(game_id: int, session: Session) -> Dict[str, Any]:
    """
    Lädt und verarbeitet alle Daten für die Game Detail Seite.
    
    Args:
        game_id: Die eindeutige ID der Partie in der Datenbank
        session: SQLAlchemy Session
        
    Returns:
        Dictionary mit allen verarbeiteten Daten für das Template
        
    Raises:
        ValueError: Wenn das Spiel nicht gefunden wird
    """
    # Lade das Spiel mit allen zugehörigen Daten
    game = session.query(Game).filter(Game.id == game_id).first()
    
    if not game:
        raise ValueError(f"Partie mit ID {game_id} nicht gefunden")
    
    # Hole sortierte Spieler-Positionen
    sorted_players = game.get_sorted_players()
    
    # Erstelle Datenstruktur für das Template
    game_data = {
        'id': game.id,
        'datum': game.datum,
        'datum_fmt': game.datum.strftime('%d.%m.%Y') if game.datum else 'Unbekannt',
        'wochentag_fmt': _translate_weekday(game.datum.strftime('%A')) if game.datum else 'Unbekannt',
        'boardgame': {
            'id': game.boardgame.bgg_id,
            'name': game.boardgame.name,
            'img': game.boardgame.img,
            'img_small': game.boardgame.img_small,
            'playtime': game.boardgame.playtime,
            'weight': game.boardgame.weight,
            'minplayers': game.boardgame.minplayers,
            'maxplayers': game.boardgame.maxplayers,
            'yearpublished': getattr(game.boardgame, 'yearpublished', None),
        },
        'location': {
            'name': game.location.name,
            'id': game.location.id
        },
        'playtime': game.playtime,
        'playtime_fmt': _format_playtime(game.playtime),
        'player_count': len(sorted_players),
        'players': _process_player_data(sorted_players)
    }
    
    return game_data


def _translate_weekday(english_weekday: str) -> str:
    """
    Übersetzt englische Wochentagsnamen ins Deutsche.
    
    Args:
        english_weekday: Englischer Wochentagsname
        
    Returns:
        Deutscher Wochentagsname
    """
    weekday_names = {
        'Monday': 'Montag', 
        'Tuesday': 'Dienstag', 
        'Wednesday': 'Mittwoch',
        'Thursday': 'Donnerstag', 
        'Friday': 'Freitag', 
        'Saturday': 'Samstag', 
        'Sunday': 'Sonntag'
    }
    return weekday_names.get(english_weekday, english_weekday)


def _format_playtime(playtime: int) -> str:
    """
    Formatiert die Spielzeit für die Anzeige.
    
    Args:
        playtime: Spielzeit in Minuten
        
    Returns:
        Formatierte Spielzeit als String
    """
    if playtime and playtime > 0:
        return f"{playtime} Minuten"
    return "Unbekannt"


def _process_player_data(sorted_players: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Verarbeitet die Spieler-Daten für die Template-Anzeige.
    
    Args:
        sorted_players: Liste der sortierten Spieler-Daten
        
    Returns:
        Liste der verarbeiteten Spieler-Daten für das Template
    """
    processed_players = []
    
    for i, player_info in enumerate(sorted_players, 1):
        player_data = {
            'position': i,
            'name': player_info['name'],
            'points': player_info.get('punkte', 0),
            'is_winner': i == 1,
            'position_suffix': _get_position_suffix(i)
        }
        processed_players.append(player_data)
    
    return processed_players


def _get_position_suffix(position: int) -> str:
    """
    Gibt das entsprechende Suffix für eine Position zurück.
    
    Args:
        position: Position des Spielers
        
    Returns:
        Positions-Suffix (momentan immer 'ter')
    """
    # Für deutsche Ordinalzahlen: 1ter, 2ter, 3ter, etc.
    return 'ter'
