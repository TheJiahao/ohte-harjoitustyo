from abc import ABC, abstractmethod
from tkinter import constants, ttk, Toplevel


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

    def show_popup_window(self, message: str, type: int = 0):
        window = Toplevel(master=self._root)
        frame = ttk.Frame(master=window)
        message_label = ttk.Label(master=frame, text=message)

        message_label.grid(row=1, columnspan=3)

        if type == -1:
            window.title("Virhe")

            ok_button = ttk.Button(master=frame, text="OK", command=window.destroy)

            ok_button.grid()
        else:
            window.title("Varmistus")

            confirm_button = ttk.Button(
                master=frame,
                text="Kyllä",
                command=lambda: self.__handle_confirm(window),
            )
            reject_button = ttk.Button(
                master=frame,
                text="Ei",
                command=lambda: self.__handle_reject(window),
            )

            confirm_button.grid(row=2, column=1, sticky=(constants.W, constants.S))
            reject_button.grid(row=2, column=2, sticky=(constants.E, constants.S))
        frame.pack()

    def show_error_window(self, message: str) -> None:
        self.show_popup_window(message, type=-1)

    def __handle_confirm(self, window: Toplevel) -> None:
        window.destroy()
        self._confirm = True

    def __handle_reject(self, window: Toplevel) -> None:
        window.destroy()
        self._confirm = False
