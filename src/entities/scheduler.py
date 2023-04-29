from heapq import heapify, heappop, heappush

from entities.course import Course


class CycleError(Exception):
    pass


class Scheduler:
    def __init__(
        self,
        courses: list[Course],
        starting_period: int = 1,
        periods_per_year: int = 4,
        max_credits: int = 15,
    ) -> None:
        self.__periods_per_year: int = periods_per_year
        self.__starting_period: int = starting_period
        self.__max_credits: int = max_credits
        self.__courses: dict[int, Course] = {course.id: course for course in courses}

        self.__in_degrees: dict[int, int] = {
            course.id: len(course.requirements) for course in courses
        }

        self.__heap: list[tuple[int, int]] = [
            (min(course.timing), course.id)
            for course in courses
            if self.__in_degrees[course.id] == 0
        ]
        heapify(self.__heap)

        self.__schedule: dict[int, list[Course]] = {}
        self.__graph: dict[int, list[int]] = self.__get_graph()

    def get_schedule(self) -> list[list[Course]]:
        """Palauttaa aikataulun, perustuu Kahnin algoritmiin.

        Returns:
            list[list[Course]]:
                Kurssit jaettuna sopiviin periodeihin.
                Periodien indeksöinti alkaa nollasta,
                ja kuvaa kuluneiden periodien määrää aloitusperiodista alkaen.
        """

        self.__generate_schedule()
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
                    # Kurssi ei ole olemassa, joten jätetään huomioimatta
                    continue

                graph[requirement_id].append(course.id)

        return graph

    def __generate_schedule(self) -> None:
        """Luo aikataulun.

        Raises:
            CycleError: Kurssit ovat keskenään riippuvia.

        Returns:
            dict[int, list[Course]]: Aikataulu ilman tyhjiä periodeja.
        """

        course_counter = 0
        remaining_credits = self.__max_credits
        i = 0

        delayed_courses: set[int] = set()

        while self.__heap:
            course = self.__courses[heappop(self.__heap)[1]]

            if course.id in delayed_courses:
                i += 1
                remaining_credits = self.__max_credits
                delayed_courses.clear()

            if course.credits > remaining_credits or self.__get_period(
                i
            ) not in self.__get_timing(course):
                self.__delay_course(course)
                delayed_courses.add(course.id)
                continue

            self.__add_course_to_schedule(course, i)
            remaining_credits -= course.credits
            course_counter += 1

        if course_counter != len(self.__courses):
            raise CycleError("Kurssit ovat keskenään riippuvia.")

    def __get_timing(self, course: Course) -> set[int]:
        return {period % self.__periods_per_year for period in course.timing}

    def __get_period(self, i: int) -> int:
        return (self.__starting_period + i) % self.__periods_per_year

    def __add_course_to_schedule(self, course: Course, i: int) -> None:
        """Lisää kurssin aikatauluun ja päivittää naapureiden tilat.

        Args:
            course (Course): Aikatauluun lisättävä kurssi.
        """

        for neighbor_id in self.__graph[course.id]:
            self.__in_degrees[neighbor_id] -= 1

            if self.__in_degrees[neighbor_id] == 0:
                neighbor = self.__courses[neighbor_id]

                heappush(self.__heap, (min(neighbor.timing), neighbor_id))

        if i not in self.__schedule:
            self.__schedule[i] = []

        self.__schedule[i].append(course)

    def __delay_course(self, course: Course) -> None:
        """Siirtää kurssin myöhempään.

        Args:
            course (Course): Siirrettävä kurssi.
        """

        min_timing = min(course.timing)

        course.remove_period(min_timing)
        course.add_period(min_timing + self.__periods_per_year)

        heappush(self.__heap, (min(course.timing), course.id))
