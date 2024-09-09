import xmltodict
import requests
from requests.exceptions import ChunkedEncodingError, RequestException
from typing import Union
import time
from bogan.config import BGG_BASE_URL, ENCODING, TAG2LIST_BOARDGAME, TAG2LIST_PLAY
from bogan.db.models import Boardgame
from bogan.utils import nested_get


def bgg_api_call_get(
    endpoint: str, parameter: dict, nested_paras: list = [], tag2list: tuple = {}, repeat: int = 3
) -> Union[dict, list[dict]]:
    """Create specific api call on bgg and convert xml to dictionary"""

    raw_json = {}

    for i in range(repeat):
        resp = requests.get("/".join((BGG_BASE_URL, endpoint)), parameter, timeout=10)
        # Fehlerbehandlung bei nicht vollständig übertragener Daten
        try:
            if resp.ok:

                tmp_convert = xmltodict.parse(resp.text, encoding=ENCODING, force_list=tag2list)
                raw_json = nested_get(tmp_convert, nested_paras)

                # TODO Remove print
                print(f"BGG API Call on URL: {resp.url}, with parameter:{parameter}")
                break
            # on negative response
            else:
                time.sleep(1)
                # TODO remove print
                print(f"Try {i+1}, Repeat API-call for URL: {resp.url}, Received status code: {resp.status_code}")
        except ChunkedEncodingError as e:
            time.sleep(1)
            # TODO remove print
            print(f"Try {i+1}, ChunkedEncodingError for URL: {resp.url if resp in locals() else endpoint}, Error: {e}")
        except RequestException as e:
            time.sleep(1)
            # TODO remove print
            print(f"Try {i+1}, RequestException for URL: {resp.url if resp in locals() else endpoint}, Error: {e}")

    return raw_json


def search_boardgame(search: str) -> list[Boardgame]:
    endpoint = "search"
    para = {"type": "boardgame", "query": search}
    bg_infos_list: list[Boardgame] = []
    # Check search not empty
    if not search:
        return []

    raw_json = bgg_api_call_get(endpoint, para, tag2list=TAG2LIST_BOARDGAME, nested_paras=["items", "item"])

    # if not empty or None
    if raw_json:
        # get ids
        ids = []
        names = []
        for item in raw_json:
            ids.append(str(item.get("@id")))

            name = nested_get(item, ["name", 0, "@value"])
            name_is_primary = True if nested_get(item, ["name", 0, "@value"]) == "primary" else False
            names.append((name, name_is_primary))

        # convert ids to correct format
        # ids_string = ",".join(ids)

        # get stats for boardgame
        bg_infos_list = ask_boardgame(ids, names=names)

    return bg_infos_list


def ask_boardgame(ids: Union[str, list[str]], names: list[tuple[str, bool]] = None) -> list[Boardgame]:
    """Get stats from specific boardgame

    Args:
        id (str, list):     all boardgame ids as list
                            or one id a str

    Returns:
        list[Boardgame]:    Boardgame object, with values.
                            extended information about all stats, for example take a look here:
                            https://boardgamegeek.com/xmlapi2/thing?id=251247&stats=1 (items/item will be removed)
    """

    def split_list(input_list, chunk_size=15):
        """
        Teilt eine Liste in mehrere Listen mit maximal 'chunk_size' Einträgen.

        :param input_list: Die Liste, die aufgeteilt werden soll.
        :param chunk_size: Die maximale Anzahl der Einträge pro Liste (Standard: 20).
        :return: Eine Liste von Listen mit jeweils maximal 'chunk_size' Einträgen.
        """
        # Erzeuge Teil-Listen mit der angegebenen Größe
        return [input_list[i : i + chunk_size] for i in range(0, len(input_list), chunk_size)]

    # Convert all types into a list with length 1 and as str
    if not isinstance(ids, list):
        ids = [str(ids)]
    else:
        ids = [str(id_) for id_ in ids]

    # Split the ids list into chunks of 20
    chunked_ids = split_list(ids, chunk_size=20)

    endpoint = "thing"
    bg_results = []

    # Process each chunk of ids
    for chunk in chunked_ids:
        # Convert list to comma separated string
        ids_chunk = ",".join(chunk)
        len_chunk = len(chunk)

        para = {"stats": 1, "id": ids_chunk}

        # Get Request as json
        raw_json = bgg_api_call_get(endpoint, para, nested_paras=["items", "item"], tag2list=TAG2LIST_BOARDGAME)

        # Check that for all Ids games are found; otherwise, set names to None
        if len_chunk != len(raw_json):
            print(
                f"Es konnte nicht für alle Ids {ids_chunk} ein Eintrag gefunden werden, bitte überprüfe die Ids! -> names=None"
            )
            names = None

        if raw_json:
            # Validate that raw_json list is the same length as the names list
            if names is not None and len_chunk != len(names):
                raise ValueError("Names muss None sein oder die gleiche Länge wie Ids haben")

            # Create Boardgame List
            for i, bg_stat in enumerate(raw_json):
                # Name anpassen, wenn gesetzt
                if names:
                    bg_results.append(Boardgame().from_bgg(bg_stat, name=names[i]))
                else:
                    bg_results.append(Boardgame().from_bgg(bg_stat))

    return bg_results


def ask_games_from(user: str, _page: int = 1, _tmp_games: list = []) -> list:
    """Erhalte Spiele eines Users aus Boargamegeek

    Args:
        user (str): Username in BGG
        _page (int, optional): wird für Rekursion benötigt, pro Seite maximal 100 Einträge. Defaults to 1.
        _tmp_games(dict, optional): wird für Rekursion benötigt, speichert aktuelle Ergebnisse

    Returns:
        dict: json-Datei mit allen Spielen
    """
    endpoint = "plays"
    para = {"username": user, "page": _page}

    response = bgg_api_call_get(endpoint, para, nested_paras=["plays", "play"], tag2list=TAG2LIST_PLAY)

    # Solange Daten erhalten werden sind, wird die nächste Seite aufgerufen
    while response:
        _tmp_games.extend(response)
        return ask_games_from(user, _page + 1, _tmp_games)

    return _tmp_games
