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
    return render_template("search.html", response=None)

@main.route("/search/", methods=["POST"])
def search_post():
    name = request.form.get("search")
    print(f"Der Suchbegriff: {name}")
    response = search_boardgame(name)
    print(f"Die Antwort: {type(response)} {response}")

    return render_template("search.html", response=response)

    