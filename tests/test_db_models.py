# tests: bogan/db/models.py

from bogan.db.models import Boardgame, Game, Location, Player, PlayerPos

def test_create_boardgame(db_session):
    """
    Einfacher Test: Boardgame anlegen und prüfen, ob es gespeichert wird.
    """
    bg = Boardgame(
        bgg_id=12345,
        name_primary="Originaltitel",
        name="Deutscher Titel",
        img="https://example.com/image.jpg",
        img_small="https://example.com/image_small.jpg",
        yearpublished=2023,
        minplayers=1,
        maxplayers=4,
        playtime=60,
        koop=False,       # oder True, je nachdem
        rating=7.2,
        weight=2.5
    )
    db_session.add(bg)
    db_session.commit()

    # Aus der DB holen und prüfen
    saved_bg = db_session.query(Boardgame).filter_by(bgg_id=12345).first()
    assert saved_bg is not None
    assert saved_bg.name == "Deutscher Titel"

def test_relationship_game(db_session):
    """
    Prüfen, ob ein Game korrekt mit einem Boardgame verknüpft werden kann.
    """
    boardgame = Boardgame(bgg_id=999, name="Game999")
    boardgame = Boardgame(
        bgg_id=999,
        name_primary="Game999 prima",
        name="Game999",
        img="https://example.com/image.jpg",
        img_small="https://example.com/image_small.jpg",
        yearpublished=2023,
        minplayers=1,
        maxplayers=4,
        playtime=60,
        koop=False,       # oder True, je nachdem
        rating=7.2,
        weight=2.5
    )
    db_session.add(boardgame)
    db_session.commit()

    game = Game(game_bgg_id=555, boardgame=boardgame, location_id=1)
    db_session.add(game)
    db_session.commit()

    # Boardgame hat 1..n Games (games-Liste bzw. game-Liste)
    assert len(boardgame.games) == 1
    assert boardgame.games[0].game_bgg_id == 555


def test_playerpos_update(db_session):
    """
    Test der update-Methode von PlayerPos
    """
    player = Player(name="Tester")
    game = Game(game_bgg_id=777, boardgame_id=1, location_id=1)
    playerpos = PlayerPos(points=10, win=False, game=game, player=player)

    db_session.add_all([player, game, playerpos])
    db_session.commit()

    # Update
    new_pp = PlayerPos(points=15, win=True, game=game, player=player)
    changed = playerpos.update(new_pp)
    db_session.commit()

    assert changed is True
    assert playerpos.points == 15
    assert playerpos.win is True
