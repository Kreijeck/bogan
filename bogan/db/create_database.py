# from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from bogan.db.models import Benutzer, SpielerPos, Partie, Ort, Brettspiel, Base
from datetime import datetime
import json
import os
from bogan.config import get_logger, CFG_YAML, get_play_engine, cfg_db, db_path
from bogan.db.get_data_from_bgg import get_and_write_play_data

log = get_logger(__file__)

engine = get_play_engine()


def check_str2float(str2float: str) -> float:
    try:
        return float(str2float)
    except ValueError:
        return None


def create_database(clear_all=True):
    # clear database
    if clear_all:
        Base.metadata.drop_all(engine)
        log.info(f"Delete old database: {db_path}")

    # Erstelle Datenbank
    Base.metadata.create_all(engine)
    log.info(f"Successfully create db: {db_path}")


def create_ort(play: dict, session: Session) -> Ort:
    ort = session.query(Ort).filter_by(name=play["@location"]).first()
    if ort is None:
        ort = Ort(name=play["@location"])
        log.debug(f"Add new Ort to db: {ort}")
        session.add(ort)

    return ort


def create_brettspiel(play: dict, session: Session) -> Brettspiel:
    brettspiel = session.query(Brettspiel).filter_by(id=play["item"]["@objectid"]).first()
    if brettspiel is None:
        brettspiel = Brettspiel(id=play["item"]["@objectid"], name=play["item"]["@name"])
        log.debug(f"Add new Brettspiel to db: {brettspiel}")
        session.add(brettspiel)

    return brettspiel


def create_benutzer(player: dict, session: Session) -> Benutzer:
    # Suche nach dem Spieler in der Benutzer-Tabelle
    # Name ist "unique" -> nur 0 oder 1 möglich
    benutzer = session.query(Benutzer).filter_by(name=player["@name"]).first()
    if benutzer is None:
        benutzer = Benutzer(name=player["@name"])
        log.debug(f"Add new Benutzer to db: {benutzer}")
        session.add(benutzer)

    return benutzer


def create_partie(play: dict, session: Session) -> Partie:
    partie = session.query(Partie).filter_by(id=play["@id"]).first()
    ort = create_ort(play, session)
    brettspiel = create_brettspiel(play, session)
    datum = datetime.strptime(play["@date"], "%Y-%m-%d").date()

    # Wenn keine Partie mit ID vorhanden ist:
    if partie is None:    
        partie = Partie(id=play["@id"], datum=datum, ort=ort, brettspiel=brettspiel)
        session.add(partie)
    # wenn id bereits vorhanden ist, soll die Partie geupdated werden
    else:
        partie.ort = ort
        partie.brettspiel = brettspiel
        partie.datum = datum
        session.commit()

    return partie
    


def read_json() -> dict:
    if cfg_db["bgg_json"]:
        json_path = os.path.join(cfg_db["dir"], cfg_db["bgg_json"])
        with open(json_path, "r", encoding=CFG_YAML["encoding"]) as f:
            json_file = json.load(f)

        return json_file


def add_data_to_database(json_file):
    # Öffne Session
    session = Session(engine)

    spieldaten = json_file

    # Füge jede Partie zur Datenbank hinzu
    for play in spieldaten["plays"]["play"]:
        try:
            partie = create_partie(play=play, session=session)

            # Füge jeden Spieler zur Partie hinzu
            for player in play["players"]["player"]:
                benutzer = create_benutzer(player=player, session=session)
                punktzahl = check_str2float(player["@score"])

                # Erstelle den Spieler und verknüpfe ihn mit dem Benutzer und der Partie
                # Überprüfe ob Punktzahl vorhanden
                spieler = SpielerPos(punktzahl=punktzahl, partie=partie, benutzer=benutzer)
                session.add(spieler)
        except Exception as e:
            log.warning(
                f"Spiel nicht in Datenbank: Partie_ID: {play['@id']}, Spiel: {play['item']['@name']}"
            )
            log.warning(f"Fehlermeldung: {e}")

    # Speicher die Änderungen
    session.commit()
    # Schließe die Session
    session.close()


def main():
    create_database()
    play_data = get_and_write_play_data()
    # json_path = os.path.join("data", "plays.json")
    # with open(json_path, 'r', encoding="utf-16") as f:
    #         play_data = json.load(f)
    add_data_to_database(play_data)


if __name__ == "__main__":
    main()
