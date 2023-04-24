from tkinter import ttk, constants

from services import planner_service
from ui.view import View


class ScheduleView(View):
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
        self.__clear_schedule()

        current_period = planner_service.starting_period
        current_year = planner_service.starting_year

        for period in planner_service.get_schedule():
            if not self.__tree.exists(str(current_year)):
                self.__tree.insert(
                    "", constants.END, str(current_year), text=str(current_year)
                )

            period_id = self.__tree.insert(
                str(current_year), constants.END, text=f"Periodi {current_period}"
            )

            for course in period:
                self.__tree.insert(period_id, constants.END, text=str(course))

            current_period += 1

            if current_period > planner_service.periods_per_year:
                current_period = 0
                current_year += 1
