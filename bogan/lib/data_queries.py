from typing import List
from sqlalchemy.orm import Session

from bogan.config import get_logger, get_play_engine
from bogan.db.models import Benutzer, Partie, SpielerPos, Brettspiel, Ort

# Init Logger
log = get_logger(__file__)

class Query:
    def __init__(self, query=None, engine=get_play_engine()) -> None:
        self.query = query
        self.engine = engine
        
    def _spieler_pos(self) -> List[SpielerPos]:
        with Session(self.engine) as session:
            query: List[SpielerPos] = session.query(SpielerPos).join(Partie).order_by(Partie.datum)
            
        return query
    
    def spieler_pos_by(self, ort:str=None,
                           brettspiel:str=None,
                           benutzer:str=None,
                           ) -> List[SpielerPos]:
        log.debug("Create Query benutzer_partien")
        query = self._spieler_pos()
        # Filter Query wenn Parameter gesetzt sind
        if ort:
            log.debug(f"Filter Query for ort={ort}")
            query = query.join(Ort).where(Ort.name == ort)
        if brettspiel:
            log.debug(f"Filter Query for brettspiel={brettspiel}")
            query = query.join(Brettspiel).where(Brettspiel.name == brettspiel)
        if benutzer:
            log.debug(f"Filter Query for benutzer={benutzer}")
            query = query.join(Benutzer).where(Benutzer.name == benutzer)

        return query
    
    def _partien(self) -> List[Partie]:
        with Session(self.engine) as session:
            query: List[Partie] = session.query(Partie)

        return query
    
    def partien_by(self,
                   ort=None,
                   brettspiel=None,
                   benutzer=None) -> List[Partie]:
        log.debug("Create Query Partien ...")
        query = self._partien()
        # Filter Query wenn Parameter gesetzt sind
        if ort:
            log.debug(f"Filter Query for ort={ort}")
            query = query.join(Ort).where(Ort.name == ort)
        if brettspiel:
            log.debug(f"Filter Query for brettspiel={brettspiel}")
            query = query.join(Brettspiel).where(Brettspiel.name == brettspiel)
        if benutzer:
            log.debug(f"Filter Query for benutzer={benutzer}")
            query = query.join(SpielerPos).join(Benutzer).where(Benutzer.name == benutzer)

        return query




