from entities.course import Course
from database_connection import get_database_connection

class CourseRepository:
    def __init__(self, connection) -> None:
        self.__connection = connection

    def create(
        self, name: str, credits: int, timing: set, requirements: set
    ) -> Course:
        course = Course(name, credits, timing, requirements)
        
        return course
