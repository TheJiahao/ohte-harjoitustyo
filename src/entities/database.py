from sqlite3 import Connection, Cursor, Row, connect

from config import DATABASE_FILE_PATH


class Database:
    """Luokka, joka vastaa tietokantayhteydestä."""

    def __init__(self) -> None:
        self.connection: Connection = connect(DATABASE_FILE_PATH)
        self.connection.row_factory = Row

        self.cursor: Cursor = self.connection.cursor()

    def create_tables(self) -> None:
        """Luo tietokantaan taulut."""

        self.cursor.execute(
            """
            CREATE TABLE Courses (
                id INTEGER PRIMARY KEY,
                name TEXT,
                credits INTEGER
            )
            """
        )

        self.cursor.execute(
            """
            CREATE TABLE Requirements (
                course_id INTEGER REFERENCES Courses,
                requirement_id INTEGER REFERENCES Courses,
                UNIQUE(course_id, requirement_id)
            )
            """
        )

        self.cursor.execute(
            """
            CREATE TABLE Periods (
                course_id INTEGER REFERENCES Courses,
                period INTEGER,
                UNIQUE(course_id, period)
            )
            """
        )

        self.connection.commit()

    def drop_tables(self) -> None:
        """Tyhjentää tietokannan."""

        self.cursor.execute("DROP TABLE IF EXISTS Requirements")
        self.cursor.execute("DROP TABLE IF EXISTS Courses")
        self.cursor.execute("DROP TABLE IF EXISTS Periods")

        self.connection.commit()

    def initialize(self):
        """Alustaa tietokannan."""

        self.drop_tables()
        self.create_tables()
