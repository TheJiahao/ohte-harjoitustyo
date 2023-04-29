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

        self.__in_degree: dict[int, int] = {
            course.id: len(course.requirements) for course in courses
        }

        self.__heap: list[tuple[int, int]] = [
            (min(course.timing), course.id)
            for course in courses
            if self.__in_degree[course.id] == 0
        ]
        heapify(self.__heap)

        self.__graph: dict[int, list[int]] = self.__get_graph()

    def get_schedule(self) -> list[list[Course]]:
        """Palauttaa aikataulun, perustuu Kahnin algoritmiin.

        Returns:
            list[list[Course]]:
                Kurssit jaettuna sopiviin periodeihin.
                Periodien indeksöinti alkaa nollasta,
                ja kuvaa kuluneiden periodien määrää aloitusperiodista alkaen.
        """

        initial_schedule = self.__generate_schedule()

        max_period = max(initial_schedule.keys())

        return [initial_schedule.get(i, []) for i in range(max_period + 1)]

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

    def __generate_schedule(self) -> dict[int, list[Course]]:
        """Luo aikataulun.

        Raises:
            CycleError: Kurssit ovat keskenään riippuvia.

        Returns:
            dict[int, list[Course]]: Aikataulu ilman tyhjiä periodeja.
        """

        result = {}
        delayed_courses = set()
        course_counter = 0
        remaining_credits = self.__max_credits
        i = 0

        while self.__heap:
            course = self.__courses[heappop(self.__heap)[1]]

            i, remaining_credits = self.__move_period(
                course, delayed_courses, i, remaining_credits
            )

            if self.__delay_course_timing(course, remaining_credits, delayed_courses):
                continue

            self.__update_neighbors(course.id)

            if i not in result:
                result[i] = []

            result[i].append(course)
            remaining_credits -= course.credits
            course_counter += 1

        if course_counter != len(self.__courses):
            raise CycleError("Kurssit ovat keskenään riippuvia.")

        return result

    def __move_period(
        self, course: Course, delayed_courses: set[int], i: int, remaining_credits: int
    ) -> tuple[int, int]:
        """Palauttaa seuraavan kelpaavan periodin ja uuden opintopisterajan.

        Args:
            course (Course): Kurssi, joka halutaan sijoittaa periodille.
            delayed_courses (set[int]): Kurssit, jotka on merkattu myöhempään periodiin.
            i (int): Periodilaskuri.
            remaining_credits (int): Tämänhetkinen opintopisteraja.

        Returns:
            tuple[int, int]: (periodilaskuri, uusi opintopisteraja)
        """

        valid_periods = [period % self.__periods_per_year for period in course.timing]

        while (
            (self.__starting_period + i) % self.__periods_per_year not in valid_periods
            or course.id in delayed_courses
        ):
            i += 1
            remaining_credits = self.__max_credits
            delayed_courses.clear()

        return (i, remaining_credits)

    def __delay_course_timing(
        self, course: Course, remaining_credits: int, delayed_courses: set[int]
    ) -> bool:
        """Päättää siirretäänkö kurssi myöhempään.

        Args:
            course (Course): Kurssi.
            current_period (int): Tarkasteltava periodi.

        Returns:
            bool: Kuvaa sitä, että siirretäänkö kurssi myöhempään.
        """

        if course.credits <= remaining_credits:
            return False

        min_timing = min(course.timing)

        course.remove_period(min_timing)
        course.add_period(min_timing + self.__periods_per_year)

        delayed_courses.add(course.id)
        heappush(self.__heap, (min(course.timing), course.id))

        return True

    def __update_neighbors(self, course_id: int) -> None:
        """Päivittää kurssin naapureiden täyttämättömien esitietovaatimuksien määrän.
        Lisäksi siirtää suoritettavat kelpaavat kurssit kekoon.

        Args:
            course_id (int): Kurssi, jonka naapurit päivitetään.
        """

        for neighbor_id in self.__graph[course_id]:
            self.__in_degree[neighbor_id] -= 1

            if self.__in_degree[neighbor_id] == 0:
                neighbor = self.__courses[neighbor_id]
                heappush(self.__heap, (min(neighbor.timing), neighbor_id))
