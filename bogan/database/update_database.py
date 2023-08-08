from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from bogan.database.models import Benutzer, Spieler, Partie, Base
import json
import os


db_path = os.path.join("data", "spiel2.db")

# def add_partie(spieldaten: list, session: Session) -> Session:
#     for play in spieldaten:
#         partie = Partie(id=play['@id'], datum=play['@date'], ort=play['@location'], name=play['item']['@name'])
#         session.add(partie)

#     return session

# def add_player(player: list, session: Session) -> Session:


    

engine = create_engine(f'sqlite:///{db_path}')
#Base = declarative_base()


# Leere Datenbank
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Öffne Session
#Session = sessionmaker(bind=engine)
session = Session(engine)

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
        # Überprüfe ob Punktzahl vorhanden
        punktzahl: str = player['@score']
        if punktzahl.isdigit():
            punktzahl = float(punktzahl)
        else:
            punktzahl = None
            
        spieler = Spieler(name=player['@name'], punktzahl=punktzahl, partie=partie, benutzer=benutzer)
        session.add(spieler)
    
    # Speicher die Änderungen
    session.commit()

    # Schließe die Session
    session.close()


