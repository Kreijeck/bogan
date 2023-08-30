import pandas as pd
from typing import List
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
    def nested_dict(self) -> list:
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
    def df(self) -> pd.DataFrame:
        data = self.nested_dict
        self.__validate_cols(data)
        return pd.DataFrame(data, columns=self.cols)

    def __row_dict_spieler_pos(self, row: SpielerPos) -> dict:
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
        return full_dict

    def __row_dict_partie(self, row: Partie) -> dict:
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
        return full_dict

    def __validate_cols(self, data: List[dict]) -> None:
        # Warning if dictionary is not valid
        # leeres dictionary
        if data:
            first = data[0]
        else:
            log.warning("Das zu validierende dictionary ist leer!")
            first = {}
            return

        # falsche cols
        missing_cols = [col for col in self.cols if col not in first.keys()]
        if missing_cols:
            log.warning(f"Columns {missing_cols} are missing in the nested_dict. Set all to 'NAN' in column")


if __name__ == "__main__":
    query = Query().spieler_pos_by(ort="Spielewochenende")

    s = Dataframe(query, cols=["sPieler", "datum", "ort"])
    print(s.query)
    print(s.type)
    print(s.df)
