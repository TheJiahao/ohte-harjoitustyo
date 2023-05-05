from tkinter import constants, ttk

from entities.course import Course
from services import planner_service
from ui.view import View


class ScheduleView(View):
    """Aikataulusta vastaava näkymä."""

    def __init__(self, root: ttk.Widget) -> None:
        super().__init__(root)

        self.__tree = ttk.Treeview(master=self._frame)

        self.__initialize()

    def __initialize(self) -> None:
        self.__tree.pack()

    def __clear_schedule(self) -> None:
        for item in self.__tree.get_children():
            self.__tree.delete(item)

    def update(self) -> None:
        """Päivittää aikataulun."""

        self.__clear_schedule()

        current_period = planner_service.starting_period
        current_year = planner_service.starting_year

        for period in planner_service.get_schedule():
            if not self.__tree.exists(str(current_year)):
                self.__tree.insert(
                    "", constants.END, str(current_year), text=str(current_year)
                )

            period_id = self.__tree.insert(str(current_year), constants.END)
            credits_of_period = self.__add_courses(period_id, period)
            self.__tree.item(
                period_id, text=f"Periodi {current_period}, {credits_of_period} op"
            )

            current_period += 1

            if current_period > planner_service.periods_per_year:
                current_period = 1
                current_year += 1

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
