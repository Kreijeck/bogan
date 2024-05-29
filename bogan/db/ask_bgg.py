import xmltodict
import requests
from typing import Union
import time
from bogan.db.config import BGG_BASE_URL, ENCODING, FORCE_LIST_BBG
from bogan.db.models import Boardgame
from bogan.utils import nested_get


def bgg_api_call_get(
    endpoint: str, parameter: dict, nested_paras: list = ['items', 'item'], repeat: int = 3
) -> Union[dict, list[dict]]:
    """Create specific api call on bgg and convert xml to dictionary"""

    raw_json = {}

    for i in range(repeat):
        resp = requests.get("/".join((BGG_BASE_URL, endpoint)), parameter)
               
        if resp.ok:
            tmp_convert = xmltodict.parse(
                resp.text, encoding=ENCODING, force_list=FORCE_LIST_BBG
            )
            raw_json = nested_get(tmp_convert, nested_paras)
            # TODO Remove print
            print(f"Received stats for URL: {resp.url}, with parameter:{parameter}")
            break
        # on negative response
        else:
            time.sleep(0.5)
            # TODO remove print
            # print(f"Try {i+1}: Repeat API-call for URL: {resp.url}, Received: {resp.status}")
            print(
                f"Try {i+1}, Repeat API-call for URL: {resp.url}, Received status code: {resp.status_code}"
            )

    return raw_json


def search_boardgame(search: str) -> list[Boardgame]:
    endpoint = "search"
    para = {"type": "boardgame", "query": search}
    bg_infos_list: list[Boardgame] = []
    # Check search not empty
    if not search:
        return []

    raw_json = bgg_api_call_get(endpoint, para)

    # if not empty or None
    if raw_json:
        # get ids
        ids = []
        names = []
        for item in raw_json:
            ids.append(str(item.get("@id")))

            name = nested_get(item, ["name", 0, "@value"])
            name_is_primary = (
                True if nested_get(item, ["name", 0, "@value"]) == "primary" else False
            )
            names.append((name, name_is_primary))

        # convert ids to correct format
        ids_string = ",".join(ids)

        # get stats for boardgame
        bg_infos_list = get_boardgame(ids_string, names=names)

    return bg_infos_list


def get_boardgame(ids: str, names: list[tuple[str, bool]] = None) -> list[Boardgame]:
    """Get stats from specific boardgame

    Args:
        id (str):   all boardgame ids to get the stats from, separated by < , >.
                    e.g.:   One ID: "12345"
                            multiple IDs: "12345,2342,2423"

    Returns:
        list[Boardgame]:    Boardgame object, with values.
                            extended information about all stats, for example take a look here:
                            https://boardgamegeek.com/xmlapi2/thing?id=251247&stats=1 (items/item will be removed)
    """
    endpoint = "thing"
    para = {"stats": 1, "id": ids}

    # Get Request as json
    raw_json = bgg_api_call_get(endpoint, para)

    bg_results = []
    len_ids = len(ids.split(","))
    # Check das für alle Ids Spiele gefunden werden. Ansonsten setze names auf None
    if len_ids != len(raw_json):
        # TODO remove print
        print(
            f"Es konnte nicht für alle Ids {ids} ein Eintrag gefunden werden, bitte überprüfe die Ids! -> names=None"
        )
        names = None

    if raw_json:
        # validate das raw_json Liste gleich lang ist wie die names liste
        if names is not None and len_ids != len(names):
            # Überlgung ob hier das gleiche passiert wie oben und names=None gesetzt wird
            raise ValueError(
                "Names muss None sein oder die gleiche Länge wie Ids haben"
            )

        # Create Boardgame List
        for i, bg_stat in enumerate(raw_json):
            # Name anpassen, wenn gesetzt
            if names:
                bg_results.append(Boardgame().from_json(bg_stat, name=names[i]))
            else:
                bg_results.append(Boardgame().from_json(bg_stat))

    return bg_results

def get_games_from(user: str, _page: int=1, _tmp_games:list = []) -> list:
    """Erhalte Spiele eines Users aus Boargamegeek

    Args:
        user (str): Username in BGG
        _page (int, optional): wird für Rekursion benötigt, pro Seite maximal 100 Einträge. Defaults to 1.
        _tmp_games(dict, optional): wird für Rekursion benötigt, speichert aktuelle Ergebnisse
    
    Returns:
        dict: json-Datei mit allen Spielen
    """
    endpoint = "plays"
    para = {
        'username': user,
        'page': _page
    }

    response = bgg_api_call_get(endpoint, para, nested_paras=["plays", "play"])
    
    # Solange Daten erhalten werden sind, wird die nächste Seite aufgerufen
    while response:
        _tmp_games.extend(response)
        return get_games_from(user, _page + 1, _tmp_games)

    return _tmp_games




# TODO Remove after trying
if __name__ == "__main__":
    res = search_boardgame("Wasserkraft")

    ## negativ Fall
    # res = get_boardgame("12234,123,78229", [("Wass2r", True),("Wasse3", True)])
    # res = get_boardgame("396802")

    for entry in res:
        print(f"NAME: {entry.name}")
        print(f"PRIMARY: {entry.name_primary}")
        print(f"IMG: {entry.img}")
        print("================")

    # import json
    # import os
    # json_file = "data/example_multiple.json"
    # with open(json_file, 'w', encoding=ENCODING) as f:
    #     json.dump(get_multiple_boardgames(), f, indent=4, ensure_ascii=False)
    #     print(f"Successfully write Json in {os.path.abspath(json_file)}")
