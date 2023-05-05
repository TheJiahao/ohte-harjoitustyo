from entities.course import Course
from entities.scheduler import Scheduler
from repositories import course_repository as default_course_repository
from repositories.course_repository import CourseRepository


class TimingError(Exception):
    pass


class MaxCreditError(Exception):
    pass


class PlannerService:
    """""Luokka, joka vastaa sovelluksen logiikasta.""" ""

    def __init__(
        self,
        periods: int,
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

        self.__course_repository: CourseRepository = course_repository
        self.__periods_per_year: int = periods
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
            ValueError: Kurssin nimi on tyhjä.
            TimingError: Kurssilla ei ole ajoitusta.
        """

        if course.name == "":
            raise ValueError("Kurssin nimi ei voi olla tyhjä.")

        if (
            not course.timing.issubset(range(1, self.__periods_per_year + 1))
            or len(course.timing) == 0
        ):
            raise TimingError("Kurssilla ei ole ajoitusta.")

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
        """Palauttaa aikataulun, perustuu Kahnin algoritmiin.

        Returns:
            list[list[Course]]:
                Kurssit jaettuna sopiviin periodeihin.
                Periodien indeksöinti alkaa nollasta,
                ja kuvaa kuluneiden periodien määrää aloitusperiodista alkaen.
        """
        scheduler = Scheduler(
            self.get_all_courses(),
            self.__starting_period,
            self.__periods_per_year,
            self.__max_credits,
        )

        return scheduler.get_schedule()
