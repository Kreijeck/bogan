"""
Player Statistics Calculator

Berechnet Statistiken und Rankings für einzelne Spieler.
"""

from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc
from bogan.db.models import Game, PlayerPos, Player
from collections import defaultdict
import bogan.config as cfg


def group_games_by_month(games: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Gruppiert Spiele nach Monaten.
    
    Args:
        games: Liste der Spiele
        
    Returns:
        Dictionary mit Monaten als Keys und Spielen als Values
    """
    months = defaultdict(list)
    
    for game in games:
        if game.get('date'):
            month_key = game['date'].strftime('%Y-%m')  # YYYY-MM Format für Sortierung
            month_display = game['date'].strftime('%B %Y')  # "Januar 2025"
            
            # Deutsche Monatsnamen
            german_months = {
                'January': 'Januar', 'February': 'Februar', 'March': 'März',
                'April': 'April', 'May': 'Mai', 'June': 'Juni',
                'July': 'Juli', 'August': 'August', 'September': 'September',
                'October': 'Oktober', 'November': 'November', 'December': 'Dezember'
            }
            
            for eng, ger in german_months.items():
                month_display = month_display.replace(eng, ger)
            
            game['month_key'] = month_key
            game['month_display'] = month_display
            months[month_key].append(game)
    
    return dict(months)


def get_player_stats(player_name: str, session: Session) -> Dict[str, Any]:
    """
    Berechnet umfassende Statistiken für einen Spieler.
    
    Args:
        player_name: Name des Spielers
        session: SQLAlchemy Session
        
    Returns:
        Dictionary mit Spielerstatistiken
    """
    # Alle Spiele des Spielers holen
    player_games = (
        session.query(Game)
        .join(PlayerPos)
        .join(Player)
        .filter(Player.name == player_name)
        .order_by(desc(Game.datum))
        .all()
    )
    
    if not player_games:
        return {
            'total_games': 0,
            'wins': 0,
            'win_rate': 0,
            'avg_position': 0,
            'best_games': [],
            'recent_games': [],
            'boardgame_stats': {}
        }
    
    # Statistiken sammeln
    total_games = len(player_games)
    wins = 0
    positions = []
    player_counts = []  # Für durchschnittliche Spieleranzahl
    boardgame_performance = defaultdict(list)
    recent_games_data = []
    
    for game in player_games:
        # Finde die Position des Spielers in diesem Spiel
        sorted_players = game.get_sorted_players()
        player_position = None
        player_points = 0
        
        for i, player_data in enumerate(sorted_players):
            if player_data['name'] == player_name:
                player_position = i + 1
                player_points = player_data.get('punkte', 0)
                break
        
        if player_position:
            positions.append(player_position)
            player_counts.append(len(sorted_players))  # Spieleranzahl für dieses Spiel
            
            if player_position == 1:
                wins += 1
            
            # Brettspiel-Performance sammeln
            boardgame_name = game.boardgame.name
            boardgame_performance[boardgame_name].append({
                'position': player_position,
                'points': player_points,
                'total_players': len(sorted_players),
                'date': game.datum,
                'game': game
            })
            
            # Recent games data
            recent_games_data.append({
                'game_id': game.id,  # Hinzugefügte Game ID
                'boardgame_name': game.boardgame.name,
                'boardgame_id': game.boardgame.bgg_id,
                'date': game.datum,
                'date_fmt': game.datum.strftime('%d.%m.%Y') if game.datum else '',
                'position': player_position,
                'points': player_points,
                'total_players': len(sorted_players),
                'location': game.location.name,
                'playtime': game.playtime,
                'won': player_position == 1
            })
    
    # Berechne Durchschnittswerte
    avg_position = sum(positions) / len(positions) if positions else 0
    avg_player_count = sum(player_counts) / len(player_counts) if player_counts else 0
    win_rate = (wins / total_games) * 100 if total_games > 0 else 0
    
    # Beste Brettspiele ermitteln (nur Spiele mit mindestens 2 Partien)
    best_games = []
    for boardgame_name, games_data in boardgame_performance.items():
        game_count = len(games_data)
        
        # Filtere nur Spiele mit mindestens 2 Partien
        if game_count < 2:
            continue
            
        avg_pos = sum(g['position'] for g in games_data) / game_count
        avg_players = sum(g['total_players'] for g in games_data) / game_count
        wins_in_game = sum(1 for g in games_data if g['position'] == 1)
        win_rate_game = (wins_in_game / game_count) * 100
        avg_points = sum(g['points'] for g in games_data) / game_count
        
        # Berechne Performance wie in boardgame_detail.html
        performance = ((avg_players - avg_pos) / (avg_players - 1) * 100) if avg_players > 1 else 0
        
        best_games.append({
            'name': boardgame_name,
            'games_played': game_count,
            'avg_position': round(avg_pos, 2),
            'avg_player_count': round(avg_players, 1),
            'wins': wins_in_game,
            'win_rate': round(win_rate_game, 1),
            'avg_points': round(avg_points, 1),
            'performance': round(performance, 1)
        })
    
    # Sortiere nach Siegquote und dann nach durchschnittlicher Position
    best_games.sort(key=lambda x: (-x['win_rate'], x['avg_position']))
    
    # Gruppiere Spiele nach Monaten
    games_by_month = group_games_by_month(recent_games_data)
    
    return {
        'total_games': total_games,
        'wins': wins,
        'win_rate': round(win_rate, 1),
        'avg_position': round(avg_position, 2),
        'avg_player_count': round(avg_player_count, 1),
        'best_games': best_games[:10],  # Top 10
        'recent_games': recent_games_data,
        'games_by_month': games_by_month,
        'boardgame_stats': dict(boardgame_performance)
    }


def get_all_players(session: Session) -> List[str]:
    """
    Holt alle Spielernamen aus der Datenbank, filtert ignorierte Spieler heraus.
    
    Args:
        session: SQLAlchemy Session
        
    Returns:
        Liste der Spielernamen (ohne ignorierte Spieler)
    """
    players = session.query(Player.name).distinct().all()
    player_names = [player.name for player in players]
    
    # Filtere ignorierte Spieler heraus
    filtered_players = [name for name in player_names if name not in cfg.IGNORED_PLAYERS]
    
    # Sortiere alphabetisch für bessere Übersicht
    return sorted(filtered_players)
