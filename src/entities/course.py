class Course:
    """Luokka, joka kuvaa kurssia.

    Attributes:
        name (str): Nimi
        credits (int): Laajuus opintopisteinä
        timing (set[int]): Periodit, joilla on kurssi on tarjolla.
        requirements (set[int]): Esitietovaatimuskurssien id:t.
        id (int): Tunniste.
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
            course_credits (int):
                Kurssin opintopistemäärä.
            timing (set[int] | None, optional):
                Kurssin perioditarjonta. Oletukseltaan None.
            requirements (set[int] | None, optional):
                Kurssin esitietovaatimuskurssien id:t.
                Oletukseltaan None.
            course_id (int | None, optional):
                Kurssin tunniste. Oletukseltaan None.

        Raises:
            ValueError: Negatiivinen opintopiste.
        """
        if course_credits < 0:
            raise ValueError("Negatiivinen opintopiste ei kelpaa.")

        self.name: str = name
        self.credits: int = course_credits
        self.timing: set[int] = timing or set()
        self.requirements: set[int] = requirements or set()
        self.id: int = course_id

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
        return f"{self.id}: {self.name}, {self.credits} op"

    def __repr__(self) -> str:
        return f"Course({self.name}, {self.credits}, {self.timing}, {self.requirements}, {self.id})"
