from flask import Blueprint, render_template, request
from flask_login import login_required
from bogan.db.ask_bgg import search_boardgame

vote = Blueprint('vote',__name__, url_prefix="vote", template_folder='templates')

@vote.route('/')
def index():
    return render_template('vote_index.html')

@vote.route("/add_game", methods=["POST"])
@login_required
def add_game():
    return render_template("vote_add_game.html")

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
   
    return render_template("vote_add_vote.html", name=name, num_of_games=num_of_games, games=games)

# TODO Muss refactored, gelöscht werden
@vote.route("/search", methods=["POST"])
def search_post():
    name = request.form.get("search")
    response = search_boardgame(name)
    data = []
    for resp in response:
        data.append({"id": resp.get("@id", ""),
                     "name": resp.get("name", "").get("@value", ""),
                     "publish": resp.get("yearpublished", "").get("@value", "") ,
                     })

    return render_template("tbd_search.html", response=data)