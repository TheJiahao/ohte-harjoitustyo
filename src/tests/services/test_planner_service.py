import os
import unittest

from services.planner_service import *
from services.scheduler_service import *


class FakeCourseRepository:
    def __init__(self) -> None:
        self.__courses: dict[int, Course] = {}
        self.__next_id: int = 1

    def create(self, course: Course) -> Course:
        if course.id == -1:
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
        self.course_ohja = Course("OhJa", 5, {2})
        self.planner_service = PlannerService(
            course_repository=FakeCourseRepository(),
            scheduler_service=SchedulerService([]),
        )

        self.planner_service.delete_all_courses()

        dirname = os.path.dirname(__file__)

        self.data_directory = os.path.join(dirname, "..", "data")

    def validate_schedule(self, schedule: list[list[Course]]) -> bool:
        seen = set()

        for period in schedule:
            seen = seen.union(map(lambda x: x.id, period))

            for course in period:
                if not course.requirements.issubset(seen):
                    return False

                seen.add(course.id)

        return True

    def test_setting_negative_starting_year_raises_error(self):
        with self.assertRaises(ValueError):
            self.planner_service.starting_year = -1

    def test_setting_negative_starting_period_raises_error(self):
        with self.assertRaises(ValueError):
            self.planner_service.starting_period = -1

    def test_setting_period_greater_than_periods_per_year_raises_error(self):
        with self.assertRaises(ValueError):
            self.planner_service.starting_period = 100

        with self.assertRaises(ValueError):
            self.planner_service.starting_period = 5

    def test_create_course_with_non_existing_course(self):
        self.planner_service.create_course(self.course_ohpe)
        self.assertEqual(self.planner_service.get_course(1), self.course_ohpe)

    def test_create_course_with_existing_course_updates_course(self):
        course_ohpe_edited = Course("OhPe", 5, {1, 2}, course_id=1)

        self.planner_service.create_course(self.course_ohpe)
        self.planner_service.create_course(course_ohpe_edited)

        self.assertEqual(self.planner_service.get_course(1), course_ohpe_edited)

    def test_create_course_raises_error_when_courses_have_invalid_timing(self):
        course_ohpe = Course("Ohpe", 5)
        course_ohja = Course("Ohja", 5, {5}, {1})
        course_jym = Course("Jym", 5, {-100})
        course_ohte = Course("Jym", 5, {-10, 20})

        with self.assertRaises(TimingError):
            self.planner_service.create_course(course_ohpe)

        with self.assertRaises(TimingError):
            self.planner_service.create_course(course_ohja)

        with self.assertRaises(TimingError):
            self.planner_service.create_course(course_jym)

        with self.assertRaises(TimingError):
            self.planner_service.create_course(course_ohte)

    def test_create_course_raises_error_with_empty_name(self):
        with self.assertRaises(ValueError):
            self.planner_service.create_course(Course("", 5))

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
            [self.course_ohpe, self.course_ohja],
        )

    def test_delete_course(self):
        self.planner_service.create_course(self.course_ohpe)
        self.planner_service.delete_course(1)

        self.assertEqual(self.planner_service.get_course(1), None)

    def test_delete_all_courses(self):
        self.planner_service.create_course(self.course_ohpe)
        self.planner_service.create_course(Course("Test1", 5, {1}))
        self.planner_service.create_course(Course("Test2", 100, {2}))

        self.planner_service.delete_all_courses()

        self.assertEqual(self.planner_service.get_all_courses(), [])

    def test_get_schedule(self):
        course_ohpe = Course("Ohpe", 5, {1, 3}, course_id=1)
        course_ohja = Course("Ohja", 5, {2, 4}, {1}, course_id=2)
        course_jym = Course("Jym", 5, {1}, course_id=3)
        course_tito = Course("Tito", 5, {2, 3}, {1}, course_id=4)
        course_tira = Course("Tira", 10, {3}, {3, 4}, course_id=5)
        course_tilpe = Course("Tilpe", 5, {4}, {4, 5}, course_id=6)

        self.planner_service.create_course(course_ohpe)
        self.planner_service.create_course(course_ohja)
        self.planner_service.create_course(course_jym)
        self.planner_service.create_course(course_tito)
        self.planner_service.create_course(course_tira)
        self.planner_service.create_course(course_tilpe)

        self.planner_service.initialize(0, 1, 15)
        schedule = self.planner_service.get_schedule()

        self.assertTrue(self.validate_schedule(schedule))

    def test_initialize(self):
        scheduler = SchedulerService([])
        planner = PlannerService(scheduler, FakeCourseRepository())

        planner.initialize(2000, 3, 100)

        self.assertEqual(planner.starting_year, 2000)
        self.assertEqual(planner.starting_period, 3)
        self.assertEqual(scheduler.max_credits, 100)

    def test_import_courses(self):
        file = os.path.join(self.data_directory, "sample.json")

        self.planner_service.import_courses(file)

        courses = self.planner_service.get_all_courses()

        self.assertEqual(courses[0], Course("A", 5, {2}, course_id=1))
        self.assertEqual(courses[1], Course("B", 5, {1, 4}, {1}, course_id=2))
        self.assertEqual(courses[2], Course("C", 10, {3}, {1}, course_id=3))

    def test_import_courses_will_delete_existing_courses(self):
        file = os.path.join(self.data_directory, "sample.json")
        a = Course("a", 5, {2}, course_id=10)

        self.planner_service.create_course(a)

        self.planner_service.import_courses(file)

        self.assertNotIn(a, self.planner_service.get_all_courses())

    def test_export_courses(self):
        file = os.path.join(self.data_directory, "test_output.json")

        self.planner_service.create_course(self.course_ohpe)
        self.planner_service.create_course(self.course_ohja)

        self.planner_service.export_courses(file)
        self.planner_service.import_courses(file)

        courses = self.planner_service.get_all_courses()

        self.assertIn(self.course_ohpe, courses)
        self.assertIn(self.course_ohja, courses)

    def test_import_courses_and_get_schedule(self):
        file = os.path.join(self.data_directory, "sample_realistic.json")

        self.planner_service.import_courses(file)
        self.planner_service.initialize(2023, 1, 15)
        schedule = self.planner_service.get_schedule()

        self.assertTrue(self.validate_schedule(schedule))
