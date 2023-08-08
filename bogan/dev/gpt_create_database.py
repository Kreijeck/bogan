from typing import Optional, List
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, Mapped, mapped_column
import json
import os

# Erstelle die Datenbank
engine = create_engine('sqlite:///spiel.db')
Base = declarative_base()

# Erstelle die Tabellenklassen
class Spiel(Base):
    __tablename__ = 'spiele'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    datum: Mapped[str] = mapped_column(String)
    ort: Mapped[str] = mapped_column(String)
    spieler: Mapped[List["Spieler"]] = relationship(back_populates="spiel", cascade="all, delete-orphan")

class Spieler(Base):
    __tablename__ = 'spieler'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    punktzahl = Column(Float)
    spiel_id = Column(Integer, ForeignKey('spiele.id'))
    spiel: Mapped["Spiel"] = relationship(back_populates="spieler")
    benutzer_id = Column(Integer, ForeignKey('benutzer.id'))
    benutzer = relationship("Benutzer", back_populates="spieler")

class Benutzer(Base):
    __tablename__ = 'benutzer'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    spieler = relationship("Spieler", back_populates="benutzer")

# Erstelle die Tabellen
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Öffne eine Sitzung
Session = sessionmaker(bind=engine)
session = Session()

# Lese die Daten aus der JSON-Datei
p = os.path.join('plays.json')
print("Der Pfad ist: ", os.path.abspath(p))
with open(p, 'r', encoding="utf16") as f:
    spieldaten = json.load(f)

# Füge jedes Spiel zur Datenbank hinzu
for play in spieldaten['plays']['play']:
    # Erstelle das Spiel
    spiel = Spiel(datum=play['@date'], ort=play['@location'], name=play['item']['@name'])
    session.add(spiel)

    # Füge jeden Spieler zum Spiel hinzu
    for player in play['players']['player']:
        # Suche nach dem Spieler in der Benutzer-Tabelle
        benutzer = session.query(Benutzer).filter_by(name=player['@name']).first()
        if benutzer is None:
            benutzer = Benutzer(name=player['@name'])
            session.add(benutzer)

        # Erstelle den Spieler und verknüpfe ihn mit dem Benutzer und dem Spiel
        try:
            spieler = Spieler(name=player['@name'], punktzahl=float(player['@score']), spiel=spiel, benutzer=benutzer)
            session.add(spieler)
        except:
            print(f"Wrong Input: Score is: {player['@score']}, Game: {play['item']['@name']}, Player: {player['@name']}")

# Speichere die Änderungen
session.commit()

# Schließe die Sitzung
session.close()