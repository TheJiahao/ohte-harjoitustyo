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

        rows = self.cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type="table"
            """
        ).fetchall()

        tables = set([row["name"] for row in rows])

        self.assertEqual(tables, {"Courses", "Requirements", "Periods"})

    def test_drop_tables(self):
        self.cursor.execute("CREATE TABLE Courses (test TEXT PRIMARY KEY)")

        drop_tables(self.connection)

        rows = self.cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type="table"
            """
        ).fetchall()

        self.assertEqual(rows, [])

    def test_initialize_database(self):
        initialize_database()

        rows = self.cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type="table"
            """
        ).fetchall()

        tables = set([row["name"] for row in rows])

        self.assertEqual(tables, {"Courses", "Requirements", "Periods"})
