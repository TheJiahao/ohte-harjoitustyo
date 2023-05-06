import json

from entities.course import Course


class FileManagerService:
    def read(self, path: str) -> list[Course]:
        data = ""

        with open(path, mode="r", encoding="utf-8") as file:
            data = json.load(file)

        courses = [self.__convert_to_course(course_dict) for course_dict in data]

        return sorted(courses, key=lambda x: x.id)

    def write(self, courses: list[Course], path: str) -> None:
        with open(path, mode="w", encoding="utf-8") as file:
            json.dump(
                sorted(courses, key=lambda x: x.id),
                file,
                default=self.__convert_course_to_dict,
                indent=4,
            )

    def __convert_to_course(self, course_dict: dict) -> Course:
        course_id = course_dict["id"]
        name = course_dict["name"]
        course_credits = course_dict["credits"]
        timing = set(course_dict["timing"])
        requirements = set(course_dict["requirements"])

        return Course(name, course_credits, timing, requirements, course_id)

    def __convert_course_to_dict(self, course: Course) -> dict:
        result = {
            "id": course.id,
            "name": course.name,
            "credits": course.credits,
            "timing": sorted(course.timing),
            "requirements": sorted(course.requirements),
        }

        return result


file_manager_service = FileManagerService()
