from flask import Flask, render_template
import dash
from dash import dcc, html


 

# Flask App
server = Flask(__name__)

 

@server.route('/')
def index():
    return render_template('index2.html')

 

# Dash App
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

 

dash_app = dash.Dash(
    __name__,
    server=server,
    routes_pathname_prefix='/dashboard/',
    external_stylesheets=external_stylesheets
)

 

dash_app.layout = html.Div([
    html.H1('Dash Embedded in Flask'),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'Montreal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

 

if __name__ == '__main__':
    server.run(debug=True)