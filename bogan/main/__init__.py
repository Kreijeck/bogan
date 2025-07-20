from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy.orm import Session

from bogan.main.lib.event_analysis import prepare_all_rankings
from bogan.main.lib.fetch_db import get_boardgame_by, get_games_by, get_all_boardgames, engine

main = Blueprint("main", __name__, template_folder="templates")


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html", name=current_user.name)


@main.route("/search")
def search():
    return render_template("search.html")


@main.route("/add_game", methods=["POST"])
def add_game():
    pass

@main.route("/event/<path:event>", methods=["GET"])
def show_event(event: str):
    # Alle Rankings und Daten auf einmal berechnen
    event_data = prepare_all_rankings(event)
    
    return render_template(
        "event.html",
        games=event_data["games"],
        max_positions=event_data["max_positions"],
        ranking_default=event_data["ranking_default"],
        ranking_playtime=event_data["ranking_playtime"],
        ranking_complexity=event_data["ranking_complexity"],
    )

@main.route("/boardgame/<path:boardgame_id>", methods=["GET"])
def show_boardgame(boardgame_id: str):
    with Session(engine) as session:
        boardgame = get_boardgame_by(boardgame_id, session)
        games = get_games_by(boardgame_id, session)
        print(games)

        return render_template("boardgame_detail.html", boardgame=boardgame, games=games)

@main.route("/boardgames", methods=["GET"])    
def show_all_boardgames():
    with Session(engine) as session:
        boardgames = get_all_boardgames(session)

        return render_template("boardgames_overview.html", boardgames=boardgames)
    
@main.route("/game", methods=["GET"])
def show_game():
    return render_template("game_detail.html")




