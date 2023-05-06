import os
import unittest

from entities.course import Course
from services.file_manager_service import file_manager_service


class TestFileManagerService(unittest.TestCase):
    def setUp(self):
        dirname = os.path.dirname(__file__)

        self.data_directory = os.path.join(dirname, "..", "data")

    def test_read(self):
        file = os.path.join(self.data_directory, "sample.json")

        courses = file_manager_service.read(file)

        self.assertEqual(len(courses), 3)
        self.assertEqual(courses[0], Course("A", 5, {2}, course_id=1))
        self.assertEqual(courses[1], Course("B", 5, {1, 4}, {1}, course_id=2))
        self.assertEqual(courses[2], Course("C", 10, {3}, {1}, course_id=3))
