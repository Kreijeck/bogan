import os
from typing import Optional, List
from sqlalchemy import create_engine, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column


Base = declarative_base()


class Partie(Base):
    """Eine Partie im gesamten

    Args:
        id (int): ID aus BGG
        name (string): Name des Brettspiels
        datum (string): Datum der Partie
        ort (string): Ort der Partie
        spieler (list): Liste der Spieler, sowie der erzielten Punkte
    """
    __tablename__ = 'partie'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    datum: Mapped[str] = mapped_column(String)
    ort: Mapped[str] = mapped_column(String)
    spieler: Mapped[List["Spieler"]] = relationship(back_populates='partie', cascade='all, delete-orphan')

class Spieler(Base):
    """Spieler inklusive Punkte bei einer absolvierten Partie

    Args:
        id (int): ID
        name (string): Spielername
        punktzahl (float): erreichte Punkte im Spiel

    """
    __tablename__ = 'spieler'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    punktzahl: Mapped[float] = mapped_column(Float, nullable=True)
    partie_id: Mapped[int] = mapped_column(ForeignKey('partie.id'))
    partie: Mapped["Partie"] = relationship(back_populates='spieler')
    benutzer_id: Mapped[int] = mapped_column(ForeignKey('benutzer.id'))
    benutzer: Mapped["Benutzer"] =  relationship(back_populates="spieler")

class Benutzer(Base):
    __tablename__ = 'benutzer'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    spieler: Mapped[List['Spieler']] = relationship('Spieler', back_populates='benutzer')

class Brettspiel(Base):
    __tablename__ = 'brettspiel'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
