import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from sqlalchemy.orm import Session

# from sqlalchemy import select
from bogan.config import get_logger, get_play_engine, cfg_db
from bogan.db.models import Benutzer, Partie, SpielerPos, Brettspiel, Ort
from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import List


# Init modules
log = get_logger(__file__)
engine = get_play_engine()
# db_file = os.path.join(cfg_db["dir"], "spiel_copy.db")
# engine = get_play_engine(path=db_file)


def points_max_player(position: int, num_players: int, complexity=1) -> float:
    """Summe der Punkte = 0
    Umso mehr Spieler umso mehr Punkte gibt es für den Sieg (Abzug bei Niederlage)
    Punkte Ranking linear
    Spieleranzahl bestimmt maximale +/- Punkte (bsp: 5 Spieler -> 1. 5Pkt; 3. 0Pkt,  5: -5Pkt)

    Berechnung: y: Anzahl Spieler
                x: Position
                c: complexity

                    (x-1)*2y
                y - --------- * c
                    y-1

    Args:
        ranking (int): Platzierung
        num_players (int): Anzahl an Spielern
        complexity (float): Komplexität: defaults=None

    Returns:
        float: Punkte
    """
    if isinstance(num_players, int) and isinstance(position, int):
        if num_players == 1:
            # TODO Check to get information about the data
            log.warn("Only 1 Player in game, please check!")
            return 0
        else:
            return round(num_players - ((position - 1) * 2 * num_players / (num_players - 1)), 2)

    else:
        # TODO Check to get information about the data
        log.warning(f"Points can't be calculated: position: {position}, num_players: {num_players}")
        return 0


def df_ranking(ort: str) -> pd.DataFrame:
    """Jede Spieler hat eigenwird als ein Namen geführt, alle Spieler sind columns

    Args:
        ort (str): gespielter Ort

    Returns:
        pd.DataFrame: Dataframe mit Infos zum Spiel
    """
    # Queries erstellen
    with Session(engine) as session:
        my_query: List[SpielerPos] = (
            session.query(SpielerPos)
            .join(Partie)
            .join(Ort)
            .where(Ort.name == ort)
            .where(SpielerPos.punktzahl)
            .order_by(Partie.datum)
        )

    # Create df
    pd_list = []
    log.info(f"Anzahl an Datensätzen: {my_query.count()}")
    for row in my_query:
        # calc additional infos
        num_players = my_query.where(Partie.id == row.partie.id).count()
        # create dictionary
        tmp_dict = {}
        tmp_dict["partie_id"] = row.partie.id
        tmp_dict["datum"] = row.partie.datum
        tmp_dict["ort"] = row.partie.ort.name
        tmp_dict["brettspiel"] = row.partie.brettspiel.name
        tmp_dict["complex"] = row.partie.brettspiel.complexity
        tmp_dict["spieler"] = row.benutzer.name
        tmp_dict["position"] = row.position
        tmp_dict["punktzahl"] = row.punktzahl
        tmp_dict["rank_points"] = points_max_player(
            position=row.position, num_players=num_players
        )

        pd_list.append(tmp_dict)

    df = pd.DataFrame(pd_list)
    df["sum_rank_points"] = df.groupby("spieler")["rank_points"].cumsum()

    # calculate Summe der Ranking points
    # names = list(df['spieler'].unique())
    # for name in names:
    #     print(names)

    return df


def get_line_plot(df: pd.DataFrame):
    fig_line = px.line(df, x=df.index, y="sum_rank_points", color="spieler", line_shape="linear", markers=True)

    # Füge vertikale Hilfslinien hinzu
    for i in df.index:
        if i % 20 == 0:
            fig_line.add_vline(x=i, line_dash="dash", line_color="gray")
    fig_line.show()


def get_table_plot(df: pd.DataFrame):
    ### Tabelle
    # Pivottabelle erstellen
    pivot_df = df.pivot_table(index="spieler", columns="datum", values="rank_points", fill_value=0)

    # Gesamte Punktzahl für jeden Spieler berechnen
    gesamte_punktzahl = df.groupby("spieler")["rank_points"].sum()

    # Neue Spalte für die Gesamtpunktzahl hinzufügen
    pivot_df["Gesamte Punktzahl"] = gesamte_punktzahl
    print(pivot_df)

    fig_table = go.Figure(
        data=[
            go.Table(
                header=dict(values=["Spieler", "Gesamte Punktzahl", list(pivot_df.columns)]),
                cells=dict(values=pivot_df),
            )
        ]
    )

    fig_table.show()


def create_plots(df: pd.DataFrame):
    get_line_plot(df)
    # get_table_plot(df)


if __name__ == "__main__":
    ort = "Mittwochsrunde"
    name = "Lasse"
    datum_start = datetime.strptime("01.01.2023", "%d.%m.%Y")

    result = df_ranking(ort=ort)
    create_plots(result)
    result.groupby("spieler")["Jochen"]

    # with Session(engine) as session:
    #     my_query: List[SpielerPos] = (
    #         session.query(SpielerPos)
    #         .join(Partie)
    #         .join(Ort)
    #         .where(Ort.name == ort)
    #         .where(SpielerPos.punktzahl)
    #         .order_by(Partie.datum)
    #     )
    # for q in my_query:
    #     print(q)
