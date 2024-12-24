# tests/conftest.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from bogan.db.models import Base

@pytest.fixture(scope="session")
def engine():
    """
    Erzeugt einen In-Memory-SQLite-Engine für alle Tests der Session.
    """
    # Für einen reinen In-Memory-Test:
    test_engine = create_engine("sqlite:///:memory:", echo=False)
    return test_engine


@pytest.fixture(scope="session")
def tables(engine):
    """
    Erzeugt alle Tabellen und zerstört sie am Ende der Test-Session wieder.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(engine, tables):
    """
    Liefert eine frische Datenbank-Session pro Test.
    Schließt die Session nach dem Test.
    """
    connection = engine.connect()
    # Optional: transaction beginnen
    trans = connection.begin()

    session = Session(bind=connection)
    yield session

    session.close()
    # transaction rollback
    trans.rollback()
    connection.close()
