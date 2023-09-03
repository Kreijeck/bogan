import random
import os
import json
from datetime import date, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from bogan.db.models import Partie, SpielerPos, Benutzer, Brettspiel, Ort, Base

# Erstelle eine SQLite-Testdatenbank im Speicher
engine = create_engine('sqlite:///tests/data/test_spiel2.db')

# Erstelle neue Datenbank
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Erstelle eine Session
session = Session(engine)

# Erstelle einige Benutzer
benutzer_namen = ["Spieler1", "Spieler2", "Spieler3", "Spieler4", "Spieler5", "Spieler6"]
benutzer_liste = [Benutzer(name=name) for name in benutzer_namen]
session.add_all(benutzer_liste)
session.commit()

# Erstelle einige Brettspiele
brettspiele = [
    Brettspiel(name="Spiel1", complexity=2.0, duration=60),
    Brettspiel(name="Spiel2", complexity=3.5, duration=90),
    Brettspiel(name="Spiel3", complexity=1.5, duration=45),
    Brettspiel(name="Spiel4", complexity=4.5, duration=30),
]
session.add_all(brettspiele)
session.commit()

# Erstelle einige Orte
orte_namen = ["Ort1", "Ort2", "Ort3"]
orte_liste = [Ort(name=name) for name in orte_namen]
session.add_all(orte_liste)
session.commit()

# Erstelle einige Partien mit Spielern
partien = []
# Erstelle Data list für json
data_list = []
for counter in range(100):
    
    # Erstelle zufällige Werte für Ort, Brettspiel, Datum
    brettspiel = random.choice(brettspiele)
    ort = random.choice(orte_liste)
    datum = date.today() - timedelta(days=random.randint(1, 600))
    
    # Erstelle dict für json
    data_dict = {}
    data_dict["brettspiel"] = brettspiel.name
    data_dict["ort"] = ort.name
    data_dict["datum"] = datum.strftime("%Y-%m-%d")
        
    spieler_list = []
    spieler = random.sample(benutzer_liste, random.randint(2, len(benutzer_liste)))


    # Erstelle Partie ohne Spieler
    partie = Partie(brettspiel=brettspiel, datum=datum, ort=ort)
    session.add(partie)

    # Füge Spieler zur Partie hinzu
    # Erzeuge Punktzahlen für Spieler
    punktzahl_liste = [round(random.uniform(-5,100),2) for _ in range(len(spieler))]
    for i, benutzer in enumerate(spieler):
        # Spieler mit größter Punktzahl erhält "win"
        punktzahl = punktzahl_liste[i]
        win = True if punktzahl == max(punktzahl_liste) else False
        
        spieler_pos = SpielerPos(punktzahl=punktzahl, win=win, benutzer=benutzer)
        partie.spieler.append(spieler_pos)

        spieler_dict = {
            "punktzahl": punktzahl,
            "benutzer": benutzer.name,
            "win": win }
        spieler_list.append(spieler_dict)
    
    data_dict["spieler"] = spieler_list
    data_list.append(data_dict)
    
    session.commit()
    partien.append(partie)


session.commit()

# Schließe die Session
session.close()

# Schreibe List-dictionary in a file:
cwd = os.path.dirname(__file__)
filename = os.path.join(cwd, "data_random.json")
with open(filename, 'w') as json_file:
    json.dump(data_list, json_file, indent=2)