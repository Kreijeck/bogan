from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bogan.database.models import Benutzer, Spieler, Partie, Base
import json
import os


db_path = os.path.join("data", "spiel2.db")


engine = create_engine(f'sqlite:///{db_path}')
#Base = declarative_base()


# Leere Datenbank
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Öffne Session
Session = sessionmaker(bind=engine)
session = Session()

# Leses Daten aus der JSON-Datei
json_path = os.path.join('data', 'plays.json')
with open(json_path, 'r', encoding='utf-16') as f:
    spieldaten = json.load(f)

# Füge jede Partie zur Datenbank hinzu
for play in spieldaten['plays']['play']:
    partie = Partie(id=play['@id'], datum=play['@date'], ort=play['@location'], name=play['item']['@name'])
    session.add(partie)

    # Füge jeden Spieler zur Partie hinzu
    for player in play['players']['player']:
        # Suche nach dem Spieler in der Benutzer-Tabelle, da Name "unique" kann hier nur 0 oder 1 Ergebnis herauskommen
        benutzer = session.query(Benutzer).filter_by(name=player['@name']).first()
        if benutzer is None:
            benutzer = Benutzer(name=player['@name'])
            session.add(benutzer)
        
        # Erstelle den Spieler und verknüpfe ihn mit dem Benutzer und der Partie
        try:
            spieler = Spieler(name=player['@name'], punktzahl=float(player['@score']), partie=partie, benutzer=benutzer)
            session.add(spieler)
        except ValueError:
            spieler = Spieler(name=player['@name'], punktzahl=None, partie=partie, benutzer=benutzer)
            session.add(spieler) 
            print(f"Wrong Input: Score is: {player['@score']}, Game: {play['item']['@name']}, Player: {player['@name']}")
    
    # Speicher die Änderungen
    session.commit()

    # Schließe die Session
    session.close()


