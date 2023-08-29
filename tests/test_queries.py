import unittest
from sqlalchemy import create_engine
import random

from bogan.lib.data_queries import Query
from bogan.config import get_logger


class TestQuery(unittest.TestCase):
    # TODO Logsnachrichten überprüfen
    @classmethod
    def setUpClass(cls) -> None:
        cls.engine = create_engine("sqlite:///tests/data/test_spiel.db")
        cls.log = get_logger(__name__)
        cls.log.debug("======================================================")
        cls.log.debug("Test query start")

    def setUp(self):
        self.query = Query(engine=self.engine)
        self.log.debug(f"SETUP: Create query from {self.engine}")

    def test_spieler_pos(self):
        # Testdaten
        result = self.query.benutzer_partien()
        num_of_entries = 414

        self.log.debug(f"Found Database entries: {result.count()}")
        self.assertEqual(num_of_entries, result.count())
        for row in result:
            self.log.debug(f"Spieler_pos found: {row}")

    def test_spieler_pos_filter_ort(self):
        # Input
        Orte = ["Ort1", "Ort2"]
        num_entries = [168, 99]
        for i, ort in enumerate(Orte):
            filter_ort = self.query.benutzer_partien_by(ort=ort)

            # Test correct length in Ort:
            self.log.debug(f"Check correct length({num_entries[i]} for {ort})")
            self.assertEqual(filter_ort.count(), num_entries[i])
            # Check entries
            for row in filter_ort:
                self.log.debug(f"Test: {row} is in {ort}")
                self.assertEqual(row.partie.ort.name, ort)

    def test_spieler_pos_filter_benutzer(self):
        # Input
        Spieler = ["Spieler1", "Spieler2"]
        num_entries = [65, 68]
        for i, user in enumerate(Spieler):
            filter_benutzer = self.query.benutzer_partien_by(benutzer=user)

            # Test correct length in Ort:
            self.log.debug(f"Check correct length({num_entries[i]} for {user})")
            self.assertEqual(filter_benutzer.count(), num_entries[i])
            # Check entries
            for row in filter_benutzer:
                self.log.debug(f"Test: {row} is in {user}")
                self.assertEqual(row.benutzer.name, user)

    def test_spieler_pos_filter_brettspiel(self):
        # Input
        Spiel = ["Spiel1", "Spiel2"]
        num_entries = [117, 100]
        for i, game in enumerate(Spiel):
            filter_brettspiel = self.query.benutzer_partien_by(brettspiel=game)

            # Test correct length in Ort:
            self.log.debug(f"Check correct length({num_entries[i]} for {game})")
            self.assertEqual(filter_brettspiel.count(), num_entries[i])
            # Check entries
            for row in filter_brettspiel:
                self.log.debug(f"Test: {row} is in {game}")
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

            filter_query = self.query.benutzer_partien_by(ort=ort, benutzer=user, brettspiel=brettspiel)

            for row in filter_query:
                self.log.debug(f"Check the filter: {row}")
                if ort is not None:
                    self.assertEqual(row.partie.ort.name, ort)
                if brettspiel is not None:
                    self.assertEqual(row.partie.brettspiel.name, brettspiel)
                if user is not None:
                    self.assertEqual(row.benutzer.name, user)

    def test_partien(self):
        result = self.query.partien()
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

            for row in filter_query:
                self.log.debug(f"Check the filter: {row}")
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
        self.log.debug("Test Ende")
        return super().tearDown()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.log.debug(" Test query end")
        cls.log.debug("======================================================")


if __name__ == "__main__":
    unittest.main()
