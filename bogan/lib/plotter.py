from typing import List
from datetime import datetime

import pandas as pd
import plotly.express as px

import sqlalchemy.orm as Session
from bogan.config import get_logger, get_play_engine
from bogan.db.models import Benutzer, Partie, SpielerPos, Brettspiel, Ort

# Init Modules
log = get_logger(__file__)

class Ranking:
    def __init__(self, df=None) -> None:
        self.engine = get_play_engine()
        self.df = df
    
    def points_max_player(self, position: int, num_players: int) -> float:
       """Summe der Punkte = 0
    Umso mehr Spieler umso mehr Punkte gibt es für den Sieg (Abzug bei Niederlage)
    Punkte Ranking linear
    Spieleranzahl bestimmt maximale +/- Punkte (bsp: 5 Spieler -> 1. 5Pkt; 3. 0Pkt,  5: -5Pkt)

    Berechnung: y: Anzahl Spieler
                x: Position

                    (x-1)*2y
                y - ---------
                    y-1

    Args:
        ranking (int): Platzierung
        num_players (int): Anzahl an Spielern

    Returns:
        float: Punkte
    """
       if isinstance(num_players, int) and isinstance(position, int):
        if num_players == 1:
           #TODO Check to get information about the data
           log.warn("Only 1 Player in game, please check!" )
           return 0
        else:
            return round(num_players - ((position - 1) * 2 * num_players / (num_players - 1)), 2)
       else:
          #TODO Check to get information about the data
          log.warning(f"Points can't be calculated: position: {position}, num_players: {num_players}")
          return 0
       
    def update_df_ort(self, ort: str, overwrite=True) -> pd.DataFrame:
        # Query erstellen
        with Session(self.engine) as session:
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
            tmp_dict["rank_points"] = self.points_max_player(position=row.position, num_players=num_players)

            pd_list.append(tmp_dict)

        df = pd.DataFrame(pd_list)
        df["sum_rank_points"] = df.groupby("spieler")["rank_points"].cumsum()

        return df