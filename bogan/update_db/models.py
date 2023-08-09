from typing import List
from datetime import date
from sqlalchemy import String, Float, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column


Base = declarative_base()


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
    spieler: Mapped[List["Spieler"]] = relationship(back_populates="partie", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"ID: {self.id}, brettspiel: {self.brettspiel.name}, datum: {self.datum}, ort: {self.ort.name}, "\
        f"Players: {self.spieler}"


class Spieler(Base):
    """Spieler inklusive Punkte bei einer absolvierten Partie

    Args:
        id (int): ID
        name (string): Spielername
        punktzahl (float): erreichte Punkte im Spiel
        partie_id (int): id der zugehörigen Partie
        benutzer_id (int): id des benutzers

    """

    __tablename__ = "spieler"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    punktzahl: Mapped[float] = mapped_column(Float, nullable=True)
    partie_id: Mapped[int] = mapped_column(ForeignKey("partie.id"))
    partie: Mapped["Partie"] = relationship(back_populates="spieler")
    benutzer_id: Mapped[int] = mapped_column(ForeignKey("benutzer.id"))
    benutzer: Mapped["Benutzer"] = relationship(back_populates="spieler")

    def __repr__(self) -> str:
        return f"ID: {self.id}, name: {self.name}, punktzahl: {self.punktzahl}, "\
            f"partie_id: {self.partie_id}, benutzer: {self.benutzer}"


class Benutzer(Base):
    """Alles wissenswerte über einen User

    Args:
        id (int): id des User
        name: (str, unique): Name des User
    """

    __tablename__ = "benutzer"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    spieler: Mapped[List["Spieler"]] = relationship("Spieler", back_populates="benutzer")

    def __repr__(self) -> str:
        return f"ID: {self.id}, name:{self.name}"


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
    partie: Mapped[List["Partie"]] = relationship(back_populates="brettspiel")

    def __repr__(self) -> str:
        return f"ID: {self.id}, name: {self.name}, "\
            f"complexity: {self.complexity or 'na'}, duration: {self.duration or 'na'}"


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
    # partie: Mapped["Partie"] = relationship(back_populates="ort")

    def __repr__(self) -> str:
        return f"ID: {self.id}, Name: {self.name}"
