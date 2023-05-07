from config import PERIODS_PER_YEAR
from entities.course import Course
from repositories.course_repository import CourseRepository
from repositories.course_repository import (
    course_repository as default_course_repository,
)
from services.export_service import ExportService
from services.export_service import export_service as default_export_service
from services.import_service import ImportService
from services.import_service import import_service as default_import_service
from services.scheduler_service import SchedulerService
from services.scheduler_service import scheduler_service as default_scheduler_service


class TimingError(Exception):
    pass


class PlannerService:
    """Luokka, joka vastaa sovelluksen logiikasta.

    Attributes:
        starting_year (int): Opintojen aloitusvuosi.
        starting_period (int): Opintojen aloitusperiodi.
    """

    def __init__(
        self,
        scheduler_service: SchedulerService = default_scheduler_service,
        course_repository: CourseRepository = default_course_repository,
        import_service: ImportService = default_import_service,
        export_service: ExportService = default_export_service,
    ) -> None:
        """Luokan konstruktori.

        Args:
            periods (int, optional):
                Periodien lukumäärä lukuvuodessa. Oletukseltaan 4.
            course_repository (CourseRepository, optional):
                Olio, joka vastaa kurssien tallentamisesta.
                Oletukseltaan default_course_repository.
        """
        self.__starting_year: int = 0

        self.__course_repository: CourseRepository = course_repository
        self.__scheduler: SchedulerService = scheduler_service
        self.__importer: ImportService = import_service
        self.__exporter: ExportService = export_service

    @property
    def starting_year(self) -> int:
        return self.__starting_year

    @property
    def starting_period(self) -> int:
        return self.__starting_period

    @starting_year.setter
    def starting_year(self, year: int) -> None:
        if year < 0:
            raise ValueError("Aloitusvuosi ei voi olla negatiivinen.")

        self.__starting_year = year

    @starting_period.setter
    def starting_period(self, period: int) -> None:
        if not 0 < period <= PERIODS_PER_YEAR:
            raise ValueError("Virheellinen aloitusperiodi.")

        self.__starting_period = period

    def initialize(
        self,
        starting_year: int,
        starting_period: int,
        max_credits: int,
    ) -> None:
        """Alustaa parametrit.

        Args:
            starting_year (int): Aloitusvuosi.
            starting_period (int): Aloitusperiodi.
            max_credits (int): Opintopisteyläraja periodille.
        """

        self.starting_year = starting_year
        self.starting_period = starting_period

        self.__scheduler.initialize(
            self.get_all_courses(), self.starting_period, max_credits
        )

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
            not course.timing.issubset(range(1, PERIODS_PER_YEAR + 1))
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

    def get_schedule(self) -> list[list[Course]]:
        """Palauttaa aikataulun.

        Returns:
            list[list[Course]]:
                Kurssit jaettuna sopiviin periodeihin.
                Periodien indeksöinti alkaa nollasta,
                ja kuvaa kuluneiden periodien määrää aloitusperiodista alkaen.
        """

        return self.__scheduler.get_schedule()

    def import_courses(self, path: str) -> None:
        """Poistaa kaikki jo olevat kurssit ja lukee kurssit tiedostosta.

        Args:
            path (str): Tiedoston polku.
        """

        self.delete_all_courses()

        for course in self.__importer.read(path):
            self.create_course(course)

    def export_courses(self, path: str) -> None:
        """Kirjoittaa kurssit tiedostoon.

        Args:
            path (str): Tiedoston polku.
        """

        self.__exporter.write(self.get_all_courses(), path)


planner_service = PlannerService()
