import unittest
from unittest.mock import Mock
from bogan.lib.data_queries import Query


class TestQuery(unittest.TestCase):
    def setUp(self):
        self.mock_engine = Mock()
        self.query = Query(engine=self.mock_engine)

    def test_partien_spieler(self):
        # Mocke die Session und die Query
        pass

if __name__ == '__main__':
    unittest.main()
