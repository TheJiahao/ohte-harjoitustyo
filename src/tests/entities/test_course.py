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

    def test_negative_credits_raises_error(self):
        with self.assertRaises(ValueError):
            Course("Test", -1)

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

    def test_setting_negative_id_raises_error(self):
        course = Course("A", 3, course_id=1)

        with self.assertRaises(ValueError):
            course.id = -10
