from abc import ABC, abstractmethod
from tkinter import Menu, constants, ttk, Toplevel, Button


class View(ABC):
    def __init__(
        self,
        root,
    ) -> None:
        self._root = root
        self._frame = ttk.Frame(master=self._root)
        self.__menubar = Menu(self._root)

        self._initialize()

    def pack(self) -> None:
        self._frame.pack(fill=constants.X)

    def destroy(self) -> None:
        self._frame.destroy()

    @abstractmethod
    def _initialize(self) -> None:
        self.__initialize_menu()

    def __initialize_menu(self) -> None:
        view_menu = Menu(self.__menubar, tearoff=0)
        view_menu.add_command(label="Kurssit")

        self.__menubar.add_cascade(label="Näkymä", menu=view_menu)

        self._root.config(menu=self.__menubar)
