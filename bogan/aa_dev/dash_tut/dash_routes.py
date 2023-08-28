from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

def dash_route():
    # Incorporate data
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

    # Initialize the app
    app1 = Dash(requests_pathname_prefix="/app1/")

    # App layout
    app1.layout = html.Div([
        html.Title('Thomas in Dash'),
        html.Div(children='My first Dash Table with Data, Graph and Radio Buttons'),
        html.Hr(),
        dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'], value='lifeExp', id='controls-and-radio-item'),
        dash_table.DataTable(data=df.to_dict('records'), page_size=10),
        dcc.Graph(figure={}, id='controls-and-graph'),
        html.P(children="Hier ist Schluss")
        ])

    # Add controls to build the interaction
    @callback(
        Output(component_id='controls-and-graph', component_property='figure'),
        Input(component_id='controls-and-radio-item', component_property='value')
    )
    def update_graph(col_chosen):
        # fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
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
    
    return app1