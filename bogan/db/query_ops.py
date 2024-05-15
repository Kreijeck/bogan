import ask_bgg as bgg
import json
import os
from config import ENCODING


# print(bgg.search_boardgame("Wasserkraft"))

# json_file = "data/example.json"
# with open(json_file, 'w', encoding=ENCODING) as f:
#     json.dump(bgg.get_boardgame_all_stats(251247), f, indent=4, ensure_ascii=False)
#     print(f"Successfully write Json in {os.path.abspath(json_file)}")

from models import Brettspiel

print(Brettspiel().convert_from_bgg_full(bgg.get_boardgame_all_stats(251247)))
