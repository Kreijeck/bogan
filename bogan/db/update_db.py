import json
import os
from sqlalchemy.orm import Session
from datetime import datetime
from bogan.db.config import ENCODING, GAME_USER
from bogan.db.models import Base, Boardgame, Location, Game, Player, PlayerPos
from bogan.db.ask_bgg import ask_boardgame, ask_games_from
from bogan.utils import nested_get, get_db_engine


engine = get_db_engine(debug=False)
## Delete Database
# Base.metadata.drop_all(engine)
## Create Database
Base.metadata.create_all(engine)
# session = Session(engine)


def get_boardgames(session: Session, my_games: dict) -> dict[Boardgame]:
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

    # Führe ein update bei allen Spielen durch oder lege es neu an
    for boardgame in boardgames:

        boardgame_db = session.query(Boardgame).filter_by(bgg_id=boardgame.bgg_id).first()

        # Update mit aktuellen Daten
        if boardgame_db:
            boardgame_db = boardgame_db.update(boardgame)
            # print(f" Update {boardgame_db.name} with id {boardgame_db.bgg_id}")

        # Erstelle neuen Eintrag
        else:
            boardgame_db = boardgame
            print(f"neues Spiel gefunden! {boardgame}")
            # session.add(boardgame_db)

        session.add(boardgame_db)
        # add to return value
        boardgames_dict[boardgame.bgg_id] = boardgame_db

    return boardgames_dict


def get_location(session: Session, json_file: dict) -> Location:
    name = json_file.get("@location")

    location = session.query(Location).filter_by(name=name).first()

    # mit aktueller Parameterliste, kann nur neuer Eintrag erzeugt werden oder nichts passiert
    if not location:
        location = Location(name=name)

    session.add(location)
    return location


def get_player(session: Session, json_file: dict) -> Player:
    name = json_file.get("@name")
    bgg_name = json_file.get("@username")
    bgg_name = bgg_name if bgg_name else None

    player = session.query(Player).filter_by(name=name).first()

    if player:
        player.bgg_name = bgg_name
    else:
        player = Player(name=name, bgg_name=bgg_name)

    session.add(player)
    return player


def get_player_pos(session: Session, json_file: dict, game: Game, player: Player) -> PlayerPos:
    points = nested_get(json_file, ["@score"], float)
    win = True if json_file.get("@win") == "1" else False

    player_pos = session.query(PlayerPos).filter_by(game=game, player=player).first()

    if player_pos:
        player_pos.points = points
        player_pos.win = win
        player_pos.player_id = player.id
    else:
        player_pos = PlayerPos(points=points, win=win, game=game, player=player)

    session.add(player_pos)
    return player_pos


def get_game(session: Session, json_file: dict, boardgame: Boardgame, location: Location) -> Game:
    game_bgg_id = nested_get(json_file, ["@id"], int)
    datum = datetime.strptime(json_file.get("@date"), "%Y-%m-%d").date()
    playtime = nested_get(json_file, ["@length"], int)

    game = session.query(Game).filter_by(game_bgg_id=game_bgg_id).first()

    if game:
        game.datum = datum
        game.playtime = playtime
        game.boardgame_id = boardgame.id
        game.location_id = location.id
    else:
        game = Game(game_bgg_id=game_bgg_id, datum=datum, playtime=playtime, boardgame=boardgame, location=location)
        #TODO remove print
        print(f"neue Partie hinzugefügt: Game(game_bgg_id={game_bgg_id}, brettspiel={game.boardgame.name}, datum={game.datum})")

    session.add(game)

    return game


def update_db():

    # MIT API CALL
    my_games = ask_games_from(GAME_USER)

    # # Speicher Datei
    # save_path = "data/example_plays.json"
    # with open(game_path, "w", encoding=ENCODING) as file:
    #     json.dump(my_games, file, indent=4, ensure_ascii=False)
    # Lade datei, für schnellere Tests
    # with open(save_path, "r", encoding=ENCODING) as file:
    #     my_games = json.load(file)

    with Session(engine) as session:
        # First fetch all boardgmes
        boardgames_dict = get_boardgames(session, my_games)

        # Run database update/creation
        for my_game in my_games:
            boardgame_obj = boardgames_dict[nested_get(my_game, ["item", "@objectid"], int)]
            location_obj = get_location(session, my_game)
            game_obj = get_game(session, my_game, boardgame_obj, location_obj)

            for player_pos_dict in my_game.get("players").get("player"):
                player_obj = get_player(session, player_pos_dict)
                get_player_pos(session, player_pos_dict, game_obj, player_obj)
            
            print(f"Update game id={game_obj.game_bgg_id} - {game_obj.boardgame.name} on {game_obj.datum}")
        session.commit()


if __name__ == "__main__":
    from time import time

    t_start = time()
    update_db()
    t_stop = time()
    # TODO remove print
    t_ges = round(t_stop - t_start, 4)
    print(f"SUCCESS: Das Updaten/Erstellen der Datenbank dauerte {t_ges} sek")
