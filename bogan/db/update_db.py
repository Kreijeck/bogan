import json
from sqlalchemy import MetaData, Table
from sqlalchemy.orm import Session
from datetime import datetime
from bogan.config import ENCODING, GAME_USER
from bogan.db.models import Base, Boardgame, Location, Game, Player, PlayerPos
from bogan.db.ask_bgg import ask_boardgame, ask_games_from
from bogan.utils import nested_get, get_db_engine, Logger

logger = Logger().setup_logger(__file__)
engine = get_db_engine()
logger.info(f"Datenbank URL {engine.url} wird verwendet")
session = Session(bind=engine)

# Erstelle alle Datenbank
Base.metadata.create_all(engine)


# -----------------------------------------------------------
# Hilfsfunktionen zum Vergleich/Update von Feldern mit Logging
# -----------------------------------------------------------


def compare_and_update_boardgame(db_obj: Boardgame, new_data: Boardgame) -> bool:
    """
    Vergleicht relevante Felder zwischen db_obj und new_data.
    Wenn sich etwas ändert, wird es übernommen und es wird True zurückgegeben.
    Bleibt alles gleich, wird False zurückgegeben.
    """
    changed = False

    # Beispielhafter Vergleich einiger Felder
    if db_obj.name != new_data.name:
        db_obj.name = new_data.name
        changed = True

    if db_obj.yearpublished != new_data.yearpublished:
        db_obj.yearpublished = new_data.yearpublished
        changed = True

    if db_obj.minplayers != new_data.minplayers:
        db_obj.minplayers = new_data.minplayers
        changed = True

    if db_obj.maxplayers != new_data.maxplayers:
        db_obj.maxplayers = new_data.maxplayers
        changed = True

    # ... weitere Felder nach Bedarf ...

    return changed


def compare_and_update_game(db_game: Game, new_datum, new_playtime, new_location_id, new_boardgame_id) -> bool:
    """
    Vergleicht relevante Felder im Game-Objekt.
    Gibt True zurück, wenn sich etwas geändert hat, sonst False.
    """
    changed = False
    if db_game.datum != new_datum:
        db_game.datum = new_datum
        changed = True

    if db_game.playtime != new_playtime:
        db_game.playtime = new_playtime
        changed = True

    if db_game.location_id != new_location_id:
        db_game.location_id = new_location_id
        changed = True

    if db_game.boardgame_id != new_boardgame_id:
        db_game.boardgame_id = new_boardgame_id
        changed = True

    return changed


def compare_and_update_playerpos(pp_obj: PlayerPos, new_points, new_win) -> bool:
    """
    Vergleicht relevante Felder im PlayerPos-Objekt.
    Gibt True zurück, wenn sich etwas geändert hat, sonst False.
    """
    changed = False
    if pp_obj.points != new_points:
        pp_obj.points = new_points
        changed = True

    if pp_obj.win != new_win:
        pp_obj.win = new_win
        changed = True

    return changed


# -----------------------------------------------------------
# Deine eigentlichen Workflow-Funktionen
# -----------------------------------------------------------


def get_boardgames(my_games: list[dict]) -> dict[int, Boardgame]:
    """
    Aktualisiert alle Boardgames in der Datenbank anhand der gesammelten IDs aus my_games.
    Gibt ein Dictionary zurück, das die bgg_id (int) auf das entsprechende Boardgame-Objekt mapped.
    """
    ids = []
    boardgames_dict = {}

    # IDs sammeln
    for game in my_games:
        bgg_id = nested_get(game, ["item", "@objectid"], int)
        if bgg_id and bgg_id not in ids:
            ids.append(bgg_id)

    # Boardgames vom BGG abfragen (falls IDs vorhanden)
    boardgames = ask_boardgame(ids) if ids else []

    # Update oder Neueintrag
    for boardgame in boardgames:
        boardgame_db = session.query(Boardgame).filter_by(bgg_id=boardgame.bgg_id).first()
        if boardgame_db:
            # Felder vergleichen und ggf. updaten
            if compare_and_update_boardgame(boardgame_db, boardgame):
                logger.info(f"Boardgame aktualisiert: {boardgame_db.name}, ID: {boardgame_db.bgg_id}")
            else:
                logger.debug(f"Boardgame unverändert: {boardgame_db.name}, ID: {boardgame_db.bgg_id}")
        else:
            # Neues Boardgame
            boardgame_db = boardgame
            session.add(boardgame_db)
            logger.info(f"Neues Boardgame angelegt: {boardgame_db.name}, ID: {boardgame_db.bgg_id}")

        boardgames_dict[boardgame_db.bgg_id] = boardgame_db

    session.commit()
    return boardgames_dict


