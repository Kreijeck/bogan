from sqlalchemy.orm import Session
from sqlalchemy import select
from bogan.config import get_logger, get_play_engine
from bogan.db.models import Benutzer, Partie, SpielerPos, Brettspiel, Ort

log = get_logger(__file__)
engine = get_play_engine()
session = Session(engine)

def get_users():
    stmt = select(Benutzer).order_by(Benutzer.id)

    return session.scalars(stmt)

def get_partien(user):
    benutzer_id = session.scalars(select(Benutzer.id).where(Benutzer.name==user)).first()
    stmt = select(Partie).join(Partie.spieler).where(SpielerPos.benutzer_id == benutzer_id)
    for i, partie in enumerate(session.scalars(stmt)):
        log.debug(f"Partie {i+1} für {user}: {partie}")
    return session.scalars(stmt)


if __name__ == "__main__":
    get_partien("Michi")
    