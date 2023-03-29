import uuid


class Course:
    def __init__(
        self,
        name: str,
        credits: int,
        timing: set[int] = set(),
        requirements: set[str] = set(),
        course_id: str | None = None,
    ) -> None:
        self.__name: str = name
        self.__credits: int = credits
        self.__timing: set[int] = timing
        self.__requiments: set[str] = requirements
        self.__id: str = course_id or str(uuid.uuid4())

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name) -> None:
        self.__name = name

    @property
    def credits(self) -> int:
        return self.__credits

    @credits.setter
    def credits(self, credits) -> None:
        if credits >= 0:
            self.__credits = credits

    @property
    def timing(self) -> set[int]:
        return self.__timing

    @property
    def requirements(self) -> set[str]:
        return self.__requiments

    @property
    def id(self) -> str:
        return self.__id

    def add_period(self, period: int) -> None:
        if period > 0:
            self.__timing.add(period)

    def remove_period(self, period: int) -> None:
        if period in self.__timing:
            self.__timing.remove(period)

    def add_requirement(self, id: str) -> None:
        self.__requiments.add(id)

    def remove_requirement(self, id: str) -> None:
        if id in self.__requiments:
            self.__requiments.remove(id)
