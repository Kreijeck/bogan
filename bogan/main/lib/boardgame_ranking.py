"""
Boardgame Ranking Calculator

Berechnet Spieler-Rankings und Statistiken für einzelne Brettspiele.
"""

from typing import List, Dict, Any


def calculate_player_ranking(games: List) -> List[Dict[str, Any]]:
    """
    Berechnet das Spieler-Ranking für ein spezifisches Brettspiel.
    
    Args:
        games: Liste der Game-Objekte für ein Brettspiel
        
    Returns:
        Liste von Spieler-Statistiken sortiert nach durchschnittlicher Position
    """
    player_stats = {}
    
    for game in games:
        sorted_players = game.get_sorted_players()
        
        for i, player_data in enumerate(sorted_players):
            player_name = player_data['name']
            position = i + 1
            points = player_data.get('punkte', 0)  # Verwende 'punkte' statt 'points'
            
            if player_name not in player_stats:
                player_stats[player_name] = {
                    'name': player_name,
                    'games_played': 0,
                    'total_points': 0,
                    'wins': 0,
                    'positions': [],
                    'best_score': None,
                    'worst_score': None
                }
            
            stats = player_stats[player_name]
            stats['games_played'] += 1
            stats['total_points'] += points
            stats['positions'].append(position)
            
            if position == 1:
                stats['wins'] += 1
            
            if stats['best_score'] is None or points > stats['best_score']:
                stats['best_score'] = points
            
            if stats['worst_score'] is None or points < stats['worst_score']:
                stats['worst_score'] = points
    
    # Berechne durchschnittliche Werte und sortiere
    ranking_data = []
    for player_name, stats in player_stats.items():
        if stats['games_played'] > 0:
            avg_points = stats['total_points'] / stats['games_played']
            avg_position = sum(stats['positions']) / len(stats['positions'])
            win_rate = (stats['wins'] / stats['games_played']) * 100
            
            ranking_data.append({
                'name': player_name,
                'games_played': stats['games_played'],
                'avg_points': round(avg_points, 1),
                'avg_position': round(avg_position, 2),
                'win_rate': round(win_rate, 1),
                'wins': stats['wins'],
                'total_points': stats['total_points'],
                'best_score': stats['best_score'],
                'worst_score': stats['worst_score']
            })
    
    # Sortiere nach durchschnittlicher Position (besser = niedriger)
    ranking_data.sort(key=lambda x: x['avg_position'])
    
    return ranking_data


def get_boardgame_stats(games: List) -> Dict[str, Any]:
    """
    Berechnet allgemeine Statistiken für ein Brettspiel.
    
    Args:
        games: Liste der Game-Objekte
        
    Returns:
        Dictionary mit allgemeinen Spielstatistiken
    """
    if not games:
        return {
            'total_games': 0,
            'avg_points': 0,
            'highest_score': 0,
            'lowest_score': 0,
            'avg_playtime': 0,
            'unique_players': 0
        }
    
    all_scores = []
    total_playtime = 0
    valid_playtimes = 0
    unique_players = set()
    
    for game in games:
        sorted_players = game.get_sorted_players()
        
        for player_data in sorted_players:
            points = player_data.get('punkte', 0)
            all_scores.append(points)
            unique_players.add(player_data['name'])
        
        if game.playtime and game.playtime > 0:
            total_playtime += game.playtime
            valid_playtimes += 1
    
    avg_points = sum(all_scores) / len(all_scores) if all_scores else 0
    avg_playtime = total_playtime / valid_playtimes if valid_playtimes > 0 else 0
    
    return {
        'total_games': len(games),
        'avg_points': round(avg_points, 1),
        'highest_score': max(all_scores) if all_scores else 0,
        'lowest_score': min(all_scores) if all_scores else 0,
        'avg_playtime': round(avg_playtime),
        'unique_players': len(unique_players)
    }


def get_boardgame_insights(games: List) -> Dict[str, Any]:
    """
    Berechnet zusätzliche Insights für ein Brettspiel.
    
    Args:
        games: Liste der Game-Objekte
        
    Returns:
        Dictionary mit Insights wie Gesamtanzahl Spiele, durchschnittliche Spielzeit, etc.
    """
    if not games:
        return {
            'total_games': 0,
            'avg_playtime': 0,
            'total_players': 0,
            'unique_players': 0
        }
    
    total_games = len(games)
    total_playtime = sum(game.playtime for game in games if game.playtime)
    avg_playtime = total_playtime / total_games if total_games > 0 else 0
    
    unique_players = set()
    total_player_instances = 0
    
    for game in games:
        for player_pos in game.player_pos:
            unique_players.add(player_pos.player.name)
            total_player_instances += 1
    
    return {
        'total_games': total_games,
        'avg_playtime': round(avg_playtime),
        'total_players': total_player_instances,
        'unique_players': len(unique_players)
    }
