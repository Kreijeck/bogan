from flask import Flask
from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import pandas as pd

import bogan.lib.sql_request as sql
from bogan.lib.dataframe import DashDf

def dashboard_rank(flask_app: Flask) -> Dash:
    dash_app = (Dash(__name__, server=flask_app, url_base_pathname="/dashboard/rank/"))

    # TODO Definition der Orte in Configfile
    orte = ["Mittwochsrunde", "Spielewochenende"]
    # Dash Layout
    dash_app.layout = html.Div(
        [
            dcc.RadioItems(
                options=[{'label': ort, 'value': ort} for ort in orte], value="Mittwochsrunde", id="radio-button-orte"
            ),
            html.Title("Ranking table für verschieden Locations"),
            dcc.Graph(figure={}, id="rank-graph")
        ]
    )

    # Dash Callbacks
    @dash_app.callback(
        Output(component_id="rank-graph", component_property="figure"),
        Input(component_id="radio-button-orte", component_property="value")
    )
    def update_graph(ort):
        print(ort)
        data = DashDf.rank_df(ort_name=ort)

        fig = px.line(data, x="partie_index", y="sum_rankpoints", color="spieler")

        return fig
    
    return dash_app


def dashboard_example(flask_app: Flask) -> Dash:
    dash_app = Dash(__name__, server=flask_app, url_base_pathname="/dashboard_init1/")

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
        
        # Ändern des Farben des Plots
        fig.update_layout(
            # plot_bgcolor="#f0f0f0",
            paper_bgcolor="#282c36",
            font=dict(color="white"),

            )

        return fig

    # return Dash App
    return dash_app


def dashboard_example2(flask_app: Flask) -> Dash:
    dash_app = Dash(__name__, server=flask_app, url_base_pathname="/dashboard_init2/")

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
            {"name": "Thomas", "played": 81},
            {"name": "Uddi", "played": 21},
            {"name": "Jochen", "played": 32},
            {"name": "Lasse", "played": 12},
            {"name": "Torsten", "played": 2},
            {"name": "Simon D.", "played": 50},

        ]
        data = pd.DataFrame(raw_data)
        print(data)

        fig = px.pie(data, values='played', names="name")
        return fig

    # return Dash App
    return dash_app
