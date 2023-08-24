from sqlalchemy.orm import Session
from sqlalchemy import select
from bogan.config import get_logger, get_play_engine, cfg_www
from bogan.db.models import Benutzer, Partie, SpielerPos, Brettspiel, Ort
from datetime import datetime
from dateutil.relativedelta import relativedelta

log = get_logger(__file__)
engine = get_play_engine()
#session = Session(engine)

def get_session() -> Session:
    return Session(engine)

def get_users():
    with Session(engine) as session:
        users = session.query(Benutzer).order_by(Benutzer.name)
        # Entferne alle user, die ignoriert werden
        for ignored in cfg_www['ignored_users_name']:
            users = users.where(Benutzer.name != ignored)
    return users

def get_boardgames():
    with Session(engine) as session:
        boardgames = session.query(Brettspiel).order_by(Brettspiel.name)
        # Entferne alle Brettspiele (id) die nicht angezeigt werden sollen
        for ignored in cfg_www['ignored_boardgames_id']:
            boardgames = boardgames.where(Brettspiel.id != ignored)
    return boardgames

def get_boardgames_detail(name):
    with Session(engine) as session:
        query = session.query(Brettspiel).where(Brettspiel.name == name).first()

    return query

def get_partien_from_game(session, name):
    query = session.query(Partie).join(Brettspiel).join(SpielerPos).where(Brettspiel.name == name).all()
    log.debug(f"SQL query found for {name} this partien: {query}")

    return query


def get_partien_by_date(user):
    with Session(engine) as session:
        user_play_query = (
            session.query(Partie).join(SpielerPos).join(Benutzer).join(Brettspiel).where(Benutzer.name == user)
        )
    # Startdatum: 01.01.2022
    datum_old = datetime.strptime("2022-01-01", "%Y-%m-%d").date()
    datum_new = datum_old + relativedelta(months=1)

    player_dict = {}

    # while bis akutelles Datum erreicht ist
    while datum_new < datetime.now().date():
        # is_in_date = ( and )
        user_play_date_query = (
            user_play_query.where(Partie.datum >= datum_old)
            .where(Partie.datum < datum_new)
            .order_by(Partie.datum)
        )
        # add key, wenn Partien in dem Monat vorhanden sind
        if user_play_date_query.first():
            # create key with date (Month Year)
            # Add games to key
            player_dict[datum_old.strftime("%B %Y")] = user_play_date_query
            log.info(f"{user} played Games in {datum_old.strftime('%B %Y')}:")
        
        for row in user_play_date_query:
            # Add games to key
            log.info(f" On {row.datum} {user} played {row.brettspiel.name}")

        # erhöhe Datum um 1 Monat
        datum_old = datum_new
        datum_new = datum_new + relativedelta(months=1)

    return player_dict




if __name__ == "__main__":
    for i in get_partien_from_game("Anachrony"):
        print(i.id)
