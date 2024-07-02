from flask import Blueprint, render_template
from flask_login import login_required, current_user

from bogan.main.lib.event_analysis import create_table, get_game_list

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
    game_list = get_game_list(event)
    table_data, players = create_table(game_list)
    return render_template("event.html", game_list=game_list, players=players, table_data=table_data)

@main.route("/table", methods=["GET"])
def table():
    def path_to_img_html(path):
        return f'<img src="{path}"/>'
    
    from bogan.main.lib.pandas_analysis import df
    df['img_small'] = df['img_small'].apply(path_to_img_html)
    html_table = df.to_html(escape=False, classes='table is-striped')

    return render_template("scretch_table.html", html_table=html_table)
