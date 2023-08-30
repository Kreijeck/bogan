import pandas as pd

# Beispiel-Daten
data = [
    {"spieler": "Thomas", "punktzahl": 122, "brettspiel": "Spiel1"},
    {"spieler": "Thomas", "punktzahl": 14, "brettspiel": "Spiel2"},
    {"spieler": "Thomas", "punktzahl": 12, "brettspiel": "Spiel3"},
    {"spieler": "Simon", "punktzahl": 222, "brettspiel": "Spiel1"},
    {"spieler": "Simon", "punktzahl": 24, "brettspiel": "Spiel2"},
    {"spieler": "Simon", "punktzahl": 2, "brettspiel": "Spiel3"},
    # Weitere Daten hier ...
]

# DataFrame erstellen
df = pd.DataFrame(data)

# Pivottabelle erstellen
pivot_df = df.pivot_table(index='spieler', columns='brettspiel', values='punktzahl', aggfunc='sum', fill_value=0)

# Gesamte Punktzahl für jeden Spieler berechnen
gesamte_punktzahl = df.groupby('spieler')['punktzahl'].sum()

# Neue Spalte für die Gesamtpunktzahl hinzufügen
pivot_df['Gesamte Punktzahl'] = gesamte_punktzahl

# Tabelle anzeigen
print(pivot_df)