import unittest

from entities import database


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.connection = database.connection
        self.cursor = database.cursor

        database.drop_tables()

    def test_create_tables(self):
        database.create_tables()

        rows = self.cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type="table"
            """
        ).fetchall()

        tables = {row["name"] for row in rows}

        self.assertEqual(tables, {"Courses", "Requirements", "Periods"})

    def test_drop_tables(self):
        self.cursor.execute("CREATE TABLE Courses (test TEXT PRIMARY KEY)")

        database.drop_tables()

        rows = self.cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type="table"
            """
        ).fetchall()

        self.assertEqual(rows, [])

    def test_initialize_database(self):
        database.initialize()

        rows = self.cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type="table"
            """
        ).fetchall()

        tables = {row["name"] for row in rows}

        self.assertEqual(tables, {"Courses", "Requirements", "Periods"})
