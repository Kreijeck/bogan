import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Beispiel-Daten
data = [
    {"spieler": "Thomas", "punktzahl": 122, "brettspiel": "Spiel1"},
    {"spieler": "Thomas", "punktzahl": 14, "brettspiel": "Spiel2"},
    {"spieler": "Thomas", "punktzahl": 12, "brettspiel": "Spiel3"},
    {"spieler": "Simon", "punktzahl": 222, "brettspiel": "Spiel1"},
    {"spieler": "Simon", "punktzahl": 24, "brettspiel": "Spiel2"},
    {"spieler": "Simon", "punktzahl": 2, "brettspiel": "Spiel3"},
    {"spieler": "Uddi", "punktzahl": 222, "brettspiel": "Spiel1"},
    # Weitere Daten hier ...
]

# DataFrame erstellen
df = pd.DataFrame(data)

def pivot_table():
    # Pivottabelle erstellen
    pivot_df = df.pivot_table(index='spieler', columns='brettspiel', values='punktzahl', aggfunc='sum', fill_value=0)

    # Gesamte Punktzahl für jeden Spieler berechnen
    gesamte_punktzahl = df.groupby('spieler')['punktzahl'].sum()

    # Neue Spalte für die Gesamtpunktzahl hinzufügen
    pivot_df['Gesamte Punktzahl'] = gesamte_punktzahl

    # Tabelle anzeigen
    print(pivot_df)
    return pivot_table

def create_table_by_game():
    game_df = df.groupby("brettspiel")
    html = {}
    for name , group_df in game_df:
        print(name)
        group_df = group_df.sort_values("punktzahl", ascending=False)
        group_df["position"] = np.argsort(-group_df["punktzahl"]) +1
        print(group_df)
        html[name] = group_df.to_html(classes="table table-hover table-striped table-bordered",  index=False)

    return html
        

def work_pivot(pivot):
    fig = go.Table()
    fig.show()

if __name__ == "__main__":
    # pivot = pivot_table()
    # work_pivot(pivot=pivot)
    create_table_by_game()
