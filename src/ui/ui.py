from tkinter import Tk, ttk

from ui.create_course_view import CreateCourseView
from ui.view import View


class UI:
    """Luokka, joka vastaa sovelluksen käyttöliittymästä."""

    def __init__(self, root: Tk) -> None:
        """Luokan konstruktori.

        Args:
            root (Tk): Tkinterin juurikomponentti.
        """

        self.__notebook: ttk.Notebook = ttk.Notebook(root)

        self.__initialize()

    def start(self) -> None:
        """Käynnistää käyttöliittymän."""

        self.__notebook.pack()

    def __initialize(self) -> None:
        create_course_view = CreateCourseView(self.__notebook)

        self.__notebook.add(create_course_view.frame, text="Lisää kurssi")
