import unittest

from entities.course import Course


class TestCourse(unittest.TestCase):
    def setUp(self) -> None:
        self.course = Course("Ohte", 5)

    def test_course_without_optional_args_initialized_correctly(self):
        course = Course("Ohte", 5)

        self.assertEqual(course.name, "Ohte")
        self.assertEqual(course.credits, 5)
        self.assertEqual(course.timing, [False] * 5)
        self.assertEqual(course.requirements, set())
        self.assertNotEqual(course.id, None)

    def test_course_with_optional_args_initialized_correctly(self):
        course = Course("Ohte", 5, [True, False, True, False], {2, 3}, 100)

        self.assertEqual(course.name, "Ohte")
        self.assertEqual(course.credits, 5)
        self.assertEqual(course.timing, [True, False, True, False])
        self.assertEqual(course.requirements, {2, 3})
        self.assertEqual(course.id, 100)

    def test_credit_setter_raises_error_if_nonpositive_value(self):
        with self.assertRaises(ValueError):
            self.course.set_period(-100, True)
            self.course.set_period(-100, False)

        with self.assertRaises(ValueError):
            self.course.set_period(0, False)
            self.course.set_period(0, True)

    def test_timing_cannot_be_modified_with_getter(self):
        self.course.timing[0] = True
        self.course.timing[4] = True

        self.assertEqual(self.course.timing, [False] * 5)

    def test_requirements_cannot_be_modified_with_getter(self):
        self.course.requirements.add(100)
        self.course.requirements.add(0)
        self.course.requirements.add(-100)

        self.assertEqual(self.course.requirements, set())

    def test_set_period(self):
        self.course.set_period(1, True)
        self.course.set_period(2, True)
        self.course.set_period(4, True)

        self.assertEqual(self.course.timing[1], True)
        self.assertEqual(self.course.timing[2], True)
        self.assertEqual(self.course.timing[4], True)

    def test_set_period_raises_error_if_invalid_period(self):
        with self.assertRaises(ValueError):
            self.course.set_period(100, True)

        with self.assertRaises(ValueError):
            self.course.set_period(0, False)

        with self.assertRaises(ValueError):
            self.course.set_period(-10, True)

    def test_add_requirements(self):
        self.course.add_requirement(2)
        self.course.add_requirement(4)
        self.course.add_requirement(10)

        self.assertEqual(self.course.requirements, {2, 4, 10})

    def test_add_requirements_raises_error_if_invalid_id(self):
        with self.assertRaises(ValueError):
            self.course.add_requirement(-100)

        with self.assertRaises(ValueError):
            self.course.add_requirement(0)

    def test_remove_requirement(self):
        self.course.add_requirement(2)
        self.course.add_requirement(5)
        self.course.add_requirement(10)

        self.course.remove_requirement(5)

        self.assertEqual(self.course.requirements, {2, 10})

    def test_remove_requirements_does_nothing_if_id_not_in_requirements(self):
        self.course.add_requirement(1)
        self.course.add_requirement(2)
        self.course.add_requirement(10)

        self.course.remove_requirement(-1000)
        self.course.remove_requirement(0)
        self.course.remove_requirement(123)

        self.assertEqual(self.course.requirements, {1, 2, 10})

    def test_credits_setter(self):
        self.course.credits = 100

        self.assertEqual(self.course.credits, 100)

    def test_credits_setter_raises_error_if_nonpositive_credit(self):
        with self.assertRaises(ValueError):
            self.course.credits = -100

        with self.assertRaises(ValueError):
            self.course.credits = 0

    def test_name_setter(self):
        self.course.name = "OhJa"

        self.assertEqual(self.course.name, "OhJa")
