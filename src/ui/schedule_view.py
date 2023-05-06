from tkinter import constants, ttk

from entities.course import Course
from services.planner_service import planner_service
from ui.view import View


class ScheduleView(View):
    """Aikataulusta vastaava näkymä."""

    def __init__(self, root: ttk.Widget) -> None:
        super().__init__(root)

        self.__tree = ttk.Treeview(master=self._frame, show="tree")

        self.__initialize()

    def __initialize(self) -> None:
        self.__tree.grid(sticky=constants.NSEW, columnspan=2)
        self._frame.grid_columnconfigure(0, weight=1)

    def __clear_schedule(self) -> None:
        """Tyhjentää aikataulun."""

        for item in self.__tree.get_children():
            self.__tree.delete(item)

    def update(self) -> None:
        """Päivittää aikataulun."""

        self.__clear_schedule()

        credits_of_year = 0
        period = planner_service.starting_period
        year = planner_service.starting_year

        for courses in planner_service.get_schedule():
            if not self.__tree.exists(str(year)):
                self.__tree.insert("", constants.END, str(year), text=str(year))

            period_id = self.__tree.insert(str(year), constants.END)

            credits_of_period = self.__add_courses(period_id, courses)
            credits_of_year += credits_of_period

            self.__tree.item(
                period_id,
                text=f"Periodi {period}, {credits_of_period} op",
            )
            self.__tree.item(
                str(year),
                text=f"{year}, {credits_of_year} op",
            )

            period += 1

            if period > planner_service.periods_per_year:
                period = 1
                year += 1
                credits_of_year = 0

    def __add_courses(self, period_id: str, courses: list[Course]) -> int:
        """Lisää kurssit annettuun periodiin.

        Args:
            period_id (str): Periodin id.
            courses (list[Course]): Lisättävät kurssit.

        Returns:
            int: Periodin opintopistemäärä.
        """

        total_credits = 0

        for course in courses:
            self.__tree.insert(period_id, constants.END, text=str(course))
            total_credits += course.credits

        return total_credits
