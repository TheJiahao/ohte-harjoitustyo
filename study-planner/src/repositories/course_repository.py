from entities.course import Course


class CourseRepository:
    def __init__(self) -> None:
        pass

    def create_course(
        self, name: str, credits: int, timing: list[bool], requirements: set
    ) -> Course:
        course = Course(name, credits, timing, requirements)
        
        return course
