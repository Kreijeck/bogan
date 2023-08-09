from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from bogan.update_db.models import Benutzer, Spieler, Partie, Ort, Brettspiel, Base
from datetime import datetime
import json
import os
from bogan.config import get_logger, CFG_YAML
from bogan.update_db.get_data_from_bgg import get_and_write_play_data

cfg_db = CFG_YAML["database"]
log = get_logger(__file__)
db_path = os.path.join(cfg_db["dir"], cfg_db["db_file"])
# create folder
if not os.path.exists(cfg_db["dir"]):
    os.mkdir(cfg_db["dir"])

engine = create_engine(f"sqlite:///{db_path}")


def check_str2float(str2float: str) -> float:
    if str2float.isdigit():
        return float(str2float)
    else:
        return None


def create_database(clear_all=True):
    # clear database
    if clear_all:
        Base.metadata.drop_all(engine)
        log.info(f"Delete old database: {cfg_db['db_file']}")

    # Erstelle Datenbank
    Base.metadata.create_all(engine)
    log.info(f"Succ")


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
            ort = create_ort(play, session)
            brettspiel = create_brettspiel(play, session)
            datum = datetime.strptime(play["@date"], "%Y-%m-%d").date()
            partie = Partie(id=play["@id"], datum=datum, ort=ort, brettspiel=brettspiel)
            session.add(partie)

            # Füge jeden Spieler zur Partie hinzu
            for player in play["players"]["player"]:
                benutzer = create_benutzer(player, session)
                punktzahl = check_str2float(player["@score"])

                # Erstelle den Spieler und verknüpfe ihn mit dem Benutzer und der Partie
                # Überprüfe ob Punktzahl vorhanden
                spieler = Spieler(name=player["@name"], punktzahl=punktzahl, partie=partie, benutzer=benutzer)
                session.add(spieler)
        except Exception as e:
            log.warning(
                f"Folgendes Spiel hat einen Fehler: Error: {e},"
                "Partie_ID: {play['@id']}, Spiel: {play['item']['@name']}"
            )

    # Speicher die Änderungen
    session.commit()
    # Schließe die Session
    session.close()


def main():
    create_database()
    play_date = get_and_write_play_data()
    add_data_to_database(play_date)


if __name__ == "__main__":
    main()
