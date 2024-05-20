from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from bogan.db.ask_bgg import search_boardgame

vote = Blueprint('vote',__name__, url_prefix="vote", template_folder='templates')

@vote.route('/')
@login_required
def index():
    return render_template('vote_index.html', name=current_user.name)

@vote.route("/add_game", methods=["POST"])
@login_required
def add_game():
    return render_template("vote_add_game.html")

@vote.route("/add_vote_list", methods=["POST"])
@login_required
def add_vote_list():
    return render_template("vote_add_vote.html")

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