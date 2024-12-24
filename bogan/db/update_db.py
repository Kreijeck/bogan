import json
from sqlalchemy.orm import Session
from datetime import datetime
from bogan.config import ENCODING, GAME_USER
from bogan.db.models import Base, Boardgame, Location, Game, Player, PlayerPos
from bogan.db.ask_bgg import ask_boardgame, ask_games_from
from bogan.utils import nested_get, get_db_engine, Logger

logger = Logger().setup_logger(__file__)
engine = get_db_engine()
logger.info(f"Datenbank URL {engine.url} wird verwendet")

# Session anlegen
session = Session(bind=engine)

# Erstelle alle Felder der Datenbank (nur beim ersten Mal oder bei Änderungen)
Base.metadata.create_all(engine)


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
            if boardgame_db.update(boardgame):
                logger.info(f"[Boardgame] aktualisiert: {boardgame_db.name}, ID: {boardgame_db.bgg_id}")
            else:
                logger.debug(f"[Boardgame] unverändert: {boardgame_db.name}, ID: {boardgame_db.bgg_id}")
        else:
            # Neues Boardgame
            boardgame_db = boardgame
            session.add(boardgame_db)
            logger.info(f"[Boardgame] neu angelegt: {boardgame_db.name}, ID: {boardgame_db.bgg_id}")

        boardgames_dict[boardgame_db.bgg_id] = boardgame_db
    
    # um alle verlinkungen zu erhalten müssen die boardgames separat commitet werden
    session.commit()

    return boardgames_dict


def get_location(json_file: dict) -> Location:
    """
    Erstelle oder finde eine Location anhand der JSON-Daten.
    
    """
    name = json_file.get("@location")

    location = session.query(Location).filter_by(name=name).first()
    if not location:
        location = Location(name=name)
        session.add(location)
        logger.info(f"[Location] neu erstellt: {name}")
    else:
        logger.debug(f"[Location] unverändert oder bereits vorhanden: {name}")

    return location


def get_or_create_player(player_json: dict) -> Player:
    """
    Erstelle oder finde einen Spieler anhand der JSON-Daten.
    
    """
    name = player_json.get("@name")
    bgg_name = player_json.get("@username") or None

    player = session.query(Player).filter_by(name=name).first()
    if not player:
        player = Player(name=name, bgg_name=bgg_name)
        session.add(player)
        logger.info(f"[Player] neu erstellt: {name}")
    else:
        logger.debug(f"[Player] unverändert oder bereits vorhanden: {name}")

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
                f"[PlayerPos] gelöscht: Player_ID={player_id} in Game_ID={db_game.id}, "
                f"BGG_ID={db_game.game_bgg_id}"
            )
            session.delete(pos_obj)

    # 4) Anlegen oder Updaten der PlayerPos aus der JSON
    for p_json in players_json:
        # passender Player
        name = p_json.get("@name")
        player_obj = session.query(Player).filter_by(name=name).first()
        if not player_obj:
            player_obj = get_or_create_player(p_json)

        points = nested_get(p_json, ["@score"], float) or 0.0
        win = (p_json.get("@win") == "1")

        current_pp = PlayerPos(
            points=points,
            win=win,
            game_id=db_game.id,
            player_id=player_obj.id,
        )

        # Falls PlayerPos existiert, updaten
        existing_pp = existing_positions_map.get(player_obj.id)
        if existing_pp:
            if existing_pp.update(current_pp):
                logger.info(
                    f"[PlayerPos] aktualisiert: Player={player_obj.name}, "
                    f"Boardgame={db_game.boardgame.name}, Game_ID={db_game.game_bgg_id} "
                    f"(points={points}, win={win})"
                )
            else:
                logger.debug(
                    f"[PlayerPos] unverändert: Player={player_obj.name}, "
                    f"Boardgame={db_game.boardgame.name}, Game_ID={db_game.game_bgg_id}"
                )
        else:
            # Neu erstellen
            pp = current_pp
            session.add(pp)
            logger.info(
                f"[PlayerPos] neu erstellt: Player={player_obj.name}, "
                f"Boardgame={db_game.boardgame.name}, Game_ID={db_game.game_bgg_id}, "
                f"(points={points}, win={win})"
            )


