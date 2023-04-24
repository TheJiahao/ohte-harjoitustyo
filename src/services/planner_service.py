from graphlib import TopologicalSorter

from entities.course import Course
from repositories import course_repository as default_course_repository
from repositories.course_repository import CourseRepository


class TimingError(Exception):
    pass


class PlannerService:
    """""Luokka, joka vastaa sovelluksen logiikasta.""" ""

    def __init__(
        self,
        periods: int = 4,
        course_repository: CourseRepository = default_course_repository,
    ) -> None:
        """Luokan konstruktori.

        Args:
            periods (int, optional):
                Periodien lukumäärä lukuvuodessa. Oletukseltaan 4.
            course_repository (CourseRepository, optional):
                Olio, joka vastaa kurssien tallentamisesta.
                Oletukseltaan default_course_repository.
        """

        self.__periods_per_year: int = periods
        self.__course_repository: CourseRepository = course_repository
        self.__starting_year: int = 0
        self.__starting_period: int = 1
        self.__max_credits: int = 15

    @property
    def periods_per_year(self) -> int:
        return self.__periods_per_year

    @property
    def starting_year(self) -> int:
        return self.__starting_year

    @property
    def starting_period(self) -> int:
        return self.__starting_period

    def get_course(self, course_id: int) -> Course | None:
        """Palauttaa id:tä vastaavan kurssin.

        Args:
            id (int): Haettavan kurssin id.

        Returns:
            Course | None: Id:tä vastaava kurssi tai None, jos kurssia ei löydy.
        """
        return self.__course_repository.find_by_id(course_id)

    def get_all_courses(self) -> list[Course]:
        """Palauttaa kaikki kurssit.

        Returns:
            list[str]: Kurssit merkkijonoina.
        """

        return self.__course_repository.find_all()

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

    def get_courses_in_topological_order(self) -> list[Course]:
        """Palauttaa kurssit topologisessa järjestyksessä.
        Jos jokin esitietovaatimuskurssi ei ole olemassa (esimerkiksi poiston takia),
        niin se jätetään huomioimatta.

        Returns:
            list[Course]: Kurssit topologisessa järjestyksessä.
        """

        dependencies_dict = {
            course.id: course.requirements for course in self.get_all_courses()
        }

        sorter = TopologicalSorter(dependencies_dict)

        return [
            course for id in sorter.static_order() if (course := self.get_course(id))
        ]

    def set(self, starting_year: int, starting_period: int, max_credits: int) -> None:
        """Asettaa parametrit aikataulun määrittämistä varten.

        Args:
            starting_year (int): Aloitusvuosi.
            starting_period (int): Aloitusperiodi.
            max_credits (int): Opintopisteyläraja periodille.
        """
        self.__max_credits = max_credits
        self.__starting_year = starting_year
        self.__starting_period = starting_period

    def get_schedule(self) -> list[list[Course]]:
        """Jakaa kurssit sopiviin periodeihin.

        Raises:
            TimingError:
                Kurssin ajoitus ei kelpaa eli on joko tyhjä tai ei sisällä sopivia periodeja.

        Returns:
            list[list[Course]]:
                Kurssit jaettuna sopiviin periodeihin.
                Periodien indeksöinti alkaa nollasta,
                ja kuvaa kuluneiden periodien määrää aloitusperiodista alkaen.
        """

        courses = self.get_courses_in_topological_order()
        result = [[]]
        passed_periods = 0
        valid_periods = list(range(1, self.__periods_per_year + 1))

        for course in courses:
            if not course.timing.intersection(valid_periods):
                raise TimingError(f"Kurssilla '{course}' ei ole ajoitusta.")

            total_credits = 0

            # Edellisen tarkistuksen takia tämä silmukka päättyy varmasti
            while (
                passed_periods + self.__starting_period % self.__periods_per_year
                not in course.timing
                or total_credits > self.__max_credits
            ):
                total_credits = 0
                passed_periods += 1
                result.append([])

            total_credits += course.credits

            result[passed_periods].append(course)

        return result
