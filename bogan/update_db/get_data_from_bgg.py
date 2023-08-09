import requests
import xmltodict
import json
import os

BASE_URL = 'https://api.geekdo.com/xmlapi2'

def get_plays_dict() -> dict:
    para = {'username': 'Kreijeck'}
    endpoint = "plays"
    resp = requests.get("/".join((BASE_URL, endpoint)), para)
    return xmltodict.parse(resp.text)


def get_boardgame_info(id) -> dict:
    para = {
        'id': id,
        'stats': 1}
    endpoint = "thing"
    resp = requests.get("/".join((BASE_URL, endpoint)), para)
    return xmltodict.parse(resp.text)["items"]["item"]


def get_plays_list():
    return get_plays_dict()["plays"]["play"]


if __name__ == "__main__":
    json_path = os.path.join('data', 'plays.json')
    with open(json_path, "w", encoding="utf-16") as file:
        json.dump(get_plays_dict(), file, indent=2)
        
    for play in get_plays_list():
        print(play)