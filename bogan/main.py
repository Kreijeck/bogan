from flask import Flask, render_template, request
import bogan.lib.sql_request as sql

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html",
                           name="BoardStats")

@app.route("/user")
def user():
    users = sql.get_users()
    return render_template("overview.html", component="user", overview=users)

@app.route("/partien")
def partien():
    return "Hier erscheint eine Liste aller Partien"

@app.route("/user/<name>")
def user_detail(name):
    partien = sql.get_partien_by_date(name)
    return render_template("user_detail.html", name=name, partien=partien)

@app.route("/boardgames")
def boardgame_overview():
    boardgames = sql.get_boardgames()
    return render_template("overview.html", component="boardgames", overview=boardgames)

@app.route("/boardgames/<name>")
def boardgame_detail(name):
    partien = []
    return f"<p>Hier erscheint die Statistik für {name}</p>"


if __name__ == '__main__':
    app.run(debug=True)