def update_or_create_game(my_game: dict, boardgame_obj: Boardgame, location_obj: Location) -> Game:
    """
    Erstellt oder aktualisiert ein Game anhand eines JSON-Eintrags.
    Loggt nur INFO, wenn sich wirklich Daten geändert haben.
    """
    game_bgg_id = nested_get(my_game, ["@id"], int)
    datum_str = my_game.get("@date")
    datum = datetime.strptime(datum_str, "%Y-%m-%d").date() if datum_str else None
    playtime = nested_get(my_game, ["@length"], int)

    current_game = Game(
        game_bgg_id=game_bgg_id,
        datum=datum,
        playtime=playtime,
        boardgame_id=boardgame_obj.id,
        location_id=location_obj.id,
    )

    db_game = session.query(Game).filter_by(game_bgg_id=game_bgg_id).first()
    if not db_game:
        # Neues Game anlegen
        db_game = current_game
        session.add(db_game)
        # Spiel in Datenbank für Logs 'flushen'
        session.flush()
        logger.info(
            f"[Game] neu erstellt: game_bgg_id={db_game.game_bgg_id}, "
            f"datum={db_game.datum}, boardgame={db_game.boardgame.name if db_game.boardgame else 'None'}"
        )
    else:
        # Updates vergleichen
        changed = db_game.update(current_game)
        if changed:
            logger.info(
                f"[Game] aktualisiert: game_bgg_id={game_bgg_id}, "
                f"datum={db_game.datum}, boardgame={db_game.boardgame.name if db_game.boardgame else 'None'}"
            )
        else:
            logger.debug(
                f"[Game] unverändert: game_bgg_id={game_bgg_id}, "
                f"datum={db_game.datum}, boardgame={db_game.boardgame.name if db_game.boardgame else 'None'}"
            )

    # Kein commit hier
    return db_game


def update_db(from_api: bool, save_file=False):
    """
    Aktualisiert die Datenbank mithilfe der JSON-Spieleliste.
    1. Boardgames updaten/erstellen.
    2. Spiele (Games) entfernen, die nicht mehr in der JSON existieren.
    3. Spiele anlegen/updaten (Game + PlayerPos + Location).
    4. Einmal am Ende committen.
    """

    save_path = "data/example/example_plays.json"

    # 1) Daten holen
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

    # 2) Boardgames aktualisieren/erstellen
    boardgames_dict = get_boardgames(my_games)

    # 3) Alte Games löschen (die nicht mehr in der JSON sind)
    json_game_ids = set()
    for my_game in my_games:
        g_id = nested_get(my_game, ["@id"], int)
        if g_id:
            json_game_ids.add(g_id)

    all_db_games = session.query(Game).all()
    for db_game in all_db_games:
        if db_game.game_bgg_id not in json_game_ids:
            logger.info(
                f"[Game] wird gelöscht, da nicht mehr in der JSON: "
                f"game_bgg_id={db_game.game_bgg_id}, datum={db_game.datum}, "
                f"boardgame={db_game.boardgame.name if db_game.boardgame else 'None'}"
            )
            session.delete(db_game)

    # 4) Alle Spiele aus der JSON -> anlegen oder updaten
    for my_game in my_games:
        # Boardgame-Objekt holen
        bgg_id = nested_get(my_game, ["item", "@objectid"], int)
        boardgame_obj = boardgames_dict.get(bgg_id)

        # Location aus JSON holen
        location_obj = get_location(my_game)

        # Game anlegen / updaten
        db_game = update_or_create_game(my_game, boardgame_obj, location_obj)

        # PlayerPos aktualisieren
        players_json = nested_get(my_game, ["players", "player"]) or []
        if isinstance(players_json, dict):
            players_json = [players_json]

        update_player_positions(db_game, players_json)

    # 5) Alles committen
    session.commit()
    logger.info("[DB-Update] abgeschlossen.")


if __name__ == "__main__":
    from time import time

    t_start = time()
    update_db(from_api=True)
    t_stop = time()
    t_ges = round(t_stop - t_start, 4)
    logger.info(f"[SUCCESS] Das Updaten/Erstellen der Datenbank dauerte {t_ges} sek")
