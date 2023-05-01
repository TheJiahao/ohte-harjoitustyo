from heapq import heappop, heappush

from entities.course import Course


class CycleError(Exception):
    pass


class Scheduler:
    """Luokka, joka vastaa kurssien aikataulutuksesta."""

    def __init__(
        self,
        courses: list[Course],
        starting_period: int = 1,
        periods_per_year: int = 4,
        max_credits: int = 15,
    ) -> None:
        """Luokan konstruktori.

        Args:
            courses (list[Course]):
                Aikatauluun lisättävät kurssit.
            starting_period (int, optional):
                Aloitusperiodi. Oletukseltaan 1.
            periods_per_year (int, optional):
                Vuoden periodien määrä. Oletukseltaan 4.
            max_credits (int, optional):
                Opintopisteyläraja periodeille. Oletukseltaan 15.
        """
        self.__periods_per_year: int = periods_per_year
        self.__starting_period: int = starting_period
        self.__max_credits: int = max_credits
        self.__courses: dict[int, Course] = {course.id: course for course in courses}

        self.__in_degrees: dict[int, int] = {
            course.id: len(course.requirements) for course in courses
        }
        self.__queues: list[list[tuple[int, int]]] = [
            [] for i in range(periods_per_year + 1)
        ]
        self.__schedule: dict[int, list[Course]] = {}

        self.__initialize(courses)

    def __initialize(self, courses: list[Course]) -> None:
        """Alustaa jonot.

        Args:
            courses (list[Course]): Lista kursseista.
        """

        for course in courses:
            if self.__in_degrees[course.id] == 0:
                self.__add_course_to_queue(course)

    def __add_course_to_queue(self, course: Course) -> None:
        for period in course.timing:
            queue = self.__queues[period]

            heappush(queue, (course.credits, course.id))

    def get_schedule(self) -> list[list[Course]]:
        """Palauttaa aikataulun.

        Returns:
            list[list[Course]]:
                Kurssit jaettuna sopiviin periodeihin.
                Periodien indeksöinti alkaa nollasta,
                ja kuvaa kuluneiden periodien määrää aloitusperiodista alkaen.
        """

        graph = self.__get_graph()

        self.__check_cycle(graph)
        self.__generate_schedule(graph)

        max_period = max(self.__schedule.keys())

        return [self.__schedule.get(i, []) for i in range(max_period + 1)]

    def __get_graph(self) -> dict[int, list[int]]:
        """Palauttaa suunnatun verkon kurssien riippuviksista.

        Returns:
            dict[int, list[int]]: Suunnattu verkko kurssien riippuvuuksista.
        """

        courses = self.__courses.values()
        graph = {course.id: [] for course in courses}

        for course in courses:
            for requirement_id in course.requirements:
                if requirement_id not in graph:
                    continue

                graph[requirement_id].append(course.id)

        return graph

    def __check_cycle(
        self,
        graph: dict[int, list[int]],
        node: int | None = None,
        states: dict[int, int] | None = None,
    ) -> None:
        """Tarkistaa syvyyshaulla verkosta syklit.

        Args:
            graph (dict[int, list[int]]): Tarkistettava verkko.
            node (int | None, optional): Solmu, josta aloitetaan syvyyshaku. Oletukseltaan None.
            states (dict[int, int] | None, optional): Solmujen tilat. Oletukseltaan None.

        Raises:
            CycleError: Verkossa on sykli.
        """

        node = node or next(iter(graph.keys()))
        states = states or {node: 0 for node in graph}

        for neighbor in graph[node]:
            if states[neighbor] == 1:
                raise CycleError("Kurssit ovat keskenään riippuvia.")

            if states[neighbor] == 0:
                states[neighbor] = 1

                self.__check_cycle(graph, neighbor, states)

        states[node] = 2

    def __generate_schedule(self, graph: dict[int, list[int]]) -> None:
        """Luo aikataulun.

        Returns:
            dict[int, list[Course]]: Aikataulu ilman tyhjiä periodeja.
        """

        remaining_credits = self.__max_credits
        i = 0
        processed = set()

        while self.__check_queues():
            period = self.__get_period(i)
            queue = self.__queues[period]
            course = self.__get_next_course(queue)

            if not course:
                i += 1
                remaining_credits = self.__max_credits
                continue

            if course.id in processed:
                continue

            if course.credits > remaining_credits:
                i += 1
                remaining_credits = self.__max_credits
                heappush(queue, (course.credits, course.id))
                continue

            self.__add_course_to_schedule(graph, course, i, processed)
            remaining_credits -= course.credits

    def __check_queues(self) -> bool:
        """Tarkistaa, ovatko jonot tyhjiä.

        Returns:
            bool: True, jos jonot eivät ole tyhjiä. Muulloin False.
        """

        for queue in self.__queues:
            if queue:
                return True

        return False

    def __get_period(self, i: int) -> int:
        period = (self.__starting_period + i) % self.__periods_per_year

        if period == 0:
            period = 4

        return period

    def __get_next_course(self, queue) -> Course | None:
        if queue:
            course_id = heappop(queue)[1]
            return self.__courses[course_id]

        return None

    def __add_course_to_schedule(
        self, graph: dict[int, list[int]], course: Course, i: int, processed: set[int]
    ) -> None:
        """Lisää kurssin aikatauluun ja päivittää naapureiden tilat.

        Args:
            course (Course): Aikatauluun lisättävä kurssi.
        """

        for neighbor_id in graph[course.id]:
            self.__in_degrees[neighbor_id] -= 1

            if self.__in_degrees[neighbor_id] == 0:
                neighbor = self.__courses[neighbor_id]
                self.__add_course_to_queue(neighbor)

        if i not in self.__schedule:
            self.__schedule[i] = []

        self.__schedule[i].append(course)
        processed.add(course.id)
