import pandas as pd
from typing import List, Union
from bogan.config import get_logger
from bogan.db.models import Partie, SpielerPos
from bogan.lib.data_queries import Query
from datetime import datetime

log = get_logger(__file__)


class Dataframe:
    def __init__(self, query, cols=None, rank_method="default") -> None:
        self._query = query
        self._cols = cols
        self._type = self.__get_type()
        self.df = self.__create_df()
        self.rank_method = rank_method

    @property
    def nested_dict(self) -> list:
        pd_list = [self.__row_dict(row) for row in self._query]

        return pd_list

    def __get_type(self):
        # bei leerer Query -> self.type = None
        if self._query.count() > 0:
            return type(self._query[0])
        else:
            return None

    def __create_df(self) -> pd.DataFrame:
        data = self.nested_dict
        self.__validate_cols_in_dictionary(data)

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

    def __validate_cols_in_dictionary(self, data: List[dict]) -> None:
        # Warning if nested dictionary has wrong columns
        # leeres dictionary
        if data:
            first_row = data[0]
        else:
            log.warning("Das zu validierende dictionary ist leer!")
            first_row = {}
            return

        # falsche columnss
        if self._cols:
            missing_cols = [col for col in self._cols if col not in first_row.keys()]
            if missing_cols:
                log.warning(f"Columns {missing_cols} are missing in the nested_dict. Set all to 'NAN' in column")

    def __default_none(self, value, self_value) -> any:
        """Set value to specific self_value if value is None

        Args:
            value (any): Value to check
            self_value (any): class variable to set

        Returns:
            None
        """
        # Default: value = self.value
        if value is None:
            return self_value
        else:
            return value

    def __needed_cols(self, df: pd.DataFrame, columns: list) -> None:
        for col in columns:
            if col not in df.columns:
                raise KeyError(f"Not all columns are available, need: {columns}")

    def add_position(self, df: pd.DataFrame = None, inplace=True) -> pd.DataFrame:
        # add 'position' column: Position des Spielers, abhängig von der erreichten Punktzahl
        df = self.__default_none(df, self.df)

        # only works if col "punktzahl" is used
        self.__needed_cols(df, ["punktzahl", "partie_id"])

        group_df = df.groupby("partie_id")
        df["position"] = group_df["punktzahl"].rank(ascending=False)

        if inplace:
            self.df = df

        return df

    def add_num_players(self, df: pd.DataFrame = None, inplace=True) -> pd.DataFrame:
        # add 'num_players' column: Anzahl der Spieler pro Partie (partie_id)
        df = self.__default_none(df, self.df)
        self.__needed_cols(df, ["partie_id", "spieler"])

        df["num_players"] = df.groupby("partie_id")["spieler"].transform("count")

        if inplace:
            self.df = df

        return df

    def add_rankpoints(self, df: pd.DataFrame = None, method: str = None, inplace=True) -> pd.DataFrame:
        # Add 'rankpoints' column: rankpoints of a game, depends on the position achieved

        df = self.__default_none(df, self.df)
        method = self.__default_none(method, self.rank_method)
        self.__needed_cols(df, ["complexity", "partie_id"])

        # Execute functions for necessary cols
        if "num_players" not in df.columns:
            log.info('"num_players" is needed to calculate "rank_points", func num_player added')
            df = self.add_num_players()
        if "position" not in df.columns:
            log.info('"position" is needed to calculate "rank_points", func add_position added')
            df = self.add_position()

        # TODO: Refactor matching complexity
        match method:
            # default case: Aktuell max_points_per_player
            case "default":
                rank_func = CalcRank.max_points_per_player

            case "max_point_per_player":
                rank_func = CalcRank.max_points_per_player

            case _:
                raise ValueError(f"{method} is not valid to caluclate ranking points")

        # Calculate rank points
        df["rankpoints"] = df.apply(
            lambda row: rank_func(position=row["position"], num_players=row["num_players"]),
            axis=1,
        )
        df["rankpoints_complex"] = df.apply(
            lambda row: rank_func(
                position=row["position"], num_players=row["num_players"], complexity=row["complexity"]
            ),
            axis=1,
        )

        if inplace:
            self.df = df
        return df

    def add_rankppoints_sum(self, df: pd.DataFrame = None, inplace=True) -> pd.DataFrame:
        # Add column 'sum_rankpoints' and 'sum_rankpoints_complex': Aufsummierte Summe der Punkte über datum der Partien
        df = self.__default_none(df, self.df)
        self.__needed_cols(df, ["datum", "spieler"])

        # Sortiere Dataframe nach Datum
        df = df.sort_values(by=["datum"]).reset_index()

        # Add rankpoints wenn diese noch nicht vorhanden
        if "rankpoints" not in df.columns or "rankpoints_complex" not in df.columns:
            log.warning("Rankpoints wurden noch nicht berechnet, aber benötigt um Summe zu berechnen!"\
                        "Funktion self.add_rankpoints wird daher ausgeführt.")
                        
            df = self.add_rankpoints()

        df["sum_rankpoints"] = df.groupby("spieler")["rankpoints"].cumsum()
        df["sum_rankpoints_complex"] = df.groupby("spieler")["rankpoints_complex"].cumsum()

        if inplace:
            self.df = df
        return df

    def strip_cols_to(self, columns: List[str], df: pd.DataFrame = None, inplace=True) -> pd.DataFrame:
        # Reduziere DF auf columns
        df = self.__default_none(df, self.df)

        df = df[columns]

        if inplace:
            self.df = df
        return df


