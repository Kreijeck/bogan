import os
from sqlalchemy import create_engine
from models import Base, User
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from flask_sqlalchemy import SQLAlchemy

def create_new_db(delete_all: bool = False):
    load_dotenv(override=True)
    db_path = os.getenv("FLASK_DATABASE_URI")
    engine = create_engine(db_path, echo=True)

    # Lösche zuerst alte Datenbank -> für debug Zwecke. Sollte später vermieden werden
    if delete_all:
        Base.metadata.drop_all(bind=engine)
    
    # Erstelle Datenbank
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        users = []
        users.append(User(email="any@nichts.de", name="admin", password="test123"))
        users.append(User(email="any@nichts2.de", name="admin2", password="test123"))
        users.append(User(email="any@nichts3.de", name="admin3", password="test123"))
        session.add_all(users)
        session.commit()



if __name__ == "__main__":
    create_new_db(delete_all=True)

    

