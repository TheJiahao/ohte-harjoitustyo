from abc import ABC
from tkinter import constants, ttk


class View(ABC):
    """Luokka, joka tarjoaa pohjan näkymille."""

    def __init__(
        self,
        root: ttk.Widget,
    ) -> None:
        self._root: ttk.Widget = root
        self._frame: ttk.Frame = ttk.Frame(master=self._root)
        self._confirm: bool = False

    def pack(self) -> None:
        self._frame.pack(fill=constants.X)

    def destroy(self) -> None:
        self._frame.destroy()
