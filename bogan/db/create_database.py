# from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from bogan.db.models import Benutzer, SpielerPos, Partie, Ort, Brettspiel, Base
from datetime import datetime
import json
import os
from bogan.config import get_logger, CFG_YAML, get_play_engine, cfg_db, db_path
from bogan.db.get_data_from_bgg import get_and_write_play_data, get_boardgame_info

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


def get_brettspiel_details(id) -> dict:
    """Holt detaillierte Informationen zu einem Brettspiel aus dem Modell 'Brettspiel'

    Args:
        id (int): ID des Brettspiels

    Returns:
        dict: Informationen zu Brettspiel
    """

    details: dict = get_boardgame_info(id)
    details_dict = {}
    # Try to add complexity and duration

    ## TODO Refactor this part
    try:
        details_dict["complexity"] = float(details["statistics"]["ratings"]["averageweight"]["@value"])
    except KeyError:
        pass

    try:
        details_dict["duration"] = int(details["playingtime"]["@value"])
    except KeyError:
        pass

    try:
        details_dict["image"] = details["image"]
    except KeyError:
        pass

    try:
        details_dict["image_small"] = details["thumbnail"]
    except KeyError:
        pass
    try:
        # Koop Flag wird gesetzt, wenn "Cooperative Game" in link gefunden wird
        coop = False
        for link in details["link"]:
            if link["@value"] == "Cooperative Game":
                coop = True
        details_dict["koop"] = coop
    except KeyError:
        pass

    return details_dict


def create_brettspiel(play: dict, session: Session) -> Brettspiel:
    brettspiel_id = play["item"]["@objectid"]
    brettspiel = session.query(Brettspiel).filter_by(id=brettspiel_id).first()
    if brettspiel is None:
        bs_details = get_brettspiel_details(id=brettspiel_id)
        brettspiel = Brettspiel(
            id=play["item"]["@objectid"],
            name=play["item"]["@name"],
        )
        # Add addition detailed information to boardgame from get_brettspiel details
        for key, value in bs_details.items():
            brettspiel.set(key, value)

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
        partie = Partie(partie_bgg_id=play["@id"], datum=datum, ort=ort, brettspiel=brettspiel)
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

            # Konvertiere Einträge zu einer Liste. Bei nur 1 Spieler wird für player nur ein dictionary verwendet
            if not isinstance(play["players"]["player"],list):
                play["players"]["player"] = [play["players"]["player"]]
                
            # Füge jeden Spieler zur Partie hinzu
            for player in play["players"]["player"]:
                
                benutzer = create_benutzer(player=player, session=session)
                win = True if (player["@win"] == "1") else False
                punktzahl = check_str2float(player["@score"])
                # Wenn keine Punktzahl vorhanden ist, setze 1 wenn Spiel gewonnen, sonst 0
                if punktzahl is None:
                    punktzahl = 1 if win else 0


                # Erstelle den Spieler und verknüpfe ihn mit dem Benutzer und der Partie
                # Überprüfe ob Punktzahl vorhanden
                spieler_pos = SpielerPos(punktzahl=punktzahl, win=win, partie=partie, benutzer=benutzer)
                session.add(spieler_pos)

                log.debug(
                    f"Partie_ID: {play['@id']}, Spiel: {play['item']['@name']} "
                    f"wurde erfolgreich in die Datenbank geschrieben."
                )
        except Exception as e:
            log.warning(
                f"Key {e} wurde nicht gefunden, bitte überprüfen!"
                f"Partie_ID: {play['@id']}, Spiel: {play['item']['@name']} "
                f"wurde nicht in die Datenbank geschrieben."
            )

    # Speicher die Änderungen
    session.commit()
    # Schließe die Session
    session.close()


def main():
    create_database()
    play_data = get_and_write_play_data()
    add_data_to_database(play_data)


if __name__ == "__main__":
    main()
