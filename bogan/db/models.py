from typing import List
from datetime import date
from sqlalchemy import String, Float, Integer, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    def set(self, attribute, value):
        """Setzt den Wert des angegebenen Attributs.

        Args:
            attribute (str): Name des Attributs.
            value: Wert, der zugewiesen werden soll.
        """
        setattr(self, attribute, value)

# Base = declarative_base()


class Partie(Base):
    """Eine Partie im gesamten

    Args:
        id (int): ID aus BGG
        brettspiel (string): Link zum Brettspiel
        datum (string): Datum der Partie
        ort (string): Link zum Ort
        spieler (list): Liste der Spieler, sowie der erzielten Punkte
    """

    __tablename__ = "partie"
    id: Mapped[int] = mapped_column(primary_key=True)
    brettspiel_id: Mapped[int] = mapped_column(ForeignKey("brettspiel.id"))
    brettspiel: Mapped["Brettspiel"] = relationship(back_populates="partie")
    datum: Mapped[date] = mapped_column(Date)
    ort_id: Mapped[int] = mapped_column(ForeignKey("ort.id"))
    ort: Mapped["Ort"] = relationship(back_populates="partie")
    spieler: Mapped[List["SpielerPos"]] = relationship(back_populates="partie", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Partie(id={self.id}, brettspiel={self.brettspiel.name}, datum={self.datum}, ort={self.ort.name}, "\
        f"Spieler={self.spieler})"


class SpielerPos(Base):
    """Spieler inklusive Punkte bei einer absolvierten Partie

    Args:
        id (int): ID
        punktzahl (float): erreichte Punkte im Spiel
        partie_id (int): id der zugehörigen Partie
        benutzer_id (int): id des benutzers

    """

    __tablename__ = "spieler_pos"
    id: Mapped[int] = mapped_column(primary_key=True)
    #name: Mapped[str] = mapped_column(String)
    punktzahl: Mapped[float] = mapped_column(Float, nullable=True)
    win: Mapped[bool] = mapped_column(Boolean)
    position: Mapped[int] = mapped_column(Integer, nullable=True)
    partie_id: Mapped[int] = mapped_column(ForeignKey("partie.id"))
    partie: Mapped["Partie"] = relationship(back_populates="spieler")
    benutzer_id: Mapped[int] = mapped_column(ForeignKey("benutzer.id"))
    benutzer: Mapped["Benutzer"] = relationship(back_populates="spieler")
    
    def __repr__(self) -> str:
        return f"SpielerPos(id={self.id}, name={self.benutzer.name}, punktzahl={self.punktzahl}, "\
    f"ranking={self.position}, partie={self.partie.brettspiel.name})"


class Benutzer(Base):
    """Alles wissenswerte über einen User

    Args:
        id (int): id des User
        name: (str, unique): Name des User
    """

    __tablename__ = "benutzer"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    spieler: Mapped[List["SpielerPos"]] = relationship("SpielerPos", back_populates="benutzer")

    def __repr__(self) -> str:
        return f"Benutzer(id={self.id}, name={self.name})"


class Brettspiel(Base):
    """Details zum Brettspiel

    Args:
        id (int): id des Brettspiels aus BGG
        name (str): Name des Spiels
        complexity (float): Komplexität des Spiels aus BGG
        duration (int): durchschnittliche Dauer eines Spiels
    """

    __tablename__ = "brettspiel"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    complexity: Mapped[float] = mapped_column(Float, nullable=True)
    duration: Mapped[int] = mapped_column(Integer, nullable=True)
    image: Mapped[str] = mapped_column(String, nullable=True)
    image_small: Mapped[str] = mapped_column(String, nullable=True)
    partie: Mapped[List["Partie"]] = relationship(back_populates="brettspiel")
    #categories: Mapped[List["BggCategory"]] = relationship(back_populates="bgg_category")

    def __repr__(self) -> str:
        return f"Brettspiel(id={self.id}, name={self.name}, "\
            f"complexity={self.complexity or 'na'}, duration={self.duration or 'na'})"

    
# class BggCategory(Base):
#     __tablename__ = "_bgg_category"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String)
#     boardgame: Mapped["Brettspiel"] = relationship(back_populates='categories')

    def __repr__(self) -> str:
        return f"BggCategory(id={self.id}, name={self.name})"



class Ort(Base):
    """Ort an dem Spiel durchgeführt wurde

    Args:
        id (int): id des Ortes
        name (str): Name des Ortes
    """

    __tablename__ = "ort"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    partie: Mapped[List["Partie"]] = relationship("Partie", back_populates="ort")

    def __repr__(self) -> str:
        return f"Ort(id={self.id}, name={self.name})"
