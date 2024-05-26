from typing import List
from sqlalchemy import String, ForeignKey, Float, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from bogan.utils import nested_get
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)



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


class Boardgame(db.Model):

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
    playtime: Mapped[int] = mapped_column(Integer)

    # Rating
    rating: Mapped[float] = mapped_column(Float)
    weight: Mapped[float] = mapped_column(Float)

    # Relationship TODO: only needed, when we want to have vote in Database
    # in_votes: Mapped[List["Vote"]] = relationship(back_populates="brettspiel", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Brettspiel {self.name_primary}, img={self.img}, img_small={self.img_small}, "\
                f"published={self.yearpublished}, for {self.minplayers} - {self.maxplayers} Players, "\
                f"playtime = {self.playtime}, rating={self.rating}, weight= {self.weight}"

    def from_json(self, json_file: dict, name:tuple[str, bool] = None):
        """Read json File and auto-fill the arguments of the current boardgame instance

        Args:
            json_file (dict): JSON file from BGG
            name (tuple[str, bool], optional): (alternative name, is_primary_name). Defaults to None.

        Returns:
            self: self with updated parameters
        """

        def create_names(name: tuple[str,bool]):
            """
            self.name and self.name_primary are calculated here

            Args:
                name (tuple[str,bool]): (alternative name, is_primary_name) or None

            Returns:
                tuple: (self.name, self.name_primary) 
            """
            default_name = nested_get(json_file, ["name", 0, "@value"], str)
            # if name not None
            if name:
                if name[1]:
                    return (name[0], name[0])
                else:
                    return (name[0], default_name)
            # both values get the primary name
            else:
                return (default_name, default_name)


        # Add all data available in bgg
        self.bgg_id = nested_get(json_file,['@id'], int)
        
        # self.name and self.name_primary can be set with this function
        self.name, self.name_primary = create_names(name)
        self.img = nested_get(json_file, ['image'], str)
        self.img_small = nested_get(json_file, ['thumbnail'], str)
        self.yearpublished = nested_get(json_file, ['yearpublished', '@value'], int)
        self.minplayers = nested_get(json_file, ['minplayers', '@value'], int)
        self.maxplayers = nested_get(json_file, ["maxplayers", "@value"], int)
        self.playtime = nested_get(json_file, ["playingtime", "@value"], int)
        self.rating = nested_get(json_file, ["statistics", "ratings", "average", "@value"], float)
        self.weight = nested_get(json_file, ["statistics", "ratings", "averageweight", "@value"], float)

        return self
