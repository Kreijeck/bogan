import os
import pandas as pd
import plotly.express as px

from sqlalchemy.orm import Session
# from sqlalchemy import select
from bogan.config import get_logger, get_play_engine, cfg_db
from bogan.db.models import Benutzer, Partie, SpielerPos, Brettspiel, Ort
from datetime import datetime
from dateutil.relativedelta import relativedelta


# Init modules
log = get_logger(__file__)
db_file = os.path.join(cfg_db["dir"], "spiel_copy.db")
engine = get_play_engine(path=db_file)
# engine = get_play_engine()


class SqlPartie:
    def __init__(self) -> None:
        self.session: Session = Session(engine)

    def all_partien(self):
        partien = (
            self.session.query(Partie)
            .join(Ort)
            #.join(SpielerPos)
            #.join(Benutzer)
            #.join(Brettspiel)
            #.order_by(SpielerPos.position, SpielerPos.win)
        )

        self.session.close()

        return partien

    def partien_from(self, user_name):
        user_query = self.all_partien().where(Benutzer.name == user_name)
        return user_query

    def convert2pandas(self, query: all_partien) -> pd.DataFrame:
        """Jede Partei wird als ein Namen geführt, alle Spieler sind columns

        Args:
            query (all_partien): _description_

        Returns:
            pd.DataFrame: _description_
        """
        pd_list = []
        my_query = self.all_partien().where(Ort.name == "Mittwochsrunde")
        print(f"Anzahl an Datensätzen: {my_query.count()}")
        for row in my_query:
            tmp_dict = {}
            tmp_dict["id"] = row.id
            tmp_dict["datum"] = row.datum
            tmp_dict["ort"] = row.ort.name
            tmp_dict["brettspiel"] = row.brettspiel.name
            tmp_dict["complex"] = row.brettspiel.complexity
            for i, spieler in enumerate(row.spieler):
                tmp_dict[spieler.benutzer.name] = spieler.position or spieler.win
            pd_list.append(tmp_dict)

        df = pd.DataFrame(pd_list)
        print(df)
    
    def convert2pandas_all(self, query: all_partien) -> pd.DataFrame:
        """Jeder Name wird als ein Eintrag geführt, mit Position

        Args:
            query (all_partien): _description_

        Returns:
            pd.DataFrame: _description_
        """
        pd_list = []
        my_query = self.all_partien().where(Ort.name == "Mittwochsrunde").order_by(Partie.datum)
        print(f"Anzahl an Datensätzen: {my_query.count()}")
        for row in my_query:
            tmp_dict = {}
            tmp_dict["id"] = row.id
            tmp_dict["datum"] = row.datum
            # tmp_dict["ort"] = row.ort.name
            tmp_dict["brettspiel"] = row.brettspiel.name
            # tmp_dict["complex"] = row.brettspiel.complexity
            for s in row.spieler:
                inset = tmp_dict.copy()
                inset["spieler_name"] = s.benutzer.name
                inset["spieler_pos"] = s.position or (1 if s.win else 0) # or spieler.win
                pd_list.append(inset)
                inset = {}
          

        df = pd.DataFrame(pd_list)
        print(df)
        return df

def create_graph(df_graph: pd.DataFrame):
    df_graph = df_graph
    fig = px.bar(df_graph, x="datum", y="spieler_pos", color="spieler_name")
    fig.update_layout(barmode='group')
    fig.show()

def query_in_dict():
    with Session(engine) as session:
        query = session.query(Partie).all()
        for_pd = []
        i = 0
        for entry in query:
            for_pd.append(entry.to_dict())
            i += 1
            if i>3:
                break
        return for_pd
    



if __name__ == "__main__":
    # ### DIAGRAM
    # sql = SqlPartie()
    # michi = sql.partien_from("Michi")
    # df_mittwoch = sql.convert2pandas_all(michi)
    # create_graph(df_mittwoch)

    for val in query_in_dict():
        print(val)
    
    # print(michi)
    # print(michi.count())
    # for i,q in enumerate(michi):
    #     print(q.spieler)

    #     if i>=2:
    #         break

    ### Sretch for to dict
    # benutzer = Benutzer(id=1, name='Alice')
    # benutzer_dict = benutzer.to_dict()
    # print(benutzer_dict)
