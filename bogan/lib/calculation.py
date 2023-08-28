import pandas as pd

from sqlalchemy.orm import Session
from bogan.db.models import Base, Benutzer, Brettspiel, Ort, Partie, SpielerPos
from bogan.config import get_logger, get_play_engine

engine = get_play_engine()
log = get_logger(__file__)


class PandaDf:
    def __init__(self, query=None) -> None:
        self.query = query

    def create_spieler_pos_query(self, ort=None, brettspiel=None):
        with Session(engine) as session:
            query = session.query(SpielerPos).join(Partie)

            # if ort is set
            if ort:
                query = query.join(Ort).where(Ort.name == ort)
            if brettspiel:
                query = query.join(Brettspiel).where(Brettspiel.name == brettspiel)
        
        return query
    
    def spieler_pos_query(self):
        with Session(engine) as session:
            # q2 = session.query(Brettspiel).join(Brettspiel).all()
            # for i in q2:
            #     print(i)
            #     break
            return session.query(SpielerPos).join(Partie)
        
    def brettspiel_query(self):
        with Session(engine) as session:
            return session.query(Brettspiel)
    
    def partie_query(self):
        with Session(engine) as session:
            return session.query(Partie)
        
    # Filter functions
    def filter_spieler_pos(self, ort=None, brettspiel=None):
        query = self.spieler_pos_query()

        if ort:
            query = query.join(Ort).where(Ort.name == ort)
        if brettspiel:
            query = query.join(Brettspiel).where(Brettspiel.name == brettspiel)
        
        return query


    def create_df(self):
        query = self.filter_spieler_pos(ort="Mittwochsrunde", brettspiel="Deal with the Devil")

        pd_list = []
        for row in query:
            tmp_dict = {}
            tmp_dict["name"] = row.benutzer.name
            tmp_dict["punktzahl"] = row.punktzahl
            tmp_dict["datum"] = row.partie.datum
            tmp_dict["brettspiel"] = row.partie.brettspiel.name

            pd_list.append(tmp_dict)
        
        df = pd.DataFrame(pd_list)
        return df




def all_games():
    with Session(engine) as session:
        query = session.query(Partie).join(Ort).join(Brettspiel).where(Ort.id == 1)

    return query

def convert2pandas(query: Session.query, **kwargs):
    pd_list = []
    for row in query:
        tmpdict = {}
        for key, value in kwargs.items():
            tmpdict[key] = getattr(row, value)
        pd_list.append(tmpdict)

    print(pd_list)
    # df = pd.DataFramereturn(pd_list)
    # print(df)


if __name__ == "__main__":
    pdf = PandaDf()
    df = pdf.create_df()
    
    print(f"Anzahl an Datensätze: {df.count()}")
    print(df)
    #print(df.index.values)
