from flask import Flask, render_template
import bogan.lib.sql_request as sql
import bogan.lib.dashboard as dabo
from bogan.aa_dev.pandas_analysis import create_table_by_game


app = Flask(__name__)

# Available Dashboards
dash_example = dabo.dashboard_example(flask_app=app)
d2 = dabo.dashboard_example2(flask_app=app)


@app.route("/")
def index():
    return render_template("index.html",
                           name="BoardStats")

# Dashboard links need / at the end
@app.route("/dashboard/")
def dashboards():
    return render_template('dash_template.html', dash_content=dash_example.index())

@app.route("/dashboard2/")
def dashboards2():
    return render_template('dash_template.html', dash_content=d2.index())

@app.route("/user/")
def user():
    users = sql.get_users()
    return render_template("overview.html", component="user", overview=users)

@app.route("/partien/")
def partien():
    return "Hier erscheint eine Liste aller Partien"

@app.route("/user/<name>/")
def user_detail(name):
    return dash_example.index()
    # partien = sql.get_partien_by_date(name)
    # return render_template("user_detail.html", name=name, partien=partien)

@app.route("/boardgames/")
def boardgames():
    boardgames = sql.get_boardgames()
    return render_template("overview.html", component="boardgames", overview=boardgames)

@app.route("/boardgames/<name>/")
def boardgame_detail(name):
    with sql.get_session() as session:
        detail_info = sql.get_boardgames_detail(name=name)
        partien = sql.get_partien_from_game(session=session, name=name)
    return render_template("boardgame_detail.html", detail= detail_info, partien=partien)

@app.route("/df")
def dataframe():
    
    df_html = create_table_by_game()
    print(df_html)
    return render_template("df.html", df_html=df_html)


if __name__ == '__main__':
    app.run(debug=True)