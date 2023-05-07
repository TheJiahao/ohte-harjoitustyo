class Course:
    """Luokka, joka kuvaa kurssia.

    Attributes:
        __name (str):
            Kurssin nimi.
        __credits (int):
            Kurssin opintopistemäärä.
        __timing (frozenset[int]):
            Kurssin perioditarjonta joukkona.
            Oletukseltaan tyhjä joukko.
        __requirements (frozenset[int]):
            Kurssin esitietovaatimuskurssien id:t joukkona.
            Oletukseltaan tyhjä joukko.
        __id (int):
            Kurssin id. Oletukseltaan -1.
    """

    def __init__(
        self,
        name: str,
        course_credits: int,
        timing: set[int] | None = None,
        requirements: set[int] | None = None,
        course_id: int = -1,
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
            course_id (int, optional):
                Kurssin id. Oletukseltaan -1.

        Raises:
            ValueError: Negatiivinen opintopistemäärä.
        """

        if course_credits < 0:
            raise ValueError("Negatiivinen opintopistemäärä ei kelpaa.")

        self.__name: str = name
        self.__credits: int = course_credits
        self.__timing: frozenset[int] = frozenset(timing or frozenset())
        self.__requiments: frozenset[int] = frozenset(requirements or frozenset())
        self.__id: int = course_id

    def __eq__(self, other: "Course") -> bool:
        if isinstance(other, Course):
            return (
                self.name == other.name
                and self.credits == other.credits
                and self.timing == other.timing
                and self.requirements == other.requirements
                and self.id == other.id
            )

        return False

    def __str__(self) -> str:
        return f"{self.__id}: {self.__name}, {self.__credits} op"

    def __repr__(self) -> str:
        return f"Course({self.name}, {self.credits}, {self.timing}, {self.requirements}, {self.id})"

    @property
    def name(self) -> str:
        return self.__name

    @property
    def credits(self) -> int:
        return self.__credits

    @property
    def timing(self) -> frozenset[int]:
        return self.__timing

    @property
    def requirements(self) -> frozenset[int]:
        return self.__requiments

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, course_id: int) -> None:
        """Asettaa uuden id:n.

        Args:
            course_id (int): Asetettava id.

        Raises:
            ValueError: Id on negatiivinen.
        """

        if course_id <= 0:
            raise ValueError(f"Negatiivinen id {course_id} ei kelpaa.")

        self.__id = course_id
