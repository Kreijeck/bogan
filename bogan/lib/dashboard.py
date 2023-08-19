from flask import Flask
from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import pandas as pd

import bogan.lib.sql_request as sql


def dashboard_example(flask_app: Flask) -> Dash:
    dash_app = Dash(__name__, server=flask_app, url_base_pathname="/dashboard_init/")

    # Dash Layout
    dash_app.layout = html.Div(
        [
            html.Title("Thomas in Dash"),
            html.Div(children="My first Dash Table with Data, Graph and Radio Buttons"),
            html.Hr(),
            dcc.RadioItems(
                options=[benutzer.name for benutzer in sql.get_users()], value="lifeExp", id="controls-and-radio-item"
            ),
            dcc.Graph(figure={}, id="dash-graph"),
            html.P(children="Hier ist Schluss"),
        ]
    )

    # Dash Callbacks
    @dash_app.callback(
        Output(component_id="dash-graph", component_property="figure"),
        Input(component_id="controls-and-radio-item", component_property="value")
        # Input(component_id='url', component_property='pathname')
    )
    def update_graph(pathname):
        # Name aus URL extrahieren
        # _ , username = pathname.split('/user/')

        # Abfrage unter Verwendung des Benutzernamens
        raw_data = [
            {"date": 1, "value": 2},
            {"date": 2, "value": 4},
            {"date": 3, "value": 3},
            {"date": 4, "value": 10},
            {"date": 5, "value": 5},
            {"date": 6, "value": 6},
            {"date": 7, "value": 7},
            {"date": 8, "value": 8},
        ]
        data = pd.DataFrame(raw_data)
        print(data)

        fig = px.bar(data, x="date", y="value")
        return fig

    # return Dash App
    return dash_app
