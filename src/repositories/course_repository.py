from sqlite3 import Connection, Row

from database_connection import get_database_connection
from entities.course import Course


class CourseRepository:
    def __init__(self, connection: Connection) -> None:
        self.__connection: Connection = connection

    def create(self, course: Course) -> Course:
        cursor = self.__connection.cursor()

        if course.id == -1:
            cursor.execute(
                "INSERT INTO Courses (name, credits) VALUES (?, ?)",
                (course.name, course.credits),
            )

            course.id = cursor.lastrowid
        else:
            if self.find_by_id(course.id) is not None:
                self.delete(course.id)

            cursor.execute(
                "INSERT INTO Courses (id, name, credits) VALUES (?, ?, ?)",
                (course.id, course.name, course.credits),
            )

        self.__connection.commit()

        self.__write_timing(course)
        self.__write_requirements(course)

        return course

    def __write_timing(self, course: Course) -> None:
        cursor = self.__connection.cursor()

        for period in course.timing:
            cursor.execute(
                "INSERT INTO Periods (course_id, period) VALUES (?, ?)",
                (course.id, period),
            )

        self.__connection.commit()

    def __write_requirements(self, course: Course) -> None:
        cursor = self.__connection.cursor()

        for requirement_id in course.requirements:
            cursor.execute(
                "INSERT INTO Requirements (course_id, requirement_id) VALUES (?, ?)",
                (course.id, requirement_id),
            )

        self.__connection.commit()

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

    def delete_all(self) -> None:
        """Poistaa kaikkien kurssien tiedot.
        """
        cursor = self.__connection.cursor()

        cursor.execute("DELETE FROM Courses")
        cursor.execute("DELETE FROM Periods")
        cursor.execute("DELETE FROM Requirements")

        self.__connection.commit()

    def find_by_id(self, id: int) -> Course:
        cursor = self.__connection.cursor()

        course_data = cursor.execute(
            "SELECT * FROM Courses WHERE id=?", (id,)
        ).fetchone()

        requirements = self.__find_requirements(id)
        timing = self.__find_timing(id)

        return Course(
            course_data["name"], course_data["credits"], timing, requirements, id
        )

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


course_repository = CourseRepository(get_database_connection())
