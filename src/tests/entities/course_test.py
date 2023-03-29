from entities.course import Course
import unittest


class TestCourse(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_course_without_requirements_initialized_correctly(self):
        course = Course("Ohte", 5, {3})

        self.assertEqual(course.name, "Ohte")
        self.assertEqual(course.credits, 5)
        self.assertEqual(course.timing, {3})
        self.assertEqual(len(course.requirements), 0)
        self.assertNotEqual(course.id, None)

    def test_course_without_timing_initialized_correctly(self):
        course = Course("Ohte", 5, requirements={"A", "B"})

        self.assertEqual(course.name, "Ohte")
        self.assertEqual(course.credits, 5)
        self.assertEqual(len(course.timing), 0)
        self.assertEqual(course.requirements, {"A", "B"})
        self.assertNotEqual(course.id, None)
