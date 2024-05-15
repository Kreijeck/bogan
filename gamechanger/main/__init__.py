from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from gamechanger.db.ask_bgg import search_boardgame

main = Blueprint('main',__name__, template_folder='templates')

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route("/search")
def search():
    return render_template("search.html")

@main.route("/search/", methods=["POST"])
def search_post():
    name = request.form.get("search")
    response = search_boardgame(name)
    data = []
    for resp in response:
        data.append({"id": resp.get("@id", ""),
                     "name": resp.get("name", "").get("@value", ""),
                     "publish": resp.get("yearpublished", "") ,
                     })

    return render_template("search.html", response=data)

@main.route("/add_game", methods=["POST"])
def add_game():
    pass

    