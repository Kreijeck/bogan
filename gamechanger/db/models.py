from typing import List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(200))

    def __repr__(self) -> str:
        return f"ID: {self.id}, EMAIL: {self.email}, NAME: {self.name}"
    
class Vote(db.Model):
    __tablename__ = "vote"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), unique=True)
    brettspiel_id : Mapped[int] = mapped_column(ForeignKey("brettspiel.id"))
    brettspiel: Mapped["Brettspiel"] = relationship(back_populates="in_votes")

class Brettspiel(db.Model):
    __tablename__ = "brettspiel"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    img: Mapped[str] = mapped_column(String(255))
    in_votes: Mapped[List["Vote"]] = relationship(back_populates="brettspiel", cascade="all, delete-orphan")
