from flask import Flask, render_template, request
import bogan.lib.sql_request as sql

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html",
                           name="BoardStats")

@app.route("/user")
def user():
    user = sql.get_user()
    return render_template("user.html", user = user)

if __name__ == '__main__':
    app.run(debug=True)