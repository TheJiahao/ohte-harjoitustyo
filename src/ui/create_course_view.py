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
        self.__course_list: list[str] = planner_service.get_all_courses()
        self.__timing_frame: ttk.Frame = ttk.Frame(master=self._frame)
        self.__timing: dict[int, BooleanVar] = {
            i: BooleanVar(value=False) for i in range(1, 5)
        }

        self.__dependency_frame: ttk.Frame = ttk.Frame(master=self._frame)
        self.__dependencies: list[StringVar] = []

        self.__current_id: int = -1

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
            text="Tallenna",
            command=self.__handle_save,
        )
        save_button.grid(row=7, column=1, sticky=(constants.W, constants.S))

        delete_button = ttk.Button(
            master=self._frame,
            text="Poista",
            command=self.__handle_delete,
        )
        delete_button.grid(row=7, column=2, sticky=(constants.E, constants.S))

    def __initialize_course_field(self) -> None:
        course_label = ttk.Label(master=self._frame, text="Selaa")

        course_dropdown_list = ttk.Combobox(
            master=self._frame,
            state="readonly",
            values=self.__course_list,
            textvariable=self.__course_variable,
            postcommand=lambda: course_dropdown_list.configure(
                values=self.__course_list
            ),
        )
        course_dropdown_list.bind("<<ComboboxSelected>>", self.__fill_course_data)

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

        for i in range(1, 5):
            button = ttk.Checkbutton(
                master=self.__timing_frame, text=str(i), variable=self.__timing[i]
            )

            button.grid(row=1, column=i)

        self.__timing_frame.grid(row=4, column=2, sticky=constants.W)

    def __initialize_dependencies_field(self) -> None:
        dependency_label = ttk.Label(master=self._frame, text="Esitietovaatimukset")

        add_dependency_button = ttk.Button(
            master=self._frame,
            text="+",
            command=self.__handle_add_dependency,
        )

        add_dependency_button.grid(row=5, column=2, sticky=constants.E)
        dependency_label.grid(row=5, column=1, sticky=constants.W)
        self.__dependency_frame.grid(row=6, column=1, columnspan=2, sticky=constants.W)

    def __fill_course_data(self, event) -> None:
        self.__current_id = self.__extract_id(self.__course_variable)

        course = planner_service.get_course(self.__current_id)

        if course is None:
            return

        self.__clear_data()

        self.__name_variable.set(course.name)
        self.__credits_variable.set(course.credits)

        for period in course.timing:
            self.__timing[period].set(True)

    def __clear_data(self) -> None:
        self.__current_id = -1
        self.__name_variable.set("")
        self.__credits_variable.set(0)

        for i in range(1, 5):
            self.__timing[i].set(False)

        for row in self.__dependency_frame.winfo_children():
            row.destroy()

    def __handle_save(self) -> None:
        name = self.__name_variable.get()
        credits = self.__credits_variable.get()

        timing = {i for i in range(1, 5) if self.__timing[i].get()}
        dependencies = {
            self.__extract_id(course_variable)
            for course_variable in self.__dependencies
        }

        course = Course(name, credits, timing, dependencies, self.__current_id)

        planner_service.create_course(course)

        self.__course_list = planner_service.get_all_courses()
        self.__clear_data()

    def __handle_delete(self) -> None:
        pass

    def __handle_add_dependency(self) -> None:
        dependency_variable = StringVar(value="")

        dependency_row = ttk.Frame(master=self.__dependency_frame)

        dependency_dropdown = ttk.Combobox(
            master=dependency_row,
            values=self.__course_list,
            state="readonly",
            textvariable=dependency_variable,
        )

        delete_button = ttk.Button(
            master=dependency_row,
            text="-",
            command=dependency_row.destroy,
        )

        delete_button.grid(row=1, column=1, sticky=constants.W)
        dependency_dropdown.grid(row=1, column=2, sticky=constants.W)
        dependency_row.grid(column=1)

        self.__dependencies.append(dependency_variable)

    def __extract_id(self, course_variable: StringVar) -> int:
        return int(course_variable.get().split(":")[0])