def get_location(json_file: dict) -> Location:
    """
    Erstelle oder finde eine Location anhand der JSON-Daten
    """
    name = json_file.get("@location")
    if not name:
        return None

    location = session.query(Location).filter_by(name=name).first()
    if not location:
        location = Location(name=name)
        session.add(location)
        session.commit()
        logger.info(f"Neue Location erstellt: {name}")
    else:
        logger.debug(f"Location unverändert oder bereits vorhanden: {name}")

    return location


def get_or_create_player(player_json: dict) -> Player:
    """
    Erstelle oder finde einen Spieler anhand der JSON-Daten
    """
    name = player_json.get("@name")
    bgg_name = player_json.get("@username") or None

    player = session.query(Player).filter_by(name=name).first()
    if not player:
        player = Player(name=name, bgg_name=bgg_name)
        session.add(player)
        session.commit()
        logger.info(f"Neuer Player erstellt: {name}")
    else:
        logger.debug(f"Player unverändert oder bereits vorhanden: {name}")
    return player


def update_player_positions(db_game: Game, players_json: list[dict]):
    """
    Aktualisiert die Spielstände (PlayerPos) zu einem bereits existierenden Game-Objekt.
    Die JSON ist Master:
    - Einträge, die nicht mehr in der JSON sind, werden gelöscht.
    - Einträge, die fehlen, werden angelegt.
    - Vorhandene Einträge werden aktualisiert (nur wenn sich was ändert -> info).
    """

    # 1) PlayerPos aus der DB laden, die zu diesem Spiel gehören
    existing_positions = session.query(PlayerPos).filter_by(game=db_game).all()
    # Mapping von player_id -> PlayerPos
    existing_positions_map = {pos.player_id: pos for pos in existing_positions}

    # 2) IDs der Player aus JSON sammeln (damit wissen wir, was neu oder gelöscht ist)
    json_player_ids = []
    for p_json in players_json:
        name = p_json.get("@name")
        player_obj = session.query(Player).filter_by(name=name).first()
        if not player_obj:
            player_obj = get_or_create_player(p_json)
        json_player_ids.append(player_obj.id)

    # 3) PlayerPos, die nicht mehr in der JSON sind, löschen
    for player_id, pos_obj in existing_positions_map.items():
        if player_id not in json_player_ids:
            logger.info(
                f"PlayerPos gelöscht: Player_ID={player_id} in Game_ID={db_game.id}, GAME_BGG_ID={db_game.game_bgg_id}"
            )
            session.delete(pos_obj)

    session.commit()

    # 4) Anlegen oder Updaten der PlayerPos aus der JSON
    for p_json in players_json:
        # passender Player
        name = p_json.get("@name")
        player_obj = session.query(Player).filter_by(name=name).first()
        if not player_obj:
            player_obj = get_or_create_player(p_json)

        points = nested_get(p_json, ["@score"], float) or 0.0
        win = True if p_json.get("@win") == "1" else False

        # Falls PlayerPos existiert, updaten
        existing_pp = existing_positions_map.get(player_obj.id)
        if existing_pp:
            changed = compare_and_update_playerpos(existing_pp, points, win)
            if changed:
                logger.info(
                    f"PlayerPos aktualisiert: Player={player_obj.name}, Game_ID={db_game.game_bgg_id} "
                    f"(points={points}, win={win})"
                )
            else:
                logger.debug(f"PlayerPos unverändert: Player={player_obj.name}, Game_ID={db_game.game_bgg_id}")
        else:
            # Neu erstellen
            pp = PlayerPos(points=points, win=win, game=db_game, player=player_obj)
            session.add(pp)
            logger.info(
                f"Neue PlayerPos erstellt: Player={player_obj.name}, "
                f"Game_ID={db_game.game_bgg_id} (points={points}, win={win})"
            )

    session.commit()


