from sqlalchemy.orm import Session

from bogan.utils import get_db_engine
from bogan.db.models import Game, Boardgame, Location

engine = get_db_engine()


def get_boardgame_by(id: str, session: Session):
    boardgame = session.query(Boardgame).filter(Boardgame.bgg_id == id).first()
    return boardgame

def get_all_boardgames(session: Session):
    boardgames = session.query(Boardgame).order_by(Boardgame.name).all()
    return boardgames


def get_games_by(boardgame_id: int, session: Session, ignore_solo:bool=True):
    """Erhalte alle Spiele zu einem Boardgame
    und sortiere sie nach Datum absteigend.

    Args:
        boardgame_id (int): ID des Boardgames
        session (Session): aktuelle Session der Datenbank
        ignore_solo (bool, optional): Ignoriere Sologames. Defaults to True.

    Returns:
        Game: SQL Object mit allen Spielen zu einem Boardgame
    """
    print(f"Type ID: {type(boardgame_id)}")
    games = session.query(Game).join(Boardgame).join(Location).filter(Boardgame.bgg_id == boardgame_id).order_by(Game.datum.desc())
    if ignore_solo:
        games = games.filter(Location.name != "Solospiel")
    games = games.all()
    
    # Sortiere die Spiele nach Punkten
    for game in games:
        game.player_pos = sorted(game.player_pos, key=lambda x: x.points, reverse=True)
    return games
