from typing import List
from sqlalchemy import String, ForeignKey, Float, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(128), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(128))
    bgg_name: Mapped[str] = mapped_column(String(128), nullable=True)

    def __repr__(self) -> str:
        return f"ID: {self.id}, EMAIL: {self.email}, NAME: {self.name}"

# TODO Think about Usage of this table 
# class Vote(db.Model):
#     __tablename__ = "vote"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(200), unique=True)
#     brettspiel_id : Mapped[int] = mapped_column(ForeignKey("brettspiel.id"))
#     brettspiel: Mapped["Brettspiel"] = relationship(back_populates="in_votes")

class Brettspiel(db.Model):
    __tablename__ = "brettspiel"
    # default Information
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    img: Mapped[str] = mapped_column(String(255))
    img_small: Mapped[str] = mapped_column(String(255))
    yearpublished: Mapped[int] = mapped_column(Integer)
    minplayers: Mapped[int] = mapped_column(Integer)
    maxplayers: Mapped[int] = mapped_column(Integer)
    playingtime: Mapped[int] = mapped_column(Integer)

    # Rating
    rating: Mapped[float] = mapped_column(Float)
    weight: Mapped[float] = mapped_column(Float)
    
    # Relationship TODO: only needed, when we want to have vote in Database
    # in_votes: Mapped[List["Vote"]] = relationship(back_populates="brettspiel", cascade="all, delete-orphan")

    def convert_from_bgg_full(self, json_file: dict):
        return {
            'bgg_id': int(json_file["@id"]),
            'name': str(json_file["name"][0]["@value"]),
            'img': str(json_file["image"]),
            'img_small': str(json_file["thumbnail"]),
            'yearpublished': int(json_file["yearpublished"]['@value']),
            'minplayers': int(json_file["minplayers"]['@value']),
            'maxplayers': int(json_file["maxplayers"]['@value']),
            'playingtime': int(json_file["playingtime"]['@value']),
            'weight': float(json_file["statistics"]["ratings"]["averageweight"]["@value"]),
            'rating': float(json_file["statistics"]["ratings"]["average"]["@value"])
        }
