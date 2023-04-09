import unittest

from entities.course import Course
from repositories import course_repository


class TestCourseRepository(unittest.TestCase):
    def setUp(self):
        course_repository.delete_all()
        self.course_ohja = Course("OhJa", 5, {1, 2}, course_id=1)
        self.course_ohte = Course("OhTe", 5, {2, 4}, {1}, course_id=3)

    def test_create(self):
        course_repository.create(self.course_ohja)
        course_repository.create(self.course_ohte)

        courses = course_repository.find_all()

        self.assertEqual(len(courses), 2)
        self.assertEqual(courses[0], self.course_ohja)
        self.assertEqual(courses[1], self.course_ohte)

    def test_create_without_existing_id(self):
        course_repository.create(Course("Tikape", 5))

        courses = course_repository.find_all()

        self.assertEqual(courses[0], Course("Tikape", 5, course_id=1))

    def test_create_updates_existing_course(self):
        course_repository.create(Course("OhJa", 5, {1, 2}, course_id=20))

        course = Course("OhPe", 5, course_id=20)
        course_repository.create(course)

        updated_course = course_repository.find_by_id(20)

        self.assertEqual(course, updated_course)

    def test_create_with_existing_id(self):
        course = Course("OhJa", 5, {1, 2}, course_id=20)
        course_repository.create(course)

        self.assertEqual(course, course_repository.find_by_id(20))

    def test_create_does_not_change_given_course(self):
        course = Course("Raja-arvot", 5, {1, 2})

        course_repository.create(course)

        self.assertEqual(course, Course("Raja-arvot", 5, {1, 2}))

    def test_delete(self):
        course_repository.create(self.course_ohja)
        course_repository.create(self.course_ohte)

        course_repository.delete(self.course_ohja.id)
        course_repository.delete(self.course_ohte.id)

        self.assertEqual(len(course_repository.find_all()), 0)

    def test_delete_all(self):
        course_repository.create(self.course_ohja)
        course_repository.create(self.course_ohte)

        course_repository.delete_all()

        self.assertEqual(len(course_repository.find_all()), 0)

    def test_find_by_id(self):
        course_repository.create(self.course_ohte)

        self.assertEqual(
            self.course_ohte, course_repository.find_by_id(self.course_ohte.id)
        )

    def test_find_by_id_returns_none_if_course_does_not_exist(self):
        self.assertEqual(course_repository.find_by_id(20), None)

    def test_find_all(self):
        course_repository.create(self.course_ohte)
        course_repository.create(self.course_ohja)

        # Testaa samalla id-järjestystä
        self.assertEqual(
            course_repository.find_all(), [self.course_ohja, self.course_ohte]
        )

    def test_find_all_returns_empty_list_if_no_courses(self):
        self.assertEqual(course_repository.find_all(), [])

    def test_find_requirements(self):
        course = course_repository.create(Course("Tikake", 5, requirements={5, 3, 2}))

        self.assertEqual(course_repository.find_requirements(course.id), {5, 3, 2})

    def test_find_requirements_returns_empty_set_if_course_does_not_exist(self):
        self.assertEqual(course_repository.find_requirements(2), set())

    def test_find_requirements_returns_empty_set_if_no_requirements(self):
        course = course_repository.create(Course("Linis 1", 5))

        self.assertEqual(course_repository.find_requirements(course.id), set())

    def test_find_timing(self):
        course = course_repository.create(Course("Tikake", 5, timing={5, 3, 2}))

        self.assertEqual(course_repository.find_timing(course.id), {5, 3, 2})

    def test_find_timing_returns_empty_set_if_course_does_not_exist(self):
        self.assertEqual(course_repository.find_timing(2), set())

    def test_find_timing_returns_empty_set_if_no_timing(self):
        course = course_repository.create(Course("Linis 1", 5))

        self.assertEqual(course_repository.find_timing(course.id), set())
