import plotly.graph_objects as go

# Beispiel Daten: Spielerpositionen für verschiedene Spiele
spieler_positionen = {
    "Spiel 1": {"Thomas": "Pos1", "Uddi": "Pos2", "Jochen": "Pos3"},
    "Spiel 2": {"Thomas": "Pos2", "Spieler B": "Pos1", "Lasse": "Pos3"},
    "Spiel 3": {"Spieler A": "Pos3", "Spieler B": "Pos2", "Spieler C": "Pos1"},
    # Weitere Spiele und Positionen hier hinzufügen
}

spiele = list(spieler_positionen.keys())
spieler = list(spieler_positionen["Spiel 1"].keys())

# Daten für das Diagramm vorbereiten
data = []
for spieler_name in spieler:
    positionen = [spieler_positionen[spiel].get(spieler_name, "") for spiel in spiele]
    data.append(go.Bar(x=spiele, y=positionen, name=spieler_name))

# Layout des Diagramms festlegen
layout = go.Layout(
    title="Spielerpositionen in verschiedenen Spielen",
    xaxis=dict(title="Spiele"),
    yaxis=dict(title="Positionen"),
    # barmode="stack"  # Stapelmodus, um die Positionen zu stapeln
)

# Diagramm erstellen und anzeigen
fig = go.Figure(data=data, layout=layout)
fig.show()