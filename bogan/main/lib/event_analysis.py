from bogan.utils import load_yaml, get_date, get_db_engine, DateFormat
import bogan.config as cfg

# To Remove?
from sqlalchemy.orm import Session
from bogan.db.models import Game, PlayerPos, Location

engine = get_db_engine(False)

events = load_yaml(cfg.EVENT_YAML)


def get_game_list(event_name:str) -> list[dict]:

    event_dict = events[event_name]
    # Create Filter for all games
    location = event_dict.get("location")
    datum_start = get_date(event_dict.get("datum_start"), DateFormat.YAML)
    datum_ende = get_date(event_dict.get("datum_ende"), DateFormat.YAML)

    with Session(engine) as session:
        match_games = (
            session.query(Game)
            .join(PlayerPos)
            .join(Location)
            .filter(Game.datum >= datum_start, Game.datum <= datum_ende, Location.name == location)
            .all()
        )
        spiele_list = []
        for match in match_games:
            spiel_dict = {}
            spiel_dict["datum"] = match.datum
            spiel_dict["name"] = match.boardgame.name
            spiel_dict["playtime"] = match.playtime
            spiel_dict["game_bgg_id"] = match.game_bgg_id
            spiel_dict["img_small"] = match.boardgame.img_small
            # Get Players and sort
            players_tmp = []
            for player in match.player_pos:
                players_tmp.append({"name": player.player.name, "punkte": player.points})

            # Sortiere nach Punkten, wenn vorhanden, ansonsten wird die Reihenfolge beibehalten
            players_tmp = [player for player in players_tmp if player["punkte"] is not None]
            if players_tmp:
                players_tmp = sorted(players_tmp, key=lambda x: x["punkte"], reverse=True)
                for pos, player in enumerate(players_tmp):
                    player["position"] = pos + 1
                spiel_dict["players"] = players_tmp
            else:
                spiel_dict["players"] = players_tmp

            spiele_list.append(spiel_dict)

        return spiele_list
    
def create_table(spiele_list: list):
    table = {}
    players = set()
    counter = 1

    for game in spiele_list:
        game_name = f"{counter:02}_{game.get('name')}"
        table[game_name] = {}

        table[game_name]['img_small'] = game.get('img_small')
        for player in game["players"]:
            name = player['name']
            punkte = player['punkte']
            position = player['position']

            if game_name not in table:
                table[game_name] = {}
            table[game_name][name] = (punkte, position)
            players.add(name)
        counter +=1
    
    #Ensure all players are in each game's entry
    for game, player_score in table.items():
        for player in players:
            if player not in player_score:
                player_score[player] = ("", "")

    return table, players



if __name__ == "__main__":
    # events = load_yaml("bogan/events.yaml")
    event_name = "Spielewochenende 2023/2"
    match_games = get_game_list(event_name=event_name)
    print("=======================")
    print(event_name)
    print("=======================")

    # for match_game in match_games:
    #     # print(i+1)
    #     # print(match)
    #     for key, value in match_game.items():
    #         print(f"{key}: {value}")
    #     print("================")

    # get data for table
    table, players = create_table(match_games)

    print(players)
    for key, value in table.items():
        print(f"{key}: {value}")
