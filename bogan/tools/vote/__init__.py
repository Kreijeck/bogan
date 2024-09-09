from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from bogan.db.ask_bgg import search_boardgame
from bogan.db.models import Boardgame, db

vote = Blueprint("vote", __name__, url_prefix="vote", template_folder="templates")

# Global Variable
current_bg_results: list[Boardgame] = []


@vote.route("/")
def index():
    boardgames = Boardgame.query.order_by("name").all()
    return render_template("vote_index.html", boardgames=boardgames)


@vote.route("/add_game", methods=["POST", "GET"])
@login_required
def add_game():
    boardgames = Boardgame.query.order_by("name").all()

    # POST Request
    if request.method == "POST":
        # Search a Boardgame
        button_pressed = request.form.get("button_pressed")
        # TODO change print to logging
        print(f"Button {button_pressed} wurde gedrückt")

        # Suche Brettspiel
        if button_pressed == "search_bg":
            search = request.form.get("search_input")
            found_games = search_boardgame(search=search)

            # save to global Variable
            global current_bg_results
            current_bg_results = found_games

            for game in found_games:
                print(f"type: {type(game)}")
                print(f"Name: {game.name}, primary_name: {game.name_primary}")

            return render_template(
                "vote_add_game.html", found_games=found_games, boardgames=boardgames
            )

        # Füge Brettspiel hinzu
        elif button_pressed == "add_bg":
            # TODO remove print
            # new_game: Boardgame = Boardgame(request.form.get("games"))
            game_id = str(request.form.get("game_id"))
            for game in current_bg_results:
                if game_id == str(game.bgg_id):
                    new_game = game

            boardgame = Boardgame.query.filter_by(bgg_id=new_game.bgg_id).first()

            if boardgame:
                # TODO Warnmeldung hinzufügen
                print(f"Spiel {new_game.name} existiert bereits in der Datenbank")
                return redirect(url_for("tools.vote.add_game"))

            # Füge Spiel hinzu
            db.session.add(new_game)
            db.session.commit()

            # TODO Hinweimeldung hinzufügen
            print(f"Add Game {new_game}")
            boardgames = Boardgame.query.order_by("name").all()

            return render_template("vote_add_game.html", boardgames=boardgames)

    # bei "GET" oder ungültigen Angaben reloade Page
    return render_template("vote_add_game.html", boardgames=boardgames)


@vote.route("/add_vote_list", methods=["POST"])
@login_required
def add_vote_list():
    num_of_games = int(request.form.get("num_of_games"))
    name = request.form.get("name")
    games = [
        "Wasserkraft",
        "Heat",
        "Gaia",
        "Wasserwerk",
    ]

    return render_template(
        "vote_add_vote.html", name=name, num_of_games=num_of_games, games=games
    )
