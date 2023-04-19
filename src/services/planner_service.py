from graphlib import TopologicalSorter

from entities.course import Course
from repositories.course_repository import CourseRepository
from repositories import course_repository


class PlannerService:
    """Luokka, joka vastaa sovelluksen logiikasta."""

    def __init__(self) -> None:
        """Luokan konstruktori."""

        self.__course_repository: CourseRepository = course_repository

    def get_courses_in_topological_order(self) -> list[Course]:
        """Palauttaa kurssit topologisessa järjestyksessä.

        Returns:
            list[Course]: Kurssit topologisessa järjestyksessä.
        """

        dependencies_dict = {
            course.id: course.requirements for course in self.get_all_courses()
        }

        sorter = TopologicalSorter(dependencies_dict)

        return [self.get_course(id) for id in sorter.static_order()]

    def get_course(self, course_id: int) -> Course | None:
        """Palauttaa id:tä vastaavan kurssin.

        Args:
            id (int): Haettavan kurssin id.

        Returns:
            Course | None: Id:tä vastaava kurssi tai None, jos kurssia ei löydy.
        """
        return self.__course_repository.find_by_id(course_id)

    def get_all_courses(self) -> list[str]:
        """Palauttaa kaikki kurssit.

        Returns:
            list[str]: Kurssit merkkijonoina.
        """

        return [str(course) for course in self.__course_repository.find_all()]

    def create_course(self, course: Course) -> None:
        """Lisää kurssin tietokantaan.

        Args:
            course (Course): Lisättävä kurssi.
        """

        self.__course_repository.create(course)

    def delete_course(self, course_id: int) -> None:
        """Poistaa id:tä vastaavan kurssin.

        Args:
            id (int): Poistettavan kurssin id.
        """

        self.__course_repository.delete(course_id)

    def delete_all_courses(self) -> None:
        """Poistaa kaikki kurssit tietokannasta."""

        self.__course_repository.delete_all()
