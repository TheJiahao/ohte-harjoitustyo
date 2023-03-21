import unittest
from entities.course import Course


class TestCourse(unittest.TestCase):
    def test_constructor_without_requirements(self):
        course = Course("Ohjelmistotekniikka", 5, {4})

        self.assertEqual(course.name, "Ohjelmistotekniikka")
        self.assertEqual(course.credits, 5)
        self.assertEqual(course.timing, {4})

    def test_constructor_with_requirements(self):
        course = Course("Ohjelmistotekniikka", 5, {4})

        self.assertEqual(course.name, "Ohjelmistotekniikka")
        self.assertEqual(course.credits, 5)
        self.assertEqual(course.timing, {4})
