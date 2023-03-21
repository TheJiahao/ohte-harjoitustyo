from database_connection import get_database_connection


def create_tables(connection):
    """Luo tietokantaan taulut."""

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE Courses (
            id INTEGER PRIMARY KEY,
            name TEXT,
            credits INTEGER,
            UNIQUE(name)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE Requirements (
            course_id INTEGER REFERENCES Courses,
            requirement_id INTEGER REFERENCES Courses,
            UNIQUE(course_id, requirement_id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE Periods (
            course_id INTEGER REFERENCES Courses,
            period INTEGER,
            UNIQUE(course_id, period)
        )
        """
    )

    connection.commit()


def drop_tables(connection):
    """Tyhjentää tietokannan."""

    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS Courses")
    cursor.execute("DROP TABLE IF EXISTS Requirements")
    cursor.execute("DROP TABLE IF EXISTS Periods")


def initialize_database():
    """Alustaa tietokannan."""

    connection = get_database_connection()

    drop_tables(connection)
    create_tables(connection)


if __name__ == "__main__":
    initialize_database()
