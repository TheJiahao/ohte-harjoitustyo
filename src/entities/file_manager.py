import json

from entities.course import Course


class FileManager:
    def read(self, path: str) -> list[Course]:
        with open(path, encoding="utf-8") as file:
            file_content = file.read()

        data = json.loads(file_content)

        return [self.__convert_to_course(course_dict) for course_dict in data]

    def __convert_to_course(self, course_dict: dict) -> Course:
        course_id = course_dict["id"]
        name = course_dict["name"]
        course_credits = course_dict["credits"]
        timing = set(course_dict["timing"])
        requirements = set(course_dict["requirements"])

        return Course(name, course_credits, timing, requirements, course_id)

    def write(self, path: str, courses: list[Course]) -> None:
        pass
