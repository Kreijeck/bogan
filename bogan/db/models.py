from typing import List
from sqlalchemy import String, ForeignKey, Float, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Hilfsmethoden
def _nested_get(d: dict, keys: list, typ: type):
    """Usage of get method for nested dictionary to convert json-files

    Args:
        nested_dict (dict): nested dictionary/list
        parameters (list): list of keys
        typ (type): convert to specific type

    Returns:
        any: return value of specific type
    """
    for key in keys:
        if isinstance(d, list):
            try:
                d = d[key]
            except IndexError:
                return None
            
        elif isinstance(d, dict):
            d = d.get(key, None)
        
        else:
            return None
        
        if d is None:
            return None

    # convert to correct type
    return typ(d)


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(128), unique=True)
    password: Mapped[str] = mapped_column(String(256))
    name: Mapped[str] = mapped_column(String(128))
    role: Mapped[str] = mapped_column(String(128), default="user")
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
    bgg_id: Mapped[int] = mapped_column(Integer)
    name_primary: Mapped[str] = mapped_column(String(255))
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

    def __repr__(self) -> str:
        return f"Brettspiel {self.name_primary}, img={self.img}, img_small={self.img_small}, "\
                f"published={self.yearpublished}, for {self.minplayers} - {self.maxplayers} Players, "\
                f"playtime = {self.playingtime}, rating={self.rating}, weight= {self.weight}"

    def convert_from_bgg_full(self, json_file: dict):
        """Read json File and auto-fill the arguments of the current boardgame

        Args:
            json_file (dict): json-file from bgg

        Returns:
            self: self with updated parameters
        """
        # Add all data available in bgg
        self.bgg_id = _nested_get(json_file,['id'], int)
        self.name_primary = _nested_get(json_file, ["name", 0, "@value"], str)
        self.img = _nested_get(json_file, ['image2'], str)
        self.img_small = _nested_get(json_file, ['thumbnail'], str)
        self.yearpublished = _nested_get(json_file, ['yearpublished', '@value'], int)
        self.minplayers = _nested_get(json_file, ['minplayers', '@value'], int)
        self.maxplayers = _nested_get(json_file, ["maxplayers", "@value"], int)
        self.playingtime = _nested_get(json_file, ["playingtime", "@value"], int)
        self.rating = _nested_get(json_file, ["statistics", "ratings", "average", "@value"], float)
        self.weight = _nested_get(json_file, ["statistics", "ratings", "averageweight", "@value"], float)

        return self
