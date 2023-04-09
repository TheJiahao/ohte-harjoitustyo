from abc import ABC, abstractmethod
from tkinter import Menu, Tk, constants, ttk


class View(ABC):
    """Luokka, joka tarjoaa pohjan näkymille."""

    def __init__(
        self,
        root: Tk,
    ) -> None:
        self._root: Tk = root
        self._frame: ttk.Frame = ttk.Frame(master=self._root)
        self.__menubar: Menu = Menu(self._root)

    def pack(self) -> None:
        self._frame.pack(fill=constants.X)

    def destroy(self) -> None:
        self._frame.destroy()

    @abstractmethod
    def _initialize(self) -> None:
        self._initialize_menu()

    def _initialize_menu(self) -> None:
        view_menu = Menu(self.__menubar, tearoff=0)

        view_menu.add_command(label="Kurssit")
        view_menu.add_command(label="Laskuri")
        view_menu.add_command(label="Aikataulu")

        self.__menubar.add_cascade(label="Näkymä", menu=view_menu)

        self._root.config(menu=self.__menubar)
