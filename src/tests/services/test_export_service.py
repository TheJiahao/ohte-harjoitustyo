import os
import unittest

from entities.course import Course
from services.export_service import export_service
from services.import_service import import_service


class TestExportService(unittest.TestCase):
    def setUp(self):
        dirname = os.path.dirname(__file__)

        self.data_directory = os.path.join(dirname, "..", "data")
        self.file = os.path.join(self.data_directory, "test_output.json")

    def test_write(self):
        a = Course("A", 10, {2}, course_id=1)
        b = Course("B", 10, {2}, {1}, course_id=2)

        export_service.write([a, b], self.file)
        courses = import_service.read(self.file)

        self.assertEqual(list(courses), [a, b])

    def test_write_empty_list(self):
        export_service.write([], self.file)

        with open(self.file, mode="r", encoding="utf-8") as file:
            data = file.read()

        self.assertEqual(data, "[]")
