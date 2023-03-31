from sqlite3 import Connection, Row

from database_connection import get_database_connection
from entities.course import Course


class CourseRepository:
    def __init__(self, connection: Connection) -> None:
        self.__connection: Connection = connection

    def create(self, course: Course) -> Course:
        cursor = self.__connection.cursor()

        cursor.execute(
            "INSERT INTO Courses (id, name, credits) VALUES (?, ?, ?)",
            (course.id, course.name, course.credits),
        )

        course.id = cursor.lastrowid

        for period in course.timing:
            cursor.execute(
                "INSERT INTO Periods (course_id, period) VALUES (?, ?)",
                (course.id, period),
            )

        for requirement_id in course.requirements:
            cursor.execute(
                "INSERT INTO Requirements (course_id, requirement_id) VALUES (?, ?)",
                (course.id, requirement_id),
            )

        self.__connection.commit()

        return course

    def delete(self, id: int) -> None:
        """Poistaa id:tä vastaavan kurssin.

        Args:
            id (int): Kurssin id.
        """
        cursor = self.__connection.cursor()

        cursor.execute("DELETE FROM Courses WHERE id=?", (id,))
        cursor.execute("DELETE FROM Periods WHERE course_id=?", (id,))
        cursor.execute(
            "DELETE FROM Requirements WHERE course_id=? or requirement_id=?", (id,)
        )

        self.__connection.commit()

    def __find_requirements(self, id: int) -> set[int]:
        cursor = self.__connection.cursor()

        requirements = cursor.execute(
            "SELECT requirement_id FROM Requirements WHERE course_id=?", (id,)
        ).fetchall()

        return {row["requirement_id"] for row in requirements}

    def __find_timing(self, id: int) -> set[int]:
        cursor = self.__connection.cursor()

        timing = cursor.execute(
            "SELECT period FROM Periods WHERE course_id=?", (id,)
        ).fetchall()

        return {row["period"] for row in timing}

    def get_course_by_row(self, row: Row) -> Course | None:
        if row is None:
            return None

        return Course(row["name"], row["credits"])


course_repository = CourseRepository(get_database_connection())
