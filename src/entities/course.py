import uuid


class Course:
    def __init__(
        self,
        name: str,
        credits: int,
        timing: set[int],
        requirements: set = set(),
    ) -> None:
        self.name: str = name
        self.credits: int = credits
        self.timing: set[int] = timing
        self.requiments: set = requirements
        self.id = str(uuid.uuid4())
