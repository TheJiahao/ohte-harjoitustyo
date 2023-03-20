from entities.course import Course


class CourseRepository:
    def __init__(self) -> None:
        pass

    def create(
        self, name: str, credits: int, timing: set, requirements: set
    ) -> Course:
        course = Course(name, credits, timing, requirements)
        
        return course