class CalcRank:
    @staticmethod
    def max_points_per_player(position: int, num_players: int, complexity=1) -> float:
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
        try:
            num_players = int(num_players)
            position = float(position)
        except ValueError:
            log.warning(
                f"Points can't be calculated - 0 points returned: position: {position}, num_players: {num_players}"
            )
            return 0.0

        # Wanted behaviour
        if num_players != 1:
            return round((num_players - ((position - 1) * 2 * num_players / (num_players - 1))) * complexity, 2)
        else:
            # TODO Check to get information about the data
            log.warning("Only 1 Player in game, please check! 0 points returned")
            return 0.0

class DashDataFrame:
    @staticmethod
    def rank_df(ort_name: str=None, start_datum: datetime=None, end_datum=None) -> pd.DataFrame:
        """Erstellt Dataframe für ein Ranking Plot

        Args:
            ort (str, optional): Ort.name. Defaults to None.
            start_datum (datetime, optional): Datum Start. Defaults to None.
            end_datum (datetime, optional): Datum Ende. Defaults to None.

        Returns:
            pd.DataFrame: df für plotly
        """
        spieler_query = Query().spieler_pos_by(ort=ort_name)
        rank_df = Dataframe(spieler_query)
        rank_df.add_rankpoints()
        rank_df.add_rankppoints_sum()
        
        rank_df.df.reset_index()
        
        #TODO reduziere Spalten
        # rank_df.strip_cols_to([])

        return rank_df.df



if __name__ == "__main__":
    query = Query().spieler_pos_by(ort="Spielewochenende")

    s = Dataframe(query)
    # print(s._query)
    # print(s._type)
    s.add_position()
    # s.add_num_players()
    # s.add_rankpoints(method="max_point_per_player")
    s.add_rankppoints_sum()
    # print(s.df.head(20))
    # print(s.df.columns)

    # s.strip_cols_to(["partie_id", "ort", "spieler"])
    # print(s.df.head(2))

    # for spieler, spieler_df in s.df.groupby("spieler"):
    #     print(spieler)
    #     print(spieler_df)
    # for key, value in create_table("Lasse", s.df).items():
    #     print(key, value)

    print(DashDataFrame.rank_df().head(10))
    
