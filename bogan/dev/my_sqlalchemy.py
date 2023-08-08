from sqlalchemy import create_engine, String, ForeignKey
from sqlalchemy.orm import Session, Mapped 
from sqlalchemy.orm import declarative_base, mapped_column, relationship
from typing import Optional, List



engine = create_engine("sqlite:///tutorial.db")
Base = declarative_base()


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]

    addresses: Mapped[List["Address"]] = relationship(back_populates="user", cascade="all, delete-orphan")  # noqa: F821

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"
    
class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")
    
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
    

# Lösche Inhalt der Datenbank
Base.metadata.drop_all(engine)
# Erstelle Datenbank
Base.metadata.create_all(engine)

with Session(engine) as session:
    spongebob = User(
        name="spongebob",
        fullname="Spongebob Squarepants",
        addresses=[Address(email_address="spongebob@sqlalchemy.org")],
    )
    sandy = User(
        name="sandy",
        fullname="Sandy Cheeks",
        addresses=[
            Address(email_address="sandy@sqlalchemy.org"),
            Address(email_address="sandy@squirrelpower.org"),
        ],
    )
    patrick = User(name="patrick", fullname="Patrick Star")
    session.add_all([spongebob, sandy, patrick])
    session.commit()

    

