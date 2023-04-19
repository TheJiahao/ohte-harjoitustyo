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

    def test_courses_with_same_attributes_are_same(self):
        course_ohte = Course("Ohte", 5, {2, 4, 5}, {1, 4}, 200)
        course_ohte2 = Course("Ohte", 5, {2, 4, 5}, {1, 4}, 200)

        self.assertEqual(course_ohte, course_ohte)
        self.assertEqual(course_ohte, course_ohte2)

    def test_courses_with_different_id_are_different(self):
        course = Course("Ohte", 5, {2, 4, 5}, {1, 4}, 200)
        course_with_different_id = Course("Ohte", 1, {2, 4, 5}, {1, 4}, 1)

        self.assertNotEqual(course, course_with_different_id)

    def test_courses_with_different_name_are_different(self):
        course = Course("Ohte", 5, {2, 4, 5}, {1, 4}, 200)
        course_with_different_name = Course("OhJa", 5, {2, 4, 5}, {1, 4}, 200)

        self.assertNotEqual(course, course_with_different_name)

    def courses_with_different_credits_are_different(self):
        course = Course("Ohte", 5, {2, 4, 5}, {1, 4}, 200)
        course_with_different_credits = Course("Ohte", 1, {2, 4, 5}, {1, 4}, 200)

        self.assertNotEqual(course, course_with_different_credits)

    def test_courses_with_different_timing_are_different(self):
        course = Course("Ohte", 5, {2, 4, 5}, {1, 4}, 200)
        course_with_different_timing = Course("Ohte", 1, {4, 5}, {1, 4}, 200)

        self.assertNotEqual(course, course_with_different_timing)

    def test_courses_with_different_requirements_are_different(self):
        course = Course("Ohte", 5, {2, 4, 5}, {1, 4}, 200)
        course_with_different_requirements = Course("Ohte", 1, {2, 4, 5}, {4}, 200)

        self.assertNotEqual(course, course_with_different_requirements)

    def test_courses_with_different_type_are_different(self):
        course = Course("Ohte", 5, {2, 4, 5}, {1, 4}, 200)

        self.assertNotEqual(course, 1)
        self.assertNotEqual(course, "a")
        self.assertNotEqual(course, [])

    def test_str(self):
        course1 = Course("Ohte", 5, {1, 2, 3}, {2, 4, 6, 5}, course_id=200)
        course2 = Course("OhJa", 5, {1, 2}, {2, 4}, course_id=10)

        self.assertEqual(str(course1), "200: Ohte, 5 op")
        self.assertEqual(str(course2), "10: OhJa, 5 op")

    def test_repr(self):
        course = course = Course("Ohte", 5, {1, 2, 3}, {2, 4}, course_id=200)

        self.assertIn(
            repr(course),
            [
                "Course(Ohte, 5, {1, 2, 3}, {2, 4}, 200)",
                "Course(Ohte, 5, {1, 2, 3}, {4, 2}, 200)",
            ],
        )
