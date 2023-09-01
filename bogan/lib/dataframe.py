import pandas as pd
from typing import List, Union
from bogan.config import get_logger
from bogan.db.models import Partie, SpielerPos
from bogan.lib.data_queries import Query

log = get_logger(__file__)


class Dataframe:
    def __init__(self, query, cols=[]) -> None:
        self._query = query
        self._cols = cols
        self._type = self.__get_type()
        self.df = self.__create_df()

    @property
    def nested_dict(self) -> list:
        pd_list = [self.__row_dict(row) for row in query]

        return pd_list

    def __get_type(self):
        # bei leerer Query -> self.type = None
        if self._query.count() > 0:
            return type(query[0])
        else:
            return None

    def __create_df(self) -> pd.DataFrame:
        data = self.nested_dict
        self.__validate_cols(data)
        return pd.DataFrame(data, columns=self._cols)

    def __row_dict(self, row: Union[SpielerPos, Partie]) -> dict:
        full_dict = {}
        if self._type == SpielerPos:
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
        elif self._type == Partie:
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
        else:
            raise TypeError(f"Query enthält kein gültiges Model: {self._type}")

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
        missing_cols = [col for col in self._cols if col not in first.keys()]
        if missing_cols:
            log.warning(f"Columns {missing_cols} are missing in the nested_dict. Set all to 'NAN' in column")

    def add_position(self, df: pd.DataFrame = None, inplace=True):
        # Default: df = self.df
        if df is None:
            df = self.df

        # only works if col "punktzahl" is used
        if "punktzahl" not in df.columns and "partie_id" not in df.columns:
            raise KeyError(f"Punktzahl oder Partie_id fehlt in Columns: {df.columns}")

        group_df = df.groupby("partie_id")
        df["position"] = group_df["punktzahl"].rank(ascending=False)

        if inplace:
            self.df = df

        return df


if __name__ == "__main__":
    query = Query().spieler_pos_by(ort="Spielewochenende")

    s = Dataframe(query, cols=["partie_id", "datum", "brettspiel", "ort", "spieler", "punktzahl"])
    print(s._query)
    print(s._type)
    s.add_position()
    print(s.df.head(20))
