from tkinter import Tk

from ui.create_course_view import CreateCourseView
from ui.view import View


class UI:
    """Luokka, joka vastaa sovelluksen käyttöliittymästä."""

    def __init__(self, root: Tk) -> None:
        """Luokan konstruktori.

        Args:
            root (Tk): Tkinterin juurikomponentti.
        """

        self.__root: Tk = root
        self.__current_view: View | None = None

    def start(self) -> None:
        """Käynnistää käyttöliittymän."""

        self.__show_create_course_view()

    def __hide_current_view(self) -> None:
        if self.__current_view:
            self.__current_view.destroy()

        self.__current_view = None

    def __show_create_course_view(self) -> None:
        self.__hide_current_view()

        self.__current_view = CreateCourseView(self.__root)

        self.__current_view.pack()
