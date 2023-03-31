import unittest

from entities.course import Course


class TestCourse(unittest.TestCase):
    def setUp(self) -> None:
        self.course = Course("Ohte", 5)

    def test_course_without_optional_args_initialized_correctly(self):
        course = Course("Ohte", 5)

        self.assertEqual(course.name, "Ohte")
        self.assertEqual(course.credits, 5)
        self.assertEqual(course.timing, set())
        self.assertEqual(course.requirements, set())
        self.assertNotEqual(course.id, None)

    def test_course_with_optional_args_initialized_correctly(self):
        course = Course("Ohte", 5, {1, 3}, {2, 3}, 100)

        self.assertEqual(course.name, "Ohte")
        self.assertEqual(course.credits, 5)
        self.assertEqual(course.timing, {1, 3})
        self.assertEqual(course.requirements, {2, 3})
        self.assertEqual(course.id, 100)

    def test_timing_cannot_be_modified_with_getter(self):
        self.course.timing.add(100)
        self.course.timing.add(40)

        self.assertEqual(self.course.timing, set())

    def test_requirements_cannot_be_modified_with_getter(self):
        self.course.requirements.add(100)
        self.course.requirements.add(0)
        self.course.requirements.add(-100)

        self.assertEqual(self.course.requirements, set())

    def test_add_period_raises_error_if_nonpositive_period(self):
        with self.assertRaises(ValueError):
            self.course.add_period(-100)

        with self.assertRaises(ValueError):
            self.course.add_period(0)

    def test_add_period(self):
        self.course.add_period(1)
        self.course.add_period(4)

        self.assertEqual(self.course.timing, {1, 4})

    def test_remove_period(self):
        self.course.add_period(1)
        self.course.add_period(4)

        self.course.remove_period(4)

        self.assertEqual(self.course.timing, {1})

    def test_remove_period_does_nothing_if_period_not_in_timing(self):
        self.course.add_period(1)
        self.course.add_period(4)

        self.course.remove_period(2)
        self.course.remove_period(-100)
        self.course.remove_period(0)

        self.assertEqual(self.course.timing, {1, 4})

    def test_add_requirement(self):
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

    def test_id_setter(self):
        self.course.id = 100

        self.assertEqual(self.course.id, 100)

    def test_id_setter_raises_error_if_nonpositive_credit(self):
        with self.assertRaises(ValueError):
            self.course.id = -100

        with self.assertRaises(ValueError):
            self.course.id = 0

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

    def test_comparing_courses_work_correctly(self):
        course_ohte = Course("Ohte", 5, course_id=200)
        course_ohte2 = Course("Ohte", 5, course_id=200)
        course_ohpe = Course("OhPe", 5, course_id=100)

        self.assertEqual(course_ohte, course_ohte)
        self.assertEqual(course_ohte, course_ohte2)
        self.assertNotEqual(course_ohpe, course_ohte)
