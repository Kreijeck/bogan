import pandas as pd
from typing import List, Union
from bogan.config import get_logger
from bogan.db.models import Partie, SpielerPos
from bogan.lib.data_queries import Query

log = get_logger(__file__)


class Dataframe:
    def __init__(self, query, cols=None) -> None:
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

    def __default_none(self, value, self_value) -> None:
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

    def __needed_cols(self, columns: list) -> None:
        for col in columns:
            if col not in columns:
                raise KeyError(f"Not all columns are available, need: {columns}")

    def add_position(self, df: pd.DataFrame = None, inplace=True) -> pd.DataFrame:
        # add 'position' column: Position des Spielers, abhängig von der erreichten Punktzahl
        df = self.__default_none(df, self.df)

        # only works if col "punktzahl" is used
        self.__needed_cols(["punktzahl", "partie_id"])

        group_df = df.groupby("partie_id")
        df["position"] = group_df["punktzahl"].rank(ascending=False)

        if inplace:
            self.df = df

        return df

    def add_num_players(self, df: pd.DataFrame = None, inplace=True) -> pd.DataFrame:
        # add 'num_players' column: Anzahl der Spieler pro Partie (partie_id)
        df = self.__default_none(df, self.df)
        self.__needed_cols(["partie_id", "spieler"])

        df["num_players"] = df.groupby("partie_id")["spieler"].transform("count")

        if inplace:
            self.df = df

        return df

    def add_rankpoints(
        self, df: pd.DataFrame = None, complexity=False, method: str = None, inplace=True
    ) -> pd.DataFrame:
        # Add 'rankpoints' column: rankpoints of a game, depends on the position achieved

        df = self.__default_none(df, self.df)
        self.__needed_cols(["complexity", "partie_id"])

        # Add num_players if not there
        if "num_players" not in df.columns:
            self.add_num_players()

        # TODO: Refactor matching complexity
        match method:
            case "max_point_per_player":
                if not complexity:
                    df["rankpoints"] = df.apply(
                        lambda row: CalcRank.max_points_per_player(
                            position=row["position"], num_players=row["num_players"]
                        ),
                        axis=1,
                    )
                else:
                    df["rankpoints_with_complex"] = df.apply(
                        lambda row: CalcRank.max_points_per_player(
                            position=row["position"], num_players=row["num_players"], complexity=row["complexity"]
                        ),
                        axis=1,
                    )
            case _:
                raise ValueError("please choose valid method")

        if inplace:
            self.df = df
        return df
    
    def strip_cols_to(self, columns: List[str], df:pd.DataFrame=None, inplace=True) -> pd.DataFrame:
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


if __name__ == "__main__":
    query = Query().spieler_pos_by(ort="Spielewochenende")

    s = Dataframe(query)
    # print(s._query)
    # print(s._type)
    s.add_position()
    #s.add_num_players()
    s.add_rankpoints(method="max_point_per_player",complexity=False)
    print(s.df.head(20))
    print(s.df.columns)

    s.strip_cols_to(["partie_id", "ort", "spieler"])
    print(s.df.head(2))
