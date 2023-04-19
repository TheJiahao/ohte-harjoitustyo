import unittest

from entities.course import Course
from services.planner_service import PlannerService


class FakeCourseRepository:
    def __init__(self) -> None:
        self.__courses: dict[int, Course] = {}
        self.__next_id: int = 1

    def create(self, course: Course) -> Course:
        if course.id == -1:
            course.id = self.__next_id
            self.__next_id += 1

        else:
            if course.id in self.__courses:
                self.delete(course.id)

            self.__next_id = max(course.id + 1, self.__next_id)

        self.__courses[course.id] = course

        return course

    def delete(self, course_id: int) -> None:
        self.__courses.pop(course_id, None)

    def delete_all(self) -> None:
        self.__courses.clear()

    def find_by_id(self, course_id: int) -> Course | None:
        return self.__courses.get(course_id, None)

    def find_all(self) -> list[Course]:
        return list(self.__courses.values())


class TestPlannerService(unittest.TestCase):
    def setUp(self) -> None:
        self.course_ohpe = Course("OhPe", 5, {1, 2, 3, 4}, course_id=1)
        self.course_ohja = Course("OhJa", 5)
        self.planner_service = PlannerService(FakeCourseRepository())

        self.planner_service.delete_all_courses()

    def test_create_course_with_non_existing_course(self):
        self.planner_service.create_course(self.course_ohpe)
        self.assertEqual(self.planner_service.get_course(1), self.course_ohpe)

    def test_create_course_with_existing_course_updates_course(self):
        course_ohpe_edited = Course("OhPe", 5, {1, 2}, course_id=1)

        self.planner_service.create_course(self.course_ohpe)
        self.planner_service.create_course(course_ohpe_edited)

        self.assertEqual(self.planner_service.get_course(1), course_ohpe_edited)

    def test_get_course_returns_course_with_existing_course(self):
        self.planner_service.create_course(self.course_ohja)

        self.assertEqual(
            self.planner_service.get_course(self.course_ohja.id), self.course_ohja
        )

    def test_get_course_returns_none_with_non_existing_course(self):
        self.assertEqual(self.planner_service.get_course(100), None)

    def test_get_all_courses_returns_empty_list_if_no_courses(self):
        self.assertEqual(self.planner_service.get_all_courses(), [])

    def test_get_all_courses(self):
        self.planner_service.create_course(self.course_ohpe)
        self.planner_service.create_course(self.course_ohja)

        self.assertEqual(
            self.planner_service.get_all_courses(),
            [str(self.course_ohpe), str(self.course_ohja)],
        )

    def test_delete_course(self):
        self.planner_service.create_course(self.course_ohpe)
        self.planner_service.delete_course(1)

        self.assertEqual(self.planner_service.get_course(1), None)

    def test_delete_all_courses(self):
        self.planner_service.create_course(self.course_ohpe)
        self.planner_service.create_course(Course("Test1", 5))
        self.planner_service.create_course(Course("Test2", 100))

        self.planner_service.delete_all_courses()

        self.assertEqual(self.planner_service.get_all_courses(), [])
