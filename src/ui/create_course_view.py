from tkinter import BooleanVar, IntVar, StringVar, Tk, constants, ttk

from entities.course import Course
from services import planner_service
from ui.view import View


class CreateCourseView(View):
    """Luokka, joka vastaa kurssin luomisnäkymästä."""

    def __init__(
        self,
        root: Tk,
    ) -> None:
        """Luokan konstruktori.

        Args:
            root (Tk): Tkinterin juurikomponentti.
        """
        super().__init__(root)

        self.__name_variable: StringVar = StringVar(value="")
        self.__credits_variable: IntVar = IntVar(value=0)
        self.__course_variable: StringVar = StringVar(value="")
        self.__course_list: list[str] = [
            str(course) for course in planner_service.get_all_courses()
        ]
        self.__timing_frame: ttk.Frame | None = None
        self.__timing: list[BooleanVar] = [BooleanVar(value=False) for i in range(4)]

        self._initialize()

    def pack(self) -> None:
        self._frame.pack(fill=constants.X)

    def destroy(self) -> None:
        self._frame.destroy()

    def _initialize(self) -> None:
        super()._initialize()

        self.__initialize_course_field()
        self.__initialize_name_field()
        self.__initialize_credits_field()
        self.__initialize_timing_field()
        self.__initialize_dependencies_field()

        save_button = ttk.Button(
            master=self._frame,
            text="Tallenna kurssi",
            command=self.__handle_save,
        )
        save_button.grid(row=6, column=1, sticky=constants.W)

        delete_button = ttk.Button(
            master=self._frame,
            text="Poista kurssi",
            command=self.__handle_delete,
        )
        delete_button.grid(row=6, column=2, sticky=constants.E)

    def __initialize_course_field(self) -> None:
        course_label = ttk.Label(master=self._frame, text="Selaa")

        course_dropdown_list = ttk.Combobox(
            master=self._frame,
            state="readonly",
            values=self.__course_list,
            textvariable=self.__course_variable,
        )
        course_dropdown_list.bind("<<ComboboxSelected>>", self.__fill_course_data)

        self.__update_course_list()

        course_label.grid(row=1, column=1, sticky=constants.W)
        course_dropdown_list.grid(row=1, column=2, sticky=constants.W)

    def __initialize_name_field(self) -> None:
        name_label = ttk.Label(master=self._frame, text="Nimi")

        name_entry = ttk.Entry(master=self._frame, textvariable=self.__name_variable)

        name_label.grid(row=2, column=1, sticky=constants.W)
        name_entry.grid(row=2, column=2, sticky=constants.W)

    def __initialize_credits_field(self) -> None:
        credits_label = ttk.Label(master=self._frame, text="Laajuus (op)")

        credits_spinbox = ttk.Spinbox(
            master=self._frame,
            from_=0,
            to=20,
            increment=1,
            width=2,
            textvariable=self.__credits_variable,
        )

        credits_label.grid(row=3, column=1, sticky=constants.W)
        credits_spinbox.grid(row=3, column=2, sticky=constants.W)

    def __initialize_timing_field(self) -> None:
        timing_label = ttk.Label(master=self._frame, text="Ajoitus (periodit)")

        timing_label.grid(row=4, column=1, sticky=constants.W)

        self.__timing_frame = ttk.Frame(master=self._frame)

        for i in range(4):
            button = ttk.Checkbutton(
                master=self.__timing_frame, text=str(i + 1), variable=self.__timing[i]
            )

            button.grid(row=1, column=i + 1)

        self.__timing_frame.grid(row=4, column=2, sticky=constants.W)

    def __initialize_dependencies_field(self) -> None:
        dependency_label = ttk.Label(master=self._frame, text="Esitietovaatimukset")

        add_dependency_button = ttk.Button(master=self._frame, text="Lisää")

        add_dependency_button.grid(row=5, column=2, sticky=constants.E)
        dependency_label.grid(row=5, column=1, sticky=constants.W)
