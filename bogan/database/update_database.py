from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from bogan.database.models import Benutzer, Spieler, Partie, Base
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


def add_data_to_database():
    # Öffne Session
    session = Session(engine)

    # Leses Daten aus der JSON-Datei
    json_path = os.path.join("data", "plays.json")
    with open(json_path, "r", encoding="utf-16") as f:
        spieldaten = json.load(f)

    # Füge jede Partie zur Datenbank hinzu
    for play in spieldaten["plays"]["play"]:
        partie = Partie(id=play["@id"], datum=play["@date"], ort=play["@location"], name=play["item"]["@name"])
        session.add(partie)

        # Füge jeden Spieler zur Partie hinzu
        for player in play["players"]["player"]:
            # Suche nach dem Spieler in der Benutzer-Tabelle
            # Name ist "unique" -> nur 0 oder 1 möglich
            benutzer = session.query(Benutzer).filter_by(name=player["@name"]).first()
            if benutzer is None:
                benutzer = Benutzer(name=player["@name"])
                session.add(benutzer)

            # Erstelle den Spieler und verknüpfe ihn mit dem Benutzer und der Partie
            # Überprüfe ob Punktzahl vorhanden
            punktzahl = check_str2float(player["@score"])

            spieler = Spieler(name=player["@name"], punktzahl=punktzahl, partie=partie, benutzer=benutzer)
            session.add(spieler)

        # Speicher die Änderungen
        session.commit()
        # Schließe die Session
        session.close()

def main():
    create_database()
    add_data_to_database()


if __name__ == "__main__":
    main()
