from bogan.db.config import BGG_BASE_URL, ENCODING
import xmltodict
import requests

def search_boardgame(search: str):
    endpoint = "search"
    para = {
        "type": "boardgame",
        "query": search
    }

    response = requests.get("/".join((BGG_BASE_URL, endpoint)), params=para)

    return xmltodict.parse(response.text, encoding=ENCODING)["items"]["item"]

def get_boardgame_all_stats(id: int) -> dict:
    """Get stats from specific boardgame

    Args:
        id (str): bgg_id of boardgame

    Returns:
        dict: extended information about boardgame as dictionary, for example take a look here:
                https://boardgamegeek.com/xmlapi2/thing?id=251247&stats=1 (items/item will be removed)
    """
    endpoint = "thing"
    para = {
        "stats": 1,
        "id": id
    }
    # Repeat if server is unavailable -> 25 times
    repeat = 0
    while repeat < 25:
        resp = requests.get("/".join((BGG_BASE_URL, endpoint)), para)
        
        if resp.ok:
            # Wenn id nicht vorhanden, gibt es keine ["items"]["item"]
            try:
                json_dict = xmltodict.parse(resp.text, encoding=ENCODING)["items"]["item"]
                # TODO Remove print
                print(f"Received stats for ID {id} on URL: {resp.url}")
                return json_dict
            
            except KeyError:
                repeat += 1
                continue
        else:
            repeat += 1
            # TODO Remove print
            print(f"Try {repeat}: Repeat API-call bordgamestats: Received: {resp}")

    # TODO Remove print
    print(f"no boardgame info received for id: {id} on URL: {resp.url} -> Return None")
    return None