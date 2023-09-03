from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from bogan.db.models import Partie, SpielerPos, Benutzer, Brettspiel, Ort, Base

# Erstelle eine SQLite-Testdatenbank im Speicher
engine = create_engine("sqlite:///tests/data/test_spiel2.db")
# engine = create_engine('sqlite:///:memory:')

# Erstelle neue Datenbank
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Erstelle eine Session
session = Session(engine)

# Erstelle einige Benutzer
benutzer_namen = {
    "Spieler1": Benutzer(name="Spieler1"),
    "Spieler2": Benutzer(name="Spieler2"),
    "Spieler3": Benutzer(name="Spieler3"),
    "Spieler4": Benutzer(name="Spieler4"),
    "Spieler5": Benutzer(name="Spieler5"),
    "Spieler6": Benutzer(name="Spieler6"),
}
session.add_all(benutzer_namen.values())
session.commit()


# Erstelle einige Brettspiele
brettspiel = {
    "Spiel1": Brettspiel(name="Spiel1", complexity=2.0, duration=60),
    "Spiel2": Brettspiel(name="Spiel2", complexity=3.5, duration=90),
    "Spiel3": Brettspiel(name="Spiel3", complexity=1.5, duration=45),
    "Spiel4": Brettspiel(name="Spiel4", complexity=4.5, duration=30),
}
session.add_all(brettspiel.values())
session.commit()

# Erstelle einige Orte
orte_namen = {
    "Ort1": Ort(name="Ort1"),
    "Ort2": Ort(name="Ort2"),
    "Ort3": Ort(name="Ort3"),
}
session.add_all(orte_namen.values())
session.commit()

