from typing import List
from sqlalchemy.orm import Session

from bogan.config import get_logger, get_play_engine
from bogan.db.models import Benutzer, Partie, SpielerPos, Brettspiel, Ort

# Init Logger
log = get_logger(__file__)


class Query:
    def __init__(self, query=None, engine=get_play_engine(), ignore_koop=True, ignore_solo=True) -> None:
        self.query = query
        self.engine = engine
        self.ignore_koop = ignore_koop
        self.ignore_solo = ignore_solo

    def _spieler_pos(self) -> List[SpielerPos]:
        with Session(self.engine) as session:
            query: List[SpielerPos] = (
                session.query(SpielerPos).join(Partie).join(Brettspiel).join(Ort).join(Benutzer).order_by(Partie.datum)
            )
            # Koop Spiele werden ignoriert
            if self.ignore_koop:
                query = query.where(Brettspiel.koop == False)  # noqa: E712 -> sqlAlchemy need it
             # Solo Spiele werden ignoriert
            if self.ignore_solo:
                query = query.where(Ort.name!="Solospiel")

        return query

    def spieler_pos_by(
        self,
        ort: str = None,
        brettspiel: str = None,
        benutzer: str = None,
    ) -> List[SpielerPos]:
        log.debug("Create Query benutzer_partien")
        query = self._spieler_pos()
        # Filter Query wenn Parameter gesetzt sind
        if ort:
            log.debug(f"Filter Query for ort={ort}")
            query = query.where(Ort.name == ort)
        if brettspiel:
            log.debug(f"Filter Query for brettspiel={brettspiel}")
            query = query.where(Brettspiel.name == brettspiel)
        if benutzer:
            log.debug(f"Filter Query for benutzer={benutzer}")
            query = query.where(Benutzer.name == benutzer)

        return query

    def _partien(self) -> List[Partie]:
        with Session(self.engine) as session:
            # Join von models, die nicht die Anzahl der Einträge ändern -> Ein Ort möglich
            query: List[Partie] = session.query(Partie).join(Ort).join(Brettspiel)

            # Koop Spiele werden ignoriert
            if self.ignore_koop:
                query = query.where(Brettspiel.koop == False)  # noqa: E712 -> sqlAlchemy need it
            
            # Solo Spiele werden ignoriert
            if self.ignore_solo:
                query = query.where(Ort.name!="Solospiel")

        return query

    def partien_by(
        self,
        ort=None,
        brettspiel=None,
        benutzer=None,
    ) -> List[Partie]:
        log.debug("Create Query Partien ...")
        query = self._partien()
        # Filter Query wenn Parameter gesetzt sind
        if ort:
            log.debug(f"Filter Query for ort={ort}")
            query = query.where(Ort.name == ort)
        if brettspiel:
            log.debug(f"Filter Query for brettspiel={brettspiel}")
            query = query.where(Brettspiel.name == brettspiel)
        if benutzer:
            log.debug(f"Filter Query for benutzer={benutzer}")
            # Hier erst join SpielerPos, da sonst Einträge der query verändert werden
            query = query.join(SpielerPos).join(Benutzer).where(Benutzer.name == benutzer)

        return query


if __name__ == "__main__":
    q = Query().spieler_pos_by(brettspiel="The Search for Planet X")

    for row in q:
        print(row.partie)
    
    print(f"Count: {q.count()}")

    # q = Query().spieler_pos_by(brettspiel="Gaia Project")
    # # q = Query().spieler_pos_by()

    # for row in q:
    #     print(row.partie.brettspiel)
