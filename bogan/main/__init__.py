from flask import Blueprint, render_template
from flask_login import login_required, current_user

from bogan.main.lib.event_analysis import get_game_list, prepare_ranking_table

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
    game_list_default = get_game_list(event, mode="default")
    game_list_playtime = get_game_list(event, mode="playtime")
    game_list_complexity = get_game_list(event, mode="complexity")
    max_positions = max((len(game['players']) for game in game_list_default if isinstance(game.get('players'), list)), default=0)

    # Ranking-Daten vorbereiten
    ranking_default = prepare_ranking_table(game_list_default, event)
    ranking_playtime = prepare_ranking_table(game_list_playtime, event)
    ranking_complexity = prepare_ranking_table(game_list_complexity, event)

    return render_template(
        "event.html",
        games=game_list_default,
        max_positions=max_positions,
        ranking_default=ranking_default,
        ranking_playtime=ranking_playtime,
        ranking_complexity=ranking_complexity,
    )



