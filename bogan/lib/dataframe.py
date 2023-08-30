import pandas as pd
from bogan.config import get_logger
from bogan.db.models import Benutzer, Partie, SpielerPos, Brettspiel, Ort, Base
from bogan.lib.data_queries import Query

log = get_logger(__file__)


class Dataframe:
    def __init__(self, query, cols=[]) -> None:
        self.query = query
        self.cols = cols
        # bei leerer Query -> self.type = None
        if query.count() > 0:
            self.type = type(query[0])
        else:
            self.type = None

    @property
    def nested_dict(self):
        pd_list = []
        for row in query:
            if self.type == SpielerPos:
                pd_list.append(self.__row_dict_spieler_pos(row=row))
            elif self.type == Partie:
                pd_list.append(self.__row_dict_partie(row=row))
            else:
                log.warning(f"Query enthält kein gültiges Model: {self.type}")

        return pd_list

    @property
    def df(self):
        return pd.DataFrame(self.nested_dict)


    def __row_dict_spieler_pos(self, row: SpielerPos):
        full_dict = {
            "partie_id": row.partie.id,
            "datum": row.partie.datum,
            "ort": row.partie.ort.name,
            "brettspiel": row.partie.brettspiel.name,
            "complexity": row.partie.brettspiel.complexity,
            "spieler": row.benutzer.name,
            "position": row.position,
            "punktzahl": row.punktzahl,
            "win": row.win,
        }
        return self.__filter_cols(full_dict)

    def __row_dict_partie(self, row: Partie):
        full_dict = {
            "id": row.id,
            "datum": row.datum,
            "brettspiel": row.brettspiel.name,
            "ort": row.ort.name,
            "brettspiel_complexity": row.brettspiel.complexity,
            # TODO duration has to been added in models.partie
            # "duration": row.duration,
            "spieler": row.spieler,
        }
        return self.__filter_cols(full_dict)

    def __filter_cols(self, full_dict: dict):
        cols = self.cols
        if cols:
            partial_dict = {}
            for col in cols:
                if col in full_dict.keys():
                    partial_dict[col] = full_dict[col]
            return partial_dict
        else:
            return full_dict


if __name__ == "__main__":
    query = Query().spieler_pos_by(ort="Spielewochenende")

    s = Dataframe(query, cols=["partie_id", 'datum', 'spieler'])
    print(s.query)
    print(s.type)
    print(s.df)
