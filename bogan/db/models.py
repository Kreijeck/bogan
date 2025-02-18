from typing import List
from datetime import date
from sqlalchemy import String, ForeignKey, Float, Integer, Date, Boolean
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
    player_id: Mapped[int] = mapped_column(ForeignKey("player.id"), nullable=True)

    # Relationship
    player: Mapped["Player"] = relationship("Player", back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id}, email={self.email}, name={self.name}, bgg_name={self.bgg_name}, role={self.role})"


class Player(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True)
    bgg_name: Mapped[str] = mapped_column(String(128), nullable=True)
    # Relationship
    player_pos: Mapped[List["PlayerPos"]] = relationship(
        "PlayerPos", back_populates="player", cascade="all, delete-orphan"
    )
    user: Mapped["User"] = relationship("User", back_populates="player")

    def __repr__(self) -> str:
        return f"Player(id={self.id}, name={self.name}, bgg_name={self.bgg_name}, user={self.user})"


class PlayerPos(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    points: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    win: Mapped[bool] = mapped_column(Boolean)
    game_id: Mapped[int] = mapped_column(ForeignKey("game.id"))
    player_id: Mapped[int] = mapped_column(ForeignKey("player.id"))
    # Relationship
    game: Mapped["Game"] = relationship("Game", back_populates="player_pos")
    player: Mapped["Player"] = relationship("Player", back_populates="player_pos")

    def __repr__(self) -> str:
        return f"PlayerPos(id={self.id}, name={self.player.name}, punktzahl={self.points}, partie={self.game.boardgame.name})"

    def update(self, other) -> bool:
        """Update PlayerPos mit aktuellen Werten

        Args:
            other (player_pos): neues "PlayerPos"-Objekt

        Raises:
            TypeError: ungültiges Objekt übergeben

        Returns:
            bool: Gab es Änderungen
        """

        if not isinstance(other, type(self)):
            raise TypeError("Update nicht möglich, es handelt sich um kein game-model")

        changed = False

        if self.points != other.points:
            self.points = other.points
            changed = True
        if self.win != other.win:
            self.win = other.win
            changed = True
        if self.game_id != other.game_id:
            self.game_id = other.game_id
            changed = True
        if self.player_id != other.player_id:
            self.player_id = other.player_id
            changed = True

        return changed


class Location(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True)
    # Relationship
    games: Mapped[List["Game"]] = relationship("Game", back_populates="location", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Location(id={self.id}, name={self.name})"


class Game(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    game_bgg_id: Mapped[int] = mapped_column(Integer)
    datum: Mapped[date] = mapped_column(Date, nullable=True)
    playtime: Mapped[int] = mapped_column(Integer, nullable=True)
    boardgame_id: Mapped[int] = mapped_column(ForeignKey("boardgame.id"))
    location_id: Mapped[int] = mapped_column(ForeignKey("location.id"))
    # Relationship
    boardgame: Mapped["Boardgame"] = relationship(back_populates="games")
    location: Mapped["Location"] = relationship(back_populates="games")
    player_pos: Mapped[List["PlayerPos"]] = relationship(
        "PlayerPos", back_populates="game", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"Game(id={self.id}, game_bgg_id={self.game_bgg_id}, boardgame={self.boardgame.name}, "
            f"datum={self.datum}, location={self.location}, player={self.player_pos})"
        )

    def update(self, other) -> bool:
        """Update Game mit aktuellen Werten

        Args:
            other (game): neues "Game"-Objekt

        Raises:
            TypeError: ungültiges Objekt übergeben

        Returns:
            bool: Gab es Änderungen
        """

        if not isinstance(other, type(self)):
            raise TypeError("Update nicht möglich, es handelt sich um kein game-model")

        changed = False

        if self.datum != other.datum:
            self.datum = other.datum
            changed = True
        if self.playtime != other.playtime:
            self.playtime = other.playtime
            changed = True
        if self.location_id != other.location_id:
            self.location_id = other.location_id
            changed = True
        if self.boardgame_id != other.boardgame_id:
            self.boardgame_id = other.boardgame_id
            changed = True

        return changed


class Boardgame(db.Model):

    # default Information
    id: Mapped[int] = mapped_column(primary_key=True)
    bgg_id: Mapped[int] = mapped_column(Integer, unique=True)
    name_primary: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    img: Mapped[str] = mapped_column(String(255))
    img_small: Mapped[str] = mapped_column(String(255))
    yearpublished: Mapped[int] = mapped_column(Integer)
    minplayers: Mapped[int] = mapped_column(Integer)
    maxplayers: Mapped[int] = mapped_column(Integer)
    playtime: Mapped[int] = mapped_column(Integer)
    koop: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)
    rating: Mapped[float] = mapped_column(Float)
    weight: Mapped[float] = mapped_column(Float)
    # Relationship
    games: Mapped[List["Game"]] = relationship(back_populates="boardgame", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return (
            f"Boardgame (name={self.name_primary}, img={self.img}, img_small={self.img_small}, "
            f"published={self.yearpublished}, for {self.minplayers} - {self.maxplayers} Players, "
            f"playtime = {self.playtime}, rating={self.rating}, weight= {self.weight}, koop={self.koop}"
        )

    def update(self, other) -> bool:
        """Update Boardgame mit aktuellen Werten

        Args:
            other (boardgame): neues "Boardgame"-Objekt

        Raises:
            TypeError: ungültiges Objekt übergeben

        Returns:
            bool: Gab es Änderungen
        """
        if not isinstance(other, type(self)):
            raise TypeError("Update nicht möglich, es handelt sich um kein boardgame-model")
        changed = False

        if self.bgg_id != other.bgg_id:
            self.bgg_id = other.bgg_id
            changed = True
        if self.name_primary != other.name_primary:
            self.name_primary = other.name_primary
            changed = True
        if self.img != other.img:
            self.img = other.img
            changed = True
        if self.img_small != other.img_small:
            self.img_small = other.img_small
            changed = True
        if self.yearpublished != other.yearpublished:
            self.yearpublished = other.yearpublished
            changed = True
        if self.minplayers != other.minplayers:
            self.minplayers = other.minplayers
            changed = True
        if self.maxplayers != other.maxplayers:
            self.maxplayers = other.maxplayers
            changed = True
        if self.playtime != other.playtime:
            self.playtime = other.playtime
            changed = True
        if self.rating != other.rating:
            self.rating = other.rating
            changed = True
        if self.weight != other.weight:
            self.weight = other.weight
            changed = True
        if self.koop != other.koop:
            self.koop = other.koop
            changed = True

        return changed

    def from_bgg(self, json_file: dict, name: tuple[str, bool] = None):
        """Read json File and auto-fill the arguments of the current boardgame instance

        Args:
            json_file (dict): JSON file from BGG
            name (tuple[str, bool], optional): (alternative name, is_primary_name). Defaults to None.

        Returns:
            self: self with updated parameters
        """
        ### Helper Functions ###

        def create_names(name: tuple[str, bool]):
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

        def is_koop() -> bool:
            koop = False
            for link in json_file.get("link"):
                if link.get("@value") == "Cooperative Game":
                    koop = True
            return koop

        ########################

        # Add all data available in bgg
        self.bgg_id = nested_get(json_file, ["@id"], int)
        self.name, self.name_primary = create_names(name)
        self.img = nested_get(json_file, ["image"], str)
        self.img_small = nested_get(json_file, ["thumbnail"], str)
        self.yearpublished = nested_get(json_file, ["yearpublished", "@value"], int)
        self.minplayers = nested_get(json_file, ["minplayers", "@value"], int)
        self.maxplayers = nested_get(json_file, ["maxplayers", "@value"], int)
        self.playtime = nested_get(json_file, ["playingtime", "@value"], int)
        self.rating = nested_get(json_file, ["statistics", "ratings", "average", "@value"], float)
        self.weight = nested_get(json_file, ["statistics", "ratings", "averageweight", "@value"], float)
        self.koop = is_koop()

        return self
