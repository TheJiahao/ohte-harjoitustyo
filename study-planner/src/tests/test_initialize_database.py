import unittest
from initialize_database import *
from database_connection import get_database_connection

class TestInitializeDatabase(unittest.TestCase):
    def setUp(self):
        self.connection = get_database_connection()
        self.cursor = self.connection.cursor()

        drop_tables(self.connection)

    def test_create_tables(self):
        create_tables(self.connection)

    def test_drop_tables(self):
        pass

    def test_initialize_database(self):
        pass
