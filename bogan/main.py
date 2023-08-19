from flask import Flask, render_template
from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import bogan.lib.sql_request as sql

import pandas as pd

app = Flask(__name__)

# Dash App erstellen
dash_app = Dash(__name__, server=app, url_base_pathname='/dashboard_init/')



# Dash-App-Layout
dash_app.layout = html.Div([
        html.Title('Thomas in Dash'),
        html.Div(children='My first Dash Table with Data, Graph and Radio Buttons'),
        html.Hr(),
        dcc.RadioItems(options=[benutzer.name for benutzer in sql.get_users()], value='lifeExp', id='controls-and-radio-item'),
        dcc.Graph(figure={}, id='dash-graph'),
        html.P(children="Hier ist Schluss")
        ])

# Dash Callbacks
@dash_app.callback(
        Output(component_id='dash-graph', component_property='figure'),
        Input(component_id='controls-and-radio-item', component_property='value')
        #Input(component_id='url', component_property='pathname')
)
def update_graph(pathname):
    # Name aus URL extrahieren
    #_ , username = pathname.split('/user/')

    # Abfrage unter Verwendung des Benutzernamens
    raw_data = [
        {'date': 1, 'value': 2},
        {'date': 2, 'value': 4},
        {'date': 3, 'value': 3},
        {'date': 4, 'value': 10},
        {'date': 5, 'value': 5},
        {'date': 6, 'value': 6},
        {'date': 7, 'value': 7},
        {'date': 8, 'value': 8},
        ]
    data = pd.DataFrame(raw_data)
    print(data)

    fig = px.bar(data, x='date', y='value')
    return fig


@app.route("/")
def index():
    return render_template("index.html",
                           name="BoardStats")

# Dashboard links need / at the end
@app.route("/dashboard/")
def dashboards():
    return render_template('dash_template.html', dash_content=dash_app.index())


@app.route("/user/")
def user():
    users = sql.get_users()
    return render_template("overview.html", component="user", overview=users)

@app.route("/partien/")
def partien():
    return "Hier erscheint eine Liste aller Partien"

@app.route("/user/<name>/")
def user_detail(name):
    return dash_app.index()
    # partien = sql.get_partien_by_date(name)
    # return render_template("user_detail.html", name=name, partien=partien)

@app.route("/boardgames/")
def boardgames():
    boardgames = sql.get_boardgames()
    return render_template("overview.html", component="boardgames", overview=boardgames)

@app.route("/boardgames/<name>/")
def boardgame_detail(name):
    partien = []
    return render_template("boardgame_detail.html", partien=partien)


if __name__ == '__main__':
    app.run(debug=True)