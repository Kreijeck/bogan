import json
from sqlalchemy import MetaData, Table
from sqlalchemy.orm import Session
from datetime import datetime
from bogan.config import ENCODING, GAME_USER
from bogan.db.models import Base, Boardgame, Location, Game, Player, PlayerPos
from bogan.db.ask_bgg import ask_boardgame, ask_games_from
from bogan.utils import nested_get, get_db_engine, Logger

# Add Logging
logger = Logger().setup_logger(__file__)

engine = get_db_engine(local=False)
logger.info(f"Datenbank URL {engine.url} wird verwendet")
session = Session(bind=engine)
## Delete complete Database
# Base.metadata.drop_all(engine)

# delete specific tables
table_to_reset = ["player_pos", "game", "location"]
metadata = MetaData()

for table_name in table_to_reset:
    # Versuche die Tabelle mit mit gegebenem Namen zu resetten
    try:
        # Erstelle Tabellendefinition
        table = Table(table_name, metadata, autoload_with=engine)
        # Lösche die Tabelle
        table.drop(engine)
        logger.info(f"Cleared table {table_name}")
    except Exception as e:
        logger.error(f"Table {table_name} does not exist or could not be dropped: {e}")

## Create Database
Base.metadata.create_all(engine)


def get_boardgames(my_games: dict) -> dict[Boardgame]:
    """Update aller Boardgames in der Datenbank.
    Um nur einen API Call durchzuführen werden hier erst alle IDs gesammelt und dann mit einem Call die Stats angefragt

    Args:
        my_games (dict): Spieleliste von BGG von einem speziellen User

    Returns:
        dict[Boardgame]:    Keys: BGG_ID
                            Value: Boardgame object
    """
    ids = []
    boardgames_dict = {}

    # get all different boardgames from play
    for game in my_games:
        id = nested_get(game, ["item", "@objectid"])
        if id not in ids:
            ids.append(nested_get(game, ["item", "@objectid"]))

    # Erhalte alle boardgames der angegebenen ids
    boardgames = ask_boardgame(ids) if ids else []

    # Perform update oder lege ein neues Brettspiel an
    for boardgame in boardgames:

        boardgame_db = session.query(Boardgame).filter_by(bgg_id=boardgame.bgg_id).first()

        # Update mit aktuellen Daten
        if boardgame_db:
            boardgame_db = boardgame_db.update(boardgame)
            logger.info(f" Update {boardgame_db.name}, ID: {boardgame_db.bgg_id}")

        # Erstelle neuen Eintrag
        else:
            boardgame_db = boardgame
            logger.info(f"neues Spiel gefunden! {boardgame}")
            # session.add(boardgame_db)

        session.add(boardgame_db)
        # add to return value
        boardgames_dict[boardgame.bgg_id] = boardgame_db

    return boardgames_dict


def get_location(json_file: dict) -> Location:
    """Erstelle location des Spiels falls sie nicht existiert

    Args:
        json_file (dict): einzelnes Spiel von BGG

    Returns:
        Location: object von Location
    """
    name = json_file.get("@location")

    location = session.query(Location).filter_by(name=name).first()

    # Füge neue location hinzu
    if not location:
        location = Location(name=name)
        session.add(location)

    return location


def get_player(json_file: dict) -> Player:
    """Erstelle Spieler falls er nicht existiert

    Args:
        json_file (dict): einzelnes Spiel von BGG

    Returns:
        Player: spieler Object
    """
    name = json_file.get("@name")
    bgg_name = json_file.get("@username")
    bgg_name = bgg_name if bgg_name else None

    player = session.query(Player).filter_by(name=name).first()

    if not player:
        player = Player(name=name, bgg_name=bgg_name)
        session.add(player)

    return player


def get_player_pos(json_file: dict, game: Game, player: Player) -> PlayerPos:
    """Erstelle Spieler + Punkte aus einem Spiel

    Args:
        json_file (dict): eine Zeile spieler pos
        game (Game): welches spiel gespielt wurde
        player (Player): welcher spieler verwendet wird

    Returns:
        PlayerPos: object aus spieler + punkte
    """
    points = nested_get(json_file, ["@score"], float)
    win = True if json_file.get("@win") == "1" else False

    player_pos = session.query(PlayerPos).filter_by(game=game, player=player).first()

    if not player_pos:
        player_pos = PlayerPos(points=points, win=win, game=game, player=player)
        session.add(player_pos)
    return player_pos


def get_game(json_file: dict, boardgame: Boardgame, location: Location) -> Game:
    """erstelle ein Spiel

    Args:
        json_file (dict): ein spiel aus BGG
        boardgame (Boardgame): brettspiel das gespielt wurde
        location (Location): ort an dem gespielt wurde

    Returns:
        Game: object des spiels
    """
    game_bgg_id = nested_get(json_file, ["@id"], int)
    datum = datetime.strptime(json_file.get("@date"), "%Y-%m-%d").date()
    playtime = nested_get(json_file, ["@length"], int)

    game = session.query(Game).filter_by(game_bgg_id=game_bgg_id).first()

    if not game:
        game = Game(game_bgg_id=game_bgg_id, datum=datum, playtime=playtime, boardgame=boardgame, location=location)
        session.add(game)

    return game


def update_db(from_api: bool, save_file=False):
    """Update database with new values

    Args:
        from_api (bool): True: make a real api call, False: used save-file
        save_file (bool, optional): shall the json be saved. Defaults to False.
    """

    save_path = "data/example/example_plays.json"

    # MIT API CALL
    if from_api:
        logger.info("Receive games from API")
        my_games = ask_games_from(GAME_USER)
        # Speicher Datei
        if save_file:
            with open(save_path, "w", encoding=ENCODING) as file:
                json.dump(my_games, file, indent=4, ensure_ascii=False)

    else:
        # Lade datei, für schnellere Tests
        with open(save_path, "r", encoding=ENCODING) as file:
            logger.info("Receive games from local save-file")
            my_games = json.load(file)

    # First fetch all boardgmes
    boardgames_dict = get_boardgames(my_games)

    # Run database update/creation
    for my_game in my_games:
        boardgame_obj = boardgames_dict[nested_get(my_game, ["item", "@objectid"], int)]
        location_obj = get_location(my_game)
        game_obj = get_game(my_game, boardgame_obj, location_obj)

        for player_pos_dict in my_game.get("players").get("player"):
            player_obj = get_player(player_pos_dict)
            get_player_pos(player_pos_dict, game_obj, player_obj)

        logger.info(f"Erstelle Partie: game id={game_obj.game_bgg_id} - {game_obj.boardgame.name} on {game_obj.datum}")

        # Speicher Datenbank
        session.commit()


if __name__ == "__main__":
    from time import time

    t_start = time()
    update_db(from_api=True)
    t_stop = time()
    t_ges = round(t_stop - t_start, 4)
    logger.info(f"SUCCESS: Das Updaten/Erstellen der Datenbank dauerte {t_ges} sek")
