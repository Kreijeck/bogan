import json
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from bogan.db.models import Partie, SpielerPos, Benutzer, Brettspiel, Ort, Base

# Erstelle eine SQLite-Testdatenbank im Speicher
engine = create_engine('sqlite:///:memory:')
# engine = create_engine("sqlite:///tests/data/test_spiel2.db")

# Erstelle neue Datenbank
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Erstelle eine Session
session = Session(engine)

# Erstelle einige Benutzer
benutzer_namen = {
    "Spieler1": Benutzer(name="Spieler1"),
    "Spieler2": Benutzer(name="Spieler2"),
    "Spieler3": Benutzer(name="Spieler3"),
    "Spieler4": Benutzer(name="Spieler4"),
    "Spieler5": Benutzer(name="Spieler5"),
    "Spieler6": Benutzer(name="Spieler6"),
}
session.add_all(benutzer_namen.values())
session.commit()


# Erstelle einige Brettspiele
brettspiel_obj = {
    "Spiel1": Brettspiel(name="Spiel1", complexity=2.0, duration=60),
    "Spiel2": Brettspiel(name="Spiel2", complexity=3.5, duration=90),
    "Spiel3": Brettspiel(name="Spiel3", complexity=1.5, duration=45),
    "Spiel4": Brettspiel(name="Spiel4", complexity=4.5, duration=30),
}
session.add_all(brettspiel_obj.values())
session.commit()

# Erstelle einige Orte
orte_namen = {
    "Ort1": Ort(name="Ort1"),
    "Ort2": Ort(name="Ort2"),
    "Ort3": Ort(name="Ort3"),
}
session.add_all(orte_namen.values())
session.commit()

# Lese alle Datensätze aus data_pytest.json.
file_pytest = "data_pytest.json"
json_filename = os.path.join("tests", "data", file_pytest)
with open(json_filename, 'r') as json_file:
    data_100 = json.load(json_file)

# Lese alle Dateien aus der json ein und speicher sie in der Datenbank
partien = []
for data in data_100:
    brettspiel = brettspiel_obj[data["brettspiel"]]
    ort = orte_namen[data["ort"]]
    datum = datetime.strptime(data["datum"], "%Y-%m-%d")
    spieler_list = []
    for one_spieler in data["spieler"]:
        spieler_list.append(SpielerPos(punktzahl=one_spieler["punktzahl"],
                                       benutzer=benutzer_namen[one_spieler["benutzer"]],
                                        win=one_spieler["win"], ))
    spieler = spieler_list

    # Erstelle vollständige Partie
    partie = Partie(brettspiel=brettspiel, datum=datum, ort=ort, spieler=spieler)
    session.add(partie)

session.commit()

# Schließe die Session
session.close()
