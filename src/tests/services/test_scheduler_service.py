import unittest

from entities.course import Course
from services.scheduler_service import *


class TestSchedulerService(unittest.TestCase):
    @classmethod
    def check_course_timing(cls, schedule: list[list[Course]]) -> bool:
        for i, period in enumerate(schedule):
            period_number = i % 4 + 1

            for course in period:
                if period_number not in course.timing:
                    return False

        return True

    @classmethod
    def check_credits_below_limit(
        cls, schedule: list[list[Course]], max_credits: int
    ) -> bool:
        for period in schedule:
            total_credits = sum(map(lambda x: x.credits, period))

            if total_credits > max_credits:
                return False

        return True

    @classmethod
    def check_topological_order(cls, schedule: list[list[Course]]) -> bool:
        seen = set()

        for period in schedule:
            seen = seen.union(map(lambda x: x.id, period))

            for course in period:
                if not course.requirements.issubset(seen):
                    return False

                seen.add(course.id)

        return True

    @classmethod
    def check_schedule(cls, schedule: list[list[Course]], max_credits: int) -> bool:
        return (
            cls.check_course_timing(schedule)
            and cls.check_credits_below_limit(schedule, max_credits)
            and cls.check_topological_order(schedule)
        )

    def setUp(self) -> None:
        self.scheduler = SchedulerService([])

    def test_max_credits(self):
        courses = [Course("A", 5, {2}, course_id=10), Course("B", 3, {2}, course_id=10)]

        scheduler = SchedulerService(courses)

        scheduler.max_credits = 3
        scheduler.max_credits = 2

    def test_negative_max_credits_raises_error(self):
        with self.assertRaises(MaxCreditError):
            self.scheduler.max_credits = -10

    def test_max_credits_lower_than_minimum_course_credits_raises_error(self):
        self.scheduler.initialize([Course("test", 5, {1})], 1, 15)
        with self.assertRaises(MaxCreditError):
            self.scheduler.max_credits = 2

    def test_get_schedule_raises_error_with_cycle_in_graph(self):
        courses = [
            Course("a", 5, {1}, {2}, 1),
            Course("b", 5, {2}, {3}, 2),
            Course("c", 5, {3}, {1}, 3),
            Course("d", 5, {4}, {1}, 4),
        ]

        self.scheduler.initialize(courses, 3, 20)

        with self.assertRaises(CycleError):
            self.scheduler.get_schedule()

    def test_get_schedule_delays_course_when_credits_exceed(self):
        a = Course("Ohpe", 5, {1, 3}, course_id=1)
        b = Course("Ohja", 5, {1, 2}, {1}, course_id=2)

        self.scheduler.initialize([a, b], 1, 5)

        self.assertEqual(self.scheduler.get_schedule(), [[a], [b]])

    def test_get_schedule_can_delay_course_multiple_times(self):
        a = Course("Ohpe", 5, {1, 3}, course_id=1)
        b = Course("Ohja", 5, {1, 2}, {1}, course_id=2)
        c = Course("Ohte", 5, {1, 2, 3}, {2}, course_id=3)

        self.scheduler.initialize([a, b, c], 1, 5)
        schedule = self.scheduler.get_schedule()

        self.assertEqual(schedule[0], [a])
        self.assertEqual(schedule[1], [b])
        self.assertEqual(schedule[2], [c])

    def test_get_schedule_course_placed_in_first_available_period(self):
        a = Course("a", 1, {2}, course_id=1)
        b = Course("b", 1, {1}, {1}, course_id=2)
        c = Course("c", 1, {3}, course_id=3)

        self.scheduler.initialize([a, b, c], 1, 15)

        schedule = self.scheduler.get_schedule()

        self.assertEqual(schedule[1], [a])
        self.assertEqual(schedule[2], [c])
        self.assertEqual(schedule[4], [b])

    def test_check(self):
        graph1 = {1: [2], 2: [3], 3: []}
        graph2 = {1: [2, 3], 2: [4], 3: [4], 4: []}
        graph3 = {1: [3], 2: [3], 3: []}

        self.scheduler._SchedulerService__check(graph1)
        self.scheduler._SchedulerService__check(graph2)
        self.scheduler._SchedulerService__check(graph3)

    def test_check_raises_error_with_cyclic_graph(self):
        graph1 = {1: [1]}
        graph2 = {1: [2], 2: [3], 3: [1]}
        graph3 = {
            1: [2, 4],
            2: [3, 5],
            3: [],
            4: [],
            5: [1, 3, 6],
        }

        with self.assertRaises(CycleError):
            self.scheduler._SchedulerService__check(graph1)

        with self.assertRaises(CycleError):
            self.scheduler._SchedulerService__check(graph2)

        with self.assertRaises(CycleError):
            self.scheduler._SchedulerService__check(graph3)

    def test_check_raises_error_with_empty_graph(self):
        with self.assertRaises(EmptyGraphError):
            self.scheduler._SchedulerService__check({})

    def test_non_existent_requirements_are_ignored(self):
        course1 = Course("Test1", 10, {1, 2}, {20, 99}, course_id=1)
        course2 = Course("Test2", 10, {1}, {1, 3}, course_id=2)

        self.scheduler.initialize([course1, course2], 1, 20)

        self.assertNotIn(20, self.scheduler._SchedulerService__get_graph().keys())
        self.assertNotIn(99, self.scheduler._SchedulerService__get_graph().keys())
        self.assertNotIn(3, self.scheduler._SchedulerService__get_graph().keys())

    def test_get_schedule_period_credits_within_limit(self):
        a = Course("A", 7, {1, 2}, course_id=1)
        b = Course("B", 4, {1, 2}, course_id=2)
        c = Course("C", 4, {1, 2}, course_id=3)
        d = Course("D", 7, {1, 2}, course_id=4)
        e = Course("E", 8, {1, 2}, course_id=5)

        self.scheduler.initialize([a, b, c, d, e], 1, 10)

        self.assertTrue(
            self.check_credits_below_limit(self.scheduler.get_schedule(), 10)
        )

    def test_get_schedule_courses_available_in_period(self):
        a = Course("A", 7, {1, 2}, course_id=1)
        b = Course("B", 4, {3, 4}, course_id=2)
        c = Course("C", 4, {4}, course_id=3)
        d = Course("D", 7, {1}, course_id=4)
        e = Course("E", 8, {2}, course_id=5)

        self.scheduler.initialize([a, b, c, d, e], 1, 10)

        self.assertTrue(self.check_course_timing(self.scheduler.get_schedule()))

    def test_get_schedule_with_realistic_case(self):
        courses = [
            Course("Ohpe", 5, {1, 3}, course_id=1),
            Course("Ohja", 5, {2, 4}, {1}, course_id=2),
            Course("Jym", 5, {1}, course_id=3),
            Course("Tito", 5, {2, 3}, {1}, course_id=4),
            Course("Tira", 10, {3}, {3, 4}, course_id=5),
            Course("Tilpe", 5, {4}, {4, 5}, course_id=6),
        ]

        self.scheduler.initialize(courses, 1, 15)
        schedule = self.scheduler.get_schedule()

        self.assertTrue(self.check_schedule(schedule, 15))
