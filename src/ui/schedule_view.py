from tkinter import ttk

from services import planner_service
from ui.view import View


class ScheduleView(View):
    def __init__(self, root: ttk.Widget) -> None:
        super().__init__(root)

        self.__tree = ttk.Treeview(master=self._frame)

    def __initialize(self) -> None:
        self.__tree.grid()

    def update(self) -> None:
        pass
