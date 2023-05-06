from sqlite3 import Connection, Cursor

from entities.course import Course
from lib.database import database


class CourseRepository:
    """Kurssien tietokantaoperaatioista vastaava luokka."""

    def __init__(self) -> None:
        """Luokan konstruktori.

        Args:
            connection (Connection): Tietokantayhteys.
        """

        self.__connection: Connection = database.connection
        self.__cursor: Cursor = database.cursor

    def create(self, course: Course) -> None:
        """Tallentaa kurssin tietokantaan tai muokkaa jo olevaa.
        Voi muokata annetun kurssin id:n.

        Args:
            course (Course): Tallennettava tai muokattava kurssi.
        """

        self.__cursor = self.__connection.cursor()

        if course.id == -1:
            self.__cursor.execute(
                "INSERT INTO Courses (name, credits) VALUES (?, ?)",
                (course.name, course.credits),
            )

        else:
            if self.find_by_id(course.id):
                self.delete(course.id)

            self.__cursor.execute(
                "INSERT INTO Courses (id, name, credits) VALUES (?, ?, ?)",
                (course.id, course.name, course.credits),
            )

        self.__connection.commit()

        self.__write_timing(course)
        self.__write_requirements(course)

    def __write_timing(self, course: Course) -> None:
        """Tallentaa kurssin ajoituksen tietokantaan.

        Args:
            course (Course): Kurssi, jonka ajoitus tallennetaan.
        """

        cursor = self.__connection.cursor()

        for period in course.timing:
            cursor.execute(
                "INSERT INTO Periods (course_id, period) VALUES (?, ?)",
                (course.id, period),
            )

        self.__connection.commit()

    def __write_requirements(self, course: Course) -> None:
        """Tallentaa kurssin esitietovaatimukset tietokantaan.

        Args:
            course (Course): Kurssi, jonka esitietovaatimukset tallennetaan.
        """

        cursor = self.__connection.cursor()

        for requirement_id in course.requirements:
            cursor.execute(
                "INSERT INTO Requirements (course_id, requirement_id) VALUES (?, ?)",
                (course.id, requirement_id),
            )

        self.__connection.commit()

    def delete(self, course_id: int) -> None:
        """Poistaa id:tä vastaavan kurssin.

        Args:
            course_id (int): Kurssin id.
        """

        cursor = self.__connection.cursor()

        cursor.execute("DELETE FROM Courses WHERE id=?", (course_id,))
        cursor.execute("DELETE FROM Periods WHERE course_id=?", (course_id,))
        cursor.execute(
            "DELETE FROM Requirements WHERE course_id=:course_id or requirement_id=:course_id",
            (course_id,),
        )

        self.__connection.commit()

    def delete_all(self) -> None:
        """Poistaa kaikki kurssit tietokannasta."""

        cursor = self.__connection.cursor()

        cursor.execute("DELETE FROM Courses")
        cursor.execute("DELETE FROM Periods")
        cursor.execute("DELETE FROM Requirements")

        self.__connection.commit()

    def find_by_id(self, course_id: int) -> Course | None:
        """Palauttaa id:tä vastaavan kurssin.

        Args:
            id (int): Haettavan kurssin id.

        Returns:
            Course | None: id:tä vastaava kurssi tai None, jos ei löydy.
        """

        cursor = self.__connection.cursor()

        course_data = cursor.execute(
            "SELECT * FROM Courses WHERE id=?", (course_id,)
        ).fetchone()

        if course_data is None:
            return None

        requirements = self.find_requirements(course_id)
        timing = self.find_timing(course_id)

        return Course(
            course_data["name"], course_data["credits"], timing, requirements, course_id
        )

    def find_all(self) -> list[Course]:
        """Palauttaa kaikki kurssit.

        Returns:
            list[Course]: Lista kursseista id-järjestyksessä.
        """

        cursor = self.__connection.cursor()

        rows = cursor.execute("SELECT id FROM Courses ORDER BY id").fetchall()

        return [self.find_by_id(row["id"]) for row in rows if row is not None]  # type: ignore

    def find_requirements(self, course_id: int) -> set[int]:
        """Palauttaa kurssin esitietovaatimukset.

        Args:
            id (int): Haettavan kurssin id.

        Returns:
            set[int]: Esitietokurssien id:t joukkona.
        """

        cursor = self.__connection.cursor()

        requirements = cursor.execute(
            "SELECT requirement_id FROM Requirements WHERE course_id=?", (course_id,)
        ).fetchall()

        return {row["requirement_id"] for row in requirements}

    def find_timing(self, course_id: int) -> set[int]:
        """Palauttaa kurssin perioditarjonnan.

        Args:
            id (int): Haettavan kurssin id.

        Returns:
            set[int]: Kurssin perioditarjonta.
        """

        cursor = self.__connection.cursor()

        timing = cursor.execute(
            "SELECT period FROM Periods WHERE course_id=?", (course_id,)
        ).fetchall()

        return {row["period"] for row in timing}


course_repository = CourseRepository()
