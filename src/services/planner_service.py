from heapq import heapify, heappop, heappush

from entities.course import Course
from repositories import course_repository as default_course_repository
from repositories.course_repository import CourseRepository


class TimingError(Exception):
    pass


class CycleError(Exception):
    pass


class MaxCreditError(Exception):
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

        self.__courses: dict[int, Course] = {
            course.id: course for course in self.get_all_courses()
        }
        self.__graph: dict[int, list[int]] = {}
        self.__in_degree: dict[int, int] = {}
        self.__heap: list[tuple[int, int]] = []

    @property
    def periods_per_year(self) -> int:
        return self.__periods_per_year

    @property
    def starting_year(self) -> int:
        return self.__starting_year

    @property
    def starting_period(self) -> int:
        return self.__starting_period

    @property
    def max_credits(self) -> int:
        return self.__max_credits

    @starting_year.setter
    def starting_year(self, year: int) -> None:
        if year < 0:
            raise ValueError("Aloitusvuosi ei voi olla negatiivinen.")

        self.__starting_year = year

    @starting_period.setter
    def starting_period(self, period: int) -> None:
        if not 0 < period <= self.periods_per_year:
            raise ValueError("Virheellinen aloitusperiodi.")

        self.__starting_period = period

    @max_credits.setter
    def max_credits(self, max_credits: int) -> None:
        if max_credits < 0:
            raise ValueError("Negatiivinen opintopisteyläraja ei kelpaa.")

        self.__max_credits = max_credits

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

        Raises:
            TimingError: Kurssilla ei ole ajoitusta.
        """

        if not course.timing.intersection(range(1, self.__periods_per_year + 1)):
            raise TimingError(f"Kurssilla '{course}' ei ole ajoitusta.")

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

    def get_graph(self) -> dict[int, list[int]]:
        """Palauttaa suunnatun verkon kurssien riippuviksista.

        Returns:
            dict[int, list[int]]: Suunnattu verkko kurssien riippuvuuksista.
        """

        courses = self.get_all_courses()
        graph = {course.id: [] for course in courses}

        for course in courses:
            for requirement_id in course.requirements:
                if requirement_id not in graph:
                    # Kurssi ei ole olemassa, joten jätetään huomioimatta
                    continue

                graph[requirement_id].append(course.id)

        return graph

    def set_parameters(
        self, starting_year: int, starting_period: int, max_credits: int
    ) -> None:
        """Asettaa parametrit aikataulun määrittämistä varten.

        Args:
            starting_year (int): Aloitusvuosi.
            starting_period (int): Aloitusperiodi.
            max_credits (int): Opintopisteyläraja periodille.
        """

        for course in self.get_all_courses():
            if course.credits > max_credits:
                raise MaxCreditError(
                    "Opintopisteyläraja on pienempi kuin suurin kurssin laajuus."
                )

        self.max_credits = max_credits
        self.starting_year = starting_year
        self.starting_period = starting_period

    def get_schedule(self) -> list[list[Course]]:
        """Jakaa kurssit sopiviin periodeihin. Perustuu Kahnin algoritmiin.

        Returns:
            list[list[Course]]:
                Kurssit jaettuna sopiviin periodeihin.
                Periodien indeksöinti alkaa nollasta,
                ja kuvaa kuluneiden periodien määrää aloitusperiodista alkaen.
        """

        result = [[]]
        delayed_courses = set()
        self.__prepare_get_schedule()
        course_counter = 0
        remaining_credits = self.max_credits
        i = 0

        while self.__heap:
            course = self.__courses[heappop(self.__heap)[1]]

            if course.id in delayed_courses:
                i += 1
                result.append([])
                delayed_courses.clear()
                remaining_credits = self.max_credits

            if (new_counter := self.__update_period_counter(course, i, result)) > i:
                i = new_counter
                remaining_credits = self.max_credits

            if self.__delay_course_timing(course, remaining_credits):
                delayed_courses.add(course.id)
                continue

            self.__update_neighbors(course.id)
            result[i].append(course)

            remaining_credits -= course.credits
            course_counter += 1

        if course_counter != len(self.__courses):
            raise CycleError("Kurssit ovat keskenään riippuvia.")

        return result

    def __update_period_counter(
        self, course: Course, i: int, result: list[list[int]]
    ) -> int:
        valid_periods = [period % self.periods_per_year for period in course.timing]

        while (self.starting_period + i) % self.periods_per_year not in valid_periods:
            i += 1
            result.append([])

        return i

    def __delay_course_timing(self, course: Course, remaining_credits: int) -> bool:
        """Päättää siirretäänkö kurssi myöhempään.

        Args:
            course (Course): Kurssi.
            current_period (int): Tarkasteltava periodi.

        Returns:
            bool: Kuvaa sitä, että siirretäänkö kurssi myöhempään.
        """

        min_timing = min(course.timing)

        if course.credits <= remaining_credits:
            return False

        course.remove_period(min_timing)
        course.add_period(min_timing + self.periods_per_year)

        heappush(self.__heap, (min(course.timing), course.id))

        return True

    def __prepare_get_schedule(self) -> None:
        """Alustaa topologisen järjestyksen laskuun tarvittavat muuttujat."""

        self.__courses = {course.id: course for course in self.get_all_courses()}
        self.__graph = self.get_graph()

        self.__in_degree = {
            id: len(course.requirements) for id, course in self.__courses.items()
        }

        self.__heap: list[tuple[int, int]] = [
            (min(course.timing), course.id)
            for course in self.__courses.values()
            if self.__in_degree[course.id] == 0
        ]
        heapify(self.__heap)

    def __update_neighbors(self, course_id: int) -> None:
        """Päivittää kurssin naapureiden täyttämättömien esitietovaatimuksien määrän.
        Lisäksi siirtää suoritettavat kelpaavat kurssit kekoon.

        Args:
            course_id (int): Kurssi, jonka naapurit päivitetään.
        """

        for neighbor_id in self.__graph[course_id]:
            self.__in_degree[neighbor_id] -= 1

            if self.__in_degree[neighbor_id] == 0:
                neighbor = self.__courses[neighbor_id]
                heappush(self.__heap, (min(neighbor.timing), neighbor_id))
