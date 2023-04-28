import unittest

from entities.course import Course
from services.planner_service import *


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
        self.course_ohja = Course("OhJa", 5, {2})
        self.planner_service = PlannerService(course_repository=FakeCourseRepository())

        self.planner_service.delete_all_courses()

    def validate_topological_order(self, courses: list[Course]) -> bool:
        seen = set()

        for course in courses:
            if not course.requirements.issubset(seen):
                return False

            seen.add(course.id)

        return True

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

    def test_setting_negative_max_credits_raises_error(self):
        with self.assertRaises(ValueError):
            self.planner_service.max_credits = -10

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

        schedule = self.planner_service.get_schedule()

        self.assertTrue(self.validate_schedule(schedule))

    def test_get_schedule_raises_error_with_cycle_in_graph(self):
        a = Course("a", 5, {1}, {2}, 1)
        b = Course("b", 5, {2}, {3}, 2)
        c = Course("c", 5, {3}, {1}, 3)
        d = Course("d", 5, {4}, {1}, 4)

        self.planner_service.create_course(a)
        self.planner_service.create_course(b)
        self.planner_service.create_course(c)
        self.planner_service.create_course(d)

        with self.assertRaises(CycleError):
            self.planner_service.get_schedule()

    def test_get_schedule_delays_course_when_credits_exceed(self):
        a = Course("Ohpe", 5, {1, 3}, course_id=1)
        b = Course("Ohja", 5, {1, 2}, {1}, course_id=2)

        self.planner_service.create_course(a)
        self.planner_service.create_course(b)
        self.planner_service.set_parameters(2023, 1, 5)

        schedule = self.planner_service.get_schedule()

        self.assertEqual(schedule, [[a], [b]])

    def test_get_schedule_can_delay_course_multiple_times(self):
        a = Course("Ohpe", 5, {1, 3}, course_id=1)
        b = Course("Ohja", 5, {1, 2}, {1}, course_id=2)
        c = Course("Ohte", 5, {1, 2, 3}, {2}, course_id=3)

        self.planner_service.create_course(a)
        self.planner_service.create_course(b)
        self.planner_service.create_course(c)
        self.planner_service.set_parameters(2023, 1, 5)

        schedule = self.planner_service.get_schedule()

        self.assertEqual(schedule, [[a], [b], [c]])

    def test_set_parameters(self):
        self.planner_service.set_parameters(2000, 3, 15)

        self.assertEqual(self.planner_service.starting_year, 2000)
        self.assertEqual(self.planner_service.starting_period, 3)
        self.assertEqual(self.planner_service.max_credits, 15)

    def test_set_parameters_raises_error_with_too_low_limit(self):
        self.planner_service.create_course(Course("test", 5, {1}))

        with self.assertRaises(MaxCreditError):
            self.planner_service.set_parameters(2000, 2, 1)

    def test_get_graph(self):
        course_ohpe = Course("Ohpe", 5, {1, 3}, course_id=1)
        course_ohja = Course("Ohja", 5, {2, 4}, {1}, course_id=2)
        course_ohte = Course("Ohte", 5, {2, 4}, {2}, course_id=3)

        self.planner_service.create_course(course_ohpe)
        self.planner_service.create_course(course_ohja)
        self.planner_service.create_course(course_ohte)

        graph = self.planner_service.get_graph()

        self.assertEqual(graph[1], [2])
        self.assertEqual(graph[2], [3])
        self.assertEqual(graph[3], [])

    def test_get_graph_ignores_non_existent_course(self):
        course_ohpe = Course("Ohpe", 5, {1, 3}, course_id=1)
        course_ohja = Course("Ohja", 5, {2, 4}, {1, 10}, course_id=2)

        self.planner_service.create_course(course_ohpe)
        self.planner_service.create_course(course_ohja)

        graph = self.planner_service.get_graph()

        self.assertNotIn(10, graph)
