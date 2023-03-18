import uuid


class Course:
    def __init__(
        self,
        name: str,
        credits: int,
        timing: list[bool] = [],
        requirements: set = set(),
    ) -> None:
        self.name: str = name
        self.credits: int = credits
        self.timing: list[bool] = timing
        self.requiments: set = requirements
        self.id = str(uuid.uuid4())
