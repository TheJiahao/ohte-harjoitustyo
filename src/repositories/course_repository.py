from database_connection import get_database_connection
from entities.course import Course


def get_course_by_row(row) -> Course | None:
    if row is None:
        return None

    return Course(row["name"], row["credits"])


class CourseRepository:
    def __init__(self, connection) -> None:
        self.__connection = connection
        self.__cursor = self.__connection.cursor()

    def find_all(self) -> list[Course]:
        courses = self.__cursor.execute("SELECT * FROM Courses").fetchall()

        pass

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
