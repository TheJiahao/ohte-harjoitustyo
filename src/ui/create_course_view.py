from tkinter import Checkbutton, constants, ttk

from ui.view import View


class CreateCourseView(View):
    def __init__(
        self,
        root,
    ) -> None:
        super().__init__(root)
        self.__course_drop_down_list = None
        self.__name_entry = None
        self.__credits_entry = None
        self.__timing_frame = None

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

    def __initialize_course_field(self) -> None:
        course_label = ttk.Label(master=self._frame, text="Selaa")

    def __initialize_name_field(self) -> None:
        name_label = ttk.Label(master=self._frame, text="Nimi")

        self.__name_entry = ttk.Entry(master=self._frame)

        name_label.grid(row=2, column=1)
        self.__name_entry.grid(row=2, column=2)

    def __initialize_credits_field(self) -> None:
        credits_label = ttk.Label(master=self._frame, text="Laajuus (op)")

        self.__credits_entry = ttk.Entry(master=self._frame)

        credits_label.grid(row=3, column=1)
        self.__credits_entry.grid(row=3, column=2)

    def __initialize_timing_field(self) -> None:
        timing_label = ttk.Label(master=self._frame, text="Ajoitus (periodit)")

        timing_label.grid(row=4, column=1)

        self.__timing_frame = ttk.Frame(master=self._frame)

        for i in range(1, 5):
            button = Checkbutton(master=self.__timing_frame, text=str(i))

            button.grid(row=1, column=i)

        self.__timing_frame.grid(row=4, column=2)
