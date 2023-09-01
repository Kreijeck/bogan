import pandas as pd
from typing import List

from sqlalchemy.orm import Session
from bogan.db.models import Base, Benutzer, Brettspiel, Ort, Partie, SpielerPos
from bogan.config import get_play_engine

engine = get_play_engine()

class DfUtils:
    @staticmethod
    def map_ranking(row: SpielerPos) -> dict:
        return {
            "name": row.benutzer.name,
            "punktzahl": row.punktzahl,
            "datum": row.partie.datum,
            "win": row.win,
            "position": row.position,
            "brettspiel": row.partie.brettspiel.name,
            "rank_points": DfUtils.add_rankpoints
        }
    
    @staticmethod
    def add_rankpoints(df):
        return 3

class Dataframe:
    def ranking_info(self, spieler_pos: List[SpielerPos]):
        pd_list = []
        for row in spieler_pos:
            pd_list.append(DfUtils.map_ranking(row))
        
        df = pd.DataFrame(pd_list)

        return df