def update_or_create_game(my_game: dict, boardgame_obj: Boardgame, location_obj: Location) -> Game:
    """
    Erstellt oder aktualisiert ein Game anhand eines JSON-Eintrags.
    Loggt nur INFO, wenn sich wirklich Daten geändert haben.
    """
    game_bgg_id = nested_get(my_game, ["@id"], int)
    datum_str = my_game.get("@date")
    datum = datetime.strptime(datum_str, "%Y-%m-%d").date() if datum_str else None
    playtime = nested_get(my_game, ["@length"], int)

    db_game = session.query(Game).filter_by(game_bgg_id=game_bgg_id).first()
    if not db_game:
        # Neues Game anlegen
        db_game = Game(
            game_bgg_id=game_bgg_id, datum=datum, playtime=playtime, boardgame=boardgame_obj, location=location_obj
        )
        session.add(db_game)
        session.commit()
        logger.info(f"Neues Game erstellt: game_bgg_id={game_bgg_id}")
    else:
        # Updates vergleichen
        changed = compare_and_update_game(
            db_game=db_game,
            new_datum=datum,
            new_playtime=playtime,
            new_location_id=location_obj.id if location_obj else None,
            new_boardgame_id=boardgame_obj.id if boardgame_obj else None,
        )
        if changed:
            session.commit()
            logger.info(f"Game aktualisiert: game_bgg_id={game_bgg_id}")
        else:
            logger.debug(f"Game unverändert: game_bgg_id={game_bgg_id}")

    return db_game


def update_db(from_api: bool, save_file=False):
    """
    Aktualisiert die Datenbank mithilfe der JSON-Spieleliste.
    Es werden nur Games gelöscht, die nicht mehr in der JSON vorkommen.
    Neu hinzugekommene oder geänderte Games und PlayerPos werden entsprechend angelegt oder aktualisiert.
    """

    save_path = "data/example/example_plays.json"

    if from_api:
        logger.info("Empfange Spiele von der BGG-API...")
        my_games = ask_games_from(GAME_USER)
        if save_file:
            with open(save_path, "w", encoding=ENCODING) as file:
                json.dump(my_games, file, indent=4, ensure_ascii=False)
    else:
        with open(save_path, "r", encoding=ENCODING) as file:
            logger.info("Empfange Spiele aus lokaler JSON-Datei...")
            my_games = json.load(file)

    # 1) Boardgames aktualisieren/erstellen
    boardgames_dict = get_boardgames(my_games)

    # 2) Aus der JSON alle game_bgg_ids sammeln
    json_game_ids = set()
    for my_game in my_games:
        g_id = nested_get(my_game, ["@id"], int)
        if g_id:
            json_game_ids.add(g_id)

    # 3) Bestehende DB-Spiele holen und diejenigen löschen, die nicht mehr in der JSON sind
    all_db_games = session.query(Game).all()
    for db_game in all_db_games:
        if db_game.game_bgg_id not in json_game_ids:
            logger.info(f"Game wird gelöscht, da nicht mehr in der JSON: game_bgg_id={db_game.game_bgg_id}")
            session.delete(db_game)
    session.commit()

    # 4) Alle Spiele aus der JSON durchgehen -> anlegen oder updaten
    for my_game in my_games:
        bgg_id = nested_get(my_game, ["item", "@objectid"], int)
        boardgame_obj = boardgames_dict.get(bgg_id)
        location_obj = get_location(my_game)

        db_game = update_or_create_game(my_game, boardgame_obj, location_obj)

        # PlayerPos aktualisieren
        players_json = nested_get(my_game, ["players", "player"])
        # Falls nur ein Spieler-Objekt in der JSON steht, kann es auch ein Dict statt einer Liste sein
        if isinstance(players_json, dict):
            players_json = [players_json]

        update_player_positions(db_game, players_json)

    logger.info("Update der Datenbank abgeschlossen")


if __name__ == "__main__":
    from time import time

    t_start = time()
    update_db(from_api=True)
    t_stop = time()
    t_ges = round(t_stop - t_start, 4)
    logger.info(f"SUCCESS: Das Updaten/Erstellen der Datenbank dauerte {t_ges} sek")
