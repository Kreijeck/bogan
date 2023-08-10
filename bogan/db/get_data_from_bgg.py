import requests
import xmltodict
import json
import os
from bogan.config import CFG_YAML, get_logger

cfg_db = CFG_YAML['database']
log = get_logger(__file__)
BASE_URL = cfg_db['base_url']

def get_plays_dict() -> dict:
    para = {'username': 'Kreijeck'}
    endpoint = "plays"
    resp = requests.get("/".join((BASE_URL, endpoint)), para)
    #print(xmltodict.parse(resp.text))
    return xmltodict.parse(resp.text, encoding=CFG_YAML['encoding'])


def get_boardgame_info(id) -> dict:
    para = {
        'id': id,
        'stats': 1}
    endpoint = "thing"
    resp = requests.get("/".join((BASE_URL, endpoint)), para)
    return xmltodict.parse(resp.text, encoding=CFG_YAML['encoding'])["items"]["item"]


def get_plays_list():
    return get_plays_dict()["plays"]["play"]


def get_and_write_play_data() -> dict:
    """Get Plays from BGG
    if bgg_json is not None: Json File will be saved

    Returns:
        dict: Json File with all plays
    """
    play_file = get_plays_dict()
    for play in play_file["plays"]["play"]:
        log.debug(f"Play received: {play}")
    # Create json-File
    if cfg_db['bgg_json']:
        json_path = os.path.join(cfg_db['dir'], cfg_db['bgg_json'])
        with open(json_path, 'w', encoding=CFG_YAML['encoding']) as f:
            json.dump(play_file, f, indent=2)
            log.info(f"Successfully create json-file: {json_path}")
            
    
    return play_file



if __name__ == "__main__":
    json_path = os.path.join('data', 'plays.json')
    with open(json_path, "w", encoding=CFG_YAML['encoding']) as file:
        json.dump(get_plays_dict(), file, indent=2)
        
    for play in get_plays_list():
        print(play)