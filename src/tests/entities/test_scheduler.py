import unittest

from entities.course import Course
from entities.scheduler import *


class TestScheduler(unittest.TestCase):
    def test_get_schedule_raises_error_with_cycle_in_graph(self):
        courses = []

        courses.append(Course("a", 5, {1}, {2}, 1))
        courses.append(Course("b", 5, {2}, {3}, 2))
        courses.append(Course("c", 5, {3}, {1}, 3))
        courses.append(Course("d", 5, {4}, {1}, 4))

        scheduler = Scheduler(courses)

        with self.assertRaises(CycleError):
            scheduler.get_schedule()

    def test_get_schedule_delays_course_when_credits_exceed(self):
        a = Course("Ohpe", 5, {1, 3}, course_id=1)
        b = Course("Ohja", 5, {1, 2}, {1}, course_id=2)

        courses = [a, b]

        scheduler = Scheduler(courses, 1, 4, 5)
        schedule = scheduler.get_schedule()

        self.assertEqual(schedule, [[a], [b]])

    def test_get_schedule_can_delay_course_multiple_times(self):
        a = Course("Ohpe", 5, {1, 3}, course_id=1)
        b = Course("Ohja", 5, {1, 2}, {1}, course_id=2)
        c = Course("Ohte", 5, {1, 2, 3}, {2}, course_id=3)

        courses = [a, b, c]
        scheduler = Scheduler(courses, 1, 4, 5)

        schedule = scheduler.get_schedule()

        self.assertEqual(schedule, [[a], [b], [c]])
