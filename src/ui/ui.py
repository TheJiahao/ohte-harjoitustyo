from tkinter import constants, ttk

from ui.calculation_view import CalculationView
from ui.create_course_view import CreateCourseView
from ui.schedule_view import ScheduleView
from ui.view import View


class UI(View):
    """Luokka, joka vastaa sovelluksen käyttöliittymästä."""

    def __init__(self, root: ttk.Widget) -> None:
        """Luokan konstruktori.

        Args:
            root (Tk): Tkinterin juurikomponentti.
        """

        super().__init__(root)

        self.__notebook: ttk.Notebook = ttk.Notebook(self._frame)
        self.__schedule_view: ScheduleView = ScheduleView(self.__notebook)

        self.__initialize()

    def start(self) -> None:
        """Käynnistää käyttöliittymän."""

        super().pack()

    def __initialize(self) -> None:
        create_course_view = CreateCourseView(self.__notebook)
        calculation_view = CalculationView(self.__notebook, self.__show_schedule_view)

        self.__notebook.add(create_course_view.frame, text="Lisää kurssi")
        self.__notebook.add(calculation_view.frame, text="Laskuri")
        self.__notebook.add(self.__schedule_view.frame, text="Aikataulu")

        self.__notebook.pack(fill=constants.BOTH, expand=1)

    def __show_schedule_view(self) -> None:
        self.__schedule_view.update()
        self.__notebook.select(2)
