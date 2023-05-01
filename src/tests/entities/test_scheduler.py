import unittest

from entities.course import Course
from entities.scheduler import *
from copy import deepcopy


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

        self.assertEqual(schedule[0], [a])
        self.assertEqual(schedule[1], [b])
        self.assertEqual(schedule[2], [c])

    def test_get_schedule_course_placed_in_first_available_period(self):
        a = Course("a", 1, {2}, course_id=1)
        b = Course("b", 1, {1}, {1}, course_id=2)
        c = Course("c", 1, {3}, course_id=3)

        courses = [a, b, c]
        scheduler = Scheduler(courses)

        schedule = scheduler.get_schedule()

        self.assertEqual(schedule[1], [a])
        self.assertEqual(schedule[2], [c])
        self.assertEqual(schedule[4], [b])

    def test_check_cycle_raises_error_with_cyclic_graph(self):
        graph1 = {1: [1]}
        graph2 = {1: [2], 2: [3], 3: [1]}
        graph3 = {
            1: [2, 4],
            2: [3, 5],
            3: [],
            4: [],
            5: [1, 3, 6],
        }

        scheduler = Scheduler([])

        with self.assertRaises(CycleError):
            scheduler._Scheduler__check_cycle(graph1)

        with self.assertRaises(CycleError):
            scheduler._Scheduler__check_cycle(graph2)

        with self.assertRaises(CycleError):
            scheduler._Scheduler__check_cycle(graph3)

    def test_check_cycle_does_not_raise_error_with_acyclic_graph(self):
        graph1 = {1: [2], 2: [3], 3: []}
        graph2 = {1: [2, 3], 2: [4], 3: [4], 4: []}
        graph3 = {1: [3], 2: [3], 3: []}

        scheduler = Scheduler([])

        scheduler._Scheduler__check_cycle(graph1)
        scheduler._Scheduler__check_cycle(graph2)
        scheduler._Scheduler__check_cycle(graph3)

    def test_non_existent_requirements_are_ignored(self):
        course1 = Course("Test", 10, {1, 2}, {20, 99}, course_id=1)
        course2 = Course("Test", 10, {1}, {1, 3}, course_id=2)

        scheduler = Scheduler([course1])

        self.assertNotIn(20, scheduler._Scheduler__get_graph().keys())
        self.assertNotIn(99, scheduler._Scheduler__get_graph().keys())
        self.assertNotIn(3, scheduler._Scheduler__get_graph().keys())