data_100 = [
# Partie 1
{
"brettspiel": brettspiel["Spiel3"],
"ort": orte_namen["Ort1"],
"datum": datetime.strptime("2023-08-15", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=62.93, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=95.43, benutzer=benutzer_namen["Spieler3"], win=True),
SpielerPos(punktzahl=40.14, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=11.44, benutzer=benutzer_namen["Spieler5"], win=False),
],
},
# Partie 2
{
"brettspiel": brettspiel["Spiel3"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2022-03-15", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=60.76, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=47.46, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=24.42, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=16.44, benutzer=benutzer_namen["Spieler5"], win=False),
SpielerPos(punktzahl=-3.47, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=86.59, benutzer=benutzer_namen["Spieler3"], win=True),
],
},
# Partie 3
{
"brettspiel": brettspiel["Spiel3"],
"ort": orte_namen["Ort1"],
"datum": datetime.strptime("2023-05-30", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=23.54, benutzer=benutzer_namen["Spieler1"], win=True),
SpielerPos(punktzahl=-4.64, benutzer=benutzer_namen["Spieler6"], win=False),
],
},
# Partie 4
{
"brettspiel": brettspiel["Spiel2"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2022-07-23", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=0.41, benutzer=benutzer_namen["Spieler3"], win=False),
SpielerPos(punktzahl=-0.27, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=37.63, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=19.88, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=41.63, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=73.18, benutzer=benutzer_namen["Spieler5"], win=True),
],
},
# Partie 5
{
"brettspiel": brettspiel["Spiel1"],
"ort": orte_namen["Ort3"],
"datum": datetime.strptime("2022-10-01", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=95.32, benutzer=benutzer_namen["Spieler3"], win=True),
SpielerPos(punktzahl=19.55, benutzer=benutzer_namen["Spieler5"], win=False),
SpielerPos(punktzahl=35.82, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=7.69, benutzer=benutzer_namen["Spieler4"], win=False),
],
},
# Partie 6
{
"brettspiel": brettspiel["Spiel4"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2023-07-17", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=84.85, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=97.59, benutzer=benutzer_namen["Spieler5"], win=True),
SpielerPos(punktzahl=41.98, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=54.93, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=90.6, benutzer=benutzer_namen["Spieler3"], win=False),
],
},
# Partie 7
{
"brettspiel": brettspiel["Spiel4"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2023-05-20", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=31.16, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=-3.4, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=32.47, benutzer=benutzer_namen["Spieler5"], win=True),
SpielerPos(punktzahl=-0.11, benutzer=benutzer_namen["Spieler2"], win=False),
],
},
# Partie 8
{
"brettspiel": brettspiel["Spiel3"],
"ort": orte_namen["Ort3"],
"datum": datetime.strptime("2022-06-22", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=95.13, benutzer=benutzer_namen["Spieler1"], win=True),
SpielerPos(punktzahl=56.67, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=80.1, benutzer=benutzer_namen["Spieler4"], win=False),
],
},
# Partie 9
{
"brettspiel": brettspiel["Spiel4"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2022-06-03", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=94.3, benutzer=benutzer_namen["Spieler4"], win=True),
SpielerPos(punktzahl=28.98, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=11.54, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=47.04, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=90.35, benutzer=benutzer_namen["Spieler3"], win=False),
SpielerPos(punktzahl=90.14, benutzer=benutzer_namen["Spieler5"], win=False),
],
},
# Partie 10
{
"brettspiel": brettspiel["Spiel4"],
"ort": orte_namen["Ort3"],
"datum": datetime.strptime("2023-08-31", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=31.65, benutzer=benutzer_namen["Spieler5"], win=False),
SpielerPos(punktzahl=45.88, benutzer=benutzer_namen["Spieler6"], win=True),
],
},
# Partie 11
{
"brettspiel": brettspiel["Spiel2"],
"ort": orte_namen["Ort3"],
"datum": datetime.strptime("2023-01-17", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=37.43, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=98.48, benutzer=benutzer_namen["Spieler1"], win=True),
],
},
# Partie 12
{
"brettspiel": brettspiel["Spiel3"],
"ort": orte_namen["Ort3"],
"datum": datetime.strptime("2022-04-11", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=11.07, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=35.16, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=81.87, benutzer=benutzer_namen["Spieler5"], win=False),
SpielerPos(punktzahl=93.59, benutzer=benutzer_namen["Spieler2"], win=True),
],
},
# Partie 13
{
"brettspiel": brettspiel["Spiel2"],
"ort": orte_namen["Ort1"],
"datum": datetime.strptime("2023-06-18", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=50.72, benutzer=benutzer_namen["Spieler4"], win=True),
SpielerPos(punktzahl=40.3, benutzer=benutzer_namen["Spieler3"], win=False),
SpielerPos(punktzahl=33.53, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=25.78, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=8.45, benutzer=benutzer_namen["Spieler6"], win=False),
],
},
# Partie 14
{
"brettspiel": brettspiel["Spiel2"],
"ort": orte_namen["Ort1"],
"datum": datetime.strptime("2022-12-11", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=37.48, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=-2.78, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=66.83, benutzer=benutzer_namen["Spieler5"], win=True),
SpielerPos(punktzahl=31.77, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=47.0, benutzer=benutzer_namen["Spieler3"], win=False),
],
},
# Partie 15
{
"brettspiel": brettspiel["Spiel1"],
"ort": orte_namen["Ort1"],
"datum": datetime.strptime("2023-07-29", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=76.1, benutzer=benutzer_namen["Spieler2"], win=True),
SpielerPos(punktzahl=66.16, benutzer=benutzer_namen["Spieler3"], win=False),
],
},
# Partie 16
{
"brettspiel": brettspiel["Spiel3"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2023-04-01", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=77.09, benutzer=benutzer_namen["Spieler1"], win=True),
SpielerPos(punktzahl=0.96, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=25.15, benutzer=benutzer_namen["Spieler5"], win=False),
],
},
# Partie 17
{
"brettspiel": brettspiel["Spiel4"],
"ort": orte_namen["Ort3"],
"datum": datetime.strptime("2022-09-16", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=67.42, benutzer=benutzer_namen["Spieler5"], win=False),
SpielerPos(punktzahl=66.0, benutzer=benutzer_namen["Spieler3"], win=False),
SpielerPos(punktzahl=33.85, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=67.57, benutzer=benutzer_namen["Spieler2"], win=True),
],
},
# Partie 18
{
"brettspiel": brettspiel["Spiel3"],
"ort": orte_namen["Ort1"],
"datum": datetime.strptime("2023-02-27", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=-1.33, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=36.03, benutzer=benutzer_namen["Spieler2"], win=True),
],
},
# Partie 19
{
"brettspiel": brettspiel["Spiel2"],
"ort": orte_namen["Ort3"],
"datum": datetime.strptime("2023-03-18", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=57.32, benutzer=benutzer_namen["Spieler4"], win=True),
SpielerPos(punktzahl=-2.92, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=45.28, benutzer=benutzer_namen["Spieler6"], win=False),
],
},
# Partie 20
{
"brettspiel": brettspiel["Spiel3"],
"ort": orte_namen["Ort3"],
"datum": datetime.strptime("2022-06-24", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=11.34, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=91.34, benutzer=benutzer_namen["Spieler2"], win=True),
],
},
# Partie 21
{
"brettspiel": brettspiel["Spiel1"],
"ort": orte_namen["Ort1"],
"datum": datetime.strptime("2023-03-09", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=94.33, benutzer=benutzer_namen["Spieler2"], win=True),
SpielerPos(punktzahl=44.07, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=16.49, benutzer=benutzer_namen["Spieler3"], win=False),
SpielerPos(punktzahl=87.22, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=83.45, benutzer=benutzer_namen["Spieler4"], win=False),
],
},
# Partie 22
{
"brettspiel": brettspiel["Spiel2"],
"ort": orte_namen["Ort3"],
"datum": datetime.strptime("2023-06-21", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=-4.09, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=34.92, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=53.51, benutzer=benutzer_namen["Spieler5"], win=True),
SpielerPos(punktzahl=6.09, benutzer=benutzer_namen["Spieler3"], win=False),
SpielerPos(punktzahl=7.38, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=24.19, benutzer=benutzer_namen["Spieler6"], win=False),
],
},
# Partie 23
{
"brettspiel": brettspiel["Spiel3"],
"ort": orte_namen["Ort1"],
"datum": datetime.strptime("2023-03-27", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=27.0, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=28.05, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=51.5, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=80.65, benutzer=benutzer_namen["Spieler3"], win=False),
SpielerPos(punktzahl=88.25, benutzer=benutzer_namen["Spieler5"], win=True),
],
},
# Partie 24
{
"brettspiel": brettspiel["Spiel3"],
"ort": orte_namen["Ort3"],
"datum": datetime.strptime("2022-09-24", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=33.51, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=13.8, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=79.14, benutzer=benutzer_namen["Spieler6"], win=True),
SpielerPos(punktzahl=61.21, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=12.5, benutzer=benutzer_namen["Spieler3"], win=False),
],
},
# Partie 25
{
"brettspiel": brettspiel["Spiel4"],
"ort": orte_namen["Ort3"],
"datum": datetime.strptime("2022-02-26", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=65.47, benutzer=benutzer_namen["Spieler4"], win=True),
SpielerPos(punktzahl=35.26, benutzer=benutzer_namen["Spieler3"], win=False),
SpielerPos(punktzahl=24.58, benutzer=benutzer_namen["Spieler6"], win=False),
],
},
# Partie 26
{
"brettspiel": brettspiel["Spiel2"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2022-08-19", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=77.46, benutzer=benutzer_namen["Spieler5"], win=True),
SpielerPos(punktzahl=17.72, benutzer=benutzer_namen["Spieler3"], win=False),
SpielerPos(punktzahl=36.08, benutzer=benutzer_namen["Spieler2"], win=False),
],
},
# Partie 27
{
"brettspiel": brettspiel["Spiel4"],
"ort": orte_namen["Ort1"],
"datum": datetime.strptime("2023-06-05", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=7.48, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=54.82, benutzer=benutzer_namen["Spieler3"], win=False),
SpielerPos(punktzahl=85.08, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=93.54, benutzer=benutzer_namen["Spieler4"], win=True),
SpielerPos(punktzahl=77.67, benutzer=benutzer_namen["Spieler5"], win=False),
SpielerPos(punktzahl=47.33, benutzer=benutzer_namen["Spieler6"], win=False),
],
},
# Partie 28
{
"brettspiel": brettspiel["Spiel3"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2022-06-04", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=87.18, benutzer=benutzer_namen["Spieler2"], win=True),
SpielerPos(punktzahl=53.17, benutzer=benutzer_namen["Spieler5"], win=False),
SpielerPos(punktzahl=38.68, benutzer=benutzer_namen["Spieler3"], win=False),
SpielerPos(punktzahl=13.65, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=32.94, benutzer=benutzer_namen["Spieler4"], win=False),
],
},
# Partie 29
{
"brettspiel": brettspiel["Spiel1"],
"ort": orte_namen["Ort1"],
"datum": datetime.strptime("2022-07-15", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=6.79, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=64.62, benutzer=benutzer_namen["Spieler5"], win=True),
SpielerPos(punktzahl=42.86, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=51.82, benutzer=benutzer_namen["Spieler3"], win=False),
],
},
# Partie 30
{
"brettspiel": brettspiel["Spiel4"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2022-04-17", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=67.65, benutzer=benutzer_namen["Spieler6"], win=True),
SpielerPos(punktzahl=14.88, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=60.28, benutzer=benutzer_namen["Spieler1"], win=False),
],
},
# Partie 31
{
"brettspiel": brettspiel["Spiel3"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2022-10-07", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=68.06, benutzer=benutzer_namen["Spieler3"], win=False),
SpielerPos(punktzahl=50.24, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=21.59, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=76.48, benutzer=benutzer_namen["Spieler4"], win=True),
SpielerPos(punktzahl=58.78, benutzer=benutzer_namen["Spieler2"], win=False),
],
},
# Partie 32
{
"brettspiel": brettspiel["Spiel4"],
"ort": orte_namen["Ort3"],
"datum": datetime.strptime("2022-05-18", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=-2.76, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=64.99, benutzer=benutzer_namen["Spieler5"], win=True),
SpielerPos(punktzahl=54.56, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=18.2, benutzer=benutzer_namen["Spieler3"], win=False),
],
},
# Partie 33
{
"brettspiel": brettspiel["Spiel3"],
"ort": orte_namen["Ort3"],
"datum": datetime.strptime("2023-07-08", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=21.57, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=38.34, benutzer=benutzer_namen["Spieler5"], win=False),
SpielerPos(punktzahl=84.24, benutzer=benutzer_namen["Spieler6"], win=True),
],
},
# Partie 34
{
"brettspiel": brettspiel["Spiel3"],
"ort": orte_namen["Ort1"],
"datum": datetime.strptime("2022-09-30", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=51.7, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=75.18, benutzer=benutzer_namen["Spieler3"], win=True),
SpielerPos(punktzahl=42.72, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=22.45, benutzer=benutzer_namen["Spieler5"], win=False),
SpielerPos(punktzahl=5.3, benutzer=benutzer_namen["Spieler2"], win=False),
],
},
# Partie 35
{
"brettspiel": brettspiel["Spiel3"],
"ort": orte_namen["Ort3"],
"datum": datetime.strptime("2022-04-10", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=64.75, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=95.85, benutzer=benutzer_namen["Spieler1"], win=True),
],
},
# Partie 36
{
"brettspiel": brettspiel["Spiel1"],
"ort": orte_namen["Ort3"],
"datum": datetime.strptime("2022-12-29", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=32.44, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=48.13, benutzer=benutzer_namen["Spieler3"], win=False),
SpielerPos(punktzahl=93.46, benutzer=benutzer_namen["Spieler6"], win=True),
SpielerPos(punktzahl=65.6, benutzer=benutzer_namen["Spieler5"], win=False),
SpielerPos(punktzahl=25.73, benutzer=benutzer_namen["Spieler1"], win=False),
],
},
# Partie 37
{
"brettspiel": brettspiel["Spiel1"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2022-05-20", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=55.04, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=24.23, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=59.31, benutzer=benutzer_namen["Spieler4"], win=True),
SpielerPos(punktzahl=54.28, benutzer=benutzer_namen["Spieler5"], win=False),
SpielerPos(punktzahl=-1.17, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=-3.56, benutzer=benutzer_namen["Spieler3"], win=False),
],
},
# Partie 38
{
"brettspiel": brettspiel["Spiel3"],
"ort": orte_namen["Ort1"],
"datum": datetime.strptime("2022-08-21", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=44.71, benutzer=benutzer_namen["Spieler3"], win=False),
SpielerPos(punktzahl=77.16, benutzer=benutzer_namen["Spieler2"], win=True),
],
},
# Partie 39
{
"brettspiel": brettspiel["Spiel2"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2022-09-13", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=99.92, benutzer=benutzer_namen["Spieler3"], win=True),
SpielerPos(punktzahl=30.63, benutzer=benutzer_namen["Spieler5"], win=False),
SpielerPos(punktzahl=23.91, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=86.57, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=30.03, benutzer=benutzer_namen["Spieler6"], win=False),
],
},
# Partie 40
{
"brettspiel": brettspiel["Spiel3"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2022-05-11", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=2.35, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=97.73, benutzer=benutzer_namen["Spieler4"], win=True),
SpielerPos(punktzahl=20.73, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=57.28, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=-2.16, benutzer=benutzer_namen["Spieler3"], win=False),
SpielerPos(punktzahl=35.77, benutzer=benutzer_namen["Spieler5"], win=False),
],
},
# Partie 41
{
"brettspiel": brettspiel["Spiel3"],
"ort": orte_namen["Ort1"],
"datum": datetime.strptime("2023-06-30", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=63.04, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=93.23, benutzer=benutzer_namen["Spieler4"], win=True),
SpielerPos(punktzahl=17.39, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=51.58, benutzer=benutzer_namen["Spieler2"], win=False),
],
},
# Partie 42
{
"brettspiel": brettspiel["Spiel4"],
"ort": orte_namen["Ort3"],
"datum": datetime.strptime("2023-06-12", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=82.93, benutzer=benutzer_namen["Spieler2"], win=True),
SpielerPos(punktzahl=52.84, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=43.88, benutzer=benutzer_namen["Spieler3"], win=False),
],
},
# Partie 43
{
"brettspiel": brettspiel["Spiel1"],
"ort": orte_namen["Ort1"],
"datum": datetime.strptime("2023-04-03", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=99.02, benutzer=benutzer_namen["Spieler5"], win=True),
SpielerPos(punktzahl=70.88, benutzer=benutzer_namen["Spieler3"], win=False),
SpielerPos(punktzahl=40.05, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=25.12, benutzer=benutzer_namen["Spieler6"], win=False),
],
},
# Partie 44
{
"brettspiel": brettspiel["Spiel4"],
"ort": orte_namen["Ort3"],
"datum": datetime.strptime("2022-11-09", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=49.21, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=22.08, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=97.73, benutzer=benutzer_namen["Spieler6"], win=True),
SpielerPos(punktzahl=48.95, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=2.51, benutzer=benutzer_namen["Spieler3"], win=False),
],
},
# Partie 45
{
"brettspiel": brettspiel["Spiel1"],
"ort": orte_namen["Ort3"],
"datum": datetime.strptime("2022-10-02", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=67.93, benutzer=benutzer_namen["Spieler5"], win=False),
SpielerPos(punktzahl=54.28, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=78.77, benutzer=benutzer_namen["Spieler4"], win=True),
],
},
# Partie 46
{
"brettspiel": brettspiel["Spiel4"],
"ort": orte_namen["Ort3"],
"datum": datetime.strptime("2022-08-10", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=2.22, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=68.44, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=52.89, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=42.97, benutzer=benutzer_namen["Spieler5"], win=False),
SpielerPos(punktzahl=86.03, benutzer=benutzer_namen["Spieler3"], win=True),
],
},
# Partie 47
{
"brettspiel": brettspiel["Spiel2"],
"ort": orte_namen["Ort3"],
"datum": datetime.strptime("2022-07-12", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=22.03, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=25.38, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=55.2, benutzer=benutzer_namen["Spieler5"], win=False),
SpielerPos(punktzahl=86.35, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=90.5, benutzer=benutzer_namen["Spieler1"], win=True),
],
},
# Partie 48
{
"brettspiel": brettspiel["Spiel4"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2023-04-26", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=33.44, benutzer=benutzer_namen["Spieler3"], win=False),
SpielerPos(punktzahl=92.42, benutzer=benutzer_namen["Spieler4"], win=True),
SpielerPos(punktzahl=17.67, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=90.11, benutzer=benutzer_namen["Spieler6"], win=False),
],
},
# Partie 49
{
"brettspiel": brettspiel["Spiel1"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2022-06-19", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=30.69, benutzer=benutzer_namen["Spieler5"], win=False),
SpielerPos(punktzahl=61.34, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=76.27, benutzer=benutzer_namen["Spieler2"], win=True),
SpielerPos(punktzahl=25.97, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=52.68, benutzer=benutzer_namen["Spieler3"], win=False),
],
},
# Partie 50
{
"brettspiel": brettspiel["Spiel3"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2023-03-23", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=51.11, benutzer=benutzer_namen["Spieler5"], win=False),
SpielerPos(punktzahl=74.74, benutzer=benutzer_namen["Spieler2"], win=True),
SpielerPos(punktzahl=1.94, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=70.82, benutzer=benutzer_namen["Spieler6"], win=False),
],
},
# Partie 51
{
"brettspiel": brettspiel["Spiel4"],
"ort": orte_namen["Ort3"],
"datum": datetime.strptime("2023-01-21", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=4.49, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=71.38, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=98.12, benutzer=benutzer_namen["Spieler3"], win=True),
SpielerPos(punktzahl=73.17, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=1.27, benutzer=benutzer_namen["Spieler2"], win=False),
],
},
# Partie 52
{
"brettspiel": brettspiel["Spiel2"],
"ort": orte_namen["Ort1"],
"datum": datetime.strptime("2023-04-08", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=1.89, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=7.72, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=66.4, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=36.88, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=74.29, benutzer=benutzer_namen["Spieler3"], win=True),
],
},
# Partie 53
{
"brettspiel": brettspiel["Spiel1"],
"ort": orte_namen["Ort1"],
"datum": datetime.strptime("2022-07-10", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=42.89, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=14.65, benutzer=benutzer_namen["Spieler3"], win=False),
SpielerPos(punktzahl=92.08, benutzer=benutzer_namen["Spieler6"], win=True),
SpielerPos(punktzahl=33.16, benutzer=benutzer_namen["Spieler5"], win=False),
],
},
# Partie 54
{
"brettspiel": brettspiel["Spiel3"],
"ort": orte_namen["Ort3"],
"datum": datetime.strptime("2023-05-27", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=59.14, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=61.11, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=40.2, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=46.62, benutzer=benutzer_namen["Spieler3"], win=False),
SpielerPos(punktzahl=62.33, benutzer=benutzer_namen["Spieler5"], win=True),
],
},
# Partie 55
{
"brettspiel": brettspiel["Spiel2"],
"ort": orte_namen["Ort3"],
"datum": datetime.strptime("2022-03-28", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=32.34, benutzer=benutzer_namen["Spieler5"], win=True),
SpielerPos(punktzahl=-0.41, benutzer=benutzer_namen["Spieler2"], win=False),
],
},
# Partie 56
{
"brettspiel": brettspiel["Spiel3"],
"ort": orte_namen["Ort3"],
"datum": datetime.strptime("2022-09-14", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=8.49, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=74.45, benutzer=benutzer_namen["Spieler4"], win=True),
SpielerPos(punktzahl=13.12, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=52.13, benutzer=benutzer_namen["Spieler5"], win=False),
],
},
# Partie 57
{
"brettspiel": brettspiel["Spiel2"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2022-08-31", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=22.63, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=78.91, benutzer=benutzer_namen["Spieler1"], win=True),
SpielerPos(punktzahl=49.48, benutzer=benutzer_namen["Spieler3"], win=False),
SpielerPos(punktzahl=42.63, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=67.58, benutzer=benutzer_namen["Spieler5"], win=False),
],
},
# Partie 58
{
"brettspiel": brettspiel["Spiel2"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2022-09-17", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=86.71, benutzer=benutzer_namen["Spieler1"], win=True),
SpielerPos(punktzahl=55.9, benutzer=benutzer_namen["Spieler3"], win=False),
SpielerPos(punktzahl=67.06, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=72.18, benutzer=benutzer_namen["Spieler5"], win=False),
],
},
# Partie 59
{
"brettspiel": brettspiel["Spiel1"],
"ort": orte_namen["Ort1"],
"datum": datetime.strptime("2022-12-22", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=52.72, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=78.57, benutzer=benutzer_namen["Spieler3"], win=True),
SpielerPos(punktzahl=14.34, benutzer=benutzer_namen["Spieler5"], win=False),
SpielerPos(punktzahl=24.27, benutzer=benutzer_namen["Spieler1"], win=False),
],
},
# Partie 60
{
"brettspiel": brettspiel["Spiel4"],
"ort": orte_namen["Ort3"],
"datum": datetime.strptime("2022-05-31", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=93.39, benutzer=benutzer_namen["Spieler6"], win=True),
SpielerPos(punktzahl=4.59, benutzer=benutzer_namen["Spieler3"], win=False),
SpielerPos(punktzahl=61.55, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=19.08, benutzer=benutzer_namen["Spieler5"], win=False),
SpielerPos(punktzahl=20.1, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=47.65, benutzer=benutzer_namen["Spieler4"], win=False),
],
},
# Partie 61
{
"brettspiel": brettspiel["Spiel4"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2022-11-08", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=18.16, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=72.26, benutzer=benutzer_namen["Spieler3"], win=True),
SpielerPos(punktzahl=57.1, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=1.73, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=52.16, benutzer=benutzer_namen["Spieler5"], win=False),
],
},
# Partie 62
{
"brettspiel": brettspiel["Spiel2"],
"ort": orte_namen["Ort3"],
"datum": datetime.strptime("2022-12-02", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=99.44, benutzer=benutzer_namen["Spieler5"], win=True),
SpielerPos(punktzahl=96.42, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=96.67, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=97.22, benutzer=benutzer_namen["Spieler4"], win=False),
],
},
# Partie 63
{
"brettspiel": brettspiel["Spiel3"],
"ort": orte_namen["Ort1"],
"datum": datetime.strptime("2022-03-22", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=20.6, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=16.51, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=21.21, benutzer=benutzer_namen["Spieler5"], win=False),
SpielerPos(punktzahl=96.0, benutzer=benutzer_namen["Spieler1"], win=True),
SpielerPos(punktzahl=45.19, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=92.88, benutzer=benutzer_namen["Spieler3"], win=False),
],
},
# Partie 64
{
"brettspiel": brettspiel["Spiel1"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2023-01-10", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=19.86, benutzer=benutzer_namen["Spieler5"], win=False),
SpielerPos(punktzahl=19.09, benutzer=benutzer_namen["Spieler3"], win=False),
SpielerPos(punktzahl=49.06, benutzer=benutzer_namen["Spieler6"], win=True),
SpielerPos(punktzahl=9.38, benutzer=benutzer_namen["Spieler2"], win=False),
],
},
# Partie 65
{
"brettspiel": brettspiel["Spiel4"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2023-07-19", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=42.37, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=52.34, benutzer=benutzer_namen["Spieler5"], win=True),
],
},
# Partie 66
{
"brettspiel": brettspiel["Spiel2"],
"ort": orte_namen["Ort1"],
"datum": datetime.strptime("2022-12-24", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=66.43, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=95.59, benutzer=benutzer_namen["Spieler5"], win=True),
SpielerPos(punktzahl=68.6, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=61.34, benutzer=benutzer_namen["Spieler3"], win=False),
SpielerPos(punktzahl=85.13, benutzer=benutzer_namen["Spieler6"], win=False),
],
},
# Partie 67
{
"brettspiel": brettspiel["Spiel4"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2022-09-19", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=65.14, benutzer=benutzer_namen["Spieler3"], win=True),
SpielerPos(punktzahl=42.41, benutzer=benutzer_namen["Spieler4"], win=False),
],
},
# Partie 68
{
"brettspiel": brettspiel["Spiel1"],
"ort": orte_namen["Ort3"],
"datum": datetime.strptime("2022-04-22", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=32.98, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=78.14, benutzer=benutzer_namen["Spieler5"], win=False),
SpielerPos(punktzahl=60.59, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=77.52, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=55.6, benutzer=benutzer_namen["Spieler3"], win=False),
SpielerPos(punktzahl=90.52, benutzer=benutzer_namen["Spieler1"], win=True),
],
},
# Partie 69
{
"brettspiel": brettspiel["Spiel4"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2023-06-13", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=72.78, benutzer=benutzer_namen["Spieler1"], win=True),
SpielerPos(punktzahl=34.6, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=68.1, benutzer=benutzer_namen["Spieler4"], win=False),
],
},
# Partie 70
{
"brettspiel": brettspiel["Spiel3"],
"ort": orte_namen["Ort3"],
"datum": datetime.strptime("2022-06-23", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=12.15, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=-2.51, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=96.69, benutzer=benutzer_namen["Spieler3"], win=True),
SpielerPos(punktzahl=56.52, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=29.22, benutzer=benutzer_namen["Spieler5"], win=False),
SpielerPos(punktzahl=16.79, benutzer=benutzer_namen["Spieler2"], win=False),
],
},
# Partie 71
{
"brettspiel": brettspiel["Spiel3"],
"ort": orte_namen["Ort1"],
"datum": datetime.strptime("2023-06-21", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=11.49, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=72.51, benutzer=benutzer_namen["Spieler4"], win=True),
SpielerPos(punktzahl=55.78, benutzer=benutzer_namen["Spieler6"], win=False),
],
},
# Partie 72
{
"brettspiel": brettspiel["Spiel2"],
"ort": orte_namen["Ort1"],
"datum": datetime.strptime("2023-02-09", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=94.37, benutzer=benutzer_namen["Spieler2"], win=True),
SpielerPos(punktzahl=9.51, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=50.82, benutzer=benutzer_namen["Spieler6"], win=False),
],
},
# Partie 73
{
"brettspiel": brettspiel["Spiel2"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2022-03-05", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=37.53, benutzer=benutzer_namen["Spieler5"], win=False),
SpielerPos(punktzahl=46.3, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=91.84, benutzer=benutzer_namen["Spieler2"], win=True),
SpielerPos(punktzahl=13.54, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=62.7, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=56.53, benutzer=benutzer_namen["Spieler3"], win=False),
],
},
# Partie 74
{
"brettspiel": brettspiel["Spiel3"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2022-03-14", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=41.63, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=-0.88, benutzer=benutzer_namen["Spieler3"], win=False),
SpielerPos(punktzahl=41.33, benutzer=benutzer_namen["Spieler5"], win=False),
SpielerPos(punktzahl=96.48, benutzer=benutzer_namen["Spieler2"], win=True),
SpielerPos(punktzahl=39.15, benutzer=benutzer_namen["Spieler4"], win=False),
],
},
# Partie 75
{
"brettspiel": brettspiel["Spiel1"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2023-08-22", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=65.69, benutzer=benutzer_namen["Spieler5"], win=True),
SpielerPos(punktzahl=48.71, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=55.09, benutzer=benutzer_namen["Spieler3"], win=False),
],
},
# Partie 76
{
"brettspiel": brettspiel["Spiel1"],
"ort": orte_namen["Ort1"],
"datum": datetime.strptime("2022-03-20", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=20.85, benutzer=benutzer_namen["Spieler5"], win=True),
SpielerPos(punktzahl=3.91, benutzer=benutzer_namen["Spieler4"], win=False),
],
},
# Partie 77
{
"brettspiel": brettspiel["Spiel2"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2022-04-06", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=80.86, benutzer=benutzer_namen["Spieler3"], win=True),
SpielerPos(punktzahl=4.96, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=27.08, benutzer=benutzer_namen["Spieler4"], win=False),
],
},
# Partie 78
{
"brettspiel": brettspiel["Spiel1"],
"ort": orte_namen["Ort1"],
"datum": datetime.strptime("2022-03-26", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=33.41, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=56.58, benutzer=benutzer_namen["Spieler1"], win=True),
],
},
# Partie 79
{
"brettspiel": brettspiel["Spiel4"],
"ort": orte_namen["Ort3"],
"datum": datetime.strptime("2022-07-11", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=10.98, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=95.66, benutzer=benutzer_namen["Spieler5"], win=True),
SpielerPos(punktzahl=13.05, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=57.41, benutzer=benutzer_namen["Spieler2"], win=False),
],
},
# Partie 80
{
"brettspiel": brettspiel["Spiel1"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2022-03-21", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=98.81, benutzer=benutzer_namen["Spieler5"], win=True),
SpielerPos(punktzahl=79.14, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=-1.81, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=23.91, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=88.13, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=71.05, benutzer=benutzer_namen["Spieler3"], win=False),
],
},
# Partie 81
{
"brettspiel": brettspiel["Spiel4"],
"ort": orte_namen["Ort1"],
"datum": datetime.strptime("2022-08-13", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=90.26, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=64.09, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=83.91, benutzer=benutzer_namen["Spieler5"], win=False),
SpielerPos(punktzahl=98.33, benutzer=benutzer_namen["Spieler3"], win=True),
SpielerPos(punktzahl=89.55, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=25.86, benutzer=benutzer_namen["Spieler2"], win=False),
],
},
# Partie 82
{
"brettspiel": brettspiel["Spiel2"],
"ort": orte_namen["Ort1"],
"datum": datetime.strptime("2022-04-08", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=77.0, benutzer=benutzer_namen["Spieler1"], win=True),
SpielerPos(punktzahl=38.4, benutzer=benutzer_namen["Spieler4"], win=False),
],
},
# Partie 83
{
"brettspiel": brettspiel["Spiel4"],
"ort": orte_namen["Ort3"],
"datum": datetime.strptime("2022-03-06", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=-0.67, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=27.09, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=93.91, benutzer=benutzer_namen["Spieler5"], win=True),
SpielerPos(punktzahl=32.92, benutzer=benutzer_namen["Spieler3"], win=False),
SpielerPos(punktzahl=10.15, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=55.72, benutzer=benutzer_namen["Spieler2"], win=False),
],
},
# Partie 84
{
"brettspiel": brettspiel["Spiel4"],
"ort": orte_namen["Ort1"],
"datum": datetime.strptime("2023-02-10", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=80.42, benutzer=benutzer_namen["Spieler1"], win=True),
SpielerPos(punktzahl=-4.19, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=17.17, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=42.47, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=38.33, benutzer=benutzer_namen["Spieler3"], win=False),
],
},
# Partie 85
{
"brettspiel": brettspiel["Spiel4"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2022-03-10", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=19.3, benutzer=benutzer_namen["Spieler3"], win=False),
SpielerPos(punktzahl=10.25, benutzer=benutzer_namen["Spieler5"], win=False),
SpielerPos(punktzahl=20.38, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=70.21, benutzer=benutzer_namen["Spieler4"], win=True),
],
},
# Partie 86
{
"brettspiel": brettspiel["Spiel1"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2023-02-27", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=40.53, benutzer=benutzer_namen["Spieler5"], win=False),
SpielerPos(punktzahl=72.44, benutzer=benutzer_namen["Spieler3"], win=True),
SpielerPos(punktzahl=35.98, benutzer=benutzer_namen["Spieler2"], win=False),
],
},
# Partie 87
{
"brettspiel": brettspiel["Spiel1"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2023-01-05", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=92.28, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=25.13, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=-1.25, benutzer=benutzer_namen["Spieler3"], win=False),
SpielerPos(punktzahl=98.76, benutzer=benutzer_namen["Spieler2"], win=True),
],
},
# Partie 88
{
"brettspiel": brettspiel["Spiel2"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2023-02-09", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=99.66, benutzer=benutzer_namen["Spieler6"], win=True),
SpielerPos(punktzahl=49.15, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=73.13, benutzer=benutzer_namen["Spieler5"], win=False),
SpielerPos(punktzahl=70.88, benutzer=benutzer_namen["Spieler1"], win=False),
],
},
# Partie 89
{
"brettspiel": brettspiel["Spiel4"],
"ort": orte_namen["Ort3"],
"datum": datetime.strptime("2023-04-27", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=16.59, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=79.55, benutzer=benutzer_namen["Spieler5"], win=True),
],
},
# Partie 90
{
"brettspiel": brettspiel["Spiel4"],
"ort": orte_namen["Ort1"],
"datum": datetime.strptime("2023-02-25", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=28.6, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=67.24, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=59.4, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=32.49, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=69.16, benutzer=benutzer_namen["Spieler5"], win=True),
SpielerPos(punktzahl=14.15, benutzer=benutzer_namen["Spieler3"], win=False),
],
},
# Partie 91
{
"brettspiel": brettspiel["Spiel3"],
"ort": orte_namen["Ort1"],
"datum": datetime.strptime("2023-01-08", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=70.29, benutzer=benutzer_namen["Spieler3"], win=True),
SpielerPos(punktzahl=7.58, benutzer=benutzer_namen["Spieler5"], win=False),
SpielerPos(punktzahl=11.35, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=47.03, benutzer=benutzer_namen["Spieler6"], win=False),
],
},
# Partie 92
{
"brettspiel": brettspiel["Spiel1"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2022-11-16", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=22.32, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=41.51, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=23.43, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=80.96, benutzer=benutzer_namen["Spieler3"], win=True),
SpielerPos(punktzahl=75.28, benutzer=benutzer_namen["Spieler5"], win=False),
],
},
# Partie 93
{
"brettspiel": brettspiel["Spiel2"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2023-04-14", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=31.67, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=7.1, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=66.92, benutzer=benutzer_namen["Spieler5"], win=True),
SpielerPos(punktzahl=6.24, benutzer=benutzer_namen["Spieler3"], win=False),
SpielerPos(punktzahl=22.95, benutzer=benutzer_namen["Spieler1"], win=False),
],
},
# Partie 94
{
"brettspiel": brettspiel["Spiel2"],
"ort": orte_namen["Ort3"],
"datum": datetime.strptime("2022-12-27", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=14.13, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=41.71, benutzer=benutzer_namen["Spieler5"], win=True),
],
},
# Partie 95
{
"brettspiel": brettspiel["Spiel3"],
"ort": orte_namen["Ort1"],
"datum": datetime.strptime("2023-03-12", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=-0.28, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=49.69, benutzer=benutzer_namen["Spieler5"], win=True),
],
},
# Partie 96
{
"brettspiel": brettspiel["Spiel1"],
"ort": orte_namen["Ort1"],
"datum": datetime.strptime("2023-02-20", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=41.5, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=69.57, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=93.86, benutzer=benutzer_namen["Spieler1"], win=True),
SpielerPos(punktzahl=16.63, benutzer=benutzer_namen["Spieler5"], win=False),
],
},
# Partie 97
{
"brettspiel": brettspiel["Spiel2"],
"ort": orte_namen["Ort3"],
"datum": datetime.strptime("2022-01-17", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=49.03, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=28.68, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=74.18, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=51.62, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=55.2, benutzer=benutzer_namen["Spieler5"], win=False),
SpielerPos(punktzahl=96.81, benutzer=benutzer_namen["Spieler3"], win=True),
],
},
# Partie 98
{
"brettspiel": brettspiel["Spiel1"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2023-08-17", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=27.62, benutzer=benutzer_namen["Spieler3"], win=False),
SpielerPos(punktzahl=38.15, benutzer=benutzer_namen["Spieler6"], win=False),
SpielerPos(punktzahl=98.78, benutzer=benutzer_namen["Spieler2"], win=True),
SpielerPos(punktzahl=59.85, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=71.45, benutzer=benutzer_namen["Spieler1"], win=False),
],
},
# Partie 99
{
"brettspiel": brettspiel["Spiel2"],
"ort": orte_namen["Ort2"],
"datum": datetime.strptime("2022-05-12", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=8.79, benutzer=benutzer_namen["Spieler1"], win=False),
SpielerPos(punktzahl=50.18, benutzer=benutzer_namen["Spieler5"], win=False),
SpielerPos(punktzahl=67.59, benutzer=benutzer_namen["Spieler3"], win=True),
],
},
# Partie 100
{
"brettspiel": brettspiel["Spiel1"],
"ort": orte_namen["Ort3"],
"datum": datetime.strptime("2023-01-26", "%Y-%m-%d"),
"spieler": [
SpielerPos(punktzahl=52.29, benutzer=benutzer_namen["Spieler4"], win=False),
SpielerPos(punktzahl=60.34, benutzer=benutzer_namen["Spieler3"], win=False),
SpielerPos(punktzahl=45.04, benutzer=benutzer_namen["Spieler2"], win=False),
SpielerPos(punktzahl=92.38, benutzer=benutzer_namen["Spieler1"], win=True),
],
},
]

# Erstelle einige Partien mit Spielern
partien = []
for data in data_100:
    brettspiel = data["brettspiel"]
    ort = data["ort"]
    datum = data["datum"]
    spieler = data["spieler"]

    # Erstelle vollständige Partie
    partie = Partie(brettspiel=brettspiel, datum=datum, ort=ort, spieler=spieler)
    session.add(partie)

session.commit()

# Schließe die Session
session.close()
