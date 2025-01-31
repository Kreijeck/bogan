from sqlalchemy.orm import Session

from bogan.utils import get_db_engine
from bogan.db.models import Game, Boardgame

engine = get_db_engine()


def get_boardgame_by(id: str, session: Session):
    boardgame = session.query(Boardgame).filter(Boardgame.bgg_id == id).first()
    return boardgame

def get_all_boardgames(session: Session):
    boardgames = session.query(Boardgame).order_by(Boardgame.name).all()
    return boardgames


def get_games_by(boardgame_id: int, session: Session):
    print(f"Type ID: {type(boardgame_id)}")
    games = session.query(Game).join(Boardgame).filter(Boardgame.bgg_id == boardgame_id).order_by(Game.datum.desc()).all()
    
    # Sortiere die Spiele nach Punkten
    for game in games:
        game.player_pos = sorted(game.player_pos, key=lambda x: x.points, reverse=True)
    return games
