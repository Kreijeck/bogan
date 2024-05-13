import ask_bgg as bgg
import json
import os
from config import ENCODING
print(bgg.search_boardgame("Wasserkraft"))

json_file = "data/example.json"
os.mkdir("data")
with open(json_file, 'w', encoding=ENCODING) as f:
    json.dump(bgg.get_boardgame_all_stats(251247), f, indent=4)
    print(f"Successfully write Json in {os.path.abspath(json_file)}")
