from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

# from bogan.dash_routes import dash_route
from bogan.aa_dev.dash_tut.dash_routes import dash_route
# init flask
server = flask.Flask(__name__)

@server.route("/")
def home():
    return "Hello Flask"

app1 = dash_route()
# # Incorporate data
# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# # Initialize the app
# app1 = Dash(requests_pathname_prefix="/app1/")

# # App layout
# app1.layout = html.Div([
#     html.Title('Thomas in Dash'),
#     html.Div(children='My first Dash Table with Data, Graph and Radio Buttons'),
#     html.Hr(),
#     dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'], value='lifeExp', id='controls-and-radio-item'),
#     dash_table.DataTable(data=df.to_dict('records'), page_size=10),
#     dcc.Graph(figure={}, id='controls-and-graph'),
#     html.P(children="Hier ist Schluss")
#     ])

# # Add controls to build the interaction
# @callback(
#     Output(component_id='controls-and-graph', component_property='figure'),
#     Input(component_id='controls-and-radio-item', component_property='value')
# )
# def update_graph(col_chosen):
#     fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
#     return fig


app2 = Dash(requests_pathname_prefix="/app2/")
app2.layout = html.Div("Dash 2 app")

application = DispatcherMiddleware(server,
                                   {"/app1": app1.server, "/app2": app2.server},
                                   )
if __name__ == '__main__':
    run_simple('localhost', 8050, application)
    #app1.run(debug=True)
    pass