import json
import os

from sqlalchemy.orm import Session
from bogan.db.models import db, Boardgame
from bogan.db.ask_bgg import get_boardgame, get_games_from

user="Kreijeck"

# print(get_games_from(user))
my_games = get_games_from(user)
for i in my_games:
    print(i)
    break
print(f"Anzahl an Spielen: {len(my_games)}")
