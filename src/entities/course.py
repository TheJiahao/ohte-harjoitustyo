import copy


class Course:
    """Luokka, joka kuvaa kurssia.

    Attributes:
        __name (str):
            Kurssin nimi.
        __credits (int):
            Kurssin opintopistemäärä.
        __timing (list[bool]):
            Kurssin perioditarjonta tauluna.
            Oletukseltaan 5-alkioinen taulu False-arvoilla.
        __requirements (set[int]):
            Kurssin esitietovaatimuskurssien id:t joukkona.
            Oletukseltaan tyhjä joukko.
        __course_id (int):
            Kurssin id. Oletukseltaan -1.
    """

    def __init__(
        self,
        name: str,
        credits: int,
        timing: list[bool] | None = None,
        requirements: set[int] | None = None,
        course_id: int | None = None,
    ) -> None:
        """Luokan konstruktori.

        Args:
            name (str):
                Kurssin nimi.
            credits (int):
                Kurssin opintopistemäärä.
            timing (list[bool] | None, optional):
                Kurssin perioditarjonta tauluna. Oletukseltaan None.
            requirements (set[int] | None, optional):
                Kurssin esitietovaatimuskurssien id:t joukkona.
                Oletukseltaan None.
            course_id (int | None, optional):
                Kurssin id. Oletukseltaan None.
        """
        self.__name: str = name
        self.__credits: int = credits
        self.__timing: list[bool] = timing or [False] * 5
        self.__requiments: set[int] = requirements or set()
        self.__id: int = course_id or -1

    @property
    def name(self) -> str:
        return self.__name

    @property
    def credits(self) -> int:
        return self.__credits

    @property
    def timing(self) -> list[bool]:
        return copy.copy(self.__timing)

    @property
    def requirements(self) -> set[int]:
        return copy.copy(self.__requiments)

    @property
    def id(self) -> int:
        return self.__id

    @credits.setter
    def credits(self, credits: int) -> None:
        """Asettaa opintopistemäärän kurssille.

        Args:
            credits (int): Asetettava opintopistemäärä.

        Raises:
            ValueError: Opintopistemäärä on ei-positiivinen.
        """
        if credits <= 0:
            raise ValueError("Ei-positiivinen opintopiste ei kelpaa.")

        self.__credits = credits

    @name.setter
    def name(self, name: str) -> None:
        """Asettaa uuden nimen kurssille.

        Args:
            name (str): Asetettava nimi.
        """
        self.__name = name

    def set_period(self, period: int, status: bool) -> None:
        """Asettaa annetun tilan periodille.

        Args:
            period (int): Muutettava periodi.
            status (bool): Periodin tila.

        Raises:
            ValueError: Periodi ei kelpaa.
        """
        if not 0 < period < len(self.timing):
            raise ValueError(f"Periodi {period} ei kelpaa.")

        self.__timing[period] = status

    def add_requirement(self, id: int) -> None:
        """Lisää esitietokurssin.

        Args:
            id (int): Lisättävän esitietokurssin id.

        Raises:
            ValueError: Ei-positiivinen id.
        """
        if id <= 0:
            raise ValueError("Ei-positiivinen id ei kelpaa.")

        self.__requiments.add(id)

    def remove_requirement(self, id: int) -> None:
        """Poistaa esitietokurssin, jos se on esitietovaatimuksissa.

        Args:
            id (int): Poistettavan esitietokurssin id.
        """

        if id in self.__requiments:
            self.__requiments.remove(id)
