import unittest
# from sqlalchemy import create_engine
import random
import pandas as pd

from bogan.lib.data_queries import Query
from bogan.lib.dataframe import Dataframe
from bogan.config import get_logger
import tests.data.create_100_test_data as test_data


class TestQuery(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.engine = test_data.engine
        # cls.engine = create_engine("sqlite:///tests/data/test_spiel.db")
        cls.log = get_logger(__name__)
        cls.log.debug("======================================================")
        cls.log.debug("Test query start")

    def setUp(self):
        self.query = Query(engine=self.engine)

    def test_spieler_pos(self):
        # Testdaten
        result = self.query._spieler_pos()
        self.log.debug(f"Get Spieler_Pos query with {result.count()} entries")
        num_of_entries = 394

        self.assertEqual(num_of_entries, result.count())
        for row in result:
            # Alle Einträge haben Werte
            self.assertTrue(row.benutzer)
            self.assertTrue(row.partie_id)
            self.assertIsInstance(row.win, bool)
        


    def test_spieler_pos_filter_ort(self):
        # Input
        Orte = ["Ort1", "Ort2"]
        num_entries = [122, 132]
        for i, ort in enumerate(Orte):
            filter_ort = self.query.spieler_pos_by(ort=ort)
            # Test correct length in Ort:
            self.log.debug(f"Get Spieler_Pos query with {filter_ort.count()} entries for {ort})")
            self.assertEqual(filter_ort.count(), num_entries[i])
            # Check entries
            for row in filter_ort:
                self.assertEqual(row.partie.ort.name, ort)

    def test_spieler_pos_filter_benutzer(self):
        # Input
        Spieler = ["Spieler1", "Spieler2"]
        num_entries = [63, 63]
        for i, user in enumerate(Spieler):
            filter_benutzer = self.query.spieler_pos_by(benutzer=user)
            self.log.debug(f"Get Spieler_Pos query with {filter_benutzer.count()} entries for {user})")
            
            # Test correct length in Ort:
            self.assertEqual(filter_benutzer.count(), num_entries[i])
            # Check entries
            for row in filter_benutzer:
                self.assertEqual(row.benutzer.name, user)

    def test_spieler_pos_filter_brettspiel(self):
        # Input
        Spiel = ["Spiel1", "Spiel2"]
        num_entries = [105, 77]
        for i, game in enumerate(Spiel):
            filter_brettspiel = self.query.spieler_pos_by(brettspiel=game)
            self.log.debug(f"Get Spieler_Pos query with {filter_brettspiel.count()} entries for {game})")
            # Test correct length in Ort:
            self.assertEqual(filter_brettspiel.count(), num_entries[i])
            # Check entries
            for row in filter_brettspiel:
                self.assertEqual(row.partie.brettspiel.name, game)

    def test_spieler_pos_filter_multi(self):
        Spiel = ["Spiel1", "Spiel2", None]
        Benutzer = ["Spieler1", "Spieler3", None]
        Ort = ["Ort2", "Ort3", None]

        # Überprüfe für 5 zufällig Konfigurationen ob der Filter stimmt
        for i in range(5):
            brettspiel = random.choice(Spiel)
            user = random.choice(Benutzer)
            ort = random.choice(Ort)

            filter_query = self.query.spieler_pos_by(ort=ort, benutzer=user, brettspiel=brettspiel)
            self.log.debug(f"Get Spieler_Pos query with {filter_query.count()} entries for "\
                           f"brettspiel={brettspiel}, user={user}, ort={ort})")

            for row in filter_query:
                if ort is not None:
                    self.assertEqual(row.partie.ort.name, ort)
                if brettspiel is not None:
                    self.assertEqual(row.partie.brettspiel.name, brettspiel)
                if user is not None:
                    self.assertEqual(row.benutzer.name, user)

    def test_partien(self):
        result = self.query._partien()
        num_entries = 100

        # Check correct number of results
        self.assertEqual(result.count(), num_entries)

        # Check first entry if format is correct
        self.assertTrue(str(result[0]).__contains__("Partie"))
        self.log.info(f"First entry in Partien: {result[0]}")

    def test_partien_filter_ort(self):
        Orte = ["Ort1", "Ort2", "Ort3"]

        for ort in Orte:
            result = self.query.partien_by(ort=ort)
            self.log.info(f"Anzahl Datensätze für {ort}: {result.count()}")
            if result.count() > 0:
                self.log.info(f"First entry: {result[0]}")
            else:
                self.log.warning(f"Für {ort} wurden keine Einträge in der DB gefunden")

            # Überprüfe Liste
            for row in result:
                self.assertEqual(row.ort.name, ort)

    def test_partien_filter_brettspiel(self):
        Spiele = ["Spiel1", "Spiel2", "Spiel3"]

        for brettspiel in Spiele:
            result = self.query.partien_by(brettspiel=brettspiel)
            self.log.info(f"Anzahl Datensätze für {brettspiel}: {result.count()}")
            if result.count() > 0:
                self.log.info(f"First entry: {result[0]}")
            else:
                self.log.warning(f"Für {brettspiel} wurden keine Einträge in der DB gefunden")

            # Überprüfe Liste
            for row in result:
                self.assertEqual(row.brettspiel.name, brettspiel)

    def test_partien_filter_benutzer(self):
        Benutzer = ["Spieler1", "Spieler3"]

        for user in Benutzer:
            result = self.query.partien_by(benutzer=user)
            self.log.info(f"Anzahl Datensätze für {user}: {result.count()}")
            if result.count() > 0:
                self.log.info(f"First entry: {result[0]}")
            else:
                self.log.warning(f"Für {user} wurden keine Einträge in der DB gefunden")
            
            self.log.info(f"Anzahl gefundener Datensätze: {result.count()}")
            print(f"Anzahl gefundener Datensätze: {result.count()}")
            # Überprüfe ob Spieler bei der Partie dabei war
            for row in result:
                spieler_liste = []
                for spieler_pos in row.spieler:
                    spieler_liste.append(spieler_pos.benutzer.name)
                self.assertIn(user, spieler_liste)

    def test_partien_filter_mult(self):
        Spiel = ["Spiel1", "Spiel2", None]
        Benutzer = ["Spieler1", "Spieler3", None]
        Ort = ["Ort2", "Ort3", None]

        # Überprüfe für 5 zufällig Konfigurationen ob der Filter stimmt
        for i in range(5):
            brettspiel = random.choice(Spiel)
            user = random.choice(Benutzer)
            ort = random.choice(Ort)

            filter_query = self.query.partien_by(ort=ort, benutzer=user, brettspiel=brettspiel)
            self.log.debug(f"Get Spieler_Pos query with {filter_query.count()} entries for "\
                           f"brettspiel={brettspiel}, user={user}, ort={ort})")

            for row in filter_query:
                if ort is not None:
                    self.assertEqual(row.ort.name, ort)
                if brettspiel is not None:
                    self.assertEqual(row.brettspiel.name, brettspiel)
                if user is not None:
                    # Überprüfe ob Spieler in Partie
                    spieler_liste = []
                    for spieler_pos in row.spieler:
                        spieler_liste.append(spieler_pos.benutzer.name)
                    self.assertIn(user, spieler_liste)


    def tearDown(self) -> None:
        return super().tearDown()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.log.debug(" Test query end")
        cls.log.debug("======================================================")

class TestDataframe(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.engine = test_data.engine
        cls.log = get_logger(__name__)
    
    def setUp(self):
        # Erstellen eines Dummy-Dataframes für Tests
        query_spieler_pos = Query(engine=self.engine).spieler_pos_by()
        self.test_query = Dataframe(query_spieler_pos)
    
    def test_add_position(self):
        df = self.test_query
        df.add_position()
        # Überprüfen, ob die Spalte "position" im DataFrame vorhanden ist
        self.assertIn("position", df.df.columns)
    
    def test_add_num_players(self):
        df = self.test_query
        df.add_num_players()
        # Überprüfen, ob die Spalte "num_players" im DataFrame vorhanden ist
        self.assertIn("num_players", df.df.columns)
    
    def test_add_rankpoints(self):
        df = self.test_query
        df.add_rankpoints()
        # Überprüfen, ob die Spalten "rankpoints" und "rankpoints_complex" im DataFrame vorhanden sind
        self.assertIn("rankpoints", df.df.columns)
        self.assertIn("rankpoints_complex", df.df.columns)
    
    def test_add_rankppoints_sum(self):
        df = self.test_query
        df.add_rankppoints_sum()
        # Überprüfen, ob die Spalten "sum_rankpoints" und "sum_rankpoints_complex" im DataFrame vorhanden sind
        self.assertIn("sum_rankpoints", df.df.columns)
        self.assertIn("sum_rankpoints_complex", df.df.columns)
    
    def test_strip_cols_to(self):
        df = self.test_query
        columns = ["partie_id", "spieler"]
        df.strip_cols_to(columns)
        # Überprüfen, ob nur die angegebenen Spalten im DataFrame vorhanden sind
        self.assertEqual(list(df.df.columns), columns)


if __name__ == "__main__":
    unittest.main()
