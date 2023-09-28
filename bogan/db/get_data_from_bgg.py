import requests
import xmltodict
import json
import os
from bogan.config import get_logger, cfg_encoding, cfg_db


log = get_logger(__file__)
BASE_URL = cfg_db['base_url']

def validate_json(json_file: dict) -> bool:
    """Überprüft ob json-File die keys ["plays]["play hat]

    Args:
        json_file (dict): json-file von bgg

    Returns:
        bool:   True: Partien können eingelesen werden
                False: Es fehlt ein notwendiger Key für Partien (["plays]["play])

    """
    if "plays" in json_file.keys():
        if "play" in json_file["plays"].keys():
            return True
    # Struktur leer, kein passendes Format
    return False

def get_plays_dict(page:int) -> dict:
    para = {'username': 'Kreijeck', 'page': page}
    endpoint = "plays"
    resp = requests.get("/".join((BASE_URL, endpoint)), para)
    #print(xmltodict.parse(resp.text))
    return xmltodict.parse(resp.text, encoding=cfg_encoding)


def get_boardgame_info(id) -> dict:
    para = {
        'id': id,
        'stats': 1}
    endpoint = "thing"
    
    # If key is missing: try again -> 5 times
    repeat = 0
    while repeat < 5:
        resp = requests.get("/".join((BASE_URL, endpoint)), para)
        if resp.ok:
            return xmltodict.parse(resp.text, encoding=cfg_encoding)["items"]["item"]
        else:
            repeat += 1
            log.debug(f"Try {repeat}: Repeat API-call bordgamestats: Received: {resp}")

    log.warning("received no correct format from BGG-API -> Return None")
    return None


def get_plays_list():
    return get_plays_dict()["plays"]["play"]


def get_and_write_play_data() -> dict:
    """Get Plays from BGG
    if bgg_json is not None: Json File will be saved

    Returns:
        dict: Json File with all plays
    """
    # Read all play_data (1 page max. 100 results)
    play_exist = True
    page = 1
    play_file_list = []
    while play_exist:
        tmp_play = get_plays_dict(page=page)
        play_exist = validate_json(tmp_play)
        if play_exist:
            play_file_list.append(tmp_play)
            page += 1

    # Combine playfiles
    play_file = {}
    for play_page in play_file_list:
        # On first iteration fill playfile with json-format
        if play_file:
            # Wenn json-File Partien enthält
            if validate_json(play_page):
                play_file["plays"]["@page"] = len(play_file_list)
                play_file["plays"]["play"] += play_page["plays"]["play"] 
            else:
                log.error("Format der .json-Datei von BGG entspricht nicht den Vorgaben")
                exit()
        else:
            play_file = play_page

    # Create json-File
    if cfg_db['bgg_json']:
        json_path = os.path.join(cfg_db['dir'], cfg_db['bgg_json'])
        with open(json_path, 'w', encoding=cfg_encoding) as f:
            json.dump(play_file, f, indent=2)
            log.info(f"Successfully create json-file: {json_path}")
    try:
        for play in play_file["plays"]["play"]:
            log.debug(f"Play received: {play}")
    except KeyError as e:
        log.error("Es konnte keine Daten für Spiele gefunden werden! Bitte Parameter überprüfen!")
        log.error(f"Key-Error: {e}")
        exit()
            

    return play_file



if __name__ == "__main__":
    pass