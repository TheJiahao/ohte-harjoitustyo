from sqlite3 import Connection, Cursor, Row

from entities.course import Course


def get_course_by_row(row) -> Course | None:
    if row is None:
        return None

    return Course(row["name"], row["credits"])


class CourseRepository:
    def __init__(self, connection: Connection) -> None:
        self.__connection: Connection = connection
        self.__cursor: Cursor = self.__connection.cursor()

    def create(self, course: Course) -> Course:
        self.__cursor.execute(
            "INSERT INTO Courses (id, name, credits) VALUES (?, ?, ?)",
            (course.id, course.name, course.credits),
        )

        for period in course.timing:
            self.__cursor.execute(
                "INSERT INTO Periods (course_id, period) VALUES (?, ?)",
                (course.id, period),
            )

        for requirement_id in course.requirements:
            self.__cursor.execute(
                "INSERT INTO Requirements (course_id, requirement_id) VALUES (?, ?)",
                (course.id, requirement_id),
            )

        self.__connection.commit()

        return course
