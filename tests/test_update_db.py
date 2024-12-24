# tests: bogan/db/update_db.py

import pytest
from unittest.mock import patch
from bogan.db.update_db import update_db
from bogan.db.models import Game, Boardgame

@pytest.fixture
def example_json():
    """
    Liefert ein Beispiel-JSON, das ähnlich dem BGG-Format ist,
    aber klein genug für Tests.
    """
    return [
        {
            "@id": 101,
            "@date": "2024-12-22",
            "@length": "60",
            "item": {
                "@objectid": "999"
            },
            "players": {
                "player": [
                    {"@name": "Alice", "@score": "20", "@win": "1"},
                    {"@name": "Bob", "@score": "15", "@win": "0"}
                ]
            },
            "@location": "TestLocation"
        }
    ]

@pytest.fixture
def mock_boardgame_response():
    """
    Liefert ein Mock-Objekt oder eine Liste von Boardgame-Objekten,
    so wie `ask_boardgame` sie zurückgeben würde.
    """
    # Du kannst hier echte Boardgame-Instanzen zurückgeben oder nur Dictionaries.
    # Fürs Beispiel nehmen wir direkt Model-Instanzen.
    bg = Boardgame(
        bgg_id=999,
        name_primary="Mocked BG Primary",
        name="Mocked BG",
        img="img_url",
        img_small="img_small_url",
        yearpublished=2023,
        minplayers=2,
        maxplayers=4,
        playtime=60,
        koop=False,
        rating=0.0,
        weight=2.5
    )
    return [bg]

@patch("bogan.db.update_db.ask_boardgame")
@patch("bogan.db.update_db.ask_games_from")
def test_update_db_from_api(
    mock_ask_games_from,
    mock_ask_boardgame,
    db_session,
    example_json,
    mock_boardgame_response
):
    """
    Testet update_db mit Mock-API-Antworten.
    So werden keine echten Requests an BGG gesendet.
    """
    # Mock das Ergebnis der Funktionen, die die API aufrufen.
    mock_ask_games_from.return_value = example_json
    mock_ask_boardgame.return_value = mock_boardgame_response

    # Aufruf der zu testenden Funktion
    update_db(from_api=True, save_file=False)

    # Jetzt prüfen wir, ob die DB die erwarteten Daten enthält
    # 1) Boardgame sollte angelegt sein
    bg = db_session.query(Boardgame).filter_by(bgg_id=999).first()
    assert bg is not None
    assert bg.name == "Mocked BG"

    # 2) Game sollte in DB sein
    game = db_session.query(Game).filter_by(game_bgg_id=101).first()
    assert game is not None
    assert game.playtime == 60  # Aus dem JSON-String konvertiert

    # 3) players, location, etc. kannst du analog abfragen und prüfen


def test_update_db_from_local_file(db_session, tmp_path, example_json, mock_boardgame_response):
    """
    Testet update_db ohne echten API-Call, sondern mit einer lokal gespeicherten JSON-Datei.
    """
    # 1) Erstelle eine temporäre JSON-Datei im tmp_path
    test_file = tmp_path / "test_plays.json"
    import json
    with open(test_file, "w", encoding="utf-8") as f:
        json.dump(example_json, f)

    # 2) Patch ask_boardgame so, dass es unser Mock-BG liefert
    from unittest.mock import patch

    with patch("bogan.db.update_db.ask_boardgame", return_value=mock_boardgame_response):
        # 3) update_db aufrufen mit from_api=False und unserem File
        from bogan.db.update_db import update_db
        # Hier tricksen wir ein wenig, indem wir den Pfad in unsere update_db-Funktion injizieren
        # oder du passt 'update_db' so an, dass es den Pfad als Parameter erhält.
        update_db(from_api=False, save_file=False)

    # 4) Prüfen, ob Datenbankeinträge existieren
    bg = db_session.query(Boardgame).filter_by(bgg_id=999).first()
    assert bg is not None
    assert bg.name == "Mocked BG"

    game = db_session.query(Game).filter_by(game_bgg_id=101).first()
    assert game is not None
    # usw.
