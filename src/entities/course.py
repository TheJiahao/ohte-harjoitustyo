from copy import copy


class Course:
    """Luokka, joka kuvaa kurssia.

    Attributes:
        __name (str):
            Kurssin nimi.
        __credits (int):
            Kurssin opintopistemäärä.
        __timing (set[int]):
            Kurssin perioditarjonta joukkona.
            Oletukseltaan tyhjä joukko.
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
        timing: set[int] | None = None,
        requirements: set[int] | None = None,
        course_id: int | None = None,
    ) -> None:
        """Luokan konstruktori.

        Args:
            name (str):
                Kurssin nimi.
            credits (int):
                Kurssin opintopistemäärä.
            timing (set[int] | None, optional):
                Kurssin perioditarjonta tauluna. Oletukseltaan None.
            requirements (set[int] | None, optional):
                Kurssin esitietovaatimuskurssien id:t joukkona.
                Oletukseltaan None.
            course_id (int | None, optional):
                Kurssin id. Oletukseltaan None.
        """
        self.__name: str = name
        self.__credits: int = credits
        self.__timing: set[int] = timing or set()
        self.__requiments: set[int] = requirements or set()
        self.__id: int = course_id or -1

    def __eq__(self, other: "Course") -> bool:
        return (
            self.name == other.name
            and self.credits == other.credits
            and self.timing == other.timing
            and self.requirements == other.requirements
            and self.id == other.id
        )

    @property
    def name(self) -> str:
        return self.__name

    @property
    def credits(self) -> int:
        return self.__credits

    @property
    def timing(self) -> set[int]:
        return copy(self.__timing)

    @property
    def requirements(self) -> set[int]:
        return copy(self.__requiments)

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, id: int) -> None:
        """Asettaa id:n kurssille.

        Args:
            id (int): Asetettava id.

        Raises:
            ValueError: Ei-positiivinen id.
        """

        if id <= 0:
            raise ValueError("Ei-positiivinen id ei kelpaa.")

        self.__id = id

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

    def add_period(self, period: int) -> None:
        """Lisää periodin kurssille.

        Args:
            period (int): Lisättävä periodi.

        Raises:
            ValueError: Ei-positiivinen periodi.
        """
        if period <= 0:
            raise ValueError(f"Ei-positiivinen periodi {period} ei kelpaa.")

        self.__timing.add(period)

    def remove_period(self, period: int) -> None:
        """Poistaa periodin kurssilta, jos se on perioditarjonnassa.

        Args:
            period (int): Poistettava periodi.
        """

        if period in self.__timing:
            self.__timing.remove(period)

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
