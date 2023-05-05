from datetime import date
from tkinter import IntVar, TclError, constants, ttk
from tkinter.messagebox import showerror
from typing import Callable

from entities.scheduler import CycleError, EmptyGraphError
from services import planner_service
from services.planner_service import MaxCreditError, TimingError
from ui.view import View


class CalculationView(View):
    """Laskurista vastaava näkymä."""

    def __init__(self, root: ttk.Widget, handle_show_schedule_view: Callable) -> None:
        super().__init__(root)

        self.__credits_variable: IntVar = IntVar(value=15)
        self.__period_variable: IntVar = IntVar(value=1)
        self.__year_variable: IntVar = IntVar(value=date.today().year)
        self.__handle_show_schedule_view: Callable = handle_show_schedule_view

        self.__initialize()

    def __initialize(self) -> None:
        self.__initialize_credits_field()
        self.__initialize_year_field()
        self.__initialize_period_field()

        calculate_button = ttk.Button(
            master=self._frame,
            text="Laske",
            command=self.__handle_calculate,
        )

        calculate_button.grid(row=5, column=1, sticky=constants.S + constants.W)

    def __initialize_credits_field(self) -> None:
        credits_label = ttk.Label(master=self._frame, text="Max op/periodi")

        credits_spinbox = ttk.Spinbox(
            master=self._frame,
            from_=1,
            to=300,
            increment=1,
            width=3,
            textvariable=self.__credits_variable,
        )

        credits_label.grid(row=1, column=1, sticky=constants.W)
        credits_spinbox.grid(row=1, column=2, sticky=constants.W)

    def __initialize_year_field(self) -> None:
        year_label = ttk.Label(master=self._frame, text="Aloitusvuosi")

        year_spinbox = ttk.Spinbox(
            master=self._frame,
            from_=2000,
            to=9999,
            increment=1,
            width=4,
            textvariable=self.__year_variable,
        )

        year_label.grid(row=2, column=1, sticky=constants.W)
        year_spinbox.grid(row=2, column=2, sticky=constants.W)

    def __initialize_period_field(self) -> None:
        period_label = ttk.Label(master=self._frame, text="Aloitusperiodi")

        period_spinbox = ttk.Spinbox(
            master=self._frame,
            from_=1,
            to=4,
            increment=1,
            width=1,
            textvariable=self.__period_variable,
            state="readonly",
        )

        period_label.grid(row=3, column=1, sticky=constants.W)
        period_spinbox.grid(row=3, column=2, sticky=constants.W)

    def __handle_calculate(self) -> None:
        try:
            max_credits = self.__credits_variable.get()
            starting_year = self.__year_variable.get()
            starting_period = self.__period_variable.get()

            planner_service.set_parameters(starting_year, starting_period, max_credits)

            self.__handle_show_schedule_view()

        except (TimingError, CycleError, MaxCreditError) as error:
            showerror("Virhe", str(error))

        except (TclError, EmptyGraphError):
            showerror("Virhe", "Tarkista kurssit.")
