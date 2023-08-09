from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from bogan.update_db.models import Benutzer, Spieler, Partie, Ort, Brettspiel, Base
from datetime import datetime
import json
import os


db_path = os.path.join("data", "spiel2.db")

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

    # Erstelle Datenbank
    Base.metadata.create_all(engine)


def create_ort(play: dict, session: Session) -> Ort:
    ort = session.query(Ort).filter_by(name=play["@location"]).first()
    if ort is None:
        ort = Ort(name=play["@location"])
        session.add(ort)

    return ort


def create_brettspiel(play: dict, session: Session) -> Brettspiel:
    brettspiel = session.query(Brettspiel).filter_by(id=play["item"]["@objectid"]).first()
    if brettspiel is None:
        brettspiel = Brettspiel(id=play["item"]["@objectid"], name=play["item"]["@name"])
        session.add(brettspiel)

    return brettspiel


def create_benutzer(player: dict, session: Session) -> Benutzer:
    # Suche nach dem Spieler in der Benutzer-Tabelle
    # Name ist "unique" -> nur 0 oder 1 möglich
    benutzer = session.query(Benutzer).filter_by(name=player["@name"]).first()
    if benutzer is None:
        benutzer = Benutzer(name=player["@name"])
        session.add(benutzer)

    return benutzer


def add_data_to_database():
    # Öffne Session
    session = Session(engine)

    # Leses Daten aus der JSON-Datei
    json_path = os.path.join("data", "plays.json")
    with open(json_path, "r", encoding="utf-16") as f:
        spieldaten = json.load(f)

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
            print(
                f"Folgendes Spiel hat einen Fehler: Error: {e},"\
                "Partie_ID: {play['@id']}, Spiel: {play['item']['@name']}"
            )

    # Speicher die Änderungen
    session.commit()
    # Schließe die Session
    session.close()


def main():
    create_database()
    add_data_to_database()

    from sqlalchemy import select

    session = Session(engine)
    stmt = select(Partie)
    for game in session.scalars(stmt):
        print(game)


if __name__ == "__main__":
    main()
