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
    return render_template("user.html", users = users)

@app.route("/partien")
def partien():
    return render_template("scroll_table.html")

@app.route("/user/<name>")
def user_detail(name):
    partien = sql.get_partien(name)
    return render_template("user_detail.html", name=name, partien=partien)


if __name__ == '__main__':
    app.run(debug=